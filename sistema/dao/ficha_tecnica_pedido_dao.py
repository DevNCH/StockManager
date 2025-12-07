from sistema.database.conexao import conectar
from sistema.models.ficha_tecnica_pedido import FichaTecnicaPedido

class FichaTecnicaPedidoDAO:

    @staticmethod
    def listar_por_pedido(id_pedido):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM ficha_tecnica_pedido WHERE id_pedido=%s", (id_pedido,))
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return [FichaTecnicaPedido(**d) for d in dados]

    @staticmethod
    def inserir(ftp: FichaTecnicaPedido, cursor_externo=None):
        """
        Agora aceita cursor_externo para participar da transação do Pedido.
        Também salva QUANTIDADE e VALOR_UNITARIO.
        """
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        sql = """
            INSERT INTO ficha_tecnica_pedido (id_ficha_tecnica, id_pedido, quantidade, valor_unitario)
            VALUES (%s, %s, %s, %s)
        """
        # AQUI: Adicionamos ftp.quantidade e ftp.valor_unitario
        cur.execute(sql, (ftp.id_ficha_tecnica, ftp.id_pedido, ftp.quantidade, ftp.valor_unitario))
        
        # Recupera o ID gerado para usar na tabela de customização depois
        ftp.id = cur.lastrowid

        if fechar:
            conn.commit()
            cur.close()
            conn.close()
        
        return ftp

    @staticmethod
    def atualizar(ftp: FichaTecnicaPedido):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            UPDATE ficha_tecnica_pedido
            SET id_ficha_tecnica=%s, id_pedido=%s, quantidade=%s, valor_unitario=%s
            WHERE id=%s
        """
        cur.execute(sql, (ftp.id_ficha_tecnica, ftp.id_pedido, ftp.quantidade, ftp.valor_unitario, ftp.id))
        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def deletar(id_ftp):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM ficha_tecnica_pedido WHERE id=%s", (id_ftp,))
        conn.commit()
        cur.close()
        conn.close()