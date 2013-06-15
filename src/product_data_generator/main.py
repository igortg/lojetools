from product_data_generator.lojeproductsheet_ui import LojeProductSheetUI
import Tkinter as ttk


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':    
    root = ttk.Tk()
    root.title(LojeProductSheetUI.MSG_TITLE)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe = LojeProductSheetUI(root)
    root.mainloop()
