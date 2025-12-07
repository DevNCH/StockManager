class FichaTecnicaInsumo:
    def __init__(self, id=None, id_ficha_tecnica=None, id_insumo=None, quantidade=0.0):
        self.id = id
        self.id_ficha_tecnica = id_ficha_tecnica
        self.id_insumo = id_insumo
        self.quantidade = float(quantidade)

    def to_dict(self):
        return {
            "id": self.id,
            "id_ficha_tecnica": self.id_ficha_tecnica,
            "id_insumo": self.id_insumo,
            "quantidade": self.quantidade
        }