
from flask import render_template,url_for,redirect,flash,session,request,current_app
from main_config import oprenumNum,Oprenum,Prt
from ..models import Opr,Material,User,Buy,Rework,Customerservice#Device,Client,Accessory
from ..decorators import loggedin_required
from ..__init__ import db
from .forms import LoginForm,RegistrationForm,AddMaterialForm,SearchDeviceForm
from . import ctr


@ctr.route('/welcome',methods=['GET','POST'])
def welcome_user():
    # return "welcome_user"
    return render_template('welcome.html')

@ctr.route('/about',methods=['GET','POST'])
def about_app():
    return render_template('about.html')

@ctr.route('/', methods=['GET', 'POST'])
@ctr.route('/login', methods=['GET', 'POST'])
def log_user_in():
    form=LoginForm()
    if form.validate_on_submit():
        # db.session.close()
        # db.session.rollback()
        Prt.prt(form.username.data)
        username=str(form.username.data)
        user=db.session.query(User).filter(User.user_name==username).first()
        # user=User.query.filter(User.user_name==username).first()
        Prt.prt(user)
        Prt.prt(user==None)
        Prt.prt(db)
        Prt.prt(db.session)
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

@ctr.route('/logout')
@loggedin_required
def log_user_out():
    # logout_user()
    # print(session)
    session.pop('userid',None)
    session.pop('username', None)
    session.pop('userpass', None)
    session.pop('role', None)
    flash("登出成功")
    return redirect(url_for('ctr.welcome_user'))

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

@ctr.route('/user_table',methods=['GET','POST'])
@loggedin_required
def show_users():
    # flash('购买列表')
    # db.session.flush()
    users = db.session.query(User).order_by(User.user_id.desc()).all()
    db.session.close()
    return render_template('user_table.html',users=users )




def material_isvalid_num_rev (m,diff,oprtype,batch):
    if diff<0:
        flash("数量小于等于0")##
        return False
        # if diff> self.storenum:
        #     flash("取消新添加数量大于库存数量")##
        #     return False
    # elif oprtype == Oprenum.OUTBOUND.name:
    #     if diff<=0:
    #         flash("取消出库数量小于等于0")##
    #         return False
    if oprtype == Oprenum.BUY.name:#1
        b = db.session.query(Buy).filter(Buy.batch == batch).first()
        if b==None:
            flash("购买批次不存在"+str(batch))
            return False
        if diff!= b.num:
            flash("取消购买数量不等于购买批次数量")##
            return False
    elif oprtype == Oprenum.REWORK.name:#2
        b=db.session.query(Rework).filter(Rework.batch == batch).first()
        if b==None:
            flash("返修批次不存在"+str(batch))
            return False
        if diff!=b.num:
            flash("取消返修数量不等于返修批次数量")
            return False
    elif oprtype==Oprenum.INBOUND.name:#3
        if diff>m.storenum:# 5 2  -> 7 0
            flash("取消入库数量大于库存数量")
            return False
    elif oprtype == Oprenum.RESTORE.name:#返修#4
        if diff>m.storenum:
            flash("取消修好数量大于库存数量")
            return False
    # elif oprtype == Oprenum.SCRAP.name:
    #     if diff<=0:
    #         flash("报废数量小于等于0")
    #         return False
    elif oprtype == Oprenum.RECYCLE.name:#5
        b=db.session.query(Rework).filter(Rework.batch == batch).first()
        if b==None:
            flash("售后带回批次不存在")
            return False
        if diff!=b.num:
            flash("售后带回数量不等于返修批次数量")
            return False
    elif oprtype==Oprenum.INITADD.name:#6
        pass
    elif oprtype == Oprenum.RESALE.name:#7
        pass
    elif oprtype == Oprenum.OUTBOUND.name:#8
        pass
    elif oprtype == Oprenum.CANCELBUY.name:#9
        pass
    elif oprtype == Oprenum.SCRAP.name:#10
        pass
    elif oprtype == Oprenum.PREPARE.name:#11
        if diff>m.preparenum:
            flash("取消备货数量大于备货数量")
            return False
    else:
        flash("操作类型错误")
        return False
    return True




def material_change_num_rev(m,diff,oprtype,batch):
    value=0
    if oprtype==Oprenum.OUTBOUND.name:#####1
        m.preparenum += diff
        m.salenum-=diff
        db.session.add_all([m])
    #     self.storenum -= diff
    elif oprtype == Oprenum.BUY.name:#++++#2
        db.session.query(Buy).filter(Buy.batch == batch).delete()
    elif oprtype == Oprenum.REWORK.name:#++++#3
        m.storenum += diff
        db.session.query(Rework).filter(Rework.batch == batch).delete()
        db.session.add_all([m])
    elif oprtype==Oprenum.INBOUND.name:#----#4
        m.storenum -= diff
        b = db.session.query(Buy).filter(Buy.batch == batch).first()
        if b==None:
            b=Buy(batch=batch,material_id=m.material_id,num=diff)
        else:
            b.num+=diff
        db.session.add_all([m,b])
    elif oprtype == Oprenum.RESTORE.name:#----#5
        m.storenum -= diff
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        if b==None:
            b = Rework(batch=batch, material_id=m.material_id, num=diff)
        else:
            b.num += diff
        db.session.add_all([m,b])
    elif oprtype == Oprenum.CANCELBUY.name:#>>>>#6
        b = Buy(batch=batch, material_id=m.material_id, num=diff)
        db.session.add_all([b])
    elif oprtype == Oprenum.SCRAP.name:#>>>>#7
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        if b==None:
            b = Rework(batch=batch, material_id=m.material_id, num=diff)
        else:
            b.num += diff
        db.session.add_all([b])
    elif oprtype == Oprenum.RECYCLE.name:#8
        db.session.query(Customerservice).filter(Customerservice.batch == batch).delete()
    elif oprtype == Oprenum.RESALE.name:#9
        m.storenum += diff
        m.resalenum -= diff
        db.session.add_all([m])
    elif oprtype == Oprenum.INITADD.name:######11
        pass
    elif oprtype == Oprenum.PREPARE.name:#10
        m.storenum+=diff
        m.preparenum-=diff

    else:
        flash("操作类型错误")
        value='-1'
    # if value!='-1':
    #     db.session.add(self)
    #     db.session.commit()
    return value
def customerservice_isvalid_num(cs,m,oprtype,diff,batch):
    if oprtype == Oprenum.CSFEE.name:  # 1
        if diff > cs.fee:
            return False
    elif oprtype == Oprenum.CSFEEZERO.name:  # 2
        pass
    elif oprtype == Oprenum.CSGINBOUND.name:  # 3
        if diff>m.storenum:
            return False

    elif oprtype == Oprenum.CSDRESTORE.name:  # 4
        if 1>cs.restorenum:
            return False
    elif oprtype == Oprenum.CSBROKEN.name:  # 5
        if diff>cs.brokennum:
            return False
    elif oprtype==Oprenum.CSDRECYCLE.name:
        pass
    elif oprtype == Oprenum.CSSCRAP.name:
        if diff > cs.scrapnum:
            return False
    elif oprtype == Oprenum.CSREWORK.name:
        if diff>cs.reowrknum:
            return False

def customerservice_change_num(cs,m,oprtype,diff,batch):
    if oprtype == Oprenum.CSFEE.name:  # 1
        cs.fee -= diff
    elif oprtype == Oprenum.CSFEEZERO.name:  # 2
        cs.fee = diff
    elif oprtype == Oprenum.CSGINBOUND.name:  # 3
        cs.goodnum += diff
        m.storenum -= diff
    elif oprtype == Oprenum.CSDRESTORE.name:  # 4
        cs.brokennum += 1
        cs.restorenum -= 1
    elif oprtype == Oprenum.CSBROKEN.name:  # 5
        cs.goodnum += diff
        cs.brokennum -= diff
        if cs.goodnum == cs.originnum:
            cs.goodnum == 0
            cs.brokenmnum == 0
    elif oprtype==Oprenum.CSDRECYCLE.name: #6
        db.session.delete(cs)
    elif oprtype == Oprenum.CSSCRAP.name: #7
        b = db.session.query(Rework).filter(Rework.batch == batch).first()
        if b==None:
            b=Rework(num=diff,batch=batch,service_id=cs.service_id,material_id=m.material_id)
        else:
            b.num += diff
        cs.reworknum += diff
        cs.scrapnum-=diff
    elif oprtype==Oprenum.CSREWORK.name: #8
        b=db.session.query(Rework).filter(Rework.batch==batch).first()
        db.sesion.delete(b)
        cs.brokennum += diff
        cs.reworknum -= diff
@ctr.route('/rollback_act',methods=['GET','POST'])
def rollback():
    opr = db.session.query(Opr).order_by(Opr.opr_id.desc()).first()
    if opr.oprtype[0:2]=='CS':
        cs = db.session.query(Customerservice).filter(Customerservice.service_id == opr.service_id).frist()
        if opr.oprtype==Oprenum.CSDRECYCLE.name:
            db.session.delete(cs)
        else:
            m=None
            if cs.material_id!=None:
                m=db.session.query(Material).filter(Material.material_id==cs.material_id)
            if customerservice_isvalid_num(cs=cs,m=m,oprtype=opr.oprtype,diff=opr.diff,batch=opr.batch):
                customerservice_change_num(cs=cs,m=m,oprtype=opr.oprtype,diff=opr.diff,batch=opr.batch)
                db.session.add(cs)
                db.session.commit()
                db.session.flush()
                db.session.close()
    else:
        if opr.isgroup == True:
            if opr.oprtype == Oprenum.INITADD.name :
                db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
                db.session.query(Material).filter_by(material_id=opr.material_id).delete()
                db.session.commit()
                db.session.flush()
                flash("回滚成功_主件_新添加材料")
            else:
                m = db.session.query(Material).filter_by(material_id=opr.material_id).first()
                if m != None:
                    if material_isvalid_num_rev(m=m,diff=opr.diff, batch=str(opr.oprbatch), oprtype=opr.oprtype):
                        material_change_num_rev(m=m,diff=opr.diff, batch=str(opr.oprbatch), oprtype=opr.oprtype)
                        db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
                        db.session.commit()
                        db.session.flush()
                        flash("回滚成功_主件"+str(m.material_id))
                    else:
                        flash("回滚失败-数量超标_main"+str(m.material_id))
                        return redirect(url_for('ctr.show_join_oprs_main'))
                else:
                    flash("回滚失败-材料不存在_main"+str(m.material_id))
                    return redirect(url_for('ctr.show_join_oprs_main'))
            opr = db.session.query(Opr).order_by(Opr.opr_id.desc()).first()

        while opr.isgroup == False:
            m =db.session.query(Material).filter_by(material_id=opr.material_id).first()
            if m!=None:
                if material_isvalid_num_rev(m=m,diff=opr.diff, batch=str(opr.oprbatch), oprtype=opr.oprtype):
                    material_change_num_rev(m=m,diff=opr.diff,batch=opr.oprbatch,oprtype=opr.oprtype)
                    db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
                    db.session.commit()
                    db.session.flush()
                    flash("回滚成功_配件"+str(m.material_id))
                else:
                    flash("回滚操作记录错误-数量超标_配件"+str(m.material_id))
                    return redirect(url_for('ctr.show_join_oprs_main'))
            else:
                flash("回滚操作记录错误-材料不存在_配件"+str(m.material_id))
                return redirect(url_for('ctr.show_join_oprs_main'))
            opr = db.session.query(Opr).order_by(Opr.opr_id.desc()).first()
        db.session.close()
    return redirect(url_for('ctr.show_join_oprs_main'))
