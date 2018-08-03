# import unittest
# from app.models import *
# from app import create_app,db
# from main_config import Sensorname,Oprenum,Param,params,paramnums
# import datetime
# import json
# class paramTestCase(unittest.TestCase):
#     def test_add(self):
#         brands={'brand3':Param.PARAM_3,'brand5':Param.PARAM_5,'brand7':Param.PARAM_7}
#         app = create_app('development')#development#testing
#         app.app_context().push()
#         with  app.app_context():
#             # print('***********************')
#             # print(list(brands)[0])
#             # print(list(brands.values())[0].name)
#             # print('***********************')
#             # print(params[Param.PARAM_THREE.name])
#             # for item in params[Param.PARAM_THREE.name]:
#             #     print(item)
#             # print(paramnums[Param.PARAM_THREE.name])
#             # for i in range(0,Param.PARAM_THREE.value):
#             #     print(list(params[Param.PARAM_THREE.name])[i])
#             #     print((params[Param.PARAM_THREE.name])[i])
#             #     print(paramnums[Param.PARAM_THREE.name][i])
#             for i in range(1,28):
#                 m=Material(material_name=Sensorname(i).name,countnum=20,acces_id=0,alarm_level=20)
#                 db.session.add(m)
#
#             # m=Material(material_name=list(brands)[0],countnum=5,acces_id=1,alarm_level=5)
#             # db.session.add(m)
#             # m = Material(material_name=list(brands)[1], countnum=5, reworknum=0, paramtype=list(brands.values())[1].name)
#             # db.session.add(m)
#             # m = Material(material_name=list(brands)[2], countnum=5, reworknum=0, paramtype=list(brands.values())[2].name)
#             # db.session.add(m)
#             # db.session.commit()
#             #
#             # for i in range(1,2):
#             #     o=Opr(user_id=i,diff=5,material_id=i+27,oprtype=Oprenum.INITADD.name,isgroup=1)
#             #     db.session.add(o)
#             db.session.commit()
#
#
#
#             # a= Accessory(param_num=3,param_acces=json.dumps({1:1,2:1,3:1}))
#             # db.session.add(a)
#             # a = Accessory(param_num=5, param_acces=json.dumps({1: 1, 2: 1, 3: 1,4:1,5:1}))
#             # db.session.add(a)
#             # a = Accessory(param_num=7, param_acces=json.dumps({1: 1, 2: 1, 3: 1,4:1,5:1,6:1,7:1}))
#             # db.session.add(a)
#             # db.session.commit()
#
#             # for i in range(1, 28):
#             #     m = Material(material_name=Sensorname(i).name, countnum=10, reworknum=0)
#             #     db.session.add(m)
#             # m = Material(material_name=list(brands)[0], countnum=5, reworknum=0, acces_id=1)
#             # db.session.add(m)
#             # m = Material(material_name=list(brands)[1], countnum=5, reworknum=0, acces_id=2)
#             # db.session.add(m)
#             # m = Material(material_name=list(brands)[2], countnum=5, reworknum=0, acces_id=3)
#             # db.session.add(m)
#             #
#             # for i in range(1, 4):
#             #     o = Opr(user_id=i, diff='5', material_id=i + 27, oprtype=Oprenum.INITADD.name,
#             #             momentary=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#             #     db.session.add(o)
#             # db.session.commit()
#
