from sistema.database.conexao import conectar
from sistema.dao.ficha_tecnica_dao import FichaTecnicaDAO
from sistema.dao.ficha_tecnica_insumo_dao import FichaTecnicaInsumoDAO
from sistema.dao.insumo_dao import InsumoDAO
from sistema.models.ficha_tecnica import FichaTecnica
from sistema.models.ficha_tecnica_insumo import FichaTecnicaInsumo
from sistema.utils.helpers import Helpers

class FichaTecnicaService:

    @staticmethod
    def listar_todas():
        return FichaTecnicaDAO.listar_todas()

    @staticmethod
    def buscar_insumos_opcoes():
        """Retorna lista para combobox: 'ID - Nome'"""
        insumos = InsumoDAO.listar_todos()
        return [f"{i.id} - {i.nome}" for i in insumos]

    @staticmethod
    def buscar_ficha_completa(id_ficha):
        """Retorna (objeto_ficha, lista_itens_formatada)"""
        ficha = FichaTecnicaDAO.buscar_por_id(id_ficha)
        itens = FichaTecnicaInsumoDAO.listar_por_ficha(id_ficha)
        
        itens_formatados = []
        for item in itens:
            insumo = InsumoDAO.buscar_por_id(item.id_insumo)
            itens_formatados.append({
                "id_insumo": item.id_insumo,
                "nome": insumo.nome if insumo else "Desconhecido",
                "qtd": float(item.quantidade),
                # Unidade ajuda na visualização
                "unidade": insumo.unidade_medida if insumo else "" 
            })
            
        return ficha, itens_formatados

    @staticmethod
    def salvar_ficha_completa(dados_ficha, lista_ingredientes, id_editar=None):
        """
        Salva ou Atualiza uma ficha técnica e seus ingredientes numa transação.
        dados_ficha: {'nome': str, 'valor': float}
        lista_ingredientes: [{'id_insumo': int, 'qtd': float}, ...]
        """
        conn = conectar()
        cur = conn.cursor()
        
        try:
            # 1. Salvar/Atualizar Cabeçalho (Produto)
            if id_editar:
                ficha = FichaTecnica(id=id_editar, nome=dados_ficha['nome'], valor=dados_ficha['valor'])
                FichaTecnicaDAO.atualizar(ficha, cursor_externo=cur)
                id_final = id_editar
                
                # Na edição, limpamos os ingredientes antigos para inserir os novos
                FichaTecnicaInsumoDAO.deletar_por_ficha(id_editar, cursor_externo=cur)
            else:
                ficha = FichaTecnica(nome=dados_ficha['nome'], valor=dados_ficha['valor'])
                FichaTecnicaDAO.inserir(ficha, cursor_externo=cur)
                id_final = ficha.id

            # 2. Inserir Ingredientes
            for item in lista_ingredientes:
                novo_ingrediente = FichaTecnicaInsumo(
                    id_ficha_tecnica=id_final,
                    id_insumo=item['id_insumo'],
                    quantidade=item['qtd']
                )
                FichaTecnicaInsumoDAO.inserir(novo_ingrediente, cursor_externo=cur)

            conn.commit()
            return True, "Ficha técnica salva com sucesso!"

        except Exception as e:
            conn.rollback()
            return False, f"Erro ao salvar: {e}"
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def excluir_ficha(id_ficha):
        # O banco geralmente tem ON DELETE RESTRICT ou CASCADE.
        # Se for CASCADE, deletar a ficha apaga os ingredientes.
        # Se for RESTRICT, teríamos que apagar os ingredientes antes.
        # Assumindo CASCADE configurado no banco ou deletando manual por segurança:
        conn = conectar()
        cur = conn.cursor()
        try:
            FichaTecnicaInsumoDAO.deletar_por_ficha(id_ficha, cursor_externo=cur)
            FichaTecnicaDAO.deletar(id_ficha, cursor_externo=cur)
            conn.commit()
            return True, "Ficha excluída com sucesso!"
        except Exception as e:
            conn.rollback()
            return False, f"Erro ao excluir: {e}"
        finally:
            cur.close()
            conn.close()