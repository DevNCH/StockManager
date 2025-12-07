# sistema/controllers/compra_controller.py
from tkinter import messagebox
from sistema.service.nota_fiscal_service import NotaFiscalService

class CompraController:
    
    def buscar_todas_notas(self):
        return NotaFiscalService.listar_todas()

    def buscar_insumos_para_combobox(self):
        return NotaFiscalService.buscar_insumos_opcoes()

    def buscar_nota_completa(self, id_nota):
        return NotaFiscalService.buscar_detalhes_completo(id_nota)

    def salvar_nota_completa(self, cabecalho_dict, lista_itens, janela, callback_atualizar, id_nota_editar=None):
        # 1. Validação de Formulário (Responsabilidade da Controller)
        if not cabecalho_dict['fornecedor'] or not cabecalho_dict['data']:
            messagebox.showwarning("Aviso", "Preencha Fornecedor e Data!")
            return
            
        if not lista_itens:
            messagebox.showwarning("Aviso", "Adicione pelo menos um insumo na nota!")
            return

        # 2. Chama a Service para fazer a mágica
        try:
            NotaFiscalService.salvar_nota_transacionada(cabecalho_dict, lista_itens, id_nota_editar)
            
            messagebox.showinfo("Sucesso", "Operação realizada com sucesso!")
            janela.destroy()
            callback_atualizar()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def excluir_nota(self, id_nota, callback_atualizar):
        # 1. Confirmação com usuário
        if not messagebox.askyesno("Confirmar Exclusão", 
                                   "Tem certeza? Isso excluirá a nota e ESTORNARÁ (removerá) os itens do estoque."):
            return

        # 2. Chama a Service
        try:
            NotaFiscalService.excluir_nota_transacionada(id_nota)
            
            messagebox.showinfo("Sucesso", "Nota excluída e estoque estornado com sucesso!")
            callback_atualizar()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir: {e}")