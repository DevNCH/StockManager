from sistema.database.conexao import conectar
from sistema.models.ficha_tecnica_insumo import FichaTecnicaInsumo

class FichaTecnicaInsumoDAO:

    @staticmethod
    def listar_por_ficha(id_ficha):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM ficha_tecnica_insumo WHERE id_ficha_tecnica=%s",
                    (id_ficha,))
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return [FichaTecnicaInsumo(**d) for d in dados]

    @staticmethod
    def inserir(fti: FichaTecnicaInsumo):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            INSERT INTO ficha_tecnica_insumo (id_ficha_tecnica, id_insumo, quantidade)
            VALUES (%s, %s, %s)
        """

        cur.execute(sql, (fti.id_ficha_tecnica, fti.id_insumo, fti.quantidade))
        conn.commit()

        fti.id = cur.lastrowid
        cur.close()
        conn.close()
        return fti

    @staticmethod
    def atualizar(fti: FichaTecnicaInsumo):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            UPDATE ficha_tecnica_insumo
            SET id_ficha_tecnica=%s, id_insumo=%s, quantidade=%s
            WHERE id=%s
        """

        cur.execute(sql, (
            fti.id_ficha_tecnica, fti.id_insumo,
            fti.quantidade, fti.id
        ))

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def deletar(id_fti):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM ficha_tecnica_insumo WHERE id=%s", (id_fti,))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def listar_por_fichas(lista_ids):
        if not lista_ids:
            return []

        placeholders = ",".join(["%s"] * len(lista_ids))
        sql = f"""
            SELECT *
            FROM ficha_tecnica_insumo
            WHERE id_ficha_tecnica IN ({placeholders})
        """

        try:
            conn = conectar()
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, lista_ids)
            dados = cur.fetchall()
            return [FichaTecnicaInsumo(**d) for d in dados]
        finally:
            cur.close()
            conn.close()
