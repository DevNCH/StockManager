
from sistema.database.conexao import conectar
from sistema.dao.pedido_dao import PedidoDAO
from sistema.dao.ficha_tecnica_pedido_dao import FichaTecnicaPedidoDAO
from sistema.dao.pedido_customizacao_dao import PedidoCustomizacaoDAO
from sistema.dao.ficha_tecnica_insumo_dao import FichaTecnicaInsumoDAO
from sistema.dao.ficha_tecnica_dao import FichaTecnicaDAO
from sistema.dao.insumo_dao import InsumoDAO
from sistema.models.pedido import Pedido
from sistema.models.ficha_tecnica_pedido import FichaTecnicaPedido
from sistema.models.pedido_customizacao import PedidoCustomizacao
from sistema.utils.helpers import Helpers

class PedidoService:

    @staticmethod
    def listar_todos():
        return PedidoDAO.listar_todos()

    @staticmethod
    def buscar_pedido_completo(id_pedido):
        """
        Recupera o pedido e reconstroi o 'carrinho' para a interface.
        Retorna: (objeto_pedido, lista_itens_view)
        """
        pedido = PedidoDAO.buscar_por_id(id_pedido)
        itens_db = FichaTecnicaPedidoDAO.listar_por_pedido(id_pedido)
        
        carrinho_recuperado = []
        
        for item in itens_db:
            # 1. Busca nome do produto
            ficha = FichaTecnicaDAO.buscar_por_id(item.id_ficha_tecnica)
            nome_produto = ficha.nome if ficha else "Produto Desconhecido"
            
            # 2. Busca customizações (IDs)
            ids_removidos = PedidoCustomizacaoDAO.listar_por_item(item.id)
            
            # 3. Busca nomes das customizações para exibir
            nomes_removidos = []
            for id_ins in ids_removidos:
                insumo = InsumoDAO.buscar_por_id(id_ins)
                if insumo:
                    nomes_removidos.append(insumo.nome)
            
            # Monta dicionário igual ao da View
            carrinho_recuperado.append({
                'id_ficha': item.id_ficha_tecnica,
                'nome': nome_produto,
                'qtd': float(item.quantidade),
                'valor_unit': float(item.valor_unitario),
                'removidos': ids_removidos,
                'nomes_removidos': nomes_removidos
            })
            
        return pedido, carrinho_recuperado

    @staticmethod
    def salvar_pedido_completo(dados_pedido, lista_itens, id_pedido_editar=None):
        conn = conectar()
        cur = conn.cursor()
        
        try:
            data_mysql = Helpers.data_para_mysql(dados_pedido['data'])
            
            # --- CENÁRIO 1: EDIÇÃO (ESTORNO) ---
            if id_pedido_editar:
                # 1. Buscar itens antigos para devolver ao estoque
                itens_antigos = FichaTecnicaPedidoDAO.listar_por_pedido(id_pedido_editar)
                
                for item_antigo in itens_antigos:
                    # Busca receita original
                    receita = FichaTecnicaInsumoDAO.listar_por_ficha(item_antigo.id_ficha_tecnica)
                    # Busca o que foi removido neste item (para não devolver o que não gastou)
                    ids_removidos_antigos = PedidoCustomizacaoDAO.listar_por_item(item_antigo.id)
                    
                    qtd_vendida = float(item_antigo.quantidade)
                    
                    for ingrediente in receita:
                        if ingrediente.id_insumo in ids_removidos_antigos:
                            continue # Não devolve o que não saiu
                        
                        qtd_devolver = float(ingrediente.quantidade) * qtd_vendida
                        # Atualiza estoque (Valor POSITIVO para devolver)
                        InsumoDAO.atualizar_quantidade_estoque(ingrediente.id_insumo, qtd_devolver, cursor_externo=cur)

                # 2. Deletar itens antigos (Cascade apaga customizações)
                # Como não temos um "deletar_todos_por_pedido" no DAO, deletamos um por um ou via SQL direto
                # Vamos via SQL direto no cursor para ser rápido e seguro na transação
                cur.execute("DELETE FROM ficha_tecnica_pedido WHERE id_pedido = %s", (id_pedido_editar,))
                
                # 3. Atualizar Cabeçalho
                pedido_edit = Pedido(
                    id=id_pedido_editar,
                    nome=dados_pedido['cliente'],
                    valor=dados_pedido['total'],
                    data=data_mysql,
                    telefone=dados_pedido.get('telefone', ''),
                    observacoes=dados_pedido.get('obs', ''),
                    cpf_cnpj=dados_pedido.get('cpf_cnpj', ''),
                    cep=dados_pedido.get('cep', ''),
                    unidade_federal=dados_pedido.get('uf', ''),
                    cidade=dados_pedido.get('cidade', ''),
                    bairro=dados_pedido.get('bairro', ''),
                    rua=dados_pedido.get('rua', ''),
                    numero=dados_pedido.get('numero', ''),
                    complemento=dados_pedido.get('complemento', '')
                )
                PedidoDAO.atualizar(pedido_edit) # O DAO atualizar normalmente não aceita cursor, mas ok pois o commit é no final
                id_pedido = id_pedido_editar

            # --- CENÁRIO 2: NOVO PEDIDO ---
            else:
                pedido = Pedido(
                    nome=dados_pedido['cliente'],
                    valor=dados_pedido['total'],
                    data=data_mysql,
                    telefone=dados_pedido.get('telefone', ''),
                    observacoes=dados_pedido.get('obs', ''),
                    cpf_cnpj=dados_pedido.get('cpf_cnpj', ''),
                    cep=dados_pedido.get('cep', ''),
                    unidade_federal=dados_pedido.get('uf', ''),
                    cidade=dados_pedido.get('cidade', ''),
                    bairro=dados_pedido.get('bairro', ''),
                    rua=dados_pedido.get('rua', ''),
                    numero=dados_pedido.get('numero', ''),
                    complemento=dados_pedido.get('complemento', '')
                )
                pedido_salvo = PedidoDAO.inserir(pedido, cursor_externo=cur)
                id_pedido = pedido_salvo.id

            # --- PASSO COMUM: INSERIR ITENS NOVOS E BAIXAR ESTOQUE ---
            for item in lista_itens:
                novo_item_pedido = FichaTecnicaPedido(
                    id_ficha_tecnica=item['id_ficha'],
                    id_pedido=id_pedido,
                    quantidade=item['qtd'],
                    valor_unitario=item['valor_unit']
                )
                item_salvo = FichaTecnicaPedidoDAO.inserir(novo_item_pedido, cursor_externo=cur)
                id_item_gerado = item_salvo.id

                lista_removidos = item.get('removidos', [])
                for id_insumo_removido in lista_removidos:
                    customizacao = PedidoCustomizacao(id_item_pedido=id_item_gerado, id_insumo_removido=id_insumo_removido)
                    PedidoCustomizacaoDAO.salvar(customizacao, cursor_externo=cur)

                # Baixa de Estoque
                receita_padrao = FichaTecnicaInsumoDAO.listar_por_ficha(item['id_ficha'])
                qtd_vendida_produto = float(item['qtd'])

                for ingrediente in receita_padrao:
                    if ingrediente.id_insumo in lista_removidos:
                        continue
                    
                    qtd_a_baixar = float(ingrediente.quantidade) * qtd_vendida_produto
                    InsumoDAO.atualizar_quantidade_estoque(ingrediente.id_insumo, -qtd_a_baixar, cursor_externo=cur)

            conn.commit()
            return True, "Pedido salvo com sucesso!"

        except Exception as e:
            conn.rollback()
            return False, f"Erro ao processar pedido: {e}"
        finally:
            cur.close()
            conn.close()


    @staticmethod
    def excluir_pedido(id_pedido):
        conn = conectar()
        cur = conn.cursor()
        
        try:
            # 1. Buscar itens do pedido para DEVOLVER ao estoque
            itens_pedido = FichaTecnicaPedidoDAO.listar_por_pedido(id_pedido)
            
            for item in itens_pedido:
                # Busca a receita original do produto
                receita = FichaTecnicaInsumoDAO.listar_por_ficha(item.id_ficha_tecnica)
                
                # Busca o que o cliente PEDIU PRA TIRAR (Ex: Sem Cebola)
                ids_removidos = PedidoCustomizacaoDAO.listar_por_item(item.id)
                
                qtd_vendida = float(item.quantidade)
                
                for ingrediente in receita:
                    # Se o ingrediente foi removido no pedido, ele nunca saiu do estoque.
                    # Então, não precisamos devolver.
                    if ingrediente.id_insumo in ids_removidos:
                        continue 
                    
                    # Cálculo: Qtd da Receita * Qtd de Pasteis Vendidos
                    qtd_devolver = float(ingrediente.quantidade) * qtd_vendida
                    
                    # Devolve ao estoque (Valor POSITIVO soma)
                    InsumoDAO.atualizar_quantidade_estoque(
                        ingrediente.id_insumo, 
                        qtd_devolver, 
                        cursor_externo=cur
                    )

            # 2. Deleta o Pedido
            # O 'ON DELETE CASCADE' do banco vai apagar os itens e customizações automaticamente.
            PedidoDAO.deletar(id_pedido, cursor_externo=cur)
            
            conn.commit()
            return True, "Pedido excluído e estoque estornado com sucesso!"
            
        except Exception as e:
            conn.rollback()
            return False, f"Erro ao excluir: {e}"
        finally:
            cur.close()
            conn.close()