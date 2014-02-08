#-*- coding: latin1 -*-
from ConfigParser import ConfigParser
from StringIO import StringIO
from string import Template
import csv
import socket

import re
import locale
import os


class LojeProductGenerator(object):

    PRICE_SEC = "Preco"
    PRIMARY_CATEGORY_SEC = "Categoria1"
    SECONDARY_CATEGORY_SEC = "Categoria2"
    
    CSV_DELIMITER = ';'
    
    BARCODE_HEADER = "codbar"
    IDENT_HEADER = "identificacao"
    ID_HEADER = "id"
    CATEGORY_HEADER = "categoria"
    QUANTITY_HEADER = "count"
    
    HEADER_LIST = [
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
        "fabricante",
        "categoria2",
        QUANTITY_HEADER,
        ]

    
    def __init__(self, config_filename):
        locale.setlocale(locale.LC_ALL, '')
        assert os.path.isfile(config_filename), "Config file not found"
        local_config_parser = ConfigParser()
        local_config_parser.read(config_filename)
        product_info_filename = local_config_parser.get("Config", "info_produtos")
        self._printer_name = local_config_parser.get("Config", "impressora")
        assert os.path.isfile(product_info_filename), "Product info file not found"
        # Set barcode filename
        self._barcode_filename = os.path.join(
            os.path.dirname(product_info_filename),
            "barcode"
        )

        cfg_parser = ConfigParser()
        cfg_parser.read(product_info_filename)

        self._primary_categories = dict(cfg_parser.items(self.PRIMARY_CATEGORY_SEC))
        self._secondary_categories = dict(cfg_parser.items(self.SECONDARY_CATEGORY_SEC))

        if cfg_parser.has_section(self.PRICE_SEC):
            self.price_list = []
            for opt in sorted(cfg_parser.options(self.PRICE_SEC)):
                self.price_list.append(cfg_parser.getfloat(self.PRICE_SEC, opt))
        else:
            self.price_list = [1.7, 2.21]
        
        self._label_header = cfg_parser.get("Label", "header").replace("\\n","\n")
        self._label_template = cfg_parser.get("Label", "label")
        self._labels_per_file = 30
        self._product_unity = "pç"
        self._category_on_label = cfg_parser.getint("Geral", "cat_etiqueta")
        
        
    def GenerateLojeProductSheet(self, product_ident_list, start_index, manufacturer="", increase_index=True):
        sheet = []
        product_index = start_index - 1
        product_ident_list = self._ProcessProductQuantities(product_ident_list)
        print product_ident_list
        for product_ident, quantity in product_ident_list:
            row = {}
            product_index += 1            
            row[self.ID_HEADER] = product_index
            if self._category_on_label:
                barcode = "%s%06d" % (product_ident[0].upper(), product_index)
                try:
                    int(barcode)
                except ValueError:
                    pass
                else:
                    raise RuntimeError("Product Barcode couldn't be an Integer")
            else:
                barcode = "%06d" % product_index
            row[self.BARCODE_HEADER] = barcode
            row[self.IDENT_HEADER] = product_ident.upper()
            try:
                category = self._primary_categories[product_ident[0].lower()]
            except KeyError:
                raise ProductCodeError(product_ident[0])
            row[self.CATEGORY_HEADER] = category
            row["unidade compra"] = self._product_unity
            row["unidade venda"] = self._product_unity
            price = float(product_ident[3:]) / 10.
            cost = price / self.price_list[0]
            price2 = cost * self.price_list[1]
            
            row["custo"] = locale.str(round(cost, 2))
            row["preco"] = locale.str(round(price, 2))
            row["preco2"] = locale.str(round(price2, 2))
            row["estoque"] = "v"
            try:
                sec_category = self._secondary_categories[product_ident[1:3].lower()]
            except KeyError:
                raise ProductCodeError(product_ident[1:3])
            row["descricao"] = "%s %s" % (category, sec_category)
            row["categoria2"] = sec_category
            row["fabricante"] = manufacturer
            row[self.QUANTITY_HEADER] = quantity
            sheet.append(row)
        return sheet
    
    
    def _ProcessProductQuantities(self, product_ident_list):
        quantity_list = []
        for line in sorted(product_ident_list):
            if not line.strip():
                continue
            try:
                product_ident, quantity = line.split()
            except ValueError:
                product_ident, quantity = line, 1
            product_ident = product_ident.strip().upper()
            quantity = int(quantity)
            if len(quantity_list) and product_ident == quantity_list[-1][0]:
                new_quantity = quantity_list[-1][1] + quantity
                quantity_list[-1] = (product_ident, new_quantity)
            else:
                quantity_list.append((product_ident, quantity))
        return quantity_list
    
    
    def WriteSheet(self, sheet, out_filename):
        with open(out_filename, 'w') as out_file:           
            writer = csv.DictWriter(
                out_file,
                self.HEADER_LIST,
                delimiter=self.CSV_DELIMITER,
                lineterminator="\n",
                quoting=csv.QUOTE_ALL,
                extrasaction='ignore',
                )
            writer.writeheader()
            writer.writerows(sheet)
            

    @classmethod            
    def LoadSheet(cls, sheet_filename):
        with open(sheet_filename) as sheet_file:
            header_line = sheet_file.readline()
            header = [col.strip('"') for col in header_line.split(";")]
            reader = csv.DictReader(
                sheet_file,
                header,
                delimiter=cls.CSV_DELIMITER,
                lineterminator="\n",
                quoting=csv.QUOTE_ALL,
                )
            sheet = [line for line in reader]
            return sheet[1:] #Discart header line
                
                
    def PrintSheet(self, loje_product_sheet):
        epl_code = self._GenerateEpl(loje_product_sheet)
        self._SendToPrinter(epl_code)


    def WriteInitialBarcode(self, barcode):
        with open(self._barcode_filename, 'w') as barcode_file:
            barcode_file.write('%d' %barcode)


    def AcquireInitialBarcode(self):
        if not os.path.isfile(self._barcode_filename):
            self.WriteInitialBarcode(1)
        with open(self._barcode_filename) as barcode_file:
            return int(barcode_file.read().strip())


    def _GenerateEpl(self, loje_product_sheet):
        stream = StringIO()
        header = self._label_header + "\n"
        stream.write(header)
        for row in loje_product_sheet:
            count = int(row.get(self.QUANTITY_HEADER, 1))
            for _ in range(count):
                label = self._GeneratLabelEpl(row) + "\n"
                stream.write(label)
        return stream.getvalue()
            
            
    def _SendToPrinter(self, epl_code):
        from zebra import zebra
        host_addr = r"\\\\{0}\\".format(socket.gethostname().lower())
        local_name = re.sub(self._printer_name, "", host_addr)
        zebra = zebra(local_name)
        zebra.output(epl_code)


    def _GeneratLabelEpl(self, row):
        template = Template(self._label_template)
        return template.substitute(**row)


class ProductCodeError(Exception):
    
    def __init__(self, ident):
        Exception.__init__(
            self,
            "Nao foi possivel encontrar correspondencia para codigo '%s'" % ident
        )