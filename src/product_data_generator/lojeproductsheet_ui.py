#-*- coding: latin1 -*-
'''
Created on 30/12/2012

@author: igor
'''
from product_data_generator.lojeproductgenerator import LojeProductGenerator, ProductCodeError
import Tkinter as ttk
import os
import sys
import tkFileDialog
import tkFont
import tkMessageBox
import tkSimpleDialog


#===================================================================================================
# LojeProductSheetUI
#===================================================================================================
class LojeProductSheetUI(ttk.Frame):
    
    def __init__(self, *args, **kw):
        font = tkFont.Font(family='Simplified Arabic Fixed', size=11)
        ttk.Frame.__init__(self, *args, **kw)
        self.grid(column=0, row=0, sticky=ttk.NSEW)
#         self.columnconfigure(0, weight=1)
#         self.rowconfigure(0, weight=1)

        manuf_label = ttk.Label(self, text="F�brica")
        manuf_label.grid(row=0, column=0, sticky=ttk.NW)
        self.manuf_entry = manuf_entry = ttk.Entry(self)
        manuf_entry.grid(row=0, column=1, sticky=ttk.NW)
        
        price1_label = ttk.Label(self, text="Pre�o1/Pre�o2")
        price1_label.grid(row=1, column=0, sticky=ttk.NW)
        frm = ttk.Frame(self)
        frm.grid(row=1, column=1, sticky=ttk.NW)
        self.price1 = ttk.DoubleVar(0)
        price1_entry = ttk.Entry(frm, textvariable=self.price1)
        price1_entry.pack(side=ttk.LEFT)
#         price1_entry.grid(row=1, column=1)
        self.price2 = ttk.DoubleVar(0)
        price2_entry = ttk.Entry(frm, textvariable=self.price2)
#         price2_entry.grid(row=1, column=1)
        price2_entry.pack( padx=4, side=ttk.LEFT)

        products_label = ttk.Label(self, text="C�digos")
        products_label.grid(row=2, column=0, sticky=ttk.NW)
        products_entry = self.products_entry = ttk.Text(self, font=font)
        products_entry.grid(row=2, column=1, columnspan=2, sticky=(ttk.NSEW))
        self.products_entry = products_entry
             
        #unused frame  
        fr = ttk.Frame(self)
        fr.grid(column=0, row=3, sticky=ttk.W)
        
        frm_buttons = ttk.Frame(self)
        frm_buttons.grid(row=3, columnspan=3, stick=ttk.NE)
        pack_cfn = dict(padx=4, pady=4, side=ttk.LEFT)
        btn_label = ttk.Button(frm_buttons, text="Imprimir Apenas 1 Etiqueta", command=self.PrintLabel)
        btn_label.pack(pack_cfn)
        btn_print = ttk.Button(frm_buttons, text="Imprimir de Arquivo do Loje", command=self.PrintFromFile)
        btn_print.pack(pack_cfn)
        btn_gen = ttk.Button(frm_buttons, text="Gerar Arquivo do Loje", command=self.GenerateLojeSheet)
        btn_gen.pack(pack_cfn)
        frm_buttons.pack()
        
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
        self._last_dir = ""
        if hasattr(sys, "frozen"):
            app_dirname = os.path.dirname(sys.executable)
        else:
            app_dirname = os.path.dirname(__file__)
        self._barcode_filename = os.path.join(app_dirname, "barcode")
        self._config_filename = os.path.join(app_dirname, "lps.ini")
        
        lpg = self._CreateLojeProductGenerator()
        self.price1.set(lpg.price_list[0])
        self.price2.set(lpg.price_list[1])
        
        
    def GenerateLojeSheet(self):
        try:
            self._GenerateSheet()
        except Exception, exc:
            tkMessageBox.showerror(self.MSG_TITLE, exc)

        
    def _GenerateSheet(self, ):
        lpg = self._CreateLojeProductGenerator()
        initial_index = self._AskInitialBarcode(lpg)
        if not initial_index: return
        if lpg is None or not self._IsInputValid(): return
        manufacturer = self.manuf_entry.get()
        content = self.products_entry.get(1.0, ttk.END)
        lpg.price_list[0] = self.price1.get()
        lpg.price_list[1] = self.price2.get()
        try:
            sheet = lpg.GenerateLojeProductSheet(content.split("\n"), initial_index, manufacturer)
        except ProductCodeError, exc:
            tkMessageBox.showerror(self.MSG_TITLE, exc)
            return
        filename = tkFileDialog.asksaveasfilename(
            initialdir=self._last_dir, 
            title="", 
            filetypes=[('Arquivo CSV', '*.csv')],
            defaultextension=".csv",
            parent=self)
        if not filename: return
        self._last_dir = os.path.dirname(filename)
        lpg.WriteSheet(sheet, filename)
        lpg.WriteInitialBarcode(int(sheet[-1][lpg.ID_HEADER]) + 1)
        answ_print = tkMessageBox.askyesno(self.MSG_TITLE, self.MSG_ASK_PRINT)
        if answ_print:
            self._PrintLabels(lpg, sheet)
        self.clipboard_clear()
        self.clipboard_append(os.path.normpath(filename))
        tkMessageBox.showinfo(self.MSG_TITLE, "ATEN��O: Importe o arquivo gerado no Loje imediatamente!")

            
    def PrintFromFile(self):
        sheet_filename = tkFileDialog.askopenfilename()
        if not sheet_filename: return
        lps = LojeProductGenerator(self._config_filename)
        sheet = lps.LoadSheet(sheet_filename)
        self._PrintLabels(lps, sheet)
        
        
    def PrintLabel(self):
        lps = self._CreateLojeProductGenerator()
        barcode = tkSimpleDialog.askinteger(self.MSG_TITLE, self.MSG_TYPE_BARCODE, parent=self)
        if not (lps and barcode): return
        ident = tkSimpleDialog.askstring(self.MSG_TITLE, self.MSG_IDENT_CODE, parent=self)
        if not ident: return
        count = tkSimpleDialog.askinteger(
            self.MSG_TITLE, self.MSG_LABEL_COUNT, initialvalue=1, parent=self
            )
        if not count: return
        try:
            sheet = lps.GenerateLojeProductSheet([ident] * count, barcode)
        except ProductCodeError, exc:
            tkMessageBox.showerror(self.MSG_TITLE, exc)
            return
        self._PrintLabels(lps, sheet)
        
        
    def _CreateLojeProductGenerator(self):
        try:
            return LojeProductGenerator(self._config_filename)
        except Exception, exc:
            tkMessageBox.showerror(
                self.MSG_TITLE,
                "Erro ao ler arquivo de configura��o: %s" % exc,
                )


    def _IsInputValid(self):
        content = self.products_entry.get(1.0, ttk.END)
        if not content.strip():
            tkMessageBox.showerror(self.MSG_TITLE, "Lista de Produtos vazia!", parent=self)
            return False
        return True
        

    def _PrintLabels(self, lps, sheet):
        batch_size = 30
        batch_count = (len(sheet) - 1) / batch_size + 1
        for i in range(batch_count):
            start = i * batch_size
            end = (i + 1) * batch_size
            part_sheet = sheet[start:end]
            lps.PrintSheet(part_sheet)
            is_last_batch = i == batch_count - 1
            ask_more_text = self.MSG_ASK_PRINT_MORE %batch_size
            if not is_last_batch and not tkMessageBox.askokcancel(self.MSG_TITLE, ask_more_text):
                break
        
    
    def _AskInitialBarcode(self, lpg):
        initial_barcode = tkSimpleDialog.askinteger(
            self.MSG_TITLE, 
            self.MSG_TYPE_BARCODE + "Inicial", 
            initialvalue=lpg.AcquireInitialBarcode(),
            parent=self)
        return initial_barcode
    
    
    MSG_ASK_PRINT = "Arquivo criado com sucesso. Deseja imprimir etiquetas?"
    MSG_TYPE_BARCODE = "Digite o C�digo de Barras"
    MSG_IDENT_CODE = "Digite o C�digo de Identifica��o (ex.: ABL00090)"
    MSG_LABEL_COUNT = "Digite o n�mero de c�pias desejadas"
    MSG_ASK_PRINT_MORE = "Imprimir mais %d etiquetas?"
    MSG_TITLE = "Entrade de Produtos Loje"
