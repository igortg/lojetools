#-*- coding: latin1
import xlrd


def LoadLojeProductSheet(xls_file):
    products = ProductTable()
    book  = xlrd.open_workbook(r"..\Produtos.xls")
    sheet = book.sheet_by_index(0)
    headers = [cell.value for cell in sheet.row(0)]
    cod_col = headers.index(u"Cód. Barra")
    ident_col = headers.index(u"Identificação")
    category_col = headers.index(u"Categoria")
    description_col = headers.index(u"Descrição")

    for row in range(1,sheet.nrows):
        cod = sheet.cell_value(row, cod_col)
        ident = sheet.cell_value(row, ident_col)
        category = sheet.cell_value(row, category_col) 
        description = sheet.cell_value(row, description_col) 
        products.AppendProduct(cod, ident, category, description)
        print cod, ident


#===================================================================================================
# ProductTable
#===================================================================================================
class ProductTable(object):
    
    
    def __init__(self):
        self._product_data = {}
        
    
    def AppendProduct(self, code, ident, category, description):
        self._product_data[code] = (ident, category, description)
        
        
    def GetProduct(self, code):
        return self._product_data[code]



LoadLojeProductSheet(r"..\Produtos.xls")
