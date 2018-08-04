import unittest
from main_config import Oprenum,Sensorname
from app.models import Customerservice
from app import dbsession

class SqlalchemyTestCase(unittest.TestCase):

    def test_gothrough(self):
        services=dbsession.query(Customerservice).all()
        for s in services:
            print(s.service_id)
            print(s.MN_id)
        services=dbsession.query(Customerservice).filter(Customerservice.MN_id =='914403005990821317042201').all()
        for s in services:
            print(s.service_id)
            print(s.MN_id)
