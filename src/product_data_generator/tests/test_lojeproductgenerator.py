import os
from product_data_generator.lojeproductgenerator import LojeProductGenerator, ProductCodeError
import unittest


class TestLojeProductGenerator(unittest.TestCase):
    
    
    def setUp(self):
        self.test_dirname = os.path.dirname(__file__)
        self.lps = LojeProductGenerator(os.path.join(self.test_dirname, "lps.ini"))


    def testGenerateLojeProducts(self):
        test_list = [
         "ppt00235",
         "bbl00300",
         "abl00145",
         "ppt00235 2",
         "abl00145",
        ]
        
        lps = self.lps
        sheet = lps.GenerateLojeProductSheet(test_list, 10)
        self.assertEqual(sheet[0][lps.IDENT_HEADER], "ABL00145")
        self.assertEqual(sheet[0][lps.QUANTITY_HEADER], 2)
        self.assertEqual(sheet[1][lps.ID_HEADER], 11)
        self.assertEqual(sheet[1][lps.QUANTITY_HEADER], 1)
        self.assertEqual(sheet[2][lps.ID_HEADER], 12)
        self.assertEqual(sheet[2][lps.QUANTITY_HEADER], 3)
        
        
    def testGenerateLojeProductSheetErrorHandling(self):
        test_list = [
         "b2e00300",
         "aco00145",
         "ppt00235"
        ]
        
        lps = self.lps
        self.assertRaises(ProductCodeError, lps.GenerateLojeProductSheet, test_list, 10)

        
    def testPrintLabels(self):
        test_list = [
         "bbl00300",
         "aco00145",
         "ppt00235"
         ]
        
        lps = self.lps
        sheet = lps.GenerateLojeProductSheet(test_list, 10)
        lps._GenerateEpl(sheet)
        
        
    def testLoadSheet(self):
        sheet_filename = os.path.join(self.test_dirname, "test.out.csv")
        lps = self.lps
        sheet = lps.LoadSheet(sheet_filename)
        self.assertEqual(sheet[0]['codbar'], "000300")
        self.assertEqual(sheet[1]['codbar'], "000301")
        

    def testHash(self):
        d2 = ord('z') - ord('a')
        d1 = ord('c') - ord('a')
        d2, d1
        d2 * 26 + d1 * 1


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':
    unittest.main()