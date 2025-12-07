# sistema/service/ficha_tecnica_service.py
from sistema.dao.ficha_tecnica_dao import FichaTecnicaDAO
from sistema.dao.ficha_tecnica_insumo_dao import FichaTecnicaInsumoDAO
from sistema.models.ficha_tecnica import FichaTecnica
from sistema.models.ficha_tecnica_insumo import FichaTecnicaInsumo

class FichaTecnicaService:

    @staticmethod
    def criar_ficha(nome, valor=0.0):
        ft = FichaTecnica(nome=nome, valor=valor)
        return FichaTecnicaDAO.inserir(ft)

    @staticmethod
    def atualizar_ficha_completa(id_ficha, novo_nome, nova_lista_insumos):
        """
        nova_lista_insumos = [
            {"id_insumo": 1, "quantidade": 0.5},
            {"id_insumo": 3, "quantidade": 2.0}
        ]
        """

        # 1) atualizar nome/valor da ficha
        ficha = FichaTecnica(id=id_ficha, nome=novo_nome)
        FichaTecnicaDAO.atualizar(ficha)

        # 2) buscar itens antigos
        antigos = FichaTecnicaInsumoDAO.listar_por_ficha(id_ficha)
        antigos_dict = {a.id_insumo: a for a in antigos}

        novos_ids = {i["id_insumo"] for i in nova_lista_insumos}
        antigos_ids = set(antigos_dict.keys())

        # inserir novos
        for item in nova_lista_insumos:
            if item["id_insumo"] not in antigos_ids:
                novo = FichaTecnicaInsumo(
                    id_ficha_tecnica=id_ficha,
                    id_insumo=item["id_insumo"],
                    quantidade=item["quantidade"]
                )
                FichaTecnicaInsumoDAO.inserir(novo)

        # atualizar existentes
        for item in nova_lista_insumos:
            if item["id_insumo"] in antigos_ids:
                antigo = antigos_dict[item["id_insumo"]]
                antigo.quantidade = item["quantidade"]
                FichaTecnicaInsumoDAO.atualizar(antigo)

        # deletar removidos
        ids_removidos = antigos_ids - novos_ids
        for id_insumo in ids_removidos:
            item = antigos_dict[id_insumo]
            FichaTecnicaInsumoDAO.deletar(item.id)

        return True

    @staticmethod
    def listar_fichas():
        return FichaTecnicaDAO.listar_todas()
