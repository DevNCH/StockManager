from tkinter import messagebox
from sistema.service.ficha_tecnica_service import FichaTecnicaService
from sistema.utils.helpers import Helpers
from sistema.utils.validadores import Validadores

class FichaTecnicaController:
    
    def buscar_todas(self):
        return FichaTecnicaService.listar_todas()

    def buscar_insumos_combobox(self):
        return FichaTecnicaService.buscar_insumos_opcoes()

    def buscar_ficha_completa(self, id_ficha):
        return FichaTecnicaService.buscar_ficha_completa(id_ficha)

    def salvar_ficha(self, nome, valor_str, lista_ingredientes, janela, callback_atualizar, id_editar=None):
        # 1. Validações
        if not nome:
            messagebox.showwarning("Aviso", "O nome do produto é obrigatório!")
            return
            
        if not lista_ingredientes:
            messagebox.showwarning("Aviso", "Adicione pelo menos um ingrediente à ficha!")
            return

        # 2. Conversão
        valor_float = Helpers.ler_dinheiro(valor_str)
        
        dados_ficha = {
            "nome": nome,
            "valor": valor_float
        }

        # 3. Chama Service
        try:
            sucesso, mensagem = FichaTecnicaService.salvar_ficha_completa(dados_ficha, lista_ingredientes, id_editar)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                janela.destroy()
                callback_atualizar()
            else:
                messagebox.showerror("Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha inesperada: {e}")

    def excluir_ficha(self, id_ficha, callback_atualizar):
        if messagebox.askyesno("Confirmar", "Tem certeza? Isso apagará o produto e sua receita."):
            try:
                sucesso, msg = FichaTecnicaService.excluir_ficha(id_ficha)
                if sucesso:
                    messagebox.showinfo("Sucesso", msg)
                    callback_atualizar()
                else:
                    messagebox.showerror("Erro", msg)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha: {e}")