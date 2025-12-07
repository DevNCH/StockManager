from sistema.database.conexao import conectar
from sistema.dao.pedido_dao import PedidoDAO
from sistema.dao.ficha_tecnica_pedido_dao import FichaTecnicaPedidoDAO
from sistema.dao.pedido_customizacao_dao import PedidoCustomizacaoDAO
from sistema.dao.ficha_tecnica_insumo_dao import FichaTecnicaInsumoDAO
from sistema.models.ficha_tecnica_pedido import FichaTecnicaPedido
from sistema.models.pedido_customizacao import PedidoCustomizacao

class PedidoService:
    def __init__(self):
        self.pedido_dao = PedidoDAO()
        self.item_dao = FichaTecnicaPedidoDAO()
        self.custom_dao = PedidoCustomizacaoDAO()
        self.ft_insumo_dao = FichaTecnicaInsumoDAO()

    def registrar_pedido_completo(self, pedido, lista_itens):
        """
        Registra o pedido, itens, customizações e baixa estoque em UMA transação.
        lista_itens deve vir da tela assim:
        [
            {
               'id_ficha_tecnica': 1,
               'quantidade': 2.0,
               'valor_unitario': 23.00,
               'insumos_removidos': [5, 12]  <-- IDs dos insumos que o cliente tirou
            },
            ...
        ]
        """
        conn = conectar()
        cur = conn.cursor()
        
        try:
            # 1. Salva o Pedido Principal (usando cursor externo para não fechar conexão)
            pedido_salvo = self.pedido_dao.inserir(pedido, cursor_externo=cur)
            id_pedido = pedido_salvo.id

            # 2. Itera sobre os itens do pedido
            for item_dict in lista_itens:
                # Cria objeto e salva na tabela intermediária
                novo_item = FichaTecnicaPedido(
                    id_ficha_tecnica=item_dict['id_ficha_tecnica'],
                    id_pedido=id_pedido,
                    quantidade=item_dict['quantidade'],
                    valor_unitario=item_dict['valor_unitario']
                )
                item_salvo = self.item_dao.inserir(novo_item, cursor_externo=cur)
                
                # 3. Salva Customizações (Ingredientes retirados)
                lista_removidos = item_dict.get('insumos_removidos', [])
                for id_insumo_removido in lista_removidos:
                    custom_model = PedidoCustomizacao(item_salvo.id, id_insumo_removido)
                    self.custom_dao.salvar(custom_model, cursor_externo=cur)

                # 4. Baixa de Estoque Inteligente (considera qtd vendida e exclusões)
                self._baixar_estoque(
                    item_dict['id_ficha_tecnica'], 
                    item_dict['quantidade'], 
                    lista_removidos, 
                    cur
                )

            conn.commit() # Salva tudo de uma vez
            return True, "Pedido registrado com sucesso!"

        except Exception as e:
            conn.rollback() # Cancela tudo se der erro
            print(f"Erro Transaction: {e}")
            return False, f"Erro: {str(e)}"
        finally:
            cur.close()
            conn.close()

    def _baixar_estoque(self, id_ficha_tecnica, qtd_vendida, ids_removidos, cur):
        # Busca a receita padrão
        receita = self.ft_insumo_dao.listar_por_ficha(id_ficha_tecnica)

        for item_receita in receita:
            # Se o cliente pediu "sem cebola" (id da cebola na lista), não baixa estoque
            if item_receita.id_insumo in ids_removidos:
                continue
            
            # Cálculo: (Qtd na Receita * Qtd de Pasteis Vendidos)
            qtd_total_baixar = float(item_receita.quantidade) * float(qtd_vendida)
            
            # Update direto no banco para ser rápido e seguro dentro da transação
            sql_baixa = "UPDATE insumos SET quantidade = quantidade - %s WHERE id = %s"
            cur.execute(sql_baixa, (qtd_total_baixar, item_receita.id_insumo))