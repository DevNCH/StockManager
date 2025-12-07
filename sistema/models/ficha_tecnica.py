class FichaTecnica:
    def __init__(self, id=None, nome=None, valor=0.0):
        self.id = id
        self.nome = nome
        self.valor = float(valor)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "valor": self.valor  
        }