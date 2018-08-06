# class AddClientForm(FlaskForm):
#     clientname=StringField("客户名称",validators=[DataRequired()])
#     # device_id=IntegerField("设备编号", validators=[DataRequired()])
#     MN_id=IntegerField("设备MN号", validators=[DataRequired()])
#     comment = StringField("备注", validators=[DataRequired()])
#     submit = SubmitField('添加')
# class ColorForm(FlaskForm):
#     alarm_level=IntegerField("警戒值",validators=[DataRequired()])
#     submit=SubmitField("修改")


# class OprForm(FlaskForm):
#     # nr=int(12)
#     hide=HiddenField("hide")
#     diff = IntegerField('数量', validators=[DataRequired()])
#     operation = SelectField("下拉菜单",choices=[(1, 'Foo1'), (2, 'Foo2')])
#     submit = SubmitField('登录')
#
# class ListForm(FlaskForm):
#     aopr=FormField(OprForm)
#     listopr=FieldList(FormField(OprForm))

# class EditOprForm(FlaskForm):
#     diff = IntegerField("填写入库的数量例如 10 或者 出库的数量 -10", validators=[DataRequired()])
#     submit = SubmitField('出入库')
#
# class EditReworkOprForm(FlaskForm):
#     diff = IntegerField("填写修好的数量例如 10 或者 返修中的数量例如 -10 ", validators=[DataRequired()])
#     submit = SubmitField('返修出入库')
#

from flask_wtf import Form

# @ctr.route('/add_client_post',methods=['GET','POST'])
# def add_client():#1
#     form=AddClientForm()
#     if form.validate_on_submit():
#         if db.session.query(Client).filter_by(client_name=form.clientname.data).first() == None:
#             MN_id=str(form.MN_id.data)
#             d=db.session.query(Device).filter(Device.MN_id==MN_id).first()
#             # Prt.prt(MN_id, d.device_name, d.MN_id, form.MN_id.data, d.MN_id == form.MN_id.data)
#             if d != None:
#                 c = db.session.query(Client).filter(Client.MN_id == MN_id).first()
#                 # Prt.prt(MN_id,c.client_name,c.MN_id,form.MN_id.data,c.MN_id == form.MN_id.data)
#                 if c == None:
#                     c=Client(client_name=form.clientname.data,MN_id=MN_id)
#                     db.session.add(c)
#                     # db.session.commit()
#                     db.session.flush()
#                     o = Opr(client_id=c.client_id, diff=0, user_id=session['userid'],
#                             oprtype=Oprenum.CINITADD.name, isgroup=True, oprbatch='', \
#                             momentary=datetime.datetime.now())
#                     db.session.add(o)
#                     db.session.commit()
#                     db.session.flush()
#                     db.session.close()
#                     flash("客户创建成功")
#                     return redirect(url_for('ctr.show_client_table'))
#                 else:
#                     flash("设备MN号已被使用")
#             else:
#                 flash("设备不存在")
#         else:
#             flash("客户已存在")
#     else:
#         flash("需要填写")
#     return render_template('add_client_form.html',form=form)


# @ctr.route('/materials_table_normal2')
# @loggedin_required
# def show_material_table_normal2():
#     # flash('库存列表')
#     # page=int(page)
#     # if page==None:
#     #     page=1
#     page = request.args.get('page',1,type=int)
#     pagination =db.session.query(Material).order_by(Material.material_id.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
#     materials=pagination.items
#     return render_template('material_table_normal2.html',materials=materials,pagination=pagination,Param=Param,page=page,json=json )

#materials= db.session.query(Material).order_by(Material.material_id.desc()).all()
# return render_template('material_table.html',materials=Material.query.all())


# pagination = db.session.query(Rework).order_by(Rework.batch.desc()). \
#     paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE_LIST'], error_out=False)
#
# pagination = db.session.query(Buy).order_by(Buy.batch.desc()). \
#     paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE_LIST'], error_out=False)
#
# pagination = Accessory.query.order_by(Accessory.acces_id). \
#     paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
#
# pagination = sql.paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
#
# @ctr.route('/show_client_table_get', methods=['GET', ''])
# @loggedin_required
# def show_client_table():
#     # db.session.flush()
#     clients = db.session.query(Client).order_by(Client.client_id.desc()).all()
#     db.session.close()
#     return render_template("client_table.html", clients=clients,CommentType=CommentType)



#
# @ctr.route('/rollback')
# def rollback_opr():
#     opr= db.session.query(Opr).order_by(Opr.opr_id.desc()).first()
#     while opr.isgroup == False:
#         m =db.session.query(Material).filter_by(material_id=opr.material_id).first()
#         if m!=None:
#             m.material_change_num_rev(diff=opr.diff,batch=opr.oprbatch,oprtype=opr.oprtype)
#             db.session.add(m)
#         else:
#             flash("操作记录错误")
#             return redirect(url_for('ctr.show_join_oprs_main'))
#         db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
#         db.session.commit()
#         opr = db.session.query(Opr).order_by(Opr.opr_id.desc()).first()
#     m =db.session.query(Material).filter_by(material_id=opr.material_id).first()
#     if opr.oprtype == Oprenum.INITADD.name:
#         db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
#        db.session.query(Material).filter_by(material_id=opr.material_id).delete()
#     else:
#         if m != None:
#             m.material_change_num_rev(diff=opr.diff, batch=str(opr.oprbatch), oprtype=opr.oprtype)
#             db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
#             db.session.add(m)
#         else:
#             flash("操作记录错误")
#             return redirect(url_for('ctr.show_join_oprs_main'))
#     db.session.commit()
#     flash("回滚成功")
#     return redirect(url_for('ctr.show_join_oprs_main'))

# @ctr.route('/join_oprs_main_table',methods=['GET',''])
# @loggedin_required
# def show_join_oprs_main():
#     # flash('操作记录')
#     # db.session.flush()
#     # sql1=db.session.query(Opr.opr_id,Opr.diff,User.user_name).join(User,User.user_id==Opr.user_id).all()
#     sql = db.session.query(Opr.opr_id, Opr.diff, User.user_name,Material.material_name,Material.material_id,Opr.oprtype,\
#                            Opr.isgroup,Opr.oprbatch,Opr.comment, Opr.momentary).join(User, User.user_id == Opr.user_id)\
#         .join(Material,Material.material_id==Opr.material_id).filter(Opr.isgroup==True).order_by(Opr.opr_id.desc()).limit(50)
#     # print(sql)
#     # page = request.args.get('page', 1, type=int)
#     # pagination = sql.paginate(page, per_page=current_app.config['FLASK_NUM_PER_PAGE'], error_out=False)
#     # join_oprs=pagination.items
#     # print(sql[0])
#     return render_template('join_oprs_main_table.html',join_oprs=sql,oprenumCH=oprenumCH)

#
# @ctr.route('/add_material_get',methods=['GET',''])
# @loggedin_required
# def show_add_material():
# #     return render_template("add_material_form.html")
#
#
# @ctr.route('/add_device_get',methods=['GET','POST'])
# @loggedin_required
# def show_add_device():
#     # db.session.flush()
#     m=db.session.query(Material).filter_by(acces_id=0).all()
#     db.session.close()
#     return render_template("add_device_form.html",materials=m)



#
# @ctr.route('/add_device_act', methods=['', 'POST'])
# @loggedin_required
# def add_device():#3
#     if request.method == "POST":
#         devicename=request.form['input_text_device_name']
#         MN_id = request.form['input_text_MN']
#         devicetype=request.form['input_text_device_type']
#         # storenum=convert_str_num(request.form['input_number_countnum'])
#         # alarm_level=convert_str_num(request.form['input_number_alarm_level'])
#
#         if devicename!=None and devicename!=''and devicetype!=None and devicetype!='' and  MN_id!=None and MN_id!='' :
#             if db.session.query(Device).filter_by(device_name=devicename).first() == None:
#                 if db.session.query(Device).filter_by(MN_id=MN_id).first() == None:
#                     dict={}
#                     for keyid in request.form.keys():
#                         if keyid[0:21]=='input_accessory_check':
#                             # print(key1)
#                             keynum='input_accessory_num_'+keyid[22:]
#                             if(request.form[keynum]==''or  int(request.form[keynum])<=0 ):
#                                 flash("数量应是一个正数")
#                                 return redirect(url_for('ctr.show_add_device'))
#                             else:
#                                 dict[request.form[keyid]]=request.form[keynum]
#                     acces=json.dumps(dict)
#                     if(len(dict)>0 ):
#                         if db.session.query(Accessory).filter(Accessory.param_acces==acces).first()==None:
#                             a = Accessory(param_num=len(dict),param_acces=acces)
#                             db.session.add(a)
#                             db.session.commit()
#                             db.session.flush()
#                             # db.session.close()
#                         else:
#                             a=db.session.query(Accessory).filter(Accessory.param_acces==acces).first()
#                         d = Device(device_name=devicename,device_type=devicetype,MN_id=MN_id, storenum=0,acces_id=a.acces_id)
#
#                         for material_id in dict:
#                             o = Opr(material_id=material_id, MN_id=MN_id,diff=0*int(dict[material_id]), user_id=session['userid'], oprtype=Oprenum.DINITADD.name,isgroup=False,oprbatch='',\
#                                     momentary=datetime.datetime.now())
#                             db.session.add(o)
#                             db.session.commit()
#                             db.session.flush()
#                             # db.session.close()
#                     else:
#                         flash("请勾选参数")
#                         return redirect(url_for('ctr.show_add_device'))
#                     db.session.add(d)
#                     db.session.commit()
#                     db.session.flush()
#                     d=db.session.query(Device).filter_by(device_name=devicename).first()
#                     o=Opr(device_id=d.device_id,MN_id=MN_id,diff=0,user_id=session['userid'],oprtype=Oprenum.DINITADD.name, isgroup=True,oprbatch='', \
#                           momentary=datetime.datetime.now())
#                     db.session.add(o)
#                     db.session.commit()
#                     db.session.flush()
#                     db.session.close()
#                     flash('新设备添加成功')
#                     return redirect(url_for('ctr.show_device_table',page=1))
#                 else:
#                     flash('MN号已存在')
#             else:
#                 flash('设备名已存在')
#         else:
#             flash('请正确填写设备名称,类型,MN号，警戒值')
#     return redirect(url_for('ctr.show_add_device'))
#
# @ctr.route('/form_rollback_act',methods=['','POST'])
# @loggedin_required
# def form_rollback():
#     db.session.rollback()
#     return redirect(url_for('ctr.show_join_oprs_main'))
#
#
#
# @ctr.route('/form_change_comment_act/<comment_type>',methods=['','POST'])
# @loggedin_required
# def form_change_comment(comment_type):
#     if request.method == 'POST':
#         if 'input_checkbox_comment' in request.form:
#             string=request.form['input_checkbox_comment']
#             list = string.split('_')
#             id = list[0]
#             batch = list[1]
#             comment=str(request.form['input_comment_'+string])
#             print(request.form)
#             Prt.prt(id,comment_type,comment,request)
#             if len(comment)<=Config.MAX_CHAR_PER_COMMENT:
#                 if comment_type==CommentType.REWORK.name:
#                     b=db.session.query(Rework).filter_by(batch=batch).first()
#                     b.comment=comment
#                     db.session.add(b)
#                     db.session.commit()
#                     db.session.flush()
#                     db.session.close()
#                     flash("返修备注修改成功")
#                 elif comment_type==CommentType.BUY.name:
#                     b = db.session.query(Buy).filter_by(batch=batch).first()
#                     b.comment = comment
#                     db.session.add(b)
#                     db.session.commit()
#                     db.session.flush()
#                     db.session.close()
#                     flash("购买备注修改成功")
#                 elif comment_type == CommentType.DEVICE.name:
#                     d = db.session.query(Device).filter_by(device_id=id).first()
#                     d.comment =comment
#                     db.session.add(d)
#                     db.session.commit()
#                     db.session.flush()
#                     db.session.close()
#                     flash("设备备注修改成功")
#                 elif comment_type == CommentType.CLIENT.name:
#                     c = db.session.query(Client).filter_by(client_id=id).first()
#                     c.comment =comment
#                     db.session.add(c)
#                     db.session.commit()
#                     db.session.flush()
#                     db.session.close()
#                     flash("客户备注修改成功")
#                 elif comment_type == CommentType.CUSTOMERSERVICE.name:
#                     c = db.session.query(Customerservice).filter_by(service_id=id).first()
#                     c.comment =comment
#                     db.session.add(c)
#                     db.session.commit()
#                     db.session.flush()
#                     db.session.close()
#                     flash("售后备注修改成功")
#                 else:
#                     flash("备注类型错误")
#             else:
#                 flash("每条备注不超过64个中文字")
#         else:
#             flash("请勾选返修备注")
#     if comment_type == CommentType.REWORK.name:
#         return redirect(url_for('ctr.show_rework_materials'))
#     elif comment_type == CommentType.BUY.name:
#         return redirect(url_for('ctr.show_buy_materials'))
#     if comment_type == CommentType.DEVICE.name:
#         return redirect(url_for('ctr.show_device_table'))
#     elif comment_type == CommentType.CLIENT.name:
#         return redirect(url_for('ctr.show_client_table'))
#     elif comment_type == CommentType.CUSTOMERSERVICE.name:
#         return redirect(url_for('ctr.show_customerservice_table'))
#     else:
#         flash("备注类型错误")

#
#
# elif oprtype == Oprenum.CSRINBOUND.name:  # 22
# if material_id != 'None':
#     m = db.session.query(Material).filter(Material.material_id == material_id).first()
#     if m != None:
#         if customerservice_isvalid_num(customerservice=customerservice, m=m, diff=diff, oprtype=oprtype, batch='',
#                                        MN_id=MN_id):
#             change_customerservice_oprs_db(oprtype=oprtype, service_id=service_id, materialid=material_id, MN_id=MN_id,
#                                            diff=diff, isgroup=True, batch='', comment='')
#             flash("修好入库成功")
#         else:
#             flash("修好入库失败")
#     else:
#         flash("材料不存在")
# else:
#     flash("不是材料")
#
# elif oprtype == Oprenum.DOUTBOUND.name:
# d = db.session.query(Device).filter(Device.device_id == device_id).first()
# if d != None:
#     if diff <= d.preparenum:
#         if d.acces_id != None and d.acces_id != 0:
#             a = db.session.query(Accessory).filter_by(acces_id=d.acces_id).first()
#             if a != None:
#                 data = json.loads(a.param_acces)
#                 for materialid in data:
#                     num = int(data[materialid])
#                     num = num * diff
#                     m = db.session.query(Material).filter_by(material_id=materialid).first()
#                     if material_isvalid_num(m=m, MN_id=MN_id, diff=num, oprtype=Oprenum.DOUTBOUND.name,
#                                             batch='') == False:
#                         flash("配件数量不足")
#                         return redirect(url_for('ctr.show_device_table'))
#                 for materialid in data:
#                     num = int(data[materialid])
#                     num = num * diff
#                     change_materials_oprs_db(oprtype=Oprenum.DOUTBOUND.name, materialid=materialid, MN_id=d.MN_id,
#                                              diff=num,
#                                              isgroup=False, batch='', comment='')
#                 d.preparenum -= diff
#                 d.salenum += diff
#                 # d.preparenum += diff
#                 o = Opr(device_id=device_id, MN_id=d.MN_id, diff=diff, user_id=session['userid'],
#                         oprtype=Oprenum.DOUTBOUND.name, isgroup=True, oprbatch='', comment=d.comment, \
#                         momentary=datetime.datetime.now())  # .strftime("%Y-%m-%d %H:%M:%S")
#                 db.session.add_all([d, o])
#                 db.session.commit()
#                 db.session.flush()
#                 db.session.close()
#                 flash("设备出库更新成功")
#             else:
#                 flash("设备参数不存在")
#         else:
#             flash("设备参数等于空或0")
#     else:
#         flash("出货数量大于备货数量")
# else:
#     flash("设备不存在")


# if oprtype == Oprenum.DPREPARE.name:  # 23
#     d = db.session.query(Device).filter(Device.MN_id == MN_id).first()
#     if d == None:
#         flash("设备不存在")
#     else:
#         d.preparenum += diff
#         o = Opr(device_id=d.device_id, MN_id=d.MN_id, diff=diff, user_id=session['userid'],
#                 oprtype=Oprenum.DPREPARE.name,
#                 isgroup=True, oprbatch='', comment=comment, \
#                 momentary=datetime.datetime.now())
#         db.session.add_all([d, o])
#         db.session.commit()
#         db.session.flush()
#         db.session.close()


# @ctr.route('/param_accessory_table',methods=['GET','POST'])
# @loggedin_required
# def show_param_accessory():
#     # flash('购买列表')
#     # db.session.flush()
#     page = request.args.get('page',1,type=int)
#     pagination=db.session.query(Accessory).order_by(Accessory.acces_id.desc()).paginate(page,per_page=current_app.config['FLASK_NUM_PER_PAGE'],error_out=False)
#     accessories = pagination.items
#     db.session.close()
#     return render_template('param_accessory_table.html',accessories=accessories,json=json,Material=Material,db=db )

# class Accessory(db.Model):
#     __tablename__='accessories'
#     acces_id = db.Column(db.Integer, nullable=False, primary_key=True)
#     param_num = db.Column(db.Integer, nullable=False)
#     param_acces = db.Column(db.String(2048), nullable=False)
#     devices = db.relationship('Device', backref='accessories', lazy='dynamic')

# elif oprtype == Oprenum.CSRINBOUND.name:
# if diff > cs.restorenum:
#     flash("入库数量大于售后修好数量" + str(diff) + ">" + str(cs.goodnum))
#     return False
# if cs.inboundnum + diff > cs.goodnum + cs.restorenum:
#     flash("入库数量大于售后带回数量" + str(diff) + str(cs.inboundnum) + ">" + str(cs.goodnum) + str(cs.restorenum))
#     return False

# elif oprtype == Oprenum.RINBOUND.name:
# if change_materials_oprs_db(oprtype=oprtype, materialid=materialid, device_id='', diff=diff, isgroup=True, batch='',
#                             comment='') == True:
#     flash("修好入库数量更新成功")
# else:
#     flash("修好入库数量更新失败")
#
# elif opr.oprtype == Oprenum.DINITADD.name:
# db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
# db.session.query(Device).filter_by(device_id=opr.device_id).delete()
# db.session.commit()
# db.session.flush()
# flash("回滚成功_主件_新添加设备")
# elif opr.oprtype == Oprenum.CINITADD.name:
# db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
# db.session.query(Client).filter_by(client_id=opr.client_id).delete()
# db.session.commit()
# db.session.flush()
# flash("回滚成功_主件_新添加客户")
#
# class Param(Enum):
#     PARAM_8 = 8
#     PARAM_7 = 7
#     PARAM_5 = 5
#     PARAM_3 = 3
#     PARAM_0 = 0
# from enum import Enum



# oprenum = {
#     Oprenum.INITADD:'INITADD',
#     Oprenum.INBOUND:'INBOUND',
#     Oprenum.OUTBOUND:'OUTBOUND',
#     Oprenum.REWORK:'REWORK',
#     Oprenum.RESTORE:'RESTORE'
# }

# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hard_guess@localhost:3306/testdb1?charset=utf8&autocommit=true'
#
# class Development2Config(Config):
#     # basedir = os.path.abspath(os.path.dirname(__file__))
#     # string= os.path.join(basedir,'projects\inventory2\database\data.sqlite')
#     # print("path:"+string)
#     # DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\projects\\inventory2\\database\\data.sqlite'
#     # SQLALCHEMY_DATABASE_URI = 'sqlite:///'+string
#
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aosien2016@120.76.207.142:3306/inventory?charset=utf88&autocommit=true'
#
#
# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aosien2016@120.76.207.142:3306/inventory?charset=utf88&autocommit=true'
#
#
# config = {
#     'development': DevelopmentConfig,
#     'development2': Development2Config,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#
#     'default': DevelopmentConfig
# }
#
# elif oprtype == Oprenum.CSRINBOUND.name:
# cs.restorenum -= diff
# cs.inboundnum += diff
# m.storenum += diff
# db.session.add_all([m])

# elif oprtype == Oprenum.DINITADD.name:
# pass
# elif oprtype == Oprenum.DOUTBOUND.name:
# pass
# elif oprtype == Oprenum.CINITADD.name:
# pass
#
# elif opr.oprtype == Oprenum.DOUTBOUND.name:
# d = db.session.query(Device).filter_by(device_id=opr.device_id).first()
# if d != None:
#     if opr.diff > d.storenum:
#         flash("回滚失败_主件_数量超标" + str(opr.diff) + ">" + str(d.storenum))
#         return redirect(url_for('ctr.show_join_oprs_main'))
#     else:
#         d.storenum -= opr.diff
#         db.session.add(d)
#         db.session.query(Opr).filter_by(opr_id=opr.opr_id).delete()
#         db.session.commit()
#         db.session.flush()
#         flash("回滚成功_主件")
# else:
#
#     flash("回滚失败-材料不存在_main" + str(opr.device_id))



# elif oprtype == Oprenum.DINITADD.name:
#     pass
# elif oprtype == Oprenum.DOUTBOUND.name:
#     m.preparenum+=diff
#     db.session.add_all([m])
# elif oprtype == Oprenum.CINITADD.name:
#     pass
# elif oprtype == Oprenum.RINBOUND.name:#17
#     if diff > m.restorenum:
#         flash("修好入库数量大于修好数量")

# elif oprtype == Oprenum.DINITADD.name:  # 15
# pass
# elif oprtype == Oprenum.DOUTBOUND.name:  # 16
# if diff > m.preparenum:
#     flash("设备出库数量大于备货数量" + str(diff) + ">" + str(m.preparenum))
#     return False
# elif oprtype == Oprenum.CSRESTORE.name:
#     pass
# elif oprtype == Oprenum.CSSCRAP.name:
# pass
# elif oprtype == Oprenum.CSGINBOUND.name:
# pass
# elif oprtype == Oprenum.CSRINBOUND.name:
# pass

# elif oprtype == Oprenum.DINITADD.name:
# # m.storenum += diff
# pass
# elif oprtype == Oprenum.DOUTBOUND.name:
# m.preparenum -= diff
# m.salenum += diff
# # elif oprtype == Oprenum.RINBOUND.name:
# #     # m.restorenum-=diff
# #     # m.storenum+=diff
# #     pass
# elif oprtype == Oprenum.CSRESTORE.name:
# pass
# elif oprtype == Oprenum.CSSCRAP.name:
# pass
# elif oprtype == Oprenum.CSGINBOUND.name:
# pass
# elif oprtype == Oprenum.CSRINBOUND.name:
# pass




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

# elif oprtype == Oprenum.DRECYCLE.name:
#     b=db.session.query(Rework).filter(Rework.batch == batch).first()
#     if b==None:
#         flash("售后带回批次不存在")
#         return False
#     if diff!=b.num:
#         flash("售后带回数量不等于返修批次数量")
#         return False




























