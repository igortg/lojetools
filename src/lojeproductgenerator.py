#-*- coding: latin1 -*-
from ConfigParser import ConfigParser
from string import Template
from StringIO import StringIO
import csv
import locale


#===================================================================================================
# LojeProductGenerator
#===================================================================================================
class LojeProductGenerator(object):
    
    PRICE_SEC = "Preco"
    PRIMARY_CATEGORY_SEC = "Categoria1"
    SECONDARY_CATEGORY_SEC = "Categoria2"
    
    CSV_DELIMITER = ';'
    
    BARCODE_HEADER = "codbar"
    IDENT_HEADER = "identificacao"
    ID_HEADER = "id"
    CATEGORY_HEADER = "categoria"
    
    HEADER_LIST = [
        ID_HEADER,
        BARCODE_HEADER,
        IDENT_HEADER,
        CATEGORY_HEADER,
        "unidade compra",
        "unidade venda",
        "custo",
        "preco",
        "preco2",
        "estoque",
        "descricao",
        "fabricante"            
        ]

    
    def __init__(self, config_filename):
        locale.setlocale(locale.LC_ALL, '')
        cfg_parser = ConfigParser()
        cfg_parser.read(config_filename)
        
        self._primary_category_list = dict(cfg_parser.items(self.PRIMARY_CATEGORY_SEC))
        self._secondary_category_list = dict(cfg_parser.items(self.SECONDARY_CATEGORY_SEC))
        self._price_list = []
        for opt in sorted(cfg_parser.options(self.PRICE_SEC)):
            self._price_list.append(cfg_parser.getfloat(self.PRICE_SEC, opt))
        
        self._label_header = cfg_parser.get("Label", "header").replace("\\n","\n")
        self._label_template = cfg_parser.get("Label", "label")
        self._labels_per_file = 30
        
        
    def GenerateLojeProductSheet(self, product_ident_list, start_index, manufacturer=""):
        unity = "p�"
        sheet = []
        previous_product_ident = None
        product_ident_list.sort()
        product_index = start_index - 1
        for i, product_ident in enumerate(product_ident_list):
            row = {}
            if product_ident != previous_product_ident:
                product_index += 1            
            row[self.ID_HEADER] = product_index
            row[self.BARCODE_HEADER] = "%06d" %product_index
            row[self.IDENT_HEADER] = product_ident.upper()
            try:
                category = self._primary_category_list[product_ident[0].lower()]
            except KeyError:
                raise ProductCodeError(product_ident[0], i)
            row[self.CATEGORY_HEADER] = category
            row["unidade compra"] = unity
            row["unidade venda"] = unity
            price = float(product_ident[3:]) / 10.
            cost = price / self._price_list[0]
            price2 = price * self._price_list[1]
            
            row["custo"] = locale.str(round(cost, 2))
            row["preco"] = locale.str(round(price, 2))
            row["preco2"] = locale.str(round(price2, 2))
            row["estoque"] = "c"
            try:
                sec_category = self._secondary_category_list[product_ident[1:3].lower()]
            except KeyError:
                raise ProductCodeError(product_ident[1:3], i)
            row["descricao"] = "%s" %(sec_category)
            row["fabricante"] = manufacturer
            sheet.append(row)
            previous_product_ident = product_ident
        return sheet
    
    
    def WriteSheet(self, sheet, out_filename):
        with open(out_filename, 'w') as out_file:           
            writer = csv.DictWriter(
                out_file,
                self.HEADER_LIST,
                delimiter=self.CSV_DELIMITER,
                lineterminator="\n",
                quoting=csv.QUOTE_ALL 
                )
            writer.writeheader()
            writer.writerows(sheet)
            

    @classmethod            
    def LoadSheet(cls, sheet_filename):
        with open(sheet_filename) as sheet_file:
            reader = csv.DictReader(
                sheet_file,
                cls.HEADER_LIST,
                delimiter=cls.CSV_DELIMITER,
                lineterminator="\n",
                quoting=csv.QUOTE_ALL,
                )
            sheet = [line for line in reader]
            return sheet[1:] #Discart header line
                
                
    def PrintSheet(self, loje_product_sheet):
        epl_code = self._GenerateEpl(loje_product_sheet)
        self._SentToPrinter(epl_code)
            
            
    def _GenerateEpl(self, loje_product_sheet):
        stream = StringIO()
        header = self._label_header + "\n"
        stream.write(header)
        for row in loje_product_sheet:
            label = self._GeneratLabelEpl(row) + "\n"
            stream.write(label)
        return stream.getvalue()        
            
            
    def _SentToPrinter(self, epl_code):
        from zebra import zebra
        zebra = zebra('ZDesigner TLP 2844')
        zebra.output(epl_code)
        

    def _GenerateEplFile(self, loje_product_sheet, out_basename):
        file_index = 0
        prn_file = None
        for i, row in enumerate(loje_product_sheet):
            if i % self._labels_per_file == 0:
                file_index += 1
                if prn_file:
                    prn_file.close()
                prn_filename = out_basename + "-%02d.epl" %file_index
                prn_file = open(prn_filename, "w")
                prn_file.write(self._label_header + "\n")
            prn_file.write(self._GeneratLabelEpl(row) + "\n")


    def _GeneratLabelEpl(self, row):
        template = Template(self._label_template)
        return template.substitute(**row)


#===================================================================================================
# ProductCodeError
#===================================================================================================
class ProductCodeError(Exception):
    
    def __init__(self, code, index):
        Exception.__init__(
            self,
            "Nao foi possivel encontrar correspondencia para codigo '%s' (item %d)" %(code, index+1)
        )