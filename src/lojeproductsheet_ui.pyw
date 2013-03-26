#-*- coding: latin1 -*-
'''
Created on 30/12/2012

@author: igor
'''
from lojeproductgenerator import LojeProductGenerator, ProductCodeError
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
        
        btn_print = ttk.Button(self, text="Imprimir de Arquivo", command=self.PrintFromFile)
        btn_print.grid(column=0, row=1, sticky=ttk.E)
        btn_gen = ttk.Button(self, text="Gerar Saída", command=self.GenerateSheet)
        btn_gen.grid(column=1, row=1, sticky=ttk.E)
        
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
        self._last_dir = ""
        app_dirname = os.path.dirname(__file__)
        self._barcode_filename = os.path.join(app_dirname, "barcode")
        self._config_filename = os.path.join(app_dirname, "lps.ini")

        
    def GenerateSheet(self):
        if not self._IsInputValid(): return
        initial_barcode = self._AksInitialBarcode()
        if not initial_barcode: return
        content = self.products_entry.get(1.0, ttk.END)
        lps = LojeProductGenerator(self._config_filename)
        try:
            sheet = lps.GenerateLojeProductSheet(content.split(), initial_barcode)
        except ProductCodeError, exc:
            tkMessageBox.showerror(self.MSG_TITLE, exc)
            return
        filename = tkFileDialog.asksaveasfilename(initialdir=self._last_dir, title="", parent=self)
        if not filename: return
        self._last_dir = os.path.dirname(filename)
        lps.WriteSheet(sheet, filename)
        self._WriteInitialBarcode(int(sheet[-1]['codbar']) + 1)
        answ_print = tkMessageBox.askyesno(self.MSG_TITLE, self.MSG_ASK_PRINT)
        if answ_print:
            self._PrintLabels(lps, sheet)
            
            
    def PrintFromFile(self):
        sheet_filename = tkFileDialog.askopenfilename()
        if not sheet_filename: return
        lps = LojeProductGenerator(self._config_filename)
        sheet = lps.LoadSheet(sheet_filename)
        self._PrintLabels(lps, sheet)
        
        
        
    def _IsInputValid(self):
        content = self.products_entry.get(1.0, ttk.END)
        if not content.strip():
            tkMessageBox.showerror(self.MSG_TITLE, "Lista de Produtos vazia!", parent=self)
            return False
        return True
        

    def _PrintLabels(self, lps, sheet):
        batch_size = 30
        batch_num = (len(sheet) - 1) / batch_size + 1
        for i in range(batch_num):
            start = i * batch_size
            end = (i + 1) * batch_size
            part_sheet = sheet[start:end]
            lps.PrintSheet(part_sheet)
            if i < batch_num - 1:
                tkMessageBox.askokcancel(self.MSG_TITLE, self.MSG_ASK_PRINT_MORE %batch_size)
        
    
    def _AksInitialBarcode(self):
        initial_barcode = tkSimpleDialog.askinteger(
            self.MSG_TITLE, 
            self.MSG_TYPE_BARCODE, 
            initialvalue=self._AcquireInitialBarcode(), 
            parent=self)
        return initial_barcode
    
    
    def _AcquireInitialBarcode(self):
        if not os.path.isfile(self._barcode_filename):
            self._WriteInitialBarcode(1)
        with open(self._barcode_filename) as barcode_file:
            return int(barcode_file.read().strip())
                
                
    def _WriteInitialBarcode(self, barcode):
        with open(self._barcode_filename, 'w') as barcode_file:
            barcode_file.write('%d' %barcode)


    MSG_ASK_PRINT = "Arquivo criado com sucesso. Deseja imprimir etiquetas?"
    MSG_TYPE_BARCODE = "Digite o Código de Barras Inicial"
    MSG_ASK_PRINT_MORE = "Imprimir mais %d etiquetas?"
    MSG_TITLE = "Entrade de Produtos Loje"


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
