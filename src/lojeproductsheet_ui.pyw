#-*- coding: latin1 -*-
'''
Created on 30/12/2012

@author: igor
'''
from lojeproductsheet import LojeProductSheet, ProductCodeError
import Tkinter as ttk
import os
import tkFileDialog
import tkFont
import tkMessageBox
import tkSimpleDialog


#===================================================================================================
# LojeProductSheetUI
#===================================================================================================
class LojeProductSheetUI(ttk.Frame):
    
    def __init__(self, *args, **kw):
        ttk.Frame.__init__(self, *args, **kw)
        self.grid(column=0, row=0, sticky=ttk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        font = tkFont.Font(family='Simplified Arabic Fixed', size=11)
        products_entry = ttk.Text(self, font=font)
        products_entry.grid(row=0, columnspan=2, sticky=(ttk.NSEW))
        self.products_entry = products_entry
             
        #unused frame  
        fr = ttk.Frame(self)
        fr.grid(column=0, row=1, sticky=ttk.W)
        
        btn = ttk.Button(self, text="Gerar Saída", command=self.GenerateSheet)
        btn.grid(column=1, row=1, sticky=ttk.E)
        
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
        self._last_dir = ""
        app_dirname = os.path.dirname(__file__)
        self._barcode_filename = os.path.join(app_dirname, "barcode")
        self._config_filename = os.path.join(app_dirname, "lps.ini")


    def GenerateSheet(self):
        title = "Gerar Saída"
        content = self.products_entry.get(1.0, ttk.END)
        if not content:
            tkMessageBox.showerror(title, "Lista de Produtos vazia!", parent=self)
            return
        initial_barcode = tkSimpleDialog.askinteger(
            title, 
            "Digite o Código de Barras Inicial",
            initialvalue=self.AcquireInitialBarcode(),
            parent=self)
        if not initial_barcode:
            return

        lps = LojeProductSheet(self._config_filename)
        try:
            sheet = lps.GenerateLojeProductSheet(content.split(), initial_barcode)
        except ProductCodeError, exc:
            tkMessageBox.showerror(title, exc)
            return
        filename = tkFileDialog.asksaveasfilename(initialdir=self._last_dir, title="", parent=self)
        if not filename:
            return
        self._last_dir = os.path.dirname(filename)
        lps.WriteSheet(sheet, filename)
        lps.GenerateBarcodesPrn(sheet, filename)
        self.WriteInitialBarcode(int(sheet[-1]['codbar']) + 1)
        tkMessageBox.showinfo(title, "Arquivo criado com sucesso!")
        
        
    def AcquireInitialBarcode(self):
        if not os.path.isfile(self._barcode_filename):
            self.WriteInitialBarcode(1)
        with open(self._barcode_filename) as barcode_file:
            return int(barcode_file.read().strip())
                
                
    def WriteInitialBarcode(self, barcode):
        with open(self._barcode_filename, 'w') as barcode_file:
            barcode_file.write('%d' %barcode)

#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':    
    root = ttk.Tk()
    root.title("Entrade de Produtos Loje")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe = LojeProductSheetUI(root)
    root.mainloop()
