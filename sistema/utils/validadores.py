import re
from datetime import datetime

class Validadores:

    @staticmethod
    def validar_cpf_cnpj(texto: str) -> bool:
        """
        Verifica se o texto tem o tamanho correto de um CPF (11) ou CNPJ (14).
        Retorna True se for válido, False se estiver errado.
        """
        if not texto:
            return False
            
        # Remove tudo que não for número (pontos, traços, barras)
        limpo = re.sub(r'[^0-9]', '', str(texto))

        # Verifica tamanho (11 para CPF, 14 para CNPJ)
        # Verifica também se não são todos números iguais (ex: 111.111.111-11)
        if len(limpo) not in (11, 14):
            return False
            
        if limpo == limpo[0] * len(limpo):
            return False

        return True

    @staticmethod
    def validar_telefone(texto: str) -> bool:
        """
        Verifica se tem tamanho de telefone válido (com DDD).
        Aceita fixo (10 dígitos) ou celular (11 dígitos).
        """
        if not texto:
            return False
            
        limpo = re.sub(r'[^0-9]', '', str(texto))
        
        # Brasil: DDD (2) + Número (8 ou 9) = 10 ou 11 dígitos
        return 10 <= len(limpo) <= 11

    @staticmethod
    def validar_data(data_texto: str) -> bool:
        """
        Verifica se a data digitada existe e está no formato DD/MM/AAAA.
        Ex: '30/02/2025' retorna False (pois 30 de fev não existe).
        """
        if not data_texto:
            return False
            
        try:
            # Tenta "ler" a data. Se a data for inválida (ex: mês 13), o Python gera erro.
            datetime.strptime(data_texto, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_numero(texto: str) -> bool:
        """
        Retorna True se for número, False se não for.
        """
        if texto is None: 
            return False
            
        # Converte para string para garantir
        texto_limpo = str(texto).replace('R$', '').strip()
        
        # Lógica para aceitar vírgula (BR) ou ponto (US)
        if ',' in texto_limpo:
             texto_limpo = texto_limpo.replace('.', '').replace(',', '.')
        
        try:
            float(texto_limpo)
            return True  # <--- IMPORTANTE: Retorna True, não o número
        except ValueError:
            return False