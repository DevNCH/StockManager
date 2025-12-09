from sistema.database.conexao import conectar
from sistema.models.nota_fiscal import NotaFiscal

class NotaFiscalDAO:

    @staticmethod
    def listar_todas():
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM notas_fiscais ORDER BY id DESC")
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return [NotaFiscal(**d) for d in dados]

    @staticmethod
    def buscar_por_id(id_nota):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM notas_fiscais WHERE id=%s", (id_nota,))
        dado = cur.fetchone()
        cur.close()
        conn.close()
        return NotaFiscal(**dado) if dado else None

    @staticmethod
    def inserir(nota: NotaFiscal, cursor_externo=None):
        # Se receber cursor externo (do Service), usa ele e NÃO fecha a conexão aqui
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        sql = """
            INSERT INTO notas_fiscais (nfce, serie, data_emissao, cnpj_fornecedor,
                nome_fornecedor, valor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (nota.nfce, nota.serie, nota.data_emissao,
                   nota.cnpj_fornecedor, nota.nome_fornecedor, nota.valor)

        cur.execute(sql, valores)
        nota.id = cur.lastrowid # Recupera ID gerado

        if fechar:
            conn.commit()
            cur.close()
            conn.close()
        
        return nota

    @staticmethod
    def atualizar(nota: NotaFiscal, cursor_externo=None):
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        sql = """
            UPDATE notas_fiscais
            SET nfce=%s, serie=%s, data_emissao=%s, cnpj_fornecedor=%s,
                nome_fornecedor=%s, valor=%s
            WHERE id=%s
        """
        valores = (nota.nfce, nota.serie, nota.data_emissao,
                   nota.cnpj_fornecedor, nota.nome_fornecedor,
                   nota.valor, nota.id)

        cur.execute(sql, valores)

        if fechar:
            conn.commit()
            cur.close()
            conn.close()

    @staticmethod
    def deletar(id_nota, cursor_externo=None):
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        cur.execute("DELETE FROM notas_fiscais WHERE id=%s", (id_nota,))

        if fechar:
            conn.commit()
            cur.close()
            conn.close()
            
    # buscar_por_periodo mantém igual pois é só leitura
    @staticmethod
    def buscar_por_periodo(data_inicio, data_fim):
        sql = "SELECT * FROM notas_fiscais WHERE data_emissao BETWEEN %s AND %s ORDER BY data_emissao ASC"
        try:
            conn = conectar()
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, (data_inicio, data_fim))
            dados = cur.fetchall()
            return [NotaFiscal(**d) for d in dados]
        finally:
            cur.close()
            conn.close()