
from .__init__ import db
from flask import flash
from main_config import Oprenum
import json,datetime,time
# from db.DateTime import db.DateTime
# from flask_login import UserMixin, AnonymousUserMixin

# from sqlalchemy import db.Column,db.String,db.Integer,db.ForeignKey,db.Boolean,db.DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import db.relationship

# db.Model=declarative_base()

class User(db.Model):
    __tablename__ = 'users'
    user_id=db.Column(db.Integer,nullable=False,primary_key=True)
    user_name=db.Column(db.String(64),nullable=False, unique=True, index=True)
    user_pass = db.Column(db.String(64),nullable=False)
    role = db.Column(db.Integer,nullable=False,default=1)
    oprs = db.relationship('Opr', backref='users', lazy='dynamic')
    # def __init__(self,**kwargs):
    #     # self.user_name=username
    #     # self.user_pass=userpass
    #     super(User, self).__init__(**kwargs)
    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    def verify_pass(self,password):
        return self.user_pass==password

    # def change_pass(self,newpass):
    #     self.user_pass=newpass
    #     session.add(self)
    #     session.commitAA()

    def prt(self):
        print(self.user_id,self.user_name,self.user_pass)

class Material(db.Model):
    __tablename__ = 'materials'
    material_id=db.Column(db.Integer,nullable=False,primary_key=True)
    material_name=db.Column(db.String(64),nullable=False, unique=True, index=True)##### no defalut
    storenum=db.Column(db.Integer,nullable=False,default=0)
    restorenum=db.Column(db.Integer,nullable=False,default=0)
    scrapnum=db.Column(db.Integer,nullable=False,default=0)
    preparenum=db.Column(db.Integer,nullable=False,default=0)
    salenum=db.Column(db.Integer,nullable=False,default=0)
    resalenum=db.Column(db.Integer,nullable=False,default=0)
    alarm_level=db.Column(db.Integer,nullable=False,default=0)
    acces_id=db.Column(db.Integer, db.ForeignKey('accessories.acces_id'))
    comment = db.Column(db.String(64), nullable=True, default='')
    oprs = db.relationship('Opr', backref='materials', lazy='dynamic')
    buybatches = db.relationship('Buy', backref='materials', lazy='dynamic')
    reworkbatches = db.relationship('Rework', backref='materials', lazy='dynamic')
    customerservices= db.relationship('Customerservice', backref='materials', lazy='dynamic')

    def prt(self):
        print(self.material_id, self.material_name, self.countnum,self.reworknum,self.buynum)

class Buy(db.Model):
    __tablename__='buys'
    buy_id=db.Column(db.Integer,nullable=False,primary_key=True)
    material_id = db.Column(db.Integer,db.ForeignKey('materials.material_id'), nullable=False)
    batch=db.Column(db.String(32),nullable=False,unique=True,index=True)
    num=db.Column(db.Integer,nullable=False,default=0)
    comment=db.Column(db.String(64),nullable=True,default='')

class Rework(db.Model):
    __tablename__='reworks'
    rework_id=db.Column(db.Integer,nullable=False,primary_key=True)
    material_id = db.Column(db.Integer,db.ForeignKey('materials.material_id'))
    service_id = db.Column(db.Integer,db.ForeignKey('customerservice.service_id'))
    device_id = db.Column(db.String(16), nullable=True, default='')
    batch=db.Column(db.String(32),nullable=False,unique=True,index=True,default='')
    num=db.Column(db.Integer,nullable=False,default=0)
    comment=db.Column(db.String(64),nullable=True,default='')

class Opr(db.Model):
    __tablename__ = 'oprs'
    opr_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    diff = db.Column(db.Integer, nullable=False)
    MN_id = db.Column(db.String(32), nullable=True,default='')
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))
    device_id = db.Column(db.String(16))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'))
    service_id = db.Column(db.Integer,db.ForeignKey('customerservice.service_id'))
    oprtype = db.Column(db.String(32), nullable=False)
    oprbatch = db.Column(db.String(32), nullable=False,default='')
    isgroup =db.Column(db.Boolean,nullable=False,default=0)
    comment = db.Column(db.String(64), nullable=True, default='')
    momentary = db.Column(db.DateTime, index=True,default=datetime.datetime.now())#.strftime("%Y-%m-%d %H:%M:%S")

    def prt(self):
        print(self.opr_id, self.user_id, self.diff, self.material_id)


#
# class Device(db.Model):
#     __tablename__='devices'
#     device_id = db.Column(db.Integer, nullable=False, primary_key=True)
#     MN_id = db.Column(db.String(32), nullable=False,default='')
#     device_type = db.Column(db.String(32), nullable=False,default='')
#     device_name = db.Column(db.String(32), nullable=False, default='')
#     storenum = db.Column(db.Integer, nullable=False,default=0)
#     preparenum = db.Column(db.Integer, nullable=False,default=0)
#     salenum = db.Column(db.Integer, nullable=False,default=0)
#     resalenum = db.Column(db.Integer, nullable=False,default=0)
#     acces_id = db.Column(db.Integer, db.ForeignKey('accessories.acces_id'), nullable=False)
#     comment = db.Column(db.String(64), nullable=True,default='')
#     oprs = db.relationship('Opr', backref='devices', lazy='dynamic')



class Customerservice(db.Model):
    __tablename__='customerservice'
    service_id= db.Column(db.Integer, nullable=False, primary_key=True)
    MN_id=db.Column(db.String(32), nullable=False,default='')
    material_id=db.Column(db.Integer,db.ForeignKey('materials.material_id'))
    device_id=db.Column(db.String(16))
    originnum= db.Column(db.Integer, nullable=True,default=0)
    goodnum= db.Column(db.Integer, nullable=True,default=0)
    brokennum= db.Column(db.Integer, nullable=True,default=0)
    reworknum= db.Column(db.Integer, nullable=True,default=0)
    restorenum= db.Column(db.Integer, nullable=True,default=0)
    scrapnum= db.Column(db.Integer, nullable=True,default=0)
    inboundnum= db.Column(db.Integer, nullable=True,default=0)
    resalenum= db.Column(db.Integer, nullable=True,default=0)
    fee= db.Column(db.Integer, nullable=True,default=0)
    comment= db.Column(db.String(64), nullable=True,default='')
    isold =db.Column(db.Boolean,nullable=False,default=0)

class Accessory(db.Model):
    __tablename__='accessories'
    acces_id = db.Column(db.Integer, nullable=False, primary_key=True)
    param_num = db.Column(db.Integer, nullable=False)
    param_acces = db.Column(db.String(2048), nullable=False)
    # devices = db.relationship('web_device', backref='accessories', lazy='dynamic')

class Web_device(db.Model):
    __bind_key__='web_device'
    device_id = db.Column(db.String(16),nullable = False, primary_key=True,index=True)
    name_sn = db.Column(db.String(20),nullable = True, default = 'null')
    name_ln = db.Column(db.String(50),nullable = True, default = 'null')
    description = db.Column(db.String(255),nullable = True, default = 'null')
    type = db.Column(db.String(20),nullable = True, default = 'null')
    create_dtm = db.Column(db.DateTime,nullable = True, default = 'null')
    active_ind = db.Column(db.Boolean,nullable = True, default = 'null')
    lng = db.Column(db.String(10),nullable = True, default='113.837111')
    lat = db.Column(db.String(10),nullable = True, default='22.6046912')
    online_ind = db.Column(db.Boolean,nullable = True, default = 0)
    address = db.Column(db.String(255),nullable = True, default = 'null')
    update_dtm = db.Column(db.DateTime,nullable = True, default = 'null')
    creator = db.Column(db.Integer,nullable = True, default = 'null')
    contractor = db.Column(db.String(255),nullable = True, default='')
    install_dt = db.Column(db.DateTime,nullable = True, default = 'null')
    video = db.Column(db.String(255),nullable = True, default = 'null')



class Client(db.Model):
    __tablename__='clients'
    client_id = db.Column(db.Integer, nullable=False, primary_key=True)
    client_name = db.Column(db.String(32), nullable=False)
    MN_id = db.Column(db.String(32),nullable=False,default='')
    credit=db.Column(db.Integer,nullable=True,default=0)
    comment = db.Column(db.String(64), nullable=True,default='')

# class AnonymousUser(AnonymousUserMixin):
#     def can(self, permissions):
#         return False
#
#     def is_administrator(self):pytho
#         return False
#
# login_manager.anonymous_user = AnonymousUser
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# def material_change_countnum(self, diff):
#     self.countnum += diff
#     session.add(self)
#     # session.commit()
#     return True
#
#
# def material_change_buycountnum_rev(self, diff, batch):
#     if diff < 0:
#         self.buynum[batch] -= diff
#     self.countnum += diff
#     session.add(self)
#     # session.commit()
#     return True
#
#
# def material_change_buycountnum(self, diff, batch):
#     if diff > 0:
#         self.buynum -= diff
#     self.countnum += diff
#     session.add(self)
#     # session.commit()
#     return True
#
#
# def material_change_reworknum(self, diff):
#     self.countnum += diff
#     self.reworknum -= diff
#     session.add(self)
#     # session.commit()
#     return True


# def isvalid_opr(self, diff):
#     if diff == 0:
#         return False
#     if self.buynum < diff:  # 入库
#         flash("入库数量大于购买数量")
#         return False
#     if self.countnum < -diff:  # 出库
#         flash("出库数量大于库存数量")
#         return False
#     return True
#
#
# def isvalid_rework_opr(self, diff):
#     # print("********************")
#     # print(diff)
#     # print("=====================")
#     if diff == 0:
#         return False
#     if self.reworknum < diff:  # 修好
#         flash("修好数量大于返修数量")
#         return False
#     if self.countnum < -diff:  # 返修
#         flash("返修数量大于库存数量")
#         return False
#     return True
