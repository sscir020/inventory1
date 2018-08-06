
from flask import render_template,url_for,redirect,flash,session,request,current_app
from main_config import oprenumNum,Oprenum,Prt
from ..models import Opr,Material,User,Buy,Rework,Customerservice,Web_device#Accessory
from ..decorators import loggedin_required
from ..__init__ import db
from .forms import LoginForm,RegistrationForm,AddMaterialForm,DeviceForm
from . import ctr

import json,datetime




@ctr.route('/form_change_device_act', methods=['GET', 'POST'])
@loggedin_required
def form_change_device():
    form = DeviceForm(request.form)
    if request.method == "POST":
        # print(request.form)
        diff = 1
        oprtype = form.oprtype.data
        comment = form.comment.data
        device_id = form.device_id.data
        device = db.session.query(Web_device).filter(Web_device.device_id == device_id).first()
        if device == None:
            flash("设备不存在")
        else:
            if oprtype==Oprenum.CSDRECYCLE.name:#24
                services = db.session.query(Customerservice).filter( Customerservice.device_id == device_id).filter(Customerservice.isold==False).all()  # filter(Customerservice.MN_id == d.MN_id)
                isexisted=False
                for cs in services:
                    if cs.material_id==None:
                        isexisted=True
                        break
                if isexisted==False:
                    cs = Customerservice(MN_id=device_id, device_id=device_id,originnum=diff,brokennum=diff,comment=comment)
                    db.session.add_all([cs])
                    db.session.flush()
                    # Prt.prt(c.originnum,diff)
                    # cs.originnum+=diff
                    o = Opr(device_id=device_id, MN_id=device_id,diff=diff,service_id=cs.service_id, user_id=session['userid'], oprtype=Oprenum.CSDRECYCLE.name,
                            isgroup=True, oprbatch='', comment=comment, \
                            momentary=datetime.datetime.now())
                    db.session.add_all([cs,o])
                    db.session.commit()
                    db.session.flush()
                    db.session.close()
                    flash("设备到售后列表更新成功")
                else:
                    flash("设备已存在")
            else:
                flash("操作类型错误")
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Web_device).order_by(Web_device.device_id.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
    devices=pagination.items
    db.session.close()
    return render_template("device_table.html", form=form,devices=devices,pagination=pagination)