from sistema.database.conexao import conectar
from sistema.models.ficha_tecnica import FichaTecnica

class FichaTecnicaDAO:

    @staticmethod
    def listar_todas():
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM fichas_tecnicas")
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return [FichaTecnica(**d) for d in dados]

    @staticmethod
    def buscar_por_id(id_ft):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM fichas_tecnicas WHERE id=%s", (id_ft,))
        dado = cur.fetchone()
        cur.close()
        conn.close()
        return FichaTecnica(**dado) if dado else None

    @staticmethod
    def inserir(ft: FichaTecnica):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            INSERT INTO fichas_tecnicas (nome, valor)
            VALUES (%s, %s)
        """

        cur.execute(sql, (ft.nome, ft.valor))
        conn.commit()

        ft.id = cur.lastrowid
        cur.close()
        conn.close()
        return ft

    @staticmethod
    def atualizar(ft: FichaTecnica):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            UPDATE fichas_tecnicas
            SET nome=%s, valor=%s
            WHERE id=%s
        """

        cur.execute(sql, (ft.nome, ft.valor, ft.id))
        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def deletar(id_ft):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM fichas_tecnicas WHERE id=%s", (id_ft,))
        conn.commit()
        cur.close()
        conn.close()
