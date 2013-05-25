#-*- coding: latin1
import csv
from UserDict import DictMixin
import locale

locale.setlocale(locale.LC_ALL, "")


def processReceivable(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        sheet = []
        for line in csv_reader:
            row = LojeReceivableRow()
            nonblanks = [record for record in line if record]
            if len(nonblanks) < 5:
                continue
            try:
                locale.atof(nonblanks[4])
            except ValueError:
                continue
            row["cliente"] = nonblanks[0]
            row["conta"] = nonblanks[1]
            row["centro de custos"] = nonblanks[2]
            row["vencimento"] = nonblanks[3]
            row["valor"] = nonblanks[4]
            sheet.append(row)
    return sheet
            
            
def writeLojeSheet(sheet):
    with open("rcv.csv", 'w') as out_file:           
        writer = csv.DictWriter(
            out_file,
            sheet[0].FIELDS,
            delimiter=";",
            lineterminator="\n",
            quoting=csv.QUOTE_ALL 
            )
        writer.writeheader()
        writer.writerows(sheet)    


def testReceivable():
    sheet = processReceivable("receivable.csv")
    writeLojeSheet(sheet)


class LojeReceivableRow(DictMixin):
    
    FIELDS = [
        "cliente",
        "cpf",
        "cnpj",
        "historico",
        "emissao",
        "numerodoc",
        "portador",
        "vencimento",
        "valor",
        "juros",
        "tipo juros",
        "frequencia",
        "numero vezes",
        "observacao",
        "fim frequencia",
        "formapgto",
        "boleto",
        "competencia",
        "seriedoc",
        "multa",
        "conta",
        "plano de contas",
        "centro de custos",
        ]
    
    def __init__(self):
        self._data = {}
    
    
    def __setitem__(self, key, value):
        if key not in self.FIELDS:
            raise KeyError("Invalid Field name")
        self._data[key] = value
        
        
    def __getitem__(self, key):
        if key not in self.FIELDS:
            raise KeyError("Invalid Field name")
        try:
            return self._data[key]
        except KeyError:
            return ""
        
    
    def keys(self):
        return self.FIELDS[:]
        


if __name__ == '__main__':
    testReceivable()