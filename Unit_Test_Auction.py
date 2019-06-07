import unittest
from Leap import Auction

class TestAuction(unittest.TestCase):

    def test_one(self):
        self.assertEqual(str(Auction("Test1.txt")._winners[0]), '18|430|13|SOLD|0.15|4|0.15|0.10')
        
    def test_two(self):
        self.assertEqual(str(Auction("Test2.txt")._winners), '[18|430|8|SOLD|0.20|4|0.20|0.07, 22|431||UNSOLD|0.00|3|0.15|0.14, 22|432|21|SOLD|0.07|3|0.15|0.07]')

    def test_three(self):
        self.assertEqual(str(Auction("Test3.txt")._winners), '[22|432|8|SOLD|0.12|1|0.12|0.12]')

    def test_four(self):
        self.assertEqual(str(Auction("Test4.txt")._winners), "[18|430|8|SOLD|0.20|4|0.20|0.01, 22|431||UNSOLD|0.00|3|0.15|0.14, 23|432|21|SOLD|0.07|3|0.15|0.07, 24|433|44|SOLD|0.01|3|0.04|0.01]")

    def test_five(self):
        self.assertEqual(str(Auction("Test5.txt")._winners),'[18|430|8|SOLD|0.03|3|0.07|0.03]')
        
    
if __name__ == '__main__':
    unittest.main()
