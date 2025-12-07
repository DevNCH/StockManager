class PedidoCustomizacao:
    def __init__(self, id_item_pedido, id_insumo_removido, id=None):
        self.id = id
        self.id_item_pedido = id_item_pedido
        self.id_insumo_removido = id_insumo_removido
    
    def to_dict(self):
        return {
            "id": self.id,
            "id_item_pedido": self.id_item_pedido,
            "id_insumo_pedido": self.id_insumo_removido
        }