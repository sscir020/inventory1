#coding:utf-8
from flask import render_template,url_for,redirect,flash,session,request
# from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,RegistrationForm,AddMaterialForm,SearchMNForm #AddOprForm#ColorForm#ListForm,OprForm #EditOprForm,EditReworkOprForm,AddClientForm
from ..models import Opr,Material,User,Accessory,Buy,Rework,Device,Client,Customerservice#Customerservice_his
from . import ctr
from ..__init__ import db
from ..decorators import loggedin_required
from main_config import Config,oprenumNum,oprenumCH,Oprenum,CommentType,Prt #Param,params,paramnums,

import datetime,time
import json

# from ..__init__ import db.session

@ctr.route('/', methods=['GET', 'POST'])
@ctr.route('/login', methods=['GET', 'POST'])
def log_user_in():
    form=LoginForm()
    if form.validate_on_submit():
        db.session.close()
        db.session.rollback()
        user=db.session.query(User).filter_by(user_name=form.username.data).first()
        if user == None:
            flash("用户不存在")
            return redirect(url_for('ctr.log_user_in'))
        elif not user.verify_pass(password=form.userpass.data):
            flash("密码不正确")
            return redirect(url_for('ctr.log_user_in'))
        else:
            # login_user(user)
            # next = request.args.get('next')
            # if next is None or not next.startswith('/'):
            #     return redirect(url_for('ctr.welcome_user'))
            # print(session)
            session['userid'] = user.user_id
            session['username'] = user.user_name
            session['userpass'] = user.user_pass
            session['role'] = user.role
            flash("登录成功")
            return redirect(url_for('ctr.welcome_user'))
    else:
        flash("需要登录")
    return render_template('login_form.html',form=form)

@ctr.route('/registration', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        if db.session.query(User).filter_by(user_name=form.username.data).first() == None:
            u=User(user_name=form.username.data,user_pass=form.userpass.data,role=form.role.data)
            db.session.add(u)
            db.session.commit()
            db.session.flush()
            db.session.close()
            flash('账户创建成功')
            return redirect(url_for('ctr.log_user_in'))
        else:
            flash('账户已存在')
    else:
        flash('需要注册')
    return render_template('registration_form.html',form=form)



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
                return redirect(url_for('ctr.show_material_table',page=1))
            else:
                flash('材料名已存在')
        else:
            flash('数量或者警戒值应大于等于0')
    else:
        flash('需要填写')
    return render_template('add_material_form.html',form=form)


@ctr.route('/add_device_act', methods=['', 'POST'])
@loggedin_required
def add_device():#3
    if request.method == "POST":
        devicename=request.form['input_text_device_name']
        MN_id = request.form['input_text_MN']
        devicetype=request.form['input_text_device_type']
        # storenum=convert_str_num(request.form['input_number_countnum'])
        # alarm_level=convert_str_num(request.form['input_number_alarm_level'])

        if devicename!=None and devicename!=''and devicetype!=None and devicetype!='' and  MN_id!=None and MN_id!='' :
            if db.session.query(Device).filter_by(device_name=devicename).first() == None:
                if db.session.query(Device).filter_by(MN_id=MN_id).first() == None:
                    dict={}
                    for keyid in request.form.keys():
                        if keyid[0:21]=='input_accessory_check':
                            # print(key1)
                            keynum='input_accessory_num_'+keyid[22:]
                            if(request.form[keynum]==''or  int(request.form[keynum])<=0 ):
                                flash("数量应是一个正数")
                                return redirect(url_for('ctr.show_add_device'))
                            else:
                                dict[request.form[keyid]]=request.form[keynum]
                    acces=json.dumps(dict)
                    if(len(dict)>0 ):
                        if db.session.query(Accessory).filter(Accessory.param_acces==acces).first()==None:
                            a = Accessory(param_num=len(dict),param_acces=acces)
                            db.session.add(a)
                            db.session.commit()
                            db.session.flush()
                            # db.session.close()
                        else:
                            a=db.session.query(Accessory).filter(Accessory.param_acces==acces).first()
                        d = Device(device_name=devicename,device_type=devicetype,MN_id=MN_id, storenum=0,acces_id=a.acces_id)

                        for material_id in dict:
                            o = Opr(material_id=material_id, MN_id=MN_id,diff=0*int(dict[material_id]), user_id=session['userid'], oprtype=Oprenum.DINITADD.name,isgroup=False,oprbatch='',\
                                    momentary=datetime.datetime.now())
                            db.session.add(o)
                            db.session.commit()
                            db.session.flush()
                            # db.session.close()
                    else:
                        flash("请勾选参数")
                        return redirect(url_for('ctr.show_add_device'))
                    db.session.add(d)
                    db.session.commit()
                    db.session.flush()
                    d=db.session.query(Device).filter_by(device_name=devicename).first()
                    o=Opr(device_id=d.device_id,MN_id=MN_id,diff=0,user_id=session['userid'],oprtype=Oprenum.DINITADD.name, isgroup=True,oprbatch='', \
                          momentary=datetime.datetime.now())
                    db.session.add(o)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash('新设备添加成功')
                    return redirect(url_for('ctr.show_device_table',page=1))
                else:
                    flash('MN号已存在')
            else:
                flash('设备名已存在')
        else:
            flash('请正确填写设备名称,类型,MN号，警戒值')
    return redirect(url_for('ctr.show_add_device'))

def convert_str_num(num):
    if num=='' or num =="":
        return 0
    return int(num)
def material_isvalid_num(m,diff,oprtype,batch,MN_id):
    Prt.prt(oprtype,oprtype==Oprenum.PREPARE.name)
    if diff <= 0:
        flash("数量小于等于0")
        return False
    if oprtype == Oprenum.INITADD.name:#4
        pass
    elif oprtype == Oprenum.OUTBOUND.name:#5
        if diff>m.preparenum:
            flash("出库数量大于备货数量"+str(diff)+">"+str(m.preparenum))
            return False
    elif oprtype == Oprenum.BUY.name:#6
        pass
    # elif oprtype==Oprenum.INITADD.name:
    #     if diff<=0:
    #         flash("新入库数量小于等于0")
    #         return False
    # elif oprtype == Oprenum.BUY.name:
    #     if diff<=0:
    #         flash("购买数量小于等于0")
    #         return False
    elif oprtype == Oprenum.REWORK.name:#7
        if diff>m.storenum:
            flash("返修数量大于库存数量"+str(diff)+">"+str(m.storenum))
            return False
    elif oprtype==Oprenum.INBOUND.name:#8
        b=db.session.query(Buy).filter(Buy.batch==batch).first()
        if b == None:
            flash("购买批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("入库数量大于购买批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.RESTORE.name:#9
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("修好数量大于返修批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.CANCELBUY.name:#10
        b=db.session.query(Buy).filter(Buy.batch==batch).first()
        if b == None:
            flash("购买批次不存在"+str(batch))
            return False
    elif oprtype == Oprenum.SCRAP.name:#11
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        if b == None:
            flash("返修批次不存在"+str(batch))
            return False
        if diff>b.num:
            flash("报废数量大于返修批次数量"+str(diff)+">"+str(b.num))
            return False
    elif oprtype == Oprenum.RESALE.name:#12
        if MN_id == '':
            flash("需要填写MN号"+str(MN_id))
            return False
        if diff>m.storenum:
            flash("售后带出数量大于库存数量"+str(diff)+">"+str(m.storenum))
            return False
    elif oprtype == Oprenum.RECYCLE.name:#13
        if MN_id == '':
            flash("需要填写MN号"+str(MN_id))
            return False
        # c = db.session.query(Customerservice).filter(Customerservice.MN_id == MN_id).first()
        # if c != None:
        #     flash("售后带回设备已存在"+str(MN_id))
        #     return False

    elif oprtype == Oprenum.PREPARE.name:#14
        if diff>m.storenum:
            flash("备货数量大于库存数量"+str(diff)+">"+str(m.storenum))
            return False
    elif oprtype == Oprenum.DINITADD.name:#15
        pass
    elif oprtype == Oprenum.DOUTBOUND.name:#16
        if diff > m.preparenum:
            flash("设备出库数量大于备货数量"+str(diff)+">"+str(m.preparenum))
            return False

    elif oprtype == Oprenum.RINBOUND.name:#17
        if diff > m.restorenum:
            flash("修好入库数量大于修好数量")
    elif oprtype == Oprenum.CSRESTORE.name:
        pass
    elif oprtype == Oprenum.CSSCRAP.name:
        pass
    elif oprtype == Oprenum.CSGINBOUND.name:
        pass
    elif oprtype == Oprenum.CSRINBOUND.name:
        pass
    else:
        flash("操作类型错误_判断"+str(oprtype))
        return False
    return True

def material_change_num(m,diff,oprtype,batch,MN_id):
        value=batch
        if oprtype==Oprenum.INITADD.name:#****
            # m.storenum += diff
            pass
        elif oprtype == Oprenum.OUTBOUND.name:#****
            m.preparenum -= diff
            m.salenum+=diff
        elif oprtype == Oprenum.BUY.name:#-->
            batch = datetime.datetime.now()
            b = db.session.query(Buy).filter(Buy.batch == batch).first()
            while b!=None:
                time.sleep(1)
                batch = datetime.datetime.now()
                b = db.session.query(Buy).filter(Buy.batch == batch).first()
            b=Buy(batch=batch,material_id=m.material_id,num=diff)
            db.session.add(b)
            value = batch
        elif oprtype == Oprenum.REWORK.name:#-->
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
        elif oprtype==Oprenum.INBOUND.name:####
            b = db.session.query(Buy).filter(Buy.batch == batch).first()
            b.num-=diff
            m.storenum += diff
            # db.session.add(b)
            if b.num==0:
                db.session.query(Buy).filter(Buy.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add(b)
        elif oprtype == Oprenum.RESTORE.name:####
            b = db.session.query(Rework).filter(Rework.batch == batch).first()
            b.num -= diff
            m.restorenum += diff
            if b.num == 0:
                db.session.query(Rework).filter(Rework.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add(b)
        elif oprtype == Oprenum.CANCELBUY.name:
            b = db.session.query(Buy).filter(Buy.batch == batch).first()
            value=b.num
            # Buy.query.filter(Buy.batch == batch).delete()
            db.session.query(Buy).filter(Buy.batch == batch).delete()
            # db.session.commit()
        elif oprtype == Oprenum.SCRAP.name:
            b = db.session.query(Rework).filter(Rework.batch == batch).first()
            b.num -= diff
            m.scrapnum+=diff
            if b.num == 0:
                db.session.query(Rework).filter(Rework.batch == batch).delete()
                # db.session.commit()
            else:
                db.session.add_all([b])
        elif oprtype == Oprenum.RESALE.name:#?
            m.storenum-=diff
            m.resalenum+=diff
        elif oprtype == Oprenum.RECYCLE.name:
            c= db.session.query(Customerservice).filter(Customerservice.material_id==m.material_id).filter(Customerservice.MN_id==MN_id).first()
            if c==None:
                c = Customerservice(originnum=diff, material_id=m.material_id,MN_id=MN_id)
            else:
                c.originnum+=diff
            db.session.add(c)
        elif oprtype == Oprenum.PREPARE.name:
            m.storenum-=diff
            m.preparenum+=diff
        elif oprtype == Oprenum.DINITADD.name:
            # m.storenum += diff
            pass
        elif oprtype == Oprenum.DOUTBOUND.name:
            m.preparenum -= diff
            m.salenum += diff
        elif oprtype == Oprenum.RINBOUND.name:
            m.restorenum-=diff
            m.storenum+=diff
        elif oprtype == Oprenum.CSRESTORE.name:
            pass
        elif oprtype == Oprenum.CSSCRAP.name:
            pass
        elif oprtype == Oprenum.CSGINBOUND.name:
            pass
        elif oprtype == Oprenum.CSRINBOUND.name:
            pass
        # elif oprtype == Oprenum.CSGINBOUND.name:
        #     cs=db.session(Customerservice).filter(Customerservice.MN_id==MN_id).filer(Customerservice.material_id==material_id).first()
        #     cs.goodnum -= diff
        #     cs.inboundnum += diff
        #     m.storenum += diff
        #     db.session.add_all([m, cs])
        # elif oprtype == Oprenum.CSRINBOUND.name:
        #     cs.restorenum -= diff
        #     cs.inboundnum += diff
        #     m.storenum += diff
        #     db.session.add_all([m, cs])
        else:
            flash("操作类型错误_变量"+str(oprtype))
            value='-1'
        # if value!='-1':
        #     db.session.add(self)
        #     db.session.commit()
        return value


def change_materials_oprs_db(oprtype,materialid,MN_id,diff,isgroup,batch,comment):#BUY,REWORK,OUTBOUND,INBOUND,RESTORE,SCRAP #INITADD,CANCELBUY
    print('materialid:' + str(materialid) +'MN_id:' + str(MN_id) +  ",diff:" + str(diff) + ",oprtype:" + str(oprtype) + ",batch:" + str(batch))
    m = db.session.query(Material).filter(Material.material_id==materialid).first()
    if m == None:
        flash("材料名不存在")
        return False
    elif material_isvalid_num(m=m,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id) == False:
        flash("数量超标")
        return False
    else:
        value=material_change_num(m=m,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id)
        o = Opr(material_id=materialid, MN_id=MN_id, diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=isgroup,
                oprbatch=value,comment=comment, momentary=datetime.datetime.now())
        db.session.add_all([m,o])
        db.session.commit()
        db.session.flush()
        db.session.close()
        # db.session.close()
    return True

@ctr.route('/form_rollback_act',methods=['','POST'])
@loggedin_required
def form_rollback():
    db.session.rollback()
    return redirect(url_for('ctr.show_join_oprs_main'))


@ctr.route('/form_change_material_act', methods=['', 'POST'])
@loggedin_required
def form_change_material():
    materialid=0
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    materialid=key[13:]
                    MN_id=request.form['input_text_MN_'+materialid]
                    # materialid = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            # print(request.form)
            # input_oprlist_={"},入库,修好
            if(request.form["input_oprlist_" + str(materialid)]!='') and request.form["input_oprlist_" + str(materialid)] in oprenumNum.keys():
                # print(request.form["input_list_" + str(i)])
                # print (oprenumNum[request.form["input_list_" + str(i)]].value)
                oprtype=oprenumNum[request.form["input_oprlist_" + str(materialid)]].name#.value
                # print(index)
                # oprtype=Oprenum(index).name
                # print(oprtype)
                if oprtype==Oprenum.BUY.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, MN_id='',diff=diff,isgroup=True, batch='', comment='')==True:
                        flash("购买列表数量更新成功")
                    else:
                        flash("购买列表数量更新失败")
                elif oprtype == Oprenum.REWORK.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, MN_id='',diff=diff,isgroup=True, batch='',  comment='')==True:
                        flash("返修列表数量更新成功")
                    else:
                        flash("返修列表数量更新失败")
                elif oprtype == Oprenum.RINBOUND.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, MN_id='',diff=diff,isgroup=True, batch='',  comment='')==True:
                        flash("修好入库数量更新成功")
                    else:
                        flash("修好入库数量更新失败")
                elif oprtype == Oprenum.PREPARE.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, diff=diff, isgroup=True, batch='',MN_id='',  comment='') == True:
                        flash("备货数量更新成功")
                    else:
                        flash("备货数量更新失败")
                elif oprtype==Oprenum.OUTBOUND.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, MN_id='',diff=diff,isgroup=True, batch='',  comment='') == True:
                        flash("出库数量更新成功")
                    else:
                        flash("出库数量更新失败")
                elif oprtype == Oprenum.RECYCLE.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid,MN_id=MN_id, diff=diff,isgroup=True, batch='',  comment='')==True:
                         flash("售后带回到售后列表数量更新成功")
                    else:
                        flash("售后带回到售后列表数量更新失败")
                elif oprtype == Oprenum.RESALE.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, MN_id=MN_id,diff=diff,isgroup=True, batch='', comment='')==True:
                        flash("售后带出列表数量更新成功")
                    else:
                        flash("售后带出列表数量更新失败")
                else:
                    flash("错误的操作类型")
            else:
                flash("请选择操作类型")
        else:
            flash('请填写数量')
    return redirect(url_for('ctr.show_material_table'))






@ctr.route('/form_change_customerservic_act', methods=['', 'POST'])
@loggedin_required
def form_change_customerservice():
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff >0:
                    string=key[13:]
                    # string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            # print(request.form)
            Prt.prt(string)
            oprtypech=request.form["input_oprlist_" + str(string)]
            if oprtypech!='' and oprtypech in oprenumNum.keys():
                oprtype=oprenumNum[oprtypech].name
                comment = request.form['input_comment_' + string]
                list = string.split('_')
                service_id = list[0]
                material_id = list[1]
                MN_id = list[2]
                cs=db.session.query(Customerservice).filter(Customerservice.service_id==service_id).first()
                if cs!=None:
                    if oprtype == Oprenum.CSRESALE.name:#18
                        if cs.goodnum + cs.restorenum == 0:
                            flash("没有完好或修好的设备")
                            return redirect(url_for('ctr.show_customerservice_table'))
                        if material_id=='None':
                            services = db.session.query(Customerservice).filter(Customerservice.MN_id == MN_id).filter(Customerservice.isold==False).all()
                            # services=list(customerservices)
                            # Prt.prt(services,services.count(Customerservice))
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
                                    d=db.session.query(Device).filter(Device.MN_id==MN_id).first()
                                    if d != None:
                                        s.resalenum = s.goodnum + s.restorenum
                                        d.resalenum+=s.resalenum
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
                        b = Rework(batch=batch, material_id=cs.material_id,service_id=service_id, num=diff, MN_id=MN_id)
                        if diff>cs.brokennum:
                            flash("返修数量大于损坏数量")
                        else:
                            cs.brokennum -= diff
                            cs.reworknum += diff
                            o = Opr(material_id=cs.material_id,MN_id=MN_id,service_id=service_id, diff=diff, user_id=session['userid'],
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
                        else:
                            flash("不是材料")
                    elif oprtype == Oprenum.CSRINBOUND.name:#22
                        if material_id != 'None':
                            m = db.session.query(Material).filter(Material.material_id == material_id).first()
                            if m != None:
                                if customerservice_isvalid_num(cs=cs,m=m,diff=diff, oprtype=oprtype, batch='',MN_id=MN_id):
                                    change_customerservice_oprs_db(oprtype=oprtype, service_id=service_id, materialid=material_id, MN_id=MN_id, diff=diff, isgroup=True, batch='', comment='')
                                    flash("修好入库成功")
                                else:
                                    flash("修好入库失败")
                            else:
                                flash("材料不存在")
                        else:
                            flash("不是材料")
                    elif oprtype == Oprenum.CSFEE.name:  # 22
                        fee = diff
                        Prt.prt('fee',fee,fee=='0',fee==0)
                        fee = convert_str_num(fee)
                        if fee>0:
                            cs.fee+=fee
                            db.session.add_all([cs])
                            db.session.commit()
                            db.session.flush()
                            db.session.close()
                        else:
                            ("数值应是整数")
                    else:
                        flash("操作类型错误")
                else:
                    flash("售后不存在")
            else:
                flash("操作类型不存在")
        else:
            flash("请正确填写回收数量")

    return redirect(url_for('ctr.show_customerservice_table'))


@ctr.route('/form_change_device_act', methods=['', 'POST'])
@loggedin_required
def form_change_device():
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    string=key[13:]
                    # string = request.form["input_hidden_" + str(index)]
                    break
        if diff > 0:
            oprtypech=request.form["input_oprlist_" + str(string)]
            if oprtypech!='' and oprtypech in oprenumNum.keys():
                oprtype=oprenumNum[oprtypech].name
                comment=request.form['input_comment_'+string]
                list = string.split('_')
                device_id = list[0]
                MN_id = list[1]
                Prt.prt(oprtype)
                if oprtype == Oprenum.DPREPARE.name:#23
                    d=db.session.query(Device).filter(Device.device_id==device_id).first()
                    if d == None:
                        flash("设备不存在")
                    else:
                        d.preparenum+=diff
                        o = Opr(device_id=d.device_id, MN_id=d.MN_id, diff=diff, user_id=session['userid'],
                                oprtype=Oprenum.DPREPARE.name,
                                isgroup=True, oprbatch='', comment=comment, \
                                momentary=datetime.datetime.now())
                        db.session.add_all([d,o])
                        db.session.commit()
                        db.session.flush()
                        db.session.close()
                elif oprtype==Oprenum.DRECYCLE.name:#24
                    d=db.session.query(Device).filter(Device.device_id==device_id).first()
                    if d == None:
                        flash("设备不存在")
                    else:
                        c = db.session.query(Customerservice).filter( Customerservice.device_id == device_id).first()  # filter(Customerservice.MN_id == d.MN_id)
                        if c==None:
                            c = Customerservice(MN_id=d.MN_id, device_id=device_id)
                            db.session.add_all([c])
                            db.session.flush()
                            # Prt.prt(c.originnum,diff)
                        c.originnum+=diff
                        o = Opr(device_id=d.device_id, MN_id=d.MN_id,diff=diff, user_id=session['userid'], oprtype=Oprenum.DRECYCLE.name,
                                isgroup=True, oprbatch='', comment=comment, \
                                momentary=datetime.datetime.now())
                        db.session.add_all([c,o])
                        db.session.commit()
                        db.session.flush()
                        db.session.close()
                        flash("设备到售后列表更新成功")
                elif oprtype==Oprenum.DOUTBOUND.name:
                    d = db.session.query(Device).filter(Device.device_id == device_id).first()
                    if d != None:
                        if diff <= d.preparenum:
                            if d.acces_id != None and d.acces_id != 0:
                                a = db.session.query(Accessory).filter_by(acces_id=d.acces_id).first()
                                if a != None:
                                    data = json.loads(a.param_acces)
                                    for materialid in data:
                                        num = int(data[materialid])
                                        num = num * diff
                                        m = db.session.query(Material).filter_by(material_id=materialid).first()
                                        if material_isvalid_num(m=m,MN_id=MN_id, diff=num, oprtype=Oprenum.DOUTBOUND.name, batch='') == False:
                                            flash("配件数量不足")
                                            return redirect(url_for('ctr.show_device_table'))
                                    for materialid in data:
                                        num = int(data[materialid])
                                        num = num * diff
                                        change_materials_oprs_db(oprtype=Oprenum.DOUTBOUND.name, materialid=materialid,MN_id=d.MN_id, diff=num,
                                                                 isgroup=False, batch='', comment='')
                                    d.preparenum -= diff
                                    d.salenum += diff
                                    # d.preparenum += diff
                                    o = Opr(device_id=device_id, MN_id=d.MN_id,diff=diff, user_id=session['userid'],
                                            oprtype=Oprenum.DOUTBOUND.name, isgroup=True, oprbatch='', comment=d.comment, \
                                            momentary=datetime.datetime.now())  # .strftime("%Y-%m-%d %H:%M:%S")
                                    db.session.add_all([d, o])
                                    db.session.commit()
                                    db.session.flush()
                                    db.session.close()
                                    flash("设备出库更新成功")
                                else:
                                    flash("设备参数不存在")
                            else:
                                flash("设备参数等于空或0")
                        else:
                            flash("出货数量大于备货数量")
                    else:
                        flash("设备不存在")
                else:
                    flash("操作类型错误")
            else:
                flash("操作类型不存在")
        else:
            flash("请正确填写回收数量")
    return redirect(url_for('ctr.show_device_table'))


@ctr.route('/form_change_buy_act', methods=['', 'POST'])
@loggedin_required
def form_change_buy():
    if request.method=="POST":
        # print(request.form)
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    string=key[13:]
                    break
        if diff > 0:
            oprtypech=request.form["input_oprlist_" + str(string)]
            if oprtypech!='' and oprtypech in oprenumNum.keys():
                oprtype=oprenumNum[oprtypech].name
                comment = request.form['input_comment_' + string]
                list=string.split('_')
                materialid=list[0]
                batch=list[1]
                if oprtype==Oprenum.INBOUND.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, MN_id='',diff=diff, isgroup=True,batch=batch, comment=comment):
                        flash("入库更新成功")
                    else:
                        flash("如库更新错误")
                elif oprtype==Oprenum.CANCELBUY.name:
                    b = db.session.query(Buy).filter(Buy.batch == batch).first()
                    diff = b.num
                    o = Opr(material_id=materialid,MN_id='', diff=diff, user_id=session['userid'],
                            oprtype=Oprenum.CANCELBUY.name, isgroup=True, oprbatch=batch, comment=b.comment, \
                            momentary=datetime.datetime.now())  # .strftime("%Y-%m-%d %H:%M:%S")
                    db.session.query(Buy).filter(Buy.batch == batch).delete()
                    db.session.add(o)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash("订单取消成功")
                else:
                    flash("操作类型错误")
            else:
                flash("操作类型不存在")
        else:
            flash("请正确填写数量")
    return redirect(url_for('ctr.show_buy_materials'))

def customerservice_isvalid_num(cs,m,diff,oprtype,batch,MN_id):
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
    elif oprtype == Oprenum.CSGINBOUND.name:
        if diff > cs.goodnum:
            flash("入库数量大于售后完好数量" + str(diff) + ">" + str(cs.goodnum))
            return False
        if cs.inboundnum + diff > cs.goodnum + cs.restorenum:
            flash("入库数量大于售后带回数量" + str(diff) + str(cs.inboundnum) + ">" + str(cs.goodnum) + str(cs.restorenum))
            return False
    elif oprtype == Oprenum.CSRINBOUND.name:
        if diff > cs.restorenum:
            flash("入库数量大于售后修好数量" + str(diff) + ">" + str(cs.goodnum))
            return False
        if cs.inboundnum + diff > cs.goodnum + cs.restorenum:
            flash("入库数量大于售后带回数量" + str(diff) + str(cs.inboundnum) + ">" + str(cs.goodnum) + str(cs.restorenum))
            return False
    else:
        flash("操作类型错误_判断"+str(oprtype))
        return False
    return True

def customerservice_change_num(cs,m,diff, oprtype, batch,MN_id):
    Prt.prt('cs.reworknum:' + str(cs.reworknum), 'MN_id:' + str(MN_id), "diff:" + str(diff), "oprtype:" + str(oprtype), "batch:" + str(batch))
    value=batch
    if oprtype == Oprenum.CSRESTORE.name:
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        b.num -= diff
        cs.reworknum-=diff
        cs.restorenum+=diff
        if b.num == 0:
            db.session.query(Rework).filter(Rework.batch == batch).delete()
        else:
            db.session.add_all([b])
    elif oprtype == Oprenum.CSSCRAP.name:
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        b.num -= diff
        cs.reworknum -= diff
        cs.scrapnum+=diff
        if b.num == 0:
            db.session.query(Rework).filter(Rework.batch == batch).delete()
        else:
            db.session.add_all([b])
    elif oprtype == Oprenum.CSGINBOUND.name:
        cs.goodnum -= diff
        cs.inboundnum += diff
        m.storenum += diff
        db.session.add_all([m])
    elif oprtype == Oprenum.CSRINBOUND.name:
        cs.restorenum -= diff
        cs.inboundnum += diff
        m.storenum += diff
        db.session.add_all([m])
    else:
        flash("操作类型错误_判断"+str(oprtype))
        value=-1
    return value

def change_customerservice_oprs_db(oprtype,materialid, service_id,MN_id,diff,isgroup,batch,comment):#BUY,REWORK,OUTBOUND,INBOUND,RESTORE,SCRAP #INITADD,CANCELBUY
    Prt.prt('service_id:' + str(service_id) ,'MN_id:' + str(MN_id) ,  "diff:" + str(diff) , "oprtype:" + str(oprtype) , "batch:" + str(batch))
    cs = db.session.query(Customerservice).filter(Customerservice.service_id==service_id).first()
    if cs == None:
        flash("售后不存在")
        return False
    if oprtype == Oprenum.CSRESTORE.name or oprtype == Oprenum.CSSCRAP.name:
        if customerservice_isvalid_num(cs=cs,m=None,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id) == False:
            flash("数量超标")
            return False
        else:
            value=customerservice_change_num(cs=cs,m=None,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id)
            o = Opr(service_id=service_id,MN_id=MN_id,diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=isgroup,
                    oprbatch=value,comment=comment, momentary=datetime.datetime.now())
            db.session.add_all([cs,o])
            db.session.commit()
            db.session.flush()
            db.session.close()
    if oprtype == Oprenum.CSGINBOUND.name or oprtype == Oprenum.CSRINBOUND.name:
        m = db.session.query(Material).filter(Material.material_id == materialid).first()
        if m == None:
            flash("材料不存在")
            return False
        if customerservice_isvalid_num(cs=cs,m=m,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id) == False:
            flash("数量超标")
            return False
        else:
            value=customerservice_change_num(cs=cs,m=m,diff=diff, oprtype=oprtype, batch=batch,MN_id=MN_id)
            o = Opr(service_id=service_id,material_id=materialid, MN_id=MN_id,diff=diff, user_id=session['userid'], oprtype=oprtype, isgroup=isgroup,
                    oprbatch=value,comment=comment, momentary=datetime.datetime.now())
            db.session.add_all([cs,o])
            db.session.commit()
            db.session.flush()
            db.session.close()
    return True

@ctr.route('/form_change_rework_act', methods=['', 'POST'])
@loggedin_required
def form_change_rework():
    if request.method=="POST":
        diff=0
        for key in request.form:
            if "input_number_" in key and request.form[key]!='':
                diff = convert_str_num(request.form[key])
                if diff > 0:
                    string=key[13:]
                    break
        if diff > 0:
            # print(request.form)
            # input_list={},
            oprtypech=request.form["input_oprlist_" + str(string)]
            if oprtypech!='' and oprtypech in oprenumNum.keys():
                oprtype=oprenumNum[oprtypech].name
                comment = request.form['input_comment_' + string]
                list = string.split('_')
                materialid = list[0]
                batch = list[1]
                service_id = list[2]
                MN_id = list[2]
                # print("MN_id"+str(MN_id))
                if oprtype==Oprenum.RESTORE.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, MN_id='',diff=diff, isgroup=True,batch=batch, comment=comment):
                        flash("返修列表-修好更新成功")
                    else:
                        flash("返修列表-修好更新失败")
                elif oprtype==Oprenum.SCRAP.name:
                    if change_materials_oprs_db(oprtype=oprtype, materialid=materialid,  MN_id='',diff=diff, isgroup=True,batch=batch, comment=comment):
                        flash("返修列表-报废更新成功")
                    else:
                        flash("返修列表-报废更新失败")
                elif oprtype == Oprenum.CSRESTORE.name:
                    Prt.prt(list)
                    if service_id!='None':
                        if change_customerservice_oprs_db(oprtype=oprtype, materialid=materialid, service_id=service_id,MN_id=MN_id,diff=diff, isgroup=True,batch=batch, comment=comment):
                            flash("返修列表-售后修好更新成功")
                        else:
                            flash("返修列表-售后修好更新失败")
                    else:
                        flash("返修列表-不是售后")
                elif oprtype == Oprenum.CSSCRAP.name:
                    if service_id != 'None':
                        if change_customerservice_oprs_db(oprtype=oprtype, materialid=materialid, service_id=service_id,MN_id=MN_id, diff=diff, isgroup=True, batch=batch, comment=comment):
                            flash("返修列表-售后报废更新成功")
                        else:
                            flash("返修列表-售后报废更新失败")
                    else:
                        flash("返修列表-不是售后")
                else:
                    flash("操作类型错误")
            else:
                flash("操作类型不存在")
        else:
            flash("请正确填写数量")
    return redirect(url_for('ctr.show_rework_materials'))

@ctr.route('/form_search_MN_act',methods=['GET','POST'])
@loggedin_required
def form_search_MN():
    form=SearchMNForm()
    sql=None
    if form.validate_on_submit():
        MN_id=form.MN_id.data
        if db.session.query(Device).filter(Device.MN_id==MN_id).first()!=None:
            sql = db.session.query(Opr.opr_id,Material.material_id, Material.material_name,Device.device_id,Device.device_name,Client.client_id,Client.client_name,Opr.oprtype, Opr.diff, \
                                  Opr.MN_id,Opr.isgroup,Opr.oprbatch,Opr.comment, User.user_name,Opr.momentary\
                                  ).outerjoin(Material,Material.material_id==Opr.material_id).outerjoin(Device,Device.device_id==Opr.device_id).outerjoin(Client,Client.client_id==Opr.client_id).\
                                  join(User,User.user_id==Opr.user_id).order_by(Opr.opr_id.desc()).filter(Opr.MN_id==MN_id).limit(50)
    return render_template('search_MN.html',form=form,join_oprs=sql,oprenumCH=oprenumCH)


@ctr.route('/form_change_comment_act/<comment_type>',methods=['','POST'])
@loggedin_required
def form_change_comment(comment_type):
    if request.method == 'POST':
        if 'input_checkbox_comment' in request.form:
            string=request.form['input_checkbox_comment']
            list = string.split('_')
            id = list[0]
            batch = list[1]
            comment=str(request.form['input_comment_'+string])
            print(request.form)
            Prt.prt(id,comment_type,comment,request)
            if len(comment)<=Config.MAX_CHAR_PER_COMMENT:
                if comment_type==CommentType.REWORK.name:
                    b=db.session.query(Rework).filter_by(batch=batch).first()
                    b.comment=comment
                    db.session.add(b)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash("返修备注修改成功")
                elif comment_type==CommentType.BUY.name:
                    b = db.session.query(Buy).filter_by(batch=batch).first()
                    b.comment = comment
                    db.session.add(b)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash("购买备注修改成功")
                elif comment_type == CommentType.DEVICE.name:
                    d = db.session.query(Device).filter_by(device_id=id).first()
                    d.comment =comment
                    db.session.add(d)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash("设备备注修改成功")
                elif comment_type == CommentType.CLIENT.name:
                    c = db.session.query(Client).filter_by(client_id=id).first()
                    c.comment =comment
                    db.session.add(c)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash("客户备注修改成功")
                elif comment_type == CommentType.CUSTOMERSERVICE.name:
                    c = db.session.query(Customerservice).filter_by(service_id=id).first()
                    c.comment =comment
                    db.session.add(c)
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash("售后备注修改成功")
                else:
                    flash("备注类型错误")
            else:
                flash("每条备注不超过64个中文字")
        else:
            flash("请勾选返修备注")
    if comment_type == CommentType.REWORK.name:
        return redirect(url_for('ctr.show_rework_materials'))
    elif comment_type == CommentType.BUY.name:
        return redirect(url_for('ctr.show_buy_materials'))
    if comment_type == CommentType.DEVICE.name:
        return redirect(url_for('ctr.show_device_table'))
    elif comment_type == CommentType.CLIENT.name:
        return redirect(url_for('ctr.show_client_table'))
    elif comment_type == CommentType.CUSTOMERSERVICE.name:
        return redirect(url_for('ctr.show_customerservice_table'))
    else:
        flash("备注类型错误")

#