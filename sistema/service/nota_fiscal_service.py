from sistema.database.conexao import conectar
from sistema.dao.nota_fiscal_dao import NotaFiscalDAO
from sistema.dao.registro_compra_dao import RegistroCompraDAO
from sistema.dao.insumo_dao import InsumoDAO # <--- Usaremos o DAO agora
from sistema.models.nota_fiscal import NotaFiscal
from sistema.models.registro_compra import RegistroCompra
from sistema.utils.helpers import Helpers

class NotaFiscalService:

    @staticmethod
    def listar_todas():
        return NotaFiscalDAO.listar_todas()

    @staticmethod
    def buscar_insumos_opcoes():
        insumos = InsumoDAO.listar_todos()
        return [f"{i.id} - {i.nome}" for i in insumos]

    @staticmethod
    def buscar_detalhes_completo(id_nota):
        # ... (Mantém igual, pois é só leitura) ...
        nota = NotaFiscalDAO.buscar_por_id(id_nota)
        registros = RegistroCompraDAO.listar_por_nota(id_nota)
        
        itens_formatados = []
        for reg in registros:
            insumo = InsumoDAO.buscar_por_id(reg.id_insumo)
            itens_formatados.append({
                "id_insumo": reg.id_insumo,
                "nome": insumo.nome if insumo else "Desconhecido",
                "qtd": float(reg.quantidade),
                "valor": float(reg.valor)
            })
        return nota, itens_formatados

    @staticmethod
    def salvar_nota_transacionada(cabecalho_dict, lista_itens, id_nota_editar=None):
        """
        Orquestra a transação usando APENAS DAOs. Zero SQL aqui.
        """
        valor_total = sum([item['valor'] for item in lista_itens])
        data_mysql = Helpers.data_para_mysql(cabecalho_dict['data'])
        
        conn = conectar()
        cur = conn.cursor()
        
        try:
            # --- CENÁRIO 1: EDIÇÃO ---
            if id_nota_editar:
                # 1. Estornar Estoque Antigo
                itens_antigos = RegistroCompraDAO.listar_por_nota(id_nota_editar)
                for antigo in itens_antigos:
                    # Passamos negativo para subtrair/reverter
                    InsumoDAO.atualizar_quantidade_estoque(antigo.id_insumo, -antigo.quantidade, cursor_externo=cur)
                
                # 2. Limpar registros antigos
                RegistroCompraDAO.deletar_por_nota(id_nota_editar, cursor_externo=cur)
                
                # 3. Atualizar Nota
                nota_editada = NotaFiscal(
                    id=id_nota_editar,
                    nfce=cabecalho_dict['nfce'], serie=cabecalho_dict['serie'],
                    data_emissao=data_mysql, cnpj_fornecedor=cabecalho_dict['cnpj'],
                    nome_fornecedor=cabecalho_dict['fornecedor'], valor=valor_total
                )
                NotaFiscalDAO.atualizar(nota_editada, cursor_externo=cur)
                id_nota_final = id_nota_editar
            
            # --- CENÁRIO 2: CRIAÇÃO ---
            else:
                nova_nota = NotaFiscal(
                    nfce=cabecalho_dict['nfce'], serie=cabecalho_dict['serie'],
                    data_emissao=data_mysql, cnpj_fornecedor=cabecalho_dict['cnpj'],
                    nome_fornecedor=cabecalho_dict['fornecedor'], valor=valor_total
                )
                NotaFiscalDAO.inserir(nova_nota, cursor_externo=cur)
                id_nota_final = nova_nota.id

            # --- PASSO COMUM: NOVOS ITENS E ESTOQUE ---
            for item in lista_itens:
                # 1. Inserir Registro de Compra via DAO
                novo_reg = RegistroCompra(
                    id_insumo=item['id_insumo'],
                    id_nota_fiscal=id_nota_final,
                    quantidade=item['qtd'],
                    valor=item['valor']
                )
                RegistroCompraDAO.inserir(novo_reg, cursor_externo=cur)
                
                # 2. Atualizar Estoque via DAO
                InsumoDAO.atualizar_quantidade_estoque(item['id_insumo'], item['qtd'], cursor_externo=cur)
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def excluir_nota_transacionada(id_nota):
        conn = conectar()
        cur = conn.cursor()
        try:
            # 1. Busca itens para estornar (Leitura não precisa de cursor transacionado)
            itens_da_nota = RegistroCompraDAO.listar_por_nota(id_nota)

            # 2. Estorna Estoque via DAO
            for reg in itens_da_nota:
                InsumoDAO.atualizar_quantidade_estoque(reg.id_insumo, -reg.quantidade, cursor_externo=cur)

            # 3. Deleta Nota via DAO
            NotaFiscalDAO.deletar(id_nota, cursor_externo=cur)
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()