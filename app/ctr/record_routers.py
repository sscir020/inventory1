
from flask import render_template,url_for,redirect,flash,session,request,current_app
from main_config import oprenumNum,Oprenum,Prt,oprenumCH
from ..models import Opr,Material,User,Buy,Rework,Web_device,Customerservice#Accessory
from ..decorators import loggedin_required
from ..__init__ import db
from .forms import LoginForm,RegistrationForm,AddMaterialForm,SearchDeviceForm
from . import ctr


@ctr.route('/form_search_device_act',methods=['GET','POST'])
@loggedin_required
def form_search_device():
    form=SearchDeviceForm()
    join_oprs=None
    pagination=None
    if form.validate_on_submit():
        device_id=form.device_id.data
        material_id=form.material_id.data
        if device_id!=None and device_id!="" :
            if db.session.query(Web_device).filter(Web_device.device_id==device_id).first()!=None:
                page = request.args.get('page', 1, type=int)#outerjoin(Web_device,Web_device.device_id==Opr.device_id).
                pagination = db.session.query(Opr.opr_id,Material.material_id, Material.material_name,Opr.device_id,Opr.service_id,Opr.oprtype, Opr.diff, \
                                      Opr.MN_id,Opr.isgroup,Opr.oprbatch,Opr.comment, User.user_name,Opr.momentary\
                                      ).outerjoin(Material,Material.material_id==Opr.material_id).\
                                      join(User,User.user_id==Opr.user_id).order_by(Opr.opr_id.desc()).filter(Opr.device_id==device_id).paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
                join_oprs = pagination.items
                db.session.close()
            else:
                flash("设备不存在")
        elif material_id!=None and material_id!="" :
            if db.session.query(Material).filter(Material.material_id==material_id).first()!=None:
                page = request.args.get('page', 1, type=int)#outerjoin(Web_device,Web_device.device_id==Opr.device_id).
                pagination = db.session.query(Opr.opr_id,Material.material_id, Material.material_name,Opr.device_id,Opr.service_id,Opr.oprtype, Opr.diff, \
                                      Opr.MN_id,Opr.isgroup,Opr.oprbatch,Opr.comment, User.user_name,Opr.momentary\
                                      ).outerjoin(Material,Material.material_id==Opr.material_id).\
                                      join(User,User.user_id==Opr.user_id).order_by(Opr.opr_id.desc()).filter(Opr.material_id==material_id).paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
                join_oprs = pagination.items
                db.session.close()
            else:
                flash("材料不存在")
        else:
            flash("需要填写设备id或者材料id")
    return render_template('search_device.html',form=form,join_oprs=join_oprs,pagination=pagination ,oprenumCH=oprenumCH)

@ctr.route('/join_oprs_table',methods=['GET','POST'])
# @loggedin_required
def show_join_oprs():
    # flash('操作记录')
    # db.session.flush()
    # print(sql)
    page = request.args.get('page', 1, type=int) #.outerjoin(Web_device,Web_device.device_id==Opr.device_id).
    pagination = db.session.query(Opr.opr_id,Material.material_id, Material.material_name,Opr.device_id,Opr.service_id,Opr.oprtype, Opr.diff, \
                          Opr.MN_id,Opr.isgroup,Opr.oprbatch,Opr.comment, User.user_name,Opr.momentary).\
                          outerjoin(Material,Material.material_id==Opr.material_id).\
                          join(User,User.user_id==Opr.user_id).order_by(Opr.opr_id.desc()).paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
    join_oprs=pagination.items
    db.session.close()
    return render_template('join_oprs_table.html',join_oprs=join_oprs,pagination=pagination ,oprenumCH=oprenumCH)



@ctr.route('/join_oprs_main_table',methods=['GET','POST'])
@loggedin_required
def show_join_oprs_main():
    # flash('操作记录')
    # db.session.flush()
    page = request.args.get('page', 1, type=int)#outerjoin(Web_device,Web_device.device_id==Opr.device_id).
    # sql1=db.session.query(Opr.opr_id,Opr.diff,User.user_name).join(User,User.user_id==Opr.user_id).all()#.join(User, User.user_id == Opr.user_id)\.filter(Opr.isgroup==True)
    pagination = db.session.query(Opr.opr_id,Material.material_id, Material.material_name,Opr.device_id,Opr.service_id,Opr.oprtype, Opr.diff,\
                          Opr.MN_id,Opr.isgroup,Opr.oprbatch,Opr.comment, User.user_name,Opr.momentary\
                          ).outerjoin(Material,Material.material_id==Opr.material_id).\
                          join(User,User.user_id==Opr.user_id).order_by(Opr.opr_id.desc()).filter(Opr.isgroup==True).paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
    join_oprs = pagination.items
    db.session.close()
    return render_template('join_oprs_main_table.html',join_oprs=join_oprs,pagination=pagination ,oprenumCH=oprenumCH)
