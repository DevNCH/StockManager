from datetime import datetime
import re

class Helpers:

    # --- 1. DATAS (A Ponte Brasil <-> MySQL) ---
    @staticmethod
    def data_para_mysql(data_br):
        """Recebe '25/12/2025' e retorna '2025-12-25' para o banco"""
        if not data_br: return None
        try:
            # Tenta converter
            dt = datetime.strptime(data_br, "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return None # Ou levantar erro, dependendo da sua regra

    @staticmethod
    def data_para_br(data_mysql):
        """Recebe '2025-12-25' (do banco) e retorna '25/12/2025' para a tela"""
        if not data_mysql: return ""
        # Se vier como objeto date do python, converte direto
        if hasattr(data_mysql, 'strftime'):
            return data_mysql.strftime("%d/%m/%Y")
        # Se vier como string
        try:
            dt = datetime.strptime(str(data_mysql), "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            return str(data_mysql)

    # --- 2. DINHEIRO E NÚMEROS ---
    @staticmethod
    def ler_dinheiro(valor_str):
        if not valor_str: return 0.0
        
        texto_limpo = str(valor_str).replace('R$', '').strip()
        
        if ',' in texto_limpo:
            texto_limpo = texto_limpo.replace('.', '').replace(',', '.')
            
        try:
            return float(texto_limpo)
        except ValueError:
            return 0.0
        
    @staticmethod
    def formatar_moeda(valor_float):
        if valor_float is None: valor_float = 0.0
        # Formata para padrão BR visualmente
        return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


    # --- 3. LIMPEZA (CPF/Telefone) ---
    @staticmethod
    def apenas_numeros(texto):
        """Remove tudo que não for dígito. Útil para salvar CPF/Tel limpo no banco."""
        if not texto: return ""
        return re.sub(r'[^0-9]', '', str(texto))

    @staticmethod
    def validar_telefone(telefone):
        """Verifica se tem tamanho mínimo (DDD + número)"""
        limpo = Helpers.apenas_numeros(telefone)
        return len(limpo) >= 10