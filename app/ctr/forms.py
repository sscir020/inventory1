#coding:utf-8
from wtforms import Form, StringField,IntegerField,PasswordField,BooleanField,SubmitField,SelectField,FieldList,FormField,HiddenField
from wtforms.validators import DataRequired,EqualTo
from main_config import Oprenum

class AddMaterialForm(Form):
    materialname=StringField("材料名",validators=[DataRequired()])
    storenum=IntegerField("数量",  validators=[DataRequired()])
    alarm_level=IntegerField("警戒值",  validators=[DataRequired()])
    submit=SubmitField('添加')

class LoginForm(Form):
    username = StringField('用户名',validators=[DataRequired()])
    userpass = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegistrationForm(Form):
    username=StringField("用户名-英文",validators=[DataRequired()])
    userpass=PasswordField("密码",validators=[DataRequired(),EqualTo('userpass2',message='密码不一致')])
    userpass2 = PasswordField("确认密码", validators=[DataRequired()])
    role=IntegerField("用户角色", validators=[DataRequired()])
    submit = SubmitField('注册')

class SearchMNForm(Form):
    MN_id=StringField("MN号",validators=[DataRequired()])
    submit=SubmitField("搜索")

class ChangeMaterialForm(Form):
    material_id=IntegerField("材料id",validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired()],range=[1])
    oprtype = SelectField("操作", choices=[(Oprenum.BUY, '购买'), (Oprenum.REWORK, '返修'),(Oprenum.PREPARE, "备货"), (Oprenum.OUTBOUND, "出库"), (Oprenum.RECYCLE, "售后带回"), (Oprenum.CSRESALE, "售后带出")])
    comment=StringField("注释")
    submit=SubmitField("操作")

class CustomerserviceForm(Form):
    customerservice_id=IntegerField("售后id",validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired()],range=[1])
    oprtype=SelectField("操作",choices=[(Oprenum.CSBROKEN,'售后损坏'),(Oprenum.CSREWORK,'售后返修'),(Oprenum.CSGINBOUND,"材料售后完好入库"),(Oprenum.CSFEE,"增加售后售出费用"),(Oprenum.CSFEEZERO,"费用清零")])
    comment=StringField("注释")
    submit=SubmitField("操作")

class BuyMaterialForm(Form):
    buy_id = IntegerField("购买id", validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired()],range=[1])
    oprtype=SelectField("操作",choices=[(Oprenum.INBOUND,'入库'),(Oprenum.CANCELBUY,'取消购买')])
    comment=StringField("注释")
    submit=SubmitField("操作")

class ReworkForm(Form):
    rework_id=IntegerField("返修id",validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired()],range=[1])
    oprtype=SelectField("操作",choices=[(Oprenum.CSRESTORE,'售后修好'),(Oprenum.CSSCRAP,'售后报废'),(Oprenum.RESTORE,'修好'),(Oprenum.SCRAP,'报废')])
    comment=StringField("注释")
    submit=SubmitField("操作")

class DeviceForm(Form):
    MN_id=IntegerField("MN id",validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired()])
    oprtype = SelectField("操作", choices=[(Oprenum.DRECYCLE, '设备售后带回'), (Oprenum.DOUTBOUND, '设备出库')])
    comment=StringField("注释")
    submit=SubmitField("操作")


