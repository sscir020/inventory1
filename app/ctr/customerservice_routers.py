
from flask import render_template,url_for,redirect,flash,session,request,current_app
from main_config import oprenumNum,Oprenum,Prt
from ..models import Opr,Material,User,Buy,Rework,Customerservice,Web_device#Accessory,Device
from ..decorators import loggedin_required
from ..__init__ import db
from .forms import LoginForm,RegistrationForm,AddMaterialForm,CustomerserviceForm
from . import ctr
from .material_routers import convert_str_num
from .buy_rework_routers import change_customerservice_oprs_db,customerservice_isvalid_num
import datetime

@ctr.route('/form_change_customerservic_act', methods=['GET', 'POST'])
@loggedin_required
def form_change_customerservice():
    form = CustomerserviceForm(request.form)
    if request.method == "POST":
        for key in request.form.keys():
            if "input_checkbox" in key:
                ischecked=True
        if not ischecked:
            flash("请点勾选至少一行")
        else:
            i=0
            j=0
            for key in request.form.keys():
                if "input_checkbox" in key:
                    i+=1
                    service_id=request.form[key]
                    diff=convert_str_num(request.form["input_number_"+str(service_id)])
                    oprtype = form.oprtype.data
                    comment = form.comment.data

                    cs = db.session.query(Customerservice).filter(Customerservice.service_id == service_id).first()

                    if cs == None:
                        flash("售后订单不存在")
                    else:
                        material_id = cs.material_id
                        device_id = cs.device_id
                        Prt.prt("material_id"+str(material_id))
                        if oprtype == Oprenum.CSBROKEN.name:#19
                            # if diff > cs.originnum-(cs.brokennum+cs.reworknum+cs.restorenum+cs.inboundnum+cs.scrapnum):
                            if diff < 0:
                                flash("应该填写正数或0")
                            elif material_id == None:
                                flash("不是材料")
                            else:
                                if cs.goodnum==0 and cs.brokennum==0:
                                    cs.goodnum=cs.originnum-diff
                                    cs.brokennum=diff
                                    o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id,material_id=material_id, diff=diff, user_id=session['userid'],oprtype=oprtype,
                                            isgroup=True, oprbatch=cs.batch, comment=comment, momentary=datetime.datetime.now())
                                    db.session.add_all([cs,o])
                                    db.session.commit()
                                    db.session.flush()
                                    db.session.close()
                                    flash("设备损坏更新成功")
                                    j+=1
                                else:
                                    if diff > cs.goodnum:
                                        flash("损坏数量大于售后带回数量")
                                    else:
                                        # if cs.brokennum+diff<=cs.originnum:
                                        cs.goodnum-=diff
                                        cs.brokennum+=diff
                                        o = Opr(device_id=device_id, MN_id=device_id,service_id=service_id,material_id=material_id,  diff=diff, user_id=session['userid'],oprtype=oprtype,
                                                isgroup=True, oprbatch=cs.batch, comment=comment, momentary=datetime.datetime.now())
                                        db.session.add_all([cs,o])
                                        db.session.commit()
                                        db.session.flush()
                                        db.session.close()
                                        flash("设备损坏更新成功")
                                        j += 1
                                        # else:
                                        #     flash("损害的数量大于售后带回总数量")
                        elif oprtype == Oprenum.CSREWORK.name:#20
                            # c = db.session.query(Customerservice).filter(Customerservice.service_id == service_id).first()
                            if diff <= 0:
                                flash("应该填写正数")
                            elif material_id == None:
                                flash("不是材料")
                            elif diff>cs.brokennum:
                                flash("返修数量大于损坏数量")
                            else:
                                batch = datetime.datetime.now()
                                b = db.session.query(Rework).filter(Rework.batch == batch).first()
                                while b != None:
                                    cs.sleep(1)
                                    batch = datetime.datetime.now()
                                    b = db.session.query(Rework).filter(Rework.batch == batch).first()
                                b = Rework(batch=batch, material_id=material_id,service_id=service_id, num=diff, device_id=device_id)

                                cs.brokennum -= diff
                                cs.reworknum += diff
                                o = Opr(material_id=material_id,device_id=device_id,service_id=service_id, diff=diff, user_id=session['userid'], oprtype=oprtype,
                                        isgroup=True, oprbatch=batch, comment=cs.comment,momentary=datetime.datetime.now())
                                db.session.add_all([b, cs, o])
                                db.session.commit()
                                db.session.flush()
                                db.session.close()
                                flash("售后返修成功")
                                j += 1
                        elif oprtype == Oprenum.CSGINBOUND.name:#21
                            if diff <= 0:
                                flash("应该填写正数")
                            else:
                                if material_id == None:
                                    flash("不是材料")
                                else:
                                    m = db.session.query(Material).filter(Material.material_id == material_id).first()
                                    if m!= None:
                                        # if diff > cs.goodnum:
                                        #     flash("入库数量大于售后完好数量" + str(diff) + ">" + str(cs.goodnum))
                                        #     return False
                                        # if cs.inboundnum + diff > cs.goodnum + cs.restorenum:
                                        #     flash("入库数量大于售后带回数量" + str(diff) + str(cs.inboundnum) + ">" + str(cs.goodnum) + str(cs.restorenum))
                                        #     return False
                                        # cs.goodnum -= diff
                                        cs.inboundnum += diff
                                        m.storenum += diff
                                        o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id, material_id=material_id, diff=diff, user_id=session['userid'],oprtype=oprtype,
                                                isgroup=True, oprbatch=cs.batch, comment=comment,momentary=datetime.datetime.now())
                                        db.session.add_all([m,cs,o])
                                        db.session.commit()
                                        db.session.flush()
                                        db.session.close()
                                        flash("完好入库成功")
                                        j += 1
                                    else:
                                        flash("材料不存在")
                                        db.session.close()
                        elif oprtype == Oprenum.CSFEE.name:  # 22
                            if diff <= 0:
                                flash("应该填写正数")
                            else:
                                cs.fee+=diff
                                o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id,material_id=material_id, diff=diff, user_id=session['userid'],oprtype=oprtype,
                                        isgroup=True, oprbatch=cs.batch, comment=comment, momentary=datetime.datetime.now())
                                db.session.add_all([cs,o])
                                db.session.commit()
                                db.session.flush()
                                db.session.close()
                                flash("增加费用成功")
                                j += 1
                        elif oprtype == Oprenum.CSFEEZERO.name:  # 22
                            if session['role']>1:
                                temp=cs.fee
                                cs.fee = 0
                                o = Opr(device_id=device_id, MN_id=device_id,service_id=service_id,material_id=material_id,  diff=temp, user_id=session['userid'], oprtype=oprtype,
                                        isgroup=True, oprbatch=cs.batch, comment=comment, momentary=datetime.datetime.now())
                                db.session.add_all([cs, o])
                                db.session.commit()
                                db.session.flush()
                                db.session.close()
                                flash("欠费清零成功")
                                j += 1
                            else:
                                flash("没有足够权限")
                        elif oprtype==Oprenum.COMMENT.name:
                            cs.comment=comment
                            db.session.add(cs)
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                            flash("备注修改成功")
                            j += 1
                        else:
                            flash("操作类型错误")
            flash("共选了" + str(i) + "条，" + str(j) + "条更新成功，" + str(i - j) + "条更新失败")
    # db.session.flush()
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Customerservice).order_by(Customerservice.service_id.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    customerservice=pagination.items
    db.session.close()
    return render_template("customerservice_table.html", form=form,customerservice=customerservice,pagination=pagination )