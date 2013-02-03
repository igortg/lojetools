import unittest
from productpost import QuoteSpacedText, GenerateBarcodes, GenerateBarcodesPrn


#===============================================================================
# TestCase
#===============================================================================
class TestCase(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def testQuoteSpacedText(self):
        QuoteSpacedText("test.out.csv")


    def testGenerateBarcodes(self):
        GenerateBarcodes("test.csv", "test.out.csv", 1)


    def testGenerateBarcodesPrn(self):
        GenerateBarcodesPrn("test.out.csv", 5)

#===============================================================================
# main
#===============================================================================
if __name__ == '__main__':
    unittest.main()