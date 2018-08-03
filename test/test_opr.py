# import unittest
# from app.models import *
# from app import create_app,db
#
# class OprTestCase(unittest.TestCase):
#     def test_add(self):
#         app = create_app()
#         app.app_context().push()
#         with  app.app_context():
#             o=Opr(user_id='1',diff='3',material_id='2')
#             o.prt()
#             # db.create_all()
#             db.session.add(o)
#             db.session.commit()
#
#
#
# if __name__=='__main__':
#     print(__name__)
#     unittest.main()