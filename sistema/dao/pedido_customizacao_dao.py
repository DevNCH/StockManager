from sistema.database.conexao import conectar
from sistema.models.pedido_customizacao import PedidoCustomizacao

class PedidoCustomizacaoDAO:

    @staticmethod
    def salvar(customizacao: PedidoCustomizacao, cursor_externo=None):
        """
        Salva a customização. Aceita um cursor_externo para manter
        a transação (commit único) junto com o Pedido.
        """
        # Se recebeu uma conexão externa (do Service), usa ela. Se não, abre uma nova.
        if cursor_externo:
            cur = cursor_externo
            fechar_conexao = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar_conexao = True

        sql = """
            INSERT INTO pedidos_customizacao (id_item_pedido, id_insumo_removido)
            VALUES (%s, %s)
        """
        cur.execute(sql, (customizacao.id_item_pedido, customizacao.id_insumo_removido))

        # Se abrimos a conexão aqui, precisamos fechar.
        if fechar_conexao:
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def listar_por_item(id_item_pedido):
        """
        Retorna uma LISTA DE IDs dos insumos que foram removidos neste item.
        Ex: [1, 5] (significa que removeu o insumo 1 e o 5)
        """
        conn = conectar()
        cur = conn.cursor() # mysql-connector padrão retorna tuplas
        
        sql = "SELECT id_insumo_removido FROM pedidos_customizacao WHERE id_item_pedido = %s"
        cur.execute(sql, (id_item_pedido,))
        resultado = cur.fetchall()
        
        cur.close()
        conn.close()

        # Transforma de [(1,), (5,)] para [1, 5] para facilitar a conta
        return [linha[0] for linha in resultado]
