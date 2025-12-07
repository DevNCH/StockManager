from sistema.database.conexao import conectar
from sistema.models.registro_compra import RegistroCompra

class RegistroCompraDAO:

    @staticmethod
    def listar_todos():
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM registro_compras")
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return [RegistroCompra(**d) for d in dados]

    @staticmethod
    def buscar_por_id(id_reg):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM registro_compras WHERE id=%s", (id_reg,))
        dado = cur.fetchone()
        cur.close()
        conn.close()
        return RegistroCompra(**dado) if dado else None

    @staticmethod
    def atualizar(reg: RegistroCompra):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            UPDATE registro_compras
            SET id_insumo=%s, id_nota_fiscal=%s, quantidade=%s, valor=%s
            WHERE id=%s
        """

        valores = (
            reg.id_insumo, reg.id_nota_fiscal,
            reg.quantidade, reg.valor, reg.id
        )

        cur.execute(sql, valores)
        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def deletar(id_reg):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM registro_compras WHERE id=%s", (id_reg,))
        conn.commit()
        cur.close()
        conn.close()


    @staticmethod
    def listar_por_insumo(id_insumo):
        sql = "SELECT * FROM registro_compras WHERE id_insumo=%s"
        try:
            conn = conectar()
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (id_insumo,))
            dados = cur.fetchall()
            return [RegistroCompra(**d) for d in dados]
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def listar_por_nota(id_nota):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM registro_compras WHERE id_nota_fiscal=%s", (id_nota,))
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return [RegistroCompra(**d) for d in dados]

    @staticmethod
    def inserir(reg: RegistroCompra, cursor_externo=None):
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        sql = """
            INSERT INTO registro_compras (id_insumo, id_nota_fiscal, quantidade, valor)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (reg.id_insumo, reg.id_nota_fiscal, reg.quantidade, reg.valor))
        reg.id = cur.lastrowid

        if fechar:
            conn.commit()
            cur.close()
            conn.close()
        return reg

    @staticmethod
    def deletar_por_nota(id_nota, cursor_externo=None):
        # Novo método útil para limpar itens na edição
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True
            
        cur.execute("DELETE FROM registro_compras WHERE id_nota_fiscal=%s", (id_nota,))
        
        if fechar:
            conn.commit()
            cur.close()
            conn.close()