from product_data_generator.lojeproductgenerator import LojeProductGenerator
from product_data_generator.lojeproductsheet_ui import LojeProductSheetUI
import Tkinter as ttk
import sys
import unittest


#===================================================================================================
# TestCase
#===================================================================================================
class TestCase(unittest.TestCase):
    
    def setUp(self):
        self._root = ttk.Tk()
        self.widget = LojeProductSheetUI(self._root)
        LojeProductGenerator._SendToPrinter = lambda s,out: sys.stdout.write(out)
    
        
    def testMet1(self):
        widget = self.widget
        for x in range(40):
            widget.products_entry.insert(ttk.END, "ABL00%d0\n" %x)
        self._root.mainloop()
        


#===================================================================================================
# main        
#===================================================================================================
if __name__ == '__main__':
    unittest.main()