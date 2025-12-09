from sistema.database.conexao import conectar
from sistema.models.ficha_tecnica import FichaTecnica

class FichaTecnicaDAO:

    @staticmethod
    def listar_todas():
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM fichas_tecnicas ORDER BY id DESC")
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
    def inserir(ft: FichaTecnica, cursor_externo=None):
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        sql = "INSERT INTO fichas_tecnicas (nome, valor) VALUES (%s, %s)"
        cur.execute(sql, (ft.nome, ft.valor))
        
        ft.id = cur.lastrowid # Recupera o ID gerado

        if fechar:
            conn.commit()
            cur.close()
            conn.close()
        return ft

    @staticmethod
    def atualizar(ft: FichaTecnica, cursor_externo=None):
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        sql = "UPDATE fichas_tecnicas SET nome=%s, valor=%s WHERE id=%s"
        cur.execute(sql, (ft.nome, ft.valor, ft.id))

        if fechar:
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def deletar(id_ft, cursor_externo=None):
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        cur.execute("DELETE FROM fichas_tecnicas WHERE id=%s", (id_ft,))

        if fechar:
            conn.commit()
            cur.close()
            conn.close()