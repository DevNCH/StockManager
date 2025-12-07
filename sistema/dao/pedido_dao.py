from sistema.database.conexao import conectar
from sistema.models.pedido import Pedido

class PedidoDAO:

    @staticmethod
    def listar_todos():
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM pedidos")
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return [Pedido(**d) for d in dados]

    @staticmethod
    def buscar_por_id(id_ped):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM pedidos WHERE id=%s", (id_ped,))
        dado = cur.fetchone()
        cur.close()
        conn.close()
        return Pedido(**dado) if dado else None

    @staticmethod
    def inserir(pedido: Pedido, cursor_externo=None): # Adicione cursor_externo aqui
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        sql = """
            INSERT INTO pedidos (nome, data, telefone, valor, observacoes,
                cpf_cnpj, cep, unidade_federal, cidade, bairro, rua, numero, complemento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            pedido.nome, pedido.data, pedido.telefone, pedido.valor,
            pedido.observacoes, pedido.cpf_cnpj, pedido.cep,
            pedido.unidade_federal, pedido.cidade, pedido.bairro,
            pedido.rua, pedido.numero, pedido.complemento
        )

        cur.execute(sql, valores)
        
        # Não damos commit se estivermos numa transação externa!
        if fechar:
            conn.commit()
        
        pedido.id = cur.lastrowid

        if fechar:
            cur.close()
            conn.close()
            
        return pedido

    @staticmethod
    def atualizar(pedido: Pedido):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            UPDATE pedidos
            SET nome=%s, data=%s, telefone=%s, valor=%s, observacoes=%s,
                cpf_cnpj=%s, cep=%s, unidade_federal=%s, cidade=%s,
                bairro=%s, rua=%s, numero=%s, complemento=%s
            WHERE id=%s
        """

        valores = (
            pedido.nome, pedido.data, pedido.telefone, pedido.valor,
            pedido.observacoes, pedido.cpf_cnpj, pedido.cep,
            pedido.unidade_federal, pedido.cidade, pedido.bairro,
            pedido.rua, pedido.numero, pedido.complemento,
            pedido.id
        )

        cur.execute(sql, valores)
        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def deletar(id_ped):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM pedidos WHERE id=%s", (id_ped,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def buscar_por_periodo(data_inicio, data_fim):
        sql = """
            SELECT *
            FROM pedidos
            WHERE data BETWEEN %s AND %s
            ORDER BY data ASC
        """
        try:
            conn = conectar()
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (data_inicio, data_fim))
            dados = cur.fetchall()
            return [Pedido(**d) for d in dados]
        finally:
            cur.close()
            conn.close()
