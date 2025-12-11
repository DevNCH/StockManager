from tkinter import messagebox
from datetime import datetime
from sistema.service.pedido_service import PedidoService
from sistema.service.ficha_tecnica_service import FichaTecnicaService
from sistema.utils.helpers import Helpers

class PedidoController:
    
    # ... (métodos de busca simples mantidos) ...
    def buscar_todos_pedidos(self):
        return PedidoService.listar_todos()

    def buscar_produtos_combobox(self):
        fichas = FichaTecnicaService.listar_todas()
        lista = []
        for f in fichas:
            val_fmt = Helpers.formatar_moeda(f.valor)
            lista.append(f"{f.id} - {f.nome} - {val_fmt}")
        return lista

    def buscar_ingredientes_do_produto(self, id_produto):
        _, ingredientes = FichaTecnicaService.buscar_ficha_completa(id_produto)
        return ingredientes

    # --- NOVO ---
    def buscar_pedido_edicao(self, id_pedido):
        return PedidoService.buscar_pedido_completo(id_pedido)

    def salvar_pedido(self, dados_cliente, lista_itens_carrinho, janela, callback_atualizar, id_editar=None):
        if not lista_itens_carrinho:
            messagebox.showwarning("Aviso", "O carrinho está vazio!")
            return
        if not dados_cliente.get('cliente'):
            messagebox.showwarning("Aviso", "O nome do cliente é obrigatório!")
            return
        if not dados_cliente.get('data'):
            messagebox.showwarning("Aviso", "O data do pedido é obrigatória!")
            return
        if not dados_cliente.get('telefone'):
            messagebox.showwarning("Aviso", "O telefone do cliente é obrigatório!")
            return
        total_pedido = sum([item['qtd'] * item['valor_unit'] for item in lista_itens_carrinho])
        
        dados_finais = dados_cliente.copy()
        dados_finais['total'] = total_pedido

        # Passa o ID se for edição
        sucesso, msg = PedidoService.salvar_pedido_completo(dados_finais, lista_itens_carrinho, id_editar)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            janela.destroy()
            callback_atualizar()
        else:
            messagebox.showerror("Erro", msg)

    def excluir_pedido(self, id_pedido, callback_atualizar):
        if messagebox.askyesno("Confirmar", "Deseja excluir este pedido?"):
            sucesso, msg = PedidoService.excluir_pedido(id_pedido)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                callback_atualizar()
            else:
                messagebox.showerror("Erro", msg)