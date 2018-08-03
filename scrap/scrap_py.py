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
#     return render_template("add_material_form.html")




































