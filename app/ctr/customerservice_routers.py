
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
        if "input_radio" not in request.form.keys():
            flash("请点选一行")
        else:
            service_id=request.form['input_radio']
            diff=convert_str_num(request.form["input_number_"+str(service_id)])
            # diff = form.diff.dat/a
            oprtype = form.oprtype.data
            comment = form.comment.data
            # service_id = form.customerservice_id.data
            cs = db.session.query(Customerservice).filter(Customerservice.service_id == service_id).first()

            if cs == None:
                flash("售后订单不存在")
            else:
                material_id = cs.material_id
                device_id = cs.device_id
                Prt.prt("material_id"+str(material_id))

                if oprtype == Oprenum.CSDRESALE.name:#18
                    if cs.isold == True:
                        flash("售后已售出")
                    else:
                        if cs.goodnum + cs.restorenum == 0:
                            flash("没有完好或修好的设备")
                        elif material_id!=None:
                            flash("不是设备")
                        else:
                            # services = db.session.query(Customerservice).filter(Customerservice.device_id == device_id).filter(Customerservice.isold==False).all()
                            # print(services)
                            # isexisted=False
                            # for s in services:
                            #     if s.material_id == None:
                            #         if  s.goodnum + s.restorenum > 0:
                            #             isexisted=True
                            #         else:
                            #             flash("设备没有完好或者修好的数量")
                            # if isexisted:
                            #     for s in services:
                            #         # print(s)
                            #         # print(s.material_id)
                            #         Prt.prt(s,'cs.material_id', str(s.material_id),'cs.service_id',s.service_id,s.material_id==None )
                            #         if s.material_id!=None:
                            #             m=db.session.query(Material).filter(Material.material_id==s.material_id).first()
                            #             if m!=None:
                            #         #     Prt.prt('material_id', m.material_id, 'cs.resalenum', cs.resalenum,m == None)
                            #                 s.resalenum = s.goodnum + s.restorenum
                            #                 m.resalenum+=s.resalenum
                            #                 s.goodnum=0
                            #                 s.restorenum=0
                            #                 s.isold = True
                            #                 o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id, diff=s.goodnum, user_id=session['userid'], oprtype=Oprenum.CSRESALE.name,
                            #                         isgroup=False, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                            #                 o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id, diff=s.restorenum, user_id=session['userid'], oprtype=Oprenum.CSRESALE.name,
                            #                         isgroup=False, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                            #                 db.session.add_all([s,m,o])
                            #         else:
                            #         #     # Prt.prt('MN_id', MN_id, 'cs.resalenum', cs.resalenum)
                            #             d=db.session.query(Web_device).filter(Web_device.device_id==device_id).first()
                            #             if d != None:
                            #                 s.resalenum = s.goodnum + s.restorenum
                            #                 # d.resalenum+=s.resalenum
                            #                 s.goodnum=0
                            #                 s.restorenum=0
                            #                 s.isold=True
                            #             #     # services.delete()
                            #             #     # db.session.query(Customerservice).filter(Customerservice.MN_id == MN_id).delete()
                            #                 o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id, diff=s.restorenum, user_id=session['userid'], oprtype=Oprenum.CSRESALE.name,
                            #                         isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                            #                 db.session.add_all([s,o])

                                # db.session.add(services)
                            cs.resalenum = cs.restorenum # cs.goodnum +
                            # d.resalenum+=s.resalenum
                            # o1 = Opr(device_id=device_id, MN_id=device_id, service_id=service_id, material_id=material_id,diff=cs.goodnum,
                            #         user_id=session['userid'], oprtype=Oprenum.CSDRESALE.name,
                            #         isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                            o2 = Opr(device_id=device_id, MN_id=device_id, service_id=service_id, material_id=material_id,diff=cs.restorenum,user_id=session['userid'], oprtype=oprtype,
                                    isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                            # cs.goodnum = 0
                            cs.restorenum = 0
                            cs.isold = True
                            db.session.add_all([cs,o2])#o1
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                            flash("设备售后售出成功")
                elif oprtype == Oprenum.CSMRESALE.name:  # 1
                    if cs.isold == True:
                        flash("售后已售出")
                    else:
                        if material_id == None:
                            flash("不是材料")
                        else:
                            cs.isold=True
                            o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id,material_id=material_id, diff=0,user_id=session['userid'], oprtype=oprtype,
                                    isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                            db.session.add_all([cs, o])
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                            flash("材料已经售出")
                elif oprtype == Oprenum.CSDRESTORE.name:
                    if cs.isold == True:
                        flash("售后已售出")
                    else:
                        if material_id != None:
                            flash("不是设备")
                        else:
                            cs.brokennum-=1
                            cs.restorenum+=1
                            o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id, material_id=material_id,diff=1, user_id=session['userid'],oprtype=oprtype,
                                    isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                            db.session.add_all([cs, o])
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                            flash("设备售后修好成功")
                elif oprtype == Oprenum.CSBROKEN.name:#19
                    # if diff > cs.originnum-(cs.brokennum+cs.reworknum+cs.restorenum+cs.inboundnum+cs.scrapnum):
                    if cs.isold == True:
                        flash("售后已售出")
                    else:
                        if diff < 0:
                            flash("应该填写正数或0")
                        elif material_id == None:
                            flash("不是材料")
                        else:
                            if cs.goodnum==0 and cs.brokennum==0:
                                cs.goodnum=cs.originnum-diff
                                cs.brokennum=diff
                                o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id,material_id=material_id, diff=diff, user_id=session['userid'],oprtype=oprtype,
                                        isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                                db.session.add_all([cs,o])
                                db.session.commit()
                                db.session.flush()
                                db.session.close()
                                flash("设备损坏更新成功")
                            else:
                                if diff > cs.goodnum:
                                    flash("损坏数量大于售后带回数量")
                                else:
                                    # if cs.brokennum+diff<=cs.originnum:
                                    cs.goodnum-=diff
                                    cs.brokennum+=diff
                                    o = Opr(device_id=device_id, MN_id=device_id,service_id=service_id,material_id=material_id,  diff=diff, user_id=session['userid'],oprtype=oprtype,
                                            isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                                    db.session.add_all([cs,o])
                                    db.session.commit()
                                    db.session.flush()
                                    db.session.close()
                                    flash("设备损坏更新成功")
                                    # else:
                                    #     flash("损害的数量大于售后带回总数量")
                elif oprtype == Oprenum.CSREWORK.name:#20
                    # c = db.session.query(Customerservice).filter(Customerservice.service_id == service_id).first()
                    if cs.isold == True:
                        flash("售后已售出")
                    elif diff <= 0:
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
                elif oprtype == Oprenum.CSGINBOUND.name:#21
                    if diff <= 0:
                        flash("应该填写正数")
                    elif cs.isold == True:
                        flash("售后已售出")
                    else:
                        if material_id == None:
                            flash("不是材料")
                        else:
                            m = db.session.query(Material).filter(Material.material_id == material_id).first()
                            if m!= None:
                                if customerservice_isvalid_num(cs=cs,m=m,diff=diff, oprtype=oprtype, batch='',device_id=device_id):
                                    change_customerservice_oprs_db(oprtype=oprtype, service_id=service_id,materialid=material_id, device_id=device_id, diff=diff, isgroup=True, batch='',comment='')
                                    flash("完好入库成功")
                                else:
                                    flash("完好入库失败")
                            else:
                                flash("材料不存在")
                                db.session.close()
                elif oprtype == Oprenum.CSFEE.name:  # 22
                    if diff <= 0:
                        flash("应该填写正数")
                    else:
                        cs.fee+=diff
                        o = Opr(device_id=device_id, MN_id=device_id, service_id=service_id,material_id=material_id, diff=diff, user_id=session['userid'],oprtype=Oprenum.CSFEE.name,
                                isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                        db.session.add_all([cs,o])
                        db.session.commit()
                        db.session.flush()
                        db.session.close()
                        flash("增加费用成功")
                elif oprtype == Oprenum.CSFEEZERO.name:  # 22
                    if session['role']>1:
                        temp=cs.fee
                        cs.fee = 0
                        o = Opr(device_id=device_id, MN_id=device_id,service_id=service_id,material_id=material_id,  diff=temp, user_id=session['userid'], oprtype=oprtype,
                                isgroup=True, oprbatch='', comment=comment, momentary=datetime.datetime.now())
                        db.session.add_all([cs, o])
                        db.session.commit()
                        db.session.flush()
                        db.session.close()
                        flash("欠费清零成功")
                    else:
                        flash("没有足够权限")
                elif oprtype==Oprenum.COMMENT.name:
                    cs.comment=comment
                    db.session.add(cs)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash("备注修改成功")
                else:
                    flash("操作类型错误")
    # db.session.flush()
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Customerservice).outerjoin(Material,Material.material_id==Customerservice.material_id).order_by(Customerservice.service_id.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    customerservice=pagination.items
    db.session.close()
    return render_template("customerservice_table.html", form=form,customerservice=customerservice,pagination=pagination )