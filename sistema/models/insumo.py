class Insumo:
    def __init__(self, id=None, nome=None, quantidade=None, unidade_medida=None):
        self.id = id
        self.nome = nome
        self.quantidade = float(quantidade) if quantidade is not None else 0.0
        self.unidade_medida = unidade_medida

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "unidade_medida": self.unidade_medida
        }
