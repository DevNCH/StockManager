class FichaTecnicaPedido:
    def __init__(self, id=None, id_ficha_tecnica=None, id_pedido=None, quantidade=1.0, valor_unitario=0.0):
        self.id = id
        self.id_ficha_tecnica = id_ficha_tecnica
        self.id_pedido = id_pedido
        self.quantidade = float(quantidade)
        self.valor_unitario = float(valor_unitario)

    def to_dict(self):
        return {
            "id": self.id,
            "id_ficha_tecnica": self.id_ficha_tecnica,
            "id_pedido": self.id_pedido,
            "quantidade": self.quantidade,
            "valor_unitario": self.valor_unitario
        }