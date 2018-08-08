#coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
from enum import Enum
class Uri:
	DEVELOPMENT_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hard_guess@localhost:3306/testdb1?charset=utf8&autocommit=true'
	DEVELOPMENT_SQLALCHEMY_DATABASE_URI_1 = 'sqlite:///D:\\projects\\inventory2\\database\\data.sqlite'
	TESTING_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aosien2016@120.76.207.142:3306/inventory?charset=utf8&autocommit=true'

class Config:
    SECRET_KEY =  '1AR4bnTnLHZyHaKt' #os.environ.get('SECRET_KEY') or
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hard_guess@localhost:3306/testdb1?charset=utf8&autocommit=true'
    SQLALCHEMY_BINDS ={
        'web_device': 'mysql+pymysql://root:Aosien2016@120.76.207.142:3306/osen?charset=utf8&autocommit=true',
    }
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 0
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_NUM_PER_PAGE = 15
    # FLASK_NUM_PER_PAGE_LIST = 6
#SESSION_TYPE= 'redis'
    SESSION_PERMANENT = True
    # SESSION_KEY_PREFIX='sessionp'
    MAX_CHAR_PER_COMMENT = 64
    DATABASE_URI=Uri.DEVELOPMENT_SQLALCHEMY_DATABASE_URI


    @staticmethod
    def init_app(app):
        pass




class Oprenum(Enum):
    INITADD = 1
    BUY = 2
    REWORK = 3
    PREPARE = 4
    OUTBOUND = 5
    RECYCLE = 6
    RESALE = 7
    INBOUND = 8
    CANCELBUY = 9
    RESTORE = 10
    SCRAP = 11
    CSBROKEN = 12
    CSGINBOUND = 13
    CSREWORK = 14
    CSRESTORE = 15
    CSSCRAP = 16
    CSMRESALE = 17
    CSDRECYCLE = 18
    CSDRESTORE = 19
    CSDRESALE = 20
    CSFEE = 21
    CSFEEZERO = 22
    COMMENT = 32
    # DINITADD=12
    # DPREPARE=13
    # DOUTBOUND=14
    # CINITADD=16
    # CSRINBOUND=18
    # RINBOUND =24
oprenumCH ={
    Oprenum.INITADD.name: '新添加材料',#
    Oprenum.INBOUND.name: '入库',
    Oprenum.OUTBOUND.name: '出库',
    Oprenum.RESTORE.name: '修好',
    Oprenum.REWORK.name: '返修',
    Oprenum.BUY.name:"购买",#
    Oprenum.CANCELBUY.name:'取消购买',
    Oprenum.SCRAP.name:'报废',
    Oprenum.RECYCLE.name:'材料售后带回',
    Oprenum.RESALE.name:'材料售后售出',
    Oprenum.PREPARE.name:'备货',#
    # Oprenum.DINITADD.name:'新添加设备',
    # Oprenum.DPREPARE.name:'设备备货',
    # Oprenum.DOUTBOUND.name:'设备出库',
    Oprenum.CSDRECYCLE.name:'设备售后带回',
    # Oprenum.CINITADD.name:'新添加客户',#
    Oprenum.CSGINBOUND.name:'材料售后完好入库',
    # Oprenum.CSRINBOUND.name:'材料售后修好入库',
    Oprenum.CSREWORK.name:'材料售后返修',
    Oprenum.CSRESTORE.name:'材料售后修好',
    Oprenum.CSSCRAP.name:'材料售后报废',#
    Oprenum.CSBROKEN.name:'材料售后损坏',
    Oprenum.CSDRESALE.name:'设备售后售出',
    # Oprenum.RINBOUND.name:'材料修好入库',
    Oprenum.CSFEE.name:'增加售后售出费用',
    Oprenum.CSFEEZERO.name:'欠费清零',
    Oprenum.CSDRESTORE.name:'设备售后修好',
    Oprenum.CSMRESALE.name:'材料售后售出',
    Oprenum.COMMENT.name:'备注',
}
oprenumNum = {
    '新添加材料':Oprenum.INITADD,#
    '入库':Oprenum.INBOUND,
    '出库':Oprenum.OUTBOUND,
    '修好':Oprenum.RESTORE,
    '返修':Oprenum.REWORK,
    '购买':Oprenum.BUY,#
    '取消购买':Oprenum.CANCELBUY,
    '报废':Oprenum.SCRAP,
    '材料售后带回':Oprenum.RECYCLE,
    '材料售后带出':Oprenum.RESALE,
    '备货':Oprenum.PREPARE,#
    # '新添加设备':Oprenum.DINITADD,
    # '设备备货':Oprenum.DPREPARE,
    # '设备出库':Oprenum.DOUTBOUND,
    '设备售后带回':Oprenum.CSDRECYCLE,
    # '新添加客户':Oprenum.CINITADD,
    '材料售后完好入库':Oprenum.CSGINBOUND,#
    # '材料售后修好入库':Oprenum.CSRINBOUND,#
    '材料售后返修':Oprenum.CSREWORK,
    '材料售后修好': Oprenum.CSRESTORE,
    '材料售后报废':Oprenum.CSSCRAP,
    '材料售后损坏':Oprenum.CSBROKEN,
    '设备售后售出':Oprenum.CSDRESALE,
    # '材料修好入库':Oprenum.RINBOUND,
    '增加售后售出费用':Oprenum.CSFEE,
    '欠费清零':Oprenum.CSFEEZERO,
    '设备售后修好':Oprenum.CSDRESTORE.name,
    '材料售后售出':Oprenum.CSMRESALE.name,
    '备注':Oprenum.COMMENT,
}

class CommentType(Enum):
    BUY=1
    REWORK=2
    DEVICE=3
    CLIENT =4
    CUSTOMERSERVICE=5

class Sensorname(Enum):
    P25 = 1
    P10 = 2
    TSP = 3
    NOISE = 4
    WINDSPEED = 5
    WINDDIRECTION = 6
    TEMP = 7
    PRESSURE = 8
    HUMIDITY = 9
    NEGOXYGEN = 10
    RAINFALL = 11
    ILLUM = 12
    CH2O = 13
    SO2 = 14
    NO2 = 15
    O3 = 16
    CO = 17
    CO2 = 18
    H2S = 19
    VOC = 20
    O2 = 21
    RADIATION = 22
    NH3 = 23
    SOILTEMP = 24
    SOILHUMIDITY = 25
    PHOTOSYNTHESIS = 26
    ULTRAVIOLETRAYS = 27


class Prt():
    def prt(start='',arg1='',arg2='',arg3='',arg4='',arg5='',arg6='',arg7='',arg8='',arg9='',arg10=''):
        print("*********************************************************************")
        print(str(start)+","+str(arg1)+","+str(arg2)+","+str(arg3)+","+str(arg4)+","+str(arg5)+","+str(arg6)+","+str(arg7)+","+str(arg8)+","+str(arg9)+","+str(arg10))
        print("---------------------------------------------------------------------")



