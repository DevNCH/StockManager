from tkinter import messagebox
from datetime import datetime, timedelta
from sistema.service.relatorio_service import RelatorioService
from sistema.utils.validadores import Validadores

class RelatorioController:
    
    def gerar_relatorio(self, dt_inicio, dt_fim):
        # 1. Validação de Datas
        if not Validadores.validar_data(dt_inicio) or not Validadores.validar_data(dt_fim):
            messagebox.showerror("Erro", "Datas inválidas! Use o formato DD/MM/AAAA")
            return None

        # Opcional: Validar se Inicio < Fim
        try:
            d1 = datetime.strptime(dt_inicio, "%d/%m/%Y")
            d2 = datetime.strptime(dt_fim, "%d/%m/%Y")
            if d1 > d2:
                messagebox.showwarning("Aviso", "A data de início não pode ser maior que a data fim.")
                return None
        except:
            return None

        # 2. Chama Service
        try:
            dados = RelatorioService.gerar_dados_dashboard(dt_inicio, dt_fim)
            return dados
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar relatório: {e}")
            return None
            
    def data_hoje(self):
        return datetime.now().strftime("%d/%m/%Y")
        
    def data_inicio_mes(self):
        # Retorna dia 01 do mês atual
        hoje = datetime.now()
        return hoje.replace(day=1).strftime("%d/%m/%Y")