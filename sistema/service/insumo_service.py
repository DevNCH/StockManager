# sistema/service/insumo_service.py
from sistema.dao.insumo_dao import InsumoDAO
from sistema.dao.registro_compra_dao import RegistroCompraDAO
from sistema.models.registro_compra import RegistroCompra
from sistema.models.insumo import Insumo

class InsumoService:

    # --- CRUD Básico (Que faltava) ---
    @staticmethod
    def listar_estoque():
        return InsumoDAO.listar_todos()

    @staticmethod
    def pesquisar_insumos(texto):
        if not texto or texto == "Pesquisar...":
            return InsumoDAO.listar_todos()
        else:
            return InsumoDAO.buscar_por_texto(texto)

    @staticmethod
    def criar_insumo(nome, quantidade, unidade_medida):
        # A Service que deve criar o objeto Model, não a Controller
        novo = Insumo(nome=nome, quantidade=quantidade, unidade_medida=unidade_medida)
        InsumoDAO.inserir(novo)

    @staticmethod
    def atualizar_insumo(id_insumo, nome, quantidade, unidade_medida):
        insumo_editado = Insumo(id=id_insumo, nome=nome, quantidade=quantidade, unidade_medida=unidade_medida)
        InsumoDAO.atualizar(insumo_editado)

    @staticmethod
    def excluir_insumo(id_insumo):
        InsumoDAO.deletar(id_insumo)

    # --- Regras de Negócio Existentes (Mantidas) ---
    @staticmethod
    def registrar_compra(id_insumo, quantidade, valor, id_nota_fiscal):
        insumo = InsumoDAO.buscar_por_id(id_insumo)
        if not insumo:
            raise ValueError("Insumo não encontrado.")

        insumo.quantidade = float(insumo.quantidade) + float(quantidade)
        InsumoDAO.atualizar(insumo)

        compra = RegistroCompra(
            id_insumo=id_insumo,
            id_nota_fiscal=id_nota_fiscal,
            quantidade=quantidade,
            valor=valor
        )
        return RegistroCompraDAO.inserir(compra)

    @staticmethod
    def reduzir_estoque(id_insumo, quantidade):
        insumo = InsumoDAO.buscar_por_id(id_insumo)
        if not insumo:
            raise ValueError("Insumo não encontrado.")

        if float(insumo.quantidade) < float(quantidade):
            raise ValueError("Estoque insuficiente.")

        insumo.quantidade = float(insumo.quantidade) - float(quantidade)
        InsumoDAO.atualizar(insumo)
        return insumo

    @staticmethod
    def ajuste_manual(id_insumo, nome=None, quantidade=None, unidade_medida=None):
        insumo = InsumoDAO.buscar_por_id(id_insumo)
        if not insumo:
            raise ValueError("Insumo não encontrado.")

        if nome is not None: insumo.nome = nome
        if quantidade is not None: insumo.quantidade = float(quantidade)
        if unidade_medida is not None: insumo.unidade_medida = unidade_medida

        InsumoDAO.atualizar(insumo)
        return insumo