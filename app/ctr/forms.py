
from wtforms import Form, StringField,IntegerField,PasswordField,BooleanField,SubmitField,SelectField,FieldList,FormField,HiddenField
from wtforms.validators import DataRequired,EqualTo,NumberRange
from main_config import Oprenum
from flask_wtf import FlaskForm

class AddMaterialForm(FlaskForm):
    materialname=StringField("材料名",validators=[DataRequired()])
    storenum=IntegerField("数量",  validators=[DataRequired(),NumberRange(min=0)])
    alarm_level=IntegerField("警戒值",  validators=[DataRequired()])
    submit=SubmitField('添加')

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    userpass = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username=StringField("用户名",validators=[DataRequired()])
    userpass=PasswordField("密码",validators=[DataRequired(),EqualTo('userpass2',message='密码不一致')])
    userpass2 = PasswordField("确认密码", validators=[DataRequired()])
    role=IntegerField("用户角色", validators=[DataRequired()])
    submit = SubmitField('注册')

class SearchDeviceForm(FlaskForm):
    device_id=StringField("设备id",validators=[DataRequired()])
    submit=SubmitField("搜索")

class ChangeMaterialForm(Form):#7
    material_id=IntegerField("材料id",validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired(),NumberRange(min=1)])
    oprtype = SelectField("提交", choices=[(Oprenum.BUY.name, '购买'), (Oprenum.REWORK.name, '返修'),(Oprenum.PREPARE.name, "备货"), (Oprenum.OUTBOUND.name, "出库"),
                                         (Oprenum.RECYCLE.name, "材料售后带回"), (Oprenum.RESALE.name, "材料售后带出"),(Oprenum.COMMENT.name,'修改备注')])
    device_id=StringField("设备号")
    comment=StringField("备注")
    submit=SubmitField("提交")

class CustomerserviceForm(Form):#5
    customerservice_id=IntegerField("售后id",validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired(),NumberRange(min=1)])
    oprtype=SelectField("提交",choices=[(Oprenum.CSBROKEN.name,'材料售后损坏'),(Oprenum.CSREWORK.name,'材料售后返修'),(Oprenum.CSGINBOUND.name,"材料售后完好入库"),
                                         (Oprenum.CSDRESTORE.name,"设备售后修好"),(Oprenum.CSDRESALE.name,"设备售后售出"),(Oprenum.CSMRESALE.name,"材料售后售出"),
                                         (Oprenum.CSFEE.name,"增加售后售出费用"),(Oprenum.CSFEEZERO.name,"欠费清零"),(Oprenum.COMMENT.name,'修改备注')])
    comment=StringField("备注")
    submit=SubmitField("提交")

class BuyMaterialForm(Form):#2
    buy_id = IntegerField("购买id", validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired(),NumberRange(min=1)])
    oprtype=SelectField("提交",choices=[(Oprenum.INBOUND.name,'入库'),(Oprenum.CANCELBUY.name,'取消购买'),(Oprenum.COMMENT.name,'修改备注')])#
    comment=StringField("备注")
    submit=SubmitField("提交")

class ReworkForm(Form):#4
    rework_id=IntegerField("返修id",validators=[DataRequired()])
    diff=IntegerField("数量",validators=[DataRequired(),NumberRange(min=1)])
    oprtype=SelectField("提交",choices=[(Oprenum.RESTORE.name,'修好'),(Oprenum.SCRAP.name,'报废'),(Oprenum.CSRESTORE.name,'材料售后修好'),(Oprenum.CSSCRAP.name,'材料售后报废'),(Oprenum.COMMENT.name,'修改备注')])
    comment=StringField("备注")
    submit=SubmitField("提交")

class DeviceForm(Form):#1
    device_id=StringField("设备号",validators=[DataRequired()])
    # diff=IntegerField("数量",validators=[DataRequired(),NumberRange(min=1)])
    oprtype = SelectField("提交", choices=[(Oprenum.CSDRECYCLE.name, '设备售后带回')])
    comment = StringField("备注")
    submit=SubmitField("提交")


