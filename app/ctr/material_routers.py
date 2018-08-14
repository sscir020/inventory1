
from flask import render_template,url_for,redirect,flash,session,request,current_app
from main_config import oprenumNum,Oprenum,Prt
from ..models import Opr,Material,User,Buy,Rework,Customerservice,Web_device#Device,Client,Accessory
from ..decorators import loggedin_required
from ..__init__ import db
from .forms import LoginForm,RegistrationForm,AddMaterialForm,SearchDeviceForm,BuyMaterialForm,ReworkForm,ChangeMaterialForm
from . import ctr
import datetime
import time




@ctr.route('/add_material_act', methods=['GET', 'POST'])
@loggedin_required
def add_material():#2
    form=AddMaterialForm()
    if form.validate_on_submit():
        materialname=form.materialname.data
        storenum=form.storenum.data
        alarm_level=form.alarm_level.data
        if storenum>=0 and alarm_level>=0 :
            if db.session.query(Material).filter_by(material_name=materialname).first() == None:
                m = Material(material_name=materialname, storenum=storenum, acces_id=0,alarm_level=alarm_level)
                db.session.add(m)
                db.session.commit()
                db.session.flush()
                # db.session.close()
                # m=db.session.query(Material).filter_by(material_name=materialname).first()
                o=Opr(material_id=m.material_id,diff=storenum,user_id=session['userid'],oprtype=Oprenum.INITADD.name, isgroup=True,oprbatch='', \
                      momentary=datetime.datetime.now())
                db.session.add(o)
                db.session.commit()
                db.session.flush()
                db.session.close()
                flash('新材料添加成功')
                return redirect(url_for('ctr.form_change_material'))
            else:
                flash('材料名已存在')
        else:
            flash('数量或者警戒值应大于等于0')
    else:
        flash('需要填写')
    return render_template('add_material_form.html',form=form)


def convert_str_num(num):
    if num=='' or num =="":
        return 0
    return int(num)

def material_isvalid_num(m,diff,oprtype,batch,device_id):
    Prt.prt(oprtype)
    if diff <= 0:
        flash("数量小于等于0")
        return False
    if oprtype == Oprenum.INITADD.name:#1
        pass
    elif oprtype == Oprenum.OUTBOUND.name:#2
        if diff>m.preparenum:
            flash("出库数量大于备货数量"+str(diff)+">"+str(m.preparenum))
            return False
    elif oprtype == Oprenum.BUY.name:#3
        pass
    # elif oprtype==Oprenum.INITADD.name:
    #     if diff<=0:
    #         flash("新入库数量小于等于0")
    #         return False
    # elif oprtype == Oprenum.BUY.name:
    #     if diff<=0:
    #         flash("购买数量小于等于0")
    #         return False
    elif oprtype == Oprenum.REWORK.name:#4
        if diff>m.storenum:
            flash("返修数量大于库存数量"+str(diff)+">"+str(m.storenum))
            return False
    elif oprtype==Oprenum.INBOUND.name:#8#####5
        b=db.session.query(Buy).filter(Buy.batch==batch).first()
        if b == None:
            flash("购买批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("入库数量大于购买批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.RESTORE.name:#9#####6
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("修好数量大于返修批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.CANCELBUY.name:#10#####7
        b=db.session.query(Buy).filter(Buy.batch==batch).first()
        if b == None:
            flash("购买批次不存在"+str(batch))
            return False
    elif oprtype == Oprenum.SCRAP.name:#11#####8
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("报废数量大于返修批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.RESALE.name:#9
        if device_id == '':
            flash("需要填写设备ID"+str(device_id))
            return False
        if diff>m.storenum:
            flash("售后带出数量大于库存数量"+str(diff)+">"+str(m.storenum))
            return False
    elif oprtype == Oprenum.RECYCLE.name:#10
        if device_id == '':
            flash("需要填写设备ID"+str(device_id))
            return False
        # c = db.session.query(Customerservice).filter(Customerservice.MN_id == MN_id).first()
        # if c != None:
        #     flash("售后带回设备已存在"+str(MN_id))
        #     return False

    elif oprtype == Oprenum.PREPARE.name:#11
        if diff>m.storenum:
            flash("备货数量大于库存数量"+str(diff)+">"+str(m.storenum))
            return False

    else:
        flash("操作类型错误_判断"+str(oprtype))
        return False
    return True

def material_change_num(m,diff,oprtype,batch,device_id):
        value=batch
        if oprtype==Oprenum.INITADD.name:#****#11
            # m.storenum += diff
            pass
        elif oprtype == Oprenum.OUTBOUND.name:#****#1
            m.preparenum -= diff
            m.salenum+=diff
        elif oprtype == Oprenum.BUY.name:#-->#2
            batch = datetime.datetime.now()
            b = db.session.query(Buy).filter(Buy.batch == batch).first()
            while b!=None:
                time.sleep(1)
                batch = datetime.datetime.now()
                b = db.session.query(Buy).filter(Buy.batch == batch).first()
            b=Buy(batch=batch,material_id=m.material_id,num=diff)
            db.session.add(b)
            value = batch
        elif oprtype == Oprenum.REWORK.name:#-->#3
            batch=datetime.datetime.now()
            b = db.session.query(Rework).filter(Rework.batch == batch).first()
            while b!=None:
                m.sleep(1)
                batch = datetime.datetime.now()
                b = db.session.query(Rework).filter(Rework.batch == batch).first()
            b=Rework(batch=batch,material_id=m.material_id,num=diff)
            m.storenum -= diff
            db.session.add(b)
            value = batch
        elif oprtype==Oprenum.INBOUND.name:#####4#####4
            b = db.session.query(Buy).filter(Buy.batch == batch).first()
            b.num-=diff
            m.storenum += diff
            # db.session.add(b)
            if b.num==0:
                db.session.query(Buy).filter(Buy.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add(b)
        elif oprtype == Oprenum.RESTORE.name:#####5#####
            b = db.session.query(Rework).filter(Rework.batch == batch).first()
            b.num -= diff
            m.storenum += diff
            if b.num == 0:
                db.session.query(Rework).filter(Rework.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add(b)
        elif oprtype == Oprenum.CANCELBUY.name:#6#####
            b = db.session.query(Buy).filter(Buy.batch == batch).first()
            value=b.num
            # Buy.query.filter(Buy.batch == batch).delete()
            db.session.query(Buy).filter(Buy.batch == batch).delete()
            # db.session.commit()
        elif oprtype == Oprenum.SCRAP.name:#7#####
            b = db.session.query(Rework).filter(Rework.batch == batch).first()
            b.num -= diff
            m.scrapnum+=diff
            if b.num == 0:
                db.session.query(Rework).filter(Rework.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add_all([b])
        elif oprtype == Oprenum.RESALE.name:#8
             pass
        #     m.storenum-=diff
        #     m.resalenum+=diff
        elif oprtype == Oprenum.RECYCLE.name:#9
            pass
        elif oprtype == Oprenum.PREPARE.name:#10
            m.storenum-=diff
            m.preparenum+=diff
        else:
            flash("操作类型错误_变量"+str(oprtype))
            value='-1'
        # if value!='-1':
        #     db.session.add(self)
        #     db.session.commit()
        return value


def change_materials_oprs_db(oprtype,materialid,device_id,diff,isgroup,batch,comment):#BUY,REWORK,OUTBOUND,INBOUND,RESTORE,SCRAP #INITADD,CANCELBUY
    print('materialid:' + str(materialid) +'device_id:' + str(device_id) +  ",diff:" + str(diff) + ",oprtype:" + str(oprtype) + ",batch:" + str(batch))
    m = db.session.query(Material).filter(Material.material_id==materialid).first()
    if m == None:
        flash("材料名不存在")
        return False
    elif material_isvalid_num(m=m,diff=diff, oprtype=oprtype, batch=batch,device_id=device_id) == False:
        flash("数量超标")
        return False
    else:
        if oprtype == Oprenum.RECYCLE.name:#9
            d=db.session.query(Web_device).filter(Web_device.device_id==device_id).first()
            if d==None:
                flash("设备不存在")
                return False
            else:
                batch = datetime.datetime.now()
                b = db.session.query(Customerservice).filter(Customerservice.batch == batch).first()
                while b != None:
                    m.sleep(1)
                    batch = datetime.datetime.now()
                    b = db.session.query(Customerservice).filter(Customerservice.batch == batch).first()
                cs = Customerservice( material_id=m.material_id,material_name=m.material_name,device_id=device_id,batch=batch,originnum=diff)

                db.session.add(cs)
                db.session.flush()
                o = Opr(material_id=materialid, device_id=device_id, MN_id=device_id,service_id=cs.service_id, diff=diff, user_id=session['userid'],
                        oprtype=oprtype, isgroup=isgroup, oprbatch=batch, comment=comment, momentary=datetime.datetime.now())
                db.session.add_all([m, o])
                db.session.commit()
                db.session.flush()
                db.session.close()
                return True
        elif oprtype==Oprenum.RESALE.name:#8
            d=db.session.query(Web_device).filter(Web_device.device_id==device_id).first()
            if d==None:
                flash("设备不存在")
                return False
            else:
                if diff > m.storenum:
                    flash("库存或者售后修好不足")
                    return False
                else:
                    batch = datetime.datetime.now()
                    b = db.session.query(Customerservice).filter(Customerservice.batch == batch).first()
                    while b != None:
                        m.sleep(1)
                        batch = datetime.datetime.now()
                        b = db.session.query(Customerservice).filter(Customerservice.batch == batch).first()
                    cs = Customerservice(material_id=m.material_id, material_name=m.material_name, device_id=device_id,
                                         batch=batch, originnum=0, resalenum=diff)
                    db.session.add(cs)
                    db.session.flush()

                    m.storenum -= diff
                    m.resalenum += diff
                    # cs.restorenum-=diff
                    # cs.resalenum+=diff
                    o = Opr(material_id=materialid, device_id=device_id, MN_id=device_id, service_id=cs.service_id,
                            diff=diff, user_id=session['userid'],
                            oprtype=oprtype, isgroup=isgroup, oprbatch=batch, comment=comment,
                            momentary=datetime.datetime.now())
                    db.session.add_all([m, o])
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    return True
        else:
            value=material_change_num(m=m,diff=diff, oprtype=oprtype, batch=batch,device_id=device_id)
            o = Opr(material_id=materialid, device_id=device_id,MN_id=device_id, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=isgroup,
                    oprbatch=value,comment=comment, momentary=datetime.datetime.now())
            db.session.add_all([m,o])
            db.session.commit()
            db.session.flush()
            db.session.close()
        # db.session.close()
    return True





@ctr.route('/form_change_material_act', methods=['GET', 'POST'])
@loggedin_required
def form_change_material():
    form=ChangeMaterialForm(request.form)
    ischecked = False
    if request.method=="POST":
        print(request.form)
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
                    material_id=request.form[key]
                    diff=convert_str_num(request.form["input_number_"+str(material_id)])
                    # print(request.form)
                    # diff=form.diff.data
                    oprtype=form.oprtype.data
                    comment=form.comment.data
                    # materialid=form.material_id.data
                    device_id=form.device_id.data
                    m=db.session.query(Material).filter(Material.material_id==material_id).first()
                    if m==None:
                        flash("材料不存在")
                    else:
                        Prt.prt(oprtype)
                        if oprtype==Oprenum.BUY.name:#1
                            if diff <= 0:
                                flash("应该填写正数")
                            elif change_materials_oprs_db(oprtype=oprtype, materialid=material_id, device_id='',diff=diff,isgroup=True, batch='', comment='')==True:
                                flash("购买列表数量更新成功")
                                j+=1
                            else:
                                flash("购买列表数量更新失败")
                        elif oprtype == Oprenum.REWORK.name:#2
                            if diff <= 0:
                                flash("应该填写正数")
                            elif change_materials_oprs_db(oprtype=oprtype, materialid=material_id, device_id='',diff=diff,isgroup=True, batch='',  comment='')==True:
                                flash("返修列表数量更新成功")
                                j += 1
                            else:
                                flash("返修列表数量更新失败")
                        elif oprtype == Oprenum.PREPARE.name:#3
                            if diff <= 0:
                                flash("应该填写正数")
                            elif change_materials_oprs_db(oprtype=oprtype, materialid=material_id,device_id='',  diff=diff, isgroup=True, batch='', comment='') == True:
                                flash("备货数量更新成功")
                                j += 1
                            else:
                                flash("备货数量更新失败")
                        elif oprtype==Oprenum.OUTBOUND.name:#4
                            if diff <= 0:
                                flash("应该填写正数")
                            elif device_id=='':
                                flash("需要填写设备ID")
                            else:
                                d = db.session.query(Web_device).filter(Web_device.device_id == device_id).first()
                                if d == None:
                                    flash("设备不存在")
                                else:
                                    if change_materials_oprs_db(oprtype=oprtype, materialid=material_id, device_id=device_id,diff=diff,isgroup=True, batch='',  comment='') == True:
                                        flash("出库数量更新成功")
                                        j += 1
                                    else:
                                        flash("出库数量更新失败")
                        elif oprtype == Oprenum.RECYCLE.name:#5
                            if diff <= 0:
                                flash("应该填写正数")
                            elif device_id=='':
                                flash("需要填写设备ID")
                            else:
                                d = db.session.query(Web_device).filter(Web_device.device_id == device_id).first()
                                if d == None:
                                    flash("设备不存在")
                                else:
                                    if change_materials_oprs_db(oprtype=oprtype, materialid=material_id,device_id=device_id, diff=diff,isgroup=True, batch='',  comment='')==True:
                                         flash("售后带回到售后列表数量更新成功")
                                         j += 1
                                    else:
                                        flash("售后带回到售后列表数量更新失败")
                        elif oprtype == Oprenum.RESALE.name:#6
                            if diff <= 0:
                                flash("应该填写正数")
                            elif device_id=='':
                                flash("需要填写设备ID")
                            else:
                                d = db.session.query(Web_device).filter(Web_device.device_id == device_id).first()
                                if d == None:
                                    flash("设备不存在")
                                else:
                                    if change_materials_oprs_db(oprtype=oprtype, materialid=material_id, device_id=device_id,diff=diff,isgroup=True, batch='', comment='')==True:
                                        flash("售后带出列表数量更新成功")
                                        j += 1
                                    else:
                                        flash("售后带出列表数量更新失败")
                        elif oprtype==Oprenum.COMMENT.name:
                            m.comment=comment
                            db.session.add(m)
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                            flash("备注修改成功")
                            j += 1
                        else:
                            flash("错误的操作类型")
            flash("共选了"+str(i)+"条，"+str(j)+"条更新成功，"+str(i-j)+"条更新失败")
    # print(request.url)
    # print(session)
    # flash('库存列表')
    # page=int(page)
    # if page==None:
    #     page=1
    # db.session.flush()
    page = request.args.get('page',1,type=int)
    pagination =db.session.query(Material).order_by(Material.material_id.desc()).\
        paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    materials=pagination.items
    db.session.close()
    return render_template('material_table.html',form=form,materials=materials,pagination=pagination )