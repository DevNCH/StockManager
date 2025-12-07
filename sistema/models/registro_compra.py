class RegistroCompra:
    def __init__(self, id=None, id_insumo=None, id_nota_fiscal=None,
                 quantidade=0.0, valor=0.0):
        self.id = id
        self.id_insumo = id_insumo
        self.id_nota_fiscal = id_nota_fiscal
        self.quantidade = float(quantidade)
        self.valor = float(valor)

    def to_dict(self):
        return {
            "id": self.id,
            "id_insumo": self.id_insumo,
            "id_nota_fiscal": self.id_nota_fiscal,
            "quantidade": self.quantidade,
            "valor": self.valor
        }