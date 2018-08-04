
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
        diff = form.diff.data
        oprtype = form.oprtype.data
        comment = form.comment.data
        service_id = form.customerservice_id.data
        cs = db.session.query(Customerservice).filter(Customerservice.service_id == service_id).first()
        if cs == None:
            flash("售后订单不存在")
        else:
            material_id = cs.material_id
            device_id = cs.device_id
            if oprtype == Oprenum.CSRESALE.name:#18
                if cs.goodnum + cs.restorenum == 0:
                    flash("没有完好或修好的设备")
                elif material_id=='None':
                    services = db.session.query(Customerservice).filter(Customerservice.device_id == device_id).filter(Customerservice.isold==False).all()
                    print(services)
                    for s in services:
                        print(s)
                        print(s.material_id)
                        # Prt.prt('for material_id', str(s.material_id),'cs.service_id',s.service_id,s.material_id==None )
                        if s.material_id!=None:
                            m=db.session.query(Material).filter(Material.material_id==s.material_id).first()
                            if m!=None:
                        #     Prt.prt('material_id', m.material_id, 'cs.resalenum', cs.resalenum,m == None)
                                s.resalenum = s.goodnum + s.restorenum
                                m.resalenum+=s.resalenum
                                s.goodnum=0
                                s.restorenum=0
                                s.isold = True
                                db.session.add(s)#hiscs
                                db.session.add(m)#hiscs
                        else:
                        #     # Prt.prt('MN_id', MN_id, 'cs.resalenum', cs.resalenum)
                            d=db.session.query(Web_device).filter(Web_device.device_id==device_id).first()
                            if d != None:
                                s.resalenum = s.goodnum + s.restorenum
                                # d.resalenum+=s.resalenum
                                s.goodnum=0
                                s.restorenum=0
                                s.isold=True
                            #     # services.delete()
                            #     # db.session.query(Customerservice).filter(Customerservice.MN_id == MN_id).delete()
                                db.session.add(s)
                                db.session.add(d)
                    # db.session.add(services)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                else:
                    flash("不是设备")
            elif oprtype == Oprenum.CSBROKEN.name:#19
                # if diff > cs.originnum-(cs.brokennum+cs.reworknum+cs.restorenum+cs.inboundnum+cs.scrapnum):
                if diff >cs.goodnum:
                    flash("损坏数量大于售后带回数量")
                else:
                    if cs.goodnum==0 and cs.brokennum==0:
                        cs.goodnum=cs.originnum-diff
                        cs.brokennum=diff
                        db.session.add_all([cs])
                        db.session.commit()
                        db.session.flush()
                        db.session.close()
                    else:
                        # if cs.brokennum+diff<=cs.originnum:
                        cs.goodnum-=diff
                        cs.brokennum+=diff
                        db.session.add_all([cs])
                        db.session.commit()
                        db.session.flush()
                        db.session.close()
                        # else:
                        #     flash("损害的数量大于售后带回总数量")
            elif oprtype == Oprenum.CSREWORK.name:#20
                # c = db.session.query(Customerservice).filter(Customerservice.service_id == service_id).first()
                batch = datetime.datetime.now()
                b = db.session.query(Rework).filter(Rework.batch == batch).first()
                while b != None:
                    cs.sleep(1)
                    batch = datetime.datetime.now()
                    b = db.session.query(Rework).filter(Rework.batch == batch).first()
                b = Rework(batch=batch, material_id=cs.material_id,service_id=service_id, num=diff, device_id=device_id)
                if diff>cs.brokennum:
                    flash("返修数量大于损坏数量")
                else:
                    cs.brokennum -= diff
                    cs.reworknum += diff
                    o = Opr(material_id=cs.material_id,device_id=device_id,service_id=service_id, diff=diff, user_id=session['userid'],
                            oprtype=Oprenum.CSREWORK.name,
                            isgroup=True, oprbatch='',  comment=cs.comment, \
                            momentary=datetime.datetime.now())
                    db.session.add_all([b, cs, o])
                    db.session.commit()
                    db.session.flush()
                db.session.close()
            elif oprtype == Oprenum.CSGINBOUND.name:#21
                if material_id != 'None':
                    m = db.session.query(Material).filter(Material.material_id == material_id).first()
                    if m!= None:
                        if customerservice_isvalid_num(cs=cs,m=m,diff=diff, oprtype=oprtype, batch='',MN_id=MN_id):
                            change_customerservice_oprs_db(oprtype=oprtype, service_id=service_id,materialid=material_id, MN_id=MN_id, diff=diff, isgroup=True, batch='',comment='')
                            flash("完好入库成功")
                        else:
                            flash("完好入库失败")
                    else:
                        flash("材料不存在")
                        db.session.close()
                else:
                    flash("不是材料")
            elif oprtype == Oprenum.CSFEE.name:  # 22
                cs.fee+=diff
                db.session.add_all([cs])
                db.session.commit()
                db.session.flush()
                db.session.close()
            elif oprtype == Oprenum.CSFEEZERO.name:  # 22
                cs.fee=0
                db.session.add_all([cs])
                db.session.commit()
                db.session.flush()
                db.session.close()
            elif oprtype==Oprenum.COMMENT.name:
                cs.comment=comment
                db.session.add(cs)
                db.session.commit()
                db.session.flush()
                db.session.close()
            else:
                flash("操作类型错误")
    # db.session.flush()
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Customerservice).order_by(Customerservice.service_id.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    customerservice=pagination.items
    db.session.close()
    return render_template("customerservice_table.html", form=form,customerservice=customerservice)