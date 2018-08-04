import unittest
from app import create_app

def run_tests():
    tests=unittest.TestLoader().discover('.\\storage\\test','test_*.py')
    # print(tests.countTestCases())
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
    run_tests()