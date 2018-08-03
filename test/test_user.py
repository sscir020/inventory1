# import unittest
# from app.models import *
# from app import create_app,db
#
# class UserTestCase(unittest.TestCase):
#     def setUp(self):
#         app = create_app()
#         app.app_context().push()
#         with  app.app_context():
#             if( User.query.filter_by(user_name="a").first()==None):
#                 u=User(user_name='a',user_pass='1234')
#                 u.prt()
#                 # db.create_all()
#                 db.session.add(u)
#                 db.session.commit()
#
#     def test_user(self):
#         u=User.query.filter_by(user_name="a").first()
#         u.change_pass('5678')
#         u.prt()
#
# if __name__=='__main__':
#     unittest.main()