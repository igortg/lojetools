from lojeproductsheet import LojeProductSheet, ProductCodeError
import unittest


#===================================================================================================
# TestLojeProductSheet
#===================================================================================================
class TestLojeProductSheet(unittest.TestCase):
    
    def testGenerateLojeProductSheet(self):
        
        test_list = [
         "pcb00235",
         "b2e00300",
         "abl00145",
         "pcb00235",
         "abl00145",
        ]
        
        lps = LojeProductSheet("lps.ini")
        sheet = lps.GenerateLojeProductSheet(test_list, 10)
        self.assertEqual(sheet[0][lps.IDENT_HEADER], "ABL00145")
        self.assertEqual(sheet[1][lps.ID_HEADER], 10)
        self.assertEqual(sheet[3][lps.ID_HEADER], 12)
        self.assertEqual(sheet[4][lps.ID_HEADER], 12)
        lps.GenerateBarcodesPrn(sheet, "lps")
        
        
    def testGenerateLojeProductSheetErrorHandling(self):
        
        test_list = [
         "b2e00300",
         "awz00145",
         "pcb00235"
        ]
        
        lps = LojeProductSheet("lps.ini")
        self.assertRaises(ProductCodeError, lps.GenerateLojeProductSheet, test_list, 10)

        
    def testPrintLabels(self):
        
        test_list = [
         "pcb00235",
         "b2e00300",
         "abl00145",
         ]
        
        lps = LojeProductSheet("lps.ini")
        sheet = lps.GenerateLojeProductSheet(test_list, 10)
        lps.GenerateEpl(sheet)


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