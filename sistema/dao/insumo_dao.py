from sistema.database.conexao import conectar
from sistema.models.insumo import Insumo

class InsumoDAO:

    @staticmethod
    def listar_todos():
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM insumos")
        dados = cur.fetchall()

        cur.close()
        conn.close()

        return [Insumo(**d) for d in dados]

    @staticmethod
    def buscar_por_id(id_insumo):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM insumos WHERE id=%s", (id_insumo,))
        dado = cur.fetchone()

        cur.close()
        conn.close()

        return Insumo(**dado) if dado else None

    @staticmethod
    def buscar_por_texto(texto):
        conn = conectar()
        cur = conn.cursor(dictionary=True)
        
        # Filtra por Nome (LIKE) OU por ID (se o texto for número)
        sql = """
            SELECT * FROM insumos 
            WHERE nome LIKE %s OR id = %s
        """
        
        # Prepara o termo com % para buscar em qualquer parte do texto
        termo = f"%{texto}%"
        
        # Se o texto for um número, usa ele para buscar por ID também. Se não, usa -1 (impossível)
        try:
            busca_id = int(texto)
        except ValueError:
            busca_id = -1
            
        cur.execute(sql, (termo, busca_id))
        dados = cur.fetchall()
        
        cur.close()
        conn.close()

        return [Insumo(**d) for d in dados]
    
    @staticmethod
    def inserir(insumo: Insumo):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            INSERT INTO insumos (nome, quantidade, unidade_medida)
            VALUES (%s, %s, %s)
        """
        cur.execute(sql, (insumo.nome, insumo.quantidade, insumo.unidade_medida))
        conn.commit()

        insumo.id = cur.lastrowid
        cur.close()
        conn.close()
        return insumo

    @staticmethod
    def atualizar(insumo: Insumo):
        conn = conectar()
        cur = conn.cursor()

        sql = """
            UPDATE insumos
            SET nome=%s, quantidade=%s, unidade_medida=%s
            WHERE id=%s
        """

        cur.execute(sql, (insumo.nome, insumo.quantidade, insumo.unidade_medida, insumo.id))

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def deletar(id_insumo):
        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM insumos WHERE id=%s", (id_insumo,))
        conn.commit()

        cur.close()
        conn.close()

    @staticmethod
    def atualizar_quantidade_estoque(id_insumo, delta_quantidade, cursor_externo=None):
        """
        Atualiza o estoque somando (ou subtraindo) o delta.
        Aceita cursor_externo para participar da transação da Nota Fiscal.
        """
        if cursor_externo:
            cur = cursor_externo
            fechar = False
        else:
            conn = conectar()
            cur = conn.cursor()
            fechar = True

        # SQL simples e direto para atualização de saldo
        sql = "UPDATE insumos SET quantidade = quantidade + %s WHERE id = %s"
        cur.execute(sql, (delta_quantidade, id_insumo))

        if fechar:
            conn.commit()
            cur.close()
            conn.close()