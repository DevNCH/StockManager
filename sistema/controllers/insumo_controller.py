# sistema/controllers/insumo_controller.py
from tkinter import messagebox
from sistema.service.insumo_service import InsumoService
from sistema.utils.helpers import Helpers
from sistema.utils.validadores import Validadores

class InsumoController:
    
    def __init__(self):
        pass

    def buscar_todos(self):
        return InsumoService.listar_estoque()

    def pesquisar_insumos(self, texto):
        # Chama a lógica centralizada na Service
        return InsumoService.pesquisar_insumos(texto)

    def salvar_insumo(self, nome, qtd_str, unidade, janela_popup, callback_atualizar_tabela):
        # 1. Validação
        if not nome:
            messagebox.showwarning("Atenção", "O campo Nome é obrigatório!")
            return

        if not qtd_str or qtd_str.strip() == "":
            qtd_str = "0"

        if not Validadores.validar_numero(qtd_str):
            messagebox.showerror("Erro", "Quantidade inválida! Use números.")
            return
        
        if not unidade:
            messagebox.showerror("Erro", "Preencha o campo de unidade!")

        # 2. Conversão
        qtd_float = Helpers.ler_dinheiro(qtd_str)

        # 3. Chama Service (Sem mexer em DAO aqui)
        try:
            InsumoService.criar_insumo(nome, qtd_float, unidade)
            
            messagebox.showinfo("Sucesso", f"Insumo '{nome}' salvo!")
            janela_popup.destroy()
            callback_atualizar_tabela()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def atualizar_insumo(self, id_insumo, nome, qtd_str, unidade, janela_popup, callback_atualizar_tabela):
        # 1. Validação
        if not nome:
            messagebox.showwarning("Atenção", "O campo Nome é obrigatório!")
            return

        if not qtd_str or qtd_str.strip() == "":
            qtd_str = "0"

        if not Validadores.validar_numero(qtd_str):
            messagebox.showerror("Erro", "Quantidade inválida! Use números.")
            return

        qtd_float = Helpers.ler_dinheiro(qtd_str)

        # 3. Chama Service
        try:
            InsumoService.atualizar_insumo(id_insumo, nome, qtd_float, unidade)
            
            messagebox.showinfo("Sucesso", f"Insumo '{nome}' atualizado!")
            janela_popup.destroy()
            callback_atualizar_tabela()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")
            
    def excluir_insumo(self, id_insumo, callback_atualizar_tabela):
        if not id_insumo:
            return
            
        confirmacao = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este insumo?")
        if confirmacao:
            try:
                InsumoService.excluir_insumo(id_insumo)
                callback_atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir: {e}")