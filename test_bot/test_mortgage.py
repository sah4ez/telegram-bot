import unittest
from mortgage import Mortgage

class TestMortgage(unittest.TestCase):

    def testPayment(self):
        s = 10000
        p = 12
        T = 12
        mortgage = Mortgage(s, p, T)
        self.assertEqual(888.49, mortgage.payment())