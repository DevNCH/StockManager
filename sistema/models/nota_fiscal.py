class NotaFiscal:
    def __init__(self, id=None, nfce=None, serie=None, data_emissao=None,
                 cnpj_fornecedor=None, nome_fornecedor=None, valor=0.0):
        self.id = id
        self.nfce = nfce
        self.serie = serie
        self.data_emissao = data_emissao
        self.cnpj_fornecedor = cnpj_fornecedor
        self.nome_fornecedor = nome_fornecedor
        self.valor = float(valor)

    def to_dict(self):
        return {
            "id": self.id,
            "nfce": self.nfce,
            "serie": self.serie,
            "data_emissao": self.data_emissao,
            "cnpj_fornecedor": self.cnpj_fornecedor,
            "nome_fornecedor": self.cnpj_fornecedor,
            "valor": self.valor
        }