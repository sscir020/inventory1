
from flask import render_template,url_for,redirect,flash,session,request,current_app
from main_config import oprenumNum,Oprenum,Prt
from ..models import Opr,Material,User,Buy,Rework,Customerservice
from ..decorators import loggedin_required
from ..__init__ import db
from .forms import LoginForm,RegistrationForm,AddMaterialForm,BuyMaterialForm,ReworkForm,ChangeMaterialForm
from . import ctr
from .material_routers import change_materials_oprs_db,convert_str_num
import datetime

@ctr.route('/form_change_buy_act',methods=['GET','POST'])
# @loggedin_required
def form_change_buy():
    form=BuyMaterialForm(request.form)
    if request.method=="POST":
        print(request.form)
        print(form)
        # diff=form.diff.data
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
                    buy_id=request.form[key]
                    diff=convert_str_num(request.form["input_number_"+str(buy_id)])
                    oprtype=form.oprtype.data
                    comment=form.comment.data
                    # buy_id=form.buy_id.data
                    # Prt.prt(buy_id,diff,oprtype,comment)
                    buy=db.session.query(Buy).filter(Buy.buy_id==buy_id).first()
                    if buy==None:
                        flash("订单不存在")
                        db.session.close()
                    else:
                        materialid=buy.material_id
                        batch=buy.batch
                        if oprtype==Oprenum.INBOUND.name:
                            if diff <= 0:
                                flash("应该填写正数")
                            elif change_materials_oprs_db(oprtype=oprtype, materialid=materialid, device_id='',diff=diff, isgroup=True,batch=batch, comment=comment):
                                flash("入库更新成功")
                                j+=1
                            else:
                                flash("入库更新错误")
                        elif oprtype==Oprenum.CANCELBUY.name:
                            b = db.session.query(Buy).filter(Buy.batch == batch).first()
                            diff = b.num
                            o = Opr(material_id=materialid,device_id='',MN_id='', diff=diff, user_id=session['userid'],
                                    oprtype=Oprenum.CANCELBUY.name, isgroup=True, oprbatch=batch, comment=b.comment, \
                                    momentary=datetime.datetime.now())  # .strftime("%Y-%m-%d %H:%M:%S")
                            db.session.query(Buy).filter(Buy.batch == batch).delete()
                            db.session.add(o)
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                            flash("订单取消成功")
                            j+=1
                        elif oprtype==Oprenum.COMMENT.name:
                            b = db.session.query(Buy).filter(Buy.batch == batch).first()
                            b.comment=comment
                            db.session.add(b)
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                            flash("备注修改成功")
                            j+=1
                        else:
                            flash("操作类型错误")
            flash("共选了"+str(i)+"条，"+str(j)+"条更新成功，"+str(i-j)+"条更新失败")
    # print(request)
    # flash('购买列表')
    page = request.args.get('page',1,type=int)
    pagination=db.session.query(Buy.buy_id,Buy.material_id,Material.material_name,Buy.batch,Buy.num,Buy.comment).\
        outerjoin(Material,Material.material_id==Buy.material_id).order_by(Buy.batch.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    buybatches=pagination.items
    db.session.close()
    return render_template('buy_material_table.html',form=form,buybatches=buybatches,pagination=pagination )


def customerservice_isvalid_num(cs,m,diff,oprtype,batch,device_id):
    if oprtype == Oprenum.CSRESTORE.name:
        if oprtype == Oprenum.CSRESTORE.name:
            b = db.session.query(Rework).filter(Rework.batch == batch).first()
            if b == None:
                flash("返修批次不存在" + str(batch))
                return False
            if diff > b.num:
                flash("修好数量大于返修批次数量" + str(diff) + ">" + str(b.num))
    elif oprtype == Oprenum.CSSCRAP.name:
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在" + str(batch))
            return False
        if diff > b.num:
            flash("报废数量大于返修批次数量" + str(diff) + ">" + str(b.num))
            return False
    else:
        flash("操作类型错误_判断"+str(oprtype))
        return False
    return True

def customerservice_change_num(cs,m,diff, oprtype, batch,device_id):
    Prt.prt('cs.reworknum:' + str(cs.reworknum), 'MN_id:' + str(device_id), "diff:" + str(diff), "oprtype:" + str(oprtype), "batch:" + str(batch))
    value=batch
    if oprtype == Oprenum.CSRESTORE.name:
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        b.num -= diff
        m.storenum+=diff
        cs.reworknum-=diff
        cs.restorenum+=diff
        if b.num == 0:
            db.session.query(Rework).filter(Rework.batch == batch).delete()
        else:
            db.session.add_all([b])
        db.session.add_all([m])
    elif oprtype == Oprenum.CSSCRAP.name:
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        b.num -= diff
        m.scrapnum += diff
        cs.reworknum -= diff
        cs.scrapnum+=diff
        if b.num == 0:
            db.session.query(Rework).filter(Rework.batch == batch).delete()
        else:
            db.session.add_all([b])
    else:
        flash("操作类型错误_判断"+str(oprtype))
        value=-1
    return value

def change_customerservice_oprs_db(oprtype,materialid, service_id,device_id,diff,isgroup,batch,comment):#BUY,REWORK,OUTBOUND,INBOUND,RESTORE,SCRAP #INITADD,CANCELBUY
    Prt.prt('service_id:' + str(service_id) ,'device_id:' + str(device_id) ,  "diff:" + str(diff) , "oprtype:" + str(oprtype) , "batch:" + str(batch))
    cs = db.session.query(Customerservice).filter(Customerservice.service_id==service_id).first()
    if cs == None:
        flash("售后不存在")
        db.session.close()
        return False
    else:
        m = db.session.query(Material).filter(Material.material_id == materialid).first()
        if m == None:
            flash("材料不存在")
            return False
        if customerservice_isvalid_num(cs=cs,m=m,diff=diff, oprtype=oprtype, batch=batch,device_id=device_id) == False:
            flash("数量超标")
            return False
        else:
            value=customerservice_change_num(cs=cs,m=m,diff=diff, oprtype=oprtype, batch=batch,device_id=device_id)
            o = Opr(service_id=service_id,material_id=materialid, device_id=device_id,MN_id=device_id,diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=isgroup,
                    oprbatch=value,comment=comment, momentary=datetime.datetime.now())
            db.session.add_all([cs,o])
            db.session.commit()
            db.session.flush()
            db.session.close()
    return True

@ctr.route('/form_change_rework_act', methods=['GET', 'POST'])
# @loggedin_required
def form_change_rework():
    form=ReworkForm(request.form)
    if request.method=="POST":
        # print(request.form)
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
                    rework_id=request.form[key]
                    diff=convert_str_num(request.form["input_number_"+str(rework_id)])
                    oprtype=form.oprtype.data
                    comment=form.comment.data
                    # rework_id=form.rework_id.data
                    r=db.session.query(Rework).filter(Rework.rework_id==rework_id).first()
                    if r==None:
                        flash("返修订单不存在")
                    else:
                        materialid = r.material_id
                        batch = r.batch
                        service_id = r.service_id
                        device_id = r.device_id
                        Prt.prt(service_id)
                        if oprtype==Oprenum.RESTORE.name:
                            if diff <= 0:
                                flash("应该填写正数")
                            elif service_id != None:
                                flash("请选择售后")
                            else:
                                if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, device_id='',diff=diff, isgroup=True,batch=batch, comment=comment):
                                    flash("返修列表-修好更新成功")
                                else:
                                    flash("返修列表-修好更新失败")
                        elif oprtype==Oprenum.SCRAP.name:
                            if diff <= 0:
                                flash("应该填写正数")
                            elif service_id != None:
                                flash("请选择售后")
                            else:
                                if change_materials_oprs_db(oprtype=oprtype, materialid=materialid,  device_id='',diff=diff, isgroup=True,batch=batch, comment=comment):
                                    flash("返修列表-报废更新成功")
                                else:
                                    flash("返修列表-报废更新失败")
                        elif oprtype == Oprenum.CSRESTORE.name:
                            Prt.prt(list)
                            if diff <= 0:
                                flash("应该填写正数")
                            elif service_id!=None:
                                if change_customerservice_oprs_db(oprtype=oprtype, materialid=materialid, service_id=service_id,device_id=device_id,diff=diff, isgroup=True,batch=batch, comment=comment):
                                    flash("返修列表-售后修好更新成功")
                                else:
                                    flash("返修列表-售后修好更新失败")
                            else:
                                flash("返修列表-不是售后")
                        elif oprtype == Oprenum.CSSCRAP.name:
                            if diff <= 0:
                                flash("应该填写正数")
                            elif service_id != None:
                                if change_customerservice_oprs_db(oprtype=oprtype, materialid=materialid, service_id=service_id,device_id=device_id, diff=diff, isgroup=True, batch=batch, comment=comment):
                                    flash("返修列表-售后报废更新成功")
                                else:
                                    flash("返修列表-售后报废更新失败")
                            else:
                                flash("返修列表-不是售后")
                        elif oprtype==Oprenum.COMMENT.name:
                            b = db.session.query(Rework).filter(Rework.batch == batch).first()
                            b.comment=comment
                            db.session.add(b)
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                        else:
                            flash("操作类型错误")
            flash("共选了" + str(i) + "条，" + str(j) + "条更新成功，" + str(i - j) + "条更新失败")
    # flash('返修列表')
    # db.session.flush()
    page = request.args.get('page',1,type=int)
    pagination = db.session.query(Rework.rework_id,Rework.material_id,Rework.service_id,Rework.device_id,Material.material_name,Rework.batch,Rework.num,Rework.comment). \
        outerjoin(Material, Material.material_id == Rework.material_id).order_by(Rework.batch.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    db.session.close()
    reworkbatches=pagination.items
    return render_template('rework_material_table.html',form=form,reworkbatches=reworkbatches,pagination=pagination )


