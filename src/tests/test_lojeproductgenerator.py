from lojeproductgenerator import LojeProductGenerator, ProductCodeError
import unittest


#===================================================================================================
# TestLojeProductSheet
#===================================================================================================
class TestLojeProductGenerator(unittest.TestCase):
    
    def testGenerateLojeProducts(self):
        
        test_list = [
         "pcb00235",
         "b2e00300",
         "abl00145",
         "pcb00235",
         "abl00145",
        ]
        
        lps = LojeProductGenerator("lps.ini")
        sheet = lps.GenerateLojeProductSheet(test_list, 10)
        self.assertEqual(sheet[0][lps.IDENT_HEADER], "ABL00145")
        self.assertEqual(sheet[1][lps.ID_HEADER], 10)
        self.assertEqual(sheet[3][lps.ID_HEADER], 12)
        self.assertEqual(sheet[4][lps.ID_HEADER], 12)
        lps._GenerateEplFile(sheet, "lps")
        
        
    def testGenerateLojeProductSheetErrorHandling(self):
        
        test_list = [
         "b2e00300",
         "awz00145",
         "pcb00235"
        ]
        
        lps = LojeProductGenerator("lps.ini")
        self.assertRaises(ProductCodeError, lps.GenerateLojeProductSheet, test_list, 10)

        
    def testPrintLabels(self):
        
        test_list = [
         "pcb00235",
         "b2e00300",
         "abl00145",
         ]
        
        lps = LojeProductGenerator("lps.ini")
        sheet = lps.GenerateLojeProductSheet(test_list, 10)
        lps._GenerateEpl(sheet)
        
        
    def testLoadSheet(self):
        sheet_filename = "test.out.csv"
        lps = LojeProductGenerator("lps.ini")
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