from labelprinter.lojeproductgenerator import LojeProductGenerator, ProductCodeError
import unittest


#===================================================================================================
# TestLojeProductSheet
#===================================================================================================
class TestLojeProductGenerator(unittest.TestCase):
    
    
    def setUp(self):
        self.lps = LojeProductGenerator("../lps.ini")
    
    
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
        lps._GenerateEplFile(sheet, "lps")
        
        
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
        sheet_filename = "test.out.csv"
        lps = self.lps
        sheet = lps.LoadSheet(sheet_filename)
        self.assertEqual(sheet[0]['codbar'], "000300")
        self.assertEqual(sheet[1]['codbar'], "000301")
        

    def test(self):
        d2 = ord('z') - ord('a')
        d1 = ord('c') - ord('a')
        d2, d1
        d2 * 26 + d1 * 1


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':
    unittest.main()