import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from sistema.controllers.pedido_controller import PedidoController
from sistema.utils.helpers import Helpers

class PedidoView(ctk.CTkFrame):
    def __init__(self, parent, controller_main):
        super().__init__(parent)
        self.controller = PedidoController()
        self.controller_main = controller_main
        self.pack(fill="both", expand=True)

        # --- Cabeçalho ---
        frame_head = ctk.CTkFrame(self, fg_color="transparent")
        frame_head.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(frame_head, text="← Voltar", width=60, fg_color="transparent", border_width=1, 
                      text_color=("gray10", "white"), command=self.controller_main.mostrar_home).pack(side="left")
        
        ctk.CTkLabel(frame_head, text="GERENCIAMENTO DE PEDIDOS", font=("Roboto", 20, "bold")).pack(side="left", padx=20)

        ctk.CTkButton(frame_head, text="+ Novo Pedido", fg_color="#2CC985", 
                      command=self.abrir_modal_novo).pack(side="right")

        # --- Tabela de Pedidos ---
        frame_tabela = ctk.CTkFrame(self, fg_color="transparent")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        colunas = ("id", "data", "cliente", "total")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="Cód")
        self.tree.heading("data", text="Data")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("total", text="Valor Total")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("data", width=100, anchor="center")
        self.tree.column("cliente", width=300)
        self.tree.column("total", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)
        
        # --- Botões de Ação ---
        frame_acoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_acoes.pack(pady=10)

        ctk.CTkButton(frame_acoes, text="Editar Pedido", fg_color="#F1C40F", text_color="black", hover_color="#D4AC0D",
                      command=self.abrir_modal_editar).pack(side="left", padx=10)

        ctk.CTkButton(frame_acoes, text="Excluir Pedido", fg_color="#C0392B", hover_color="#922B21",
                      command=self.acao_excluir).pack(side="left", padx=10)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        pedidos = self.controller.buscar_todos_pedidos()
        for p in pedidos:
            dt = Helpers.data_para_br(p.data)
            val = Helpers.formatar_moeda(p.valor)
            self.tree.insert("", "end", values=(p.id, dt, p.nome, val))

    # --- GERENCIAMENTO DE MODAIS ---
    def abrir_modal_novo(self):
        self._criar_modal("Novo Pedido")

    def abrir_modal_editar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um pedido para editar.")
            return
        id_ped = self.tree.item(sel[0], 'values')[0]
        # Busca dados completos do banco (Objeto Pedido + Lista de Itens do Carrinho)
        pedido_obj, itens_carrinho = self.controller.buscar_pedido_edicao(id_ped)
        self._criar_modal("Editar Pedido", pedido_obj, itens_carrinho)

    def _criar_modal(self, titulo, pedido_editar=None, itens_editar=None):
        toplevel = ctk.CTkToplevel(self)
        toplevel.title(titulo)
        toplevel.geometry("1100x800")
        
        # Correção para Linux (Tela Preta)
        toplevel.transient(self)
        toplevel.lift()
        toplevel.focus_force()
        toplevel.wait_visibility()
        toplevel.grab_set()

        # --- ÁREA 1: DADOS DO CLIENTE ---
        frame_cli = ctk.CTkFrame(toplevel)
        frame_cli.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(frame_cli, text="Dados do Cliente e Entrega", font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        frame_campos = ctk.CTkFrame(frame_cli, fg_color="transparent")
        frame_campos.pack(fill="x", padx=5, pady=5)

        # Linha 1
        ctk.CTkLabel(frame_campos, text="Nome do Cliente:").grid(row=0, column=0, sticky="w")
        entry_nome = ctk.CTkEntry(frame_campos, width=300)
        entry_nome.grid(row=1, column=0, padx=5, pady=5)

        ctk.CTkLabel(frame_campos, text="CPF/CNPJ:").grid(row=0, column=1, sticky="w")
        entry_cpf = ctk.CTkEntry(frame_campos, width=150)
        entry_cpf.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_campos, text="Telefone:").grid(row=0, column=2, sticky="w")
        entry_tel = ctk.CTkEntry(frame_campos, width=150)
        entry_tel.grid(row=1, column=2, padx=5, pady=5)

        ctk.CTkLabel(frame_campos, text="Data:").grid(row=0, column=3, sticky="w")
        entry_data = ctk.CTkEntry(frame_campos, width=100)
        entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        entry_data.grid(row=1, column=3, padx=5, pady=5)

        # Linha 2 (Endereço)
        ctk.CTkLabel(frame_campos, text="CEP:").grid(row=2, column=0, sticky="w")
        entry_cep = ctk.CTkEntry(frame_campos, width=120)
        entry_cep.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame_campos, text="UF:").grid(row=2, column=0, padx=130, sticky="w")
        entry_uf = ctk.CTkEntry(frame_campos, width=50)
        entry_uf.grid(row=3, column=0, padx=130, pady=5, sticky="w")

        ctk.CTkLabel(frame_campos, text="Cidade:").grid(row=2, column=1, sticky="w")
        entry_cidade = ctk.CTkEntry(frame_campos, width=150)
        entry_cidade.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_campos, text="Bairro:").grid(row=2, column=2, sticky="w")
        entry_bairro = ctk.CTkEntry(frame_campos, width=150)
        entry_bairro.grid(row=3, column=2, padx=5, pady=5)

        # Linha 3 (Rua e Numero)
        ctk.CTkLabel(frame_campos, text="Rua:").grid(row=4, column=0, sticky="w")
        entry_rua = ctk.CTkEntry(frame_campos, width=300)
        entry_rua.grid(row=5, column=0, padx=5, pady=5)

        ctk.CTkLabel(frame_campos, text="Número:").grid(row=4, column=1, sticky="w")
        entry_num = ctk.CTkEntry(frame_campos, width=80)
        entry_num.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame_campos, text="Complemento:").grid(row=4, column=2, sticky="w")
        entry_comp = ctk.CTkEntry(frame_campos, width=150)
        entry_comp.grid(row=5, column=2, padx=5, pady=5)

        # Linha 4 (Obs)
        ctk.CTkLabel(frame_campos, text="Observações:").grid(row=6, column=0, sticky="w")
        entry_obs = ctk.CTkEntry(frame_campos, width=600)
        entry_obs.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # --- ÁREA 2: CARRINHO DE COMPRAS ---
        frame_carrinho = ctk.CTkFrame(toplevel)
        frame_carrinho.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(frame_carrinho, text="Itens do Pedido", font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        # Controles para adicionar produto
        frame_add = ctk.CTkFrame(frame_carrinho, fg_color="transparent")
        frame_add.pack(fill="x", padx=5)

        combo_prod = ctk.CTkComboBox(frame_add, values=self.controller.buscar_produtos_combobox(), width=300)
        combo_prod.pack(side="left", padx=5)
        combo_prod.set("Selecione o Produto...")

        entry_qtd = ctk.CTkEntry(frame_add, width=60, placeholder_text="Qtd")
        entry_qtd.pack(side="left", padx=5)

        # Memória do carrinho
        carrinho_memoria = []

        tree_itens = ttk.Treeview(frame_carrinho, columns=("nome", "qtd", "valor", "custom"), show="headings", height=8)
        tree_itens.heading("nome", text="Produto")
        tree_itens.heading("qtd", text="Qtd")
        tree_itens.heading("valor", text="Unitário")
        tree_itens.heading("custom", text="Personalização")
        
        tree_itens.column("nome", width=250)
        tree_itens.column("qtd", width=50, anchor="center")
        tree_itens.column("valor", width=80, anchor="center")
        tree_itens.column("custom", width=250) 
        
        tree_itens.pack(fill="both", expand=True, padx=5, pady=5)

        def atualizar_tabela_carrinho():
            for i in tree_itens.get_children(): tree_itens.delete(i)
            for item in carrinho_memoria:
                texto_custom = "Padrão"
                if item['nomes_removidos']:
                    texto_custom = "Sem: " + ", ".join(item['nomes_removidos'])
                
                val_fmt = Helpers.formatar_moeda(item['valor_unit'])
                tree_itens.insert("", "end", values=(item['nome'], item['qtd'], val_fmt, texto_custom))

        def add_produto():
            sel = combo_prod.get()
            q_str = entry_qtd.get()
            if "Selecione" in sel or not q_str: return

            try:
                partes = sel.split(" - ")
                id_prod = int(partes[0])
                nome_prod = partes[1]
                valor_prod = Helpers.ler_dinheiro(partes[2])
                qtd = Helpers.ler_dinheiro(q_str)

                carrinho_memoria.append({
                    'id_ficha': id_prod, 'nome': nome_prod, 'qtd': qtd,
                    'valor_unit': valor_prod, 'removidos': [], 'nomes_removidos': [] 
                })
                atualizar_tabela_carrinho()
                entry_qtd.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar: {e}")

        ctk.CTkButton(frame_add, text="Adicionar", width=80, command=add_produto).pack(side="left", padx=5)

        # --- SUB-MODAL: PERSONALIZAR (Retirar Ingredientes) ---
        def abrir_personalizacao():
            sel = tree_itens.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecione um item do carrinho para personalizar.")
                return
            idx = tree_itens.index(sel[0])
            item_atual = carrinho_memoria[idx]
            
            ingredientes = self.controller.buscar_ingredientes_do_produto(item_atual['id_ficha'])
            if not ingredientes:
                messagebox.showinfo("Info", "Este produto não possui ingredientes cadastrados.")
                return

            win_cust = ctk.CTkToplevel(toplevel)
            win_cust.title(f"Personalizar {item_atual['nome']}")
            win_cust.geometry("400x500")
            
            # Fix Linux Submodal
            win_cust.transient(toplevel)
            win_cust.lift()
            win_cust.focus_force()
            win_cust.wait_visibility()
            win_cust.grab_set()

            ctk.CTkLabel(win_cust, text="Desmarque o que o cliente NÃO quer:", font=("Roboto", 14)).pack(pady=10)
            vars_checkbox = [] 
            scroll_frame = ctk.CTkScrollableFrame(win_cust)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

            for ing in ingredientes:
                esta_removido = ing['id_insumo'] in item_atual['removidos']
                var = ctk.IntVar(value=0 if esta_removido else 1)
                lbl_texto = f"{ing['nome']} ({ing['qtd']} {ing['unidade']})"
                chk = ctk.CTkCheckBox(scroll_frame, text=lbl_texto, variable=var)
                chk.pack(anchor="w", pady=5)
                vars_checkbox.append({'id': ing['id_insumo'], 'nome': ing['nome'], 'var': var})

            def salvar_customizacao():
                item_atual['removidos'] = []
                item_atual['nomes_removidos'] = []
                for obj in vars_checkbox:
                    if obj['var'].get() == 0:
                        item_atual['removidos'].append(obj['id'])
                        item_atual['nomes_removidos'].append(obj['nome'])
                atualizar_tabela_carrinho()
                win_cust.destroy()

            ctk.CTkButton(win_cust, text="Confirmar Alterações", fg_color="#F1C40F", text_color="black",
                          command=salvar_customizacao).pack(pady=10)

        # Botões do Carrinho
        frame_botoes_cart = ctk.CTkFrame(frame_carrinho, fg_color="transparent")
        frame_botoes_cart.pack(pady=5)
        ctk.CTkButton(frame_botoes_cart, text="Personalizar / Retirar Ingredientes", 
                      fg_color="#F1C40F", text_color="black", hover_color="#D4AC0D",
                      command=abrir_personalizacao).pack(side="left", padx=10)
        
        def remover_item_carrinho():
            sel = tree_itens.selection()
            if sel:
                idx = tree_itens.index(sel[0])
                carrinho_memoria.pop(idx)
                atualizar_tabela_carrinho()

        ctk.CTkButton(frame_botoes_cart, text="Remover do Carrinho", fg_color="#C0392B", hover_color="#922B21",
                      command=remover_item_carrinho).pack(side="left", padx=10)

        # --- PREENCHIMENTO SE FOR EDIÇÃO ---
        if pedido_editar:
            entry_nome.insert(0, pedido_editar.nome)
            if pedido_editar.cpf_cnpj: entry_cpf.insert(0, pedido_editar.cpf_cnpj)
            if pedido_editar.telefone: entry_tel.insert(0, pedido_editar.telefone)
            
            entry_data.delete(0, "end")
            entry_data.insert(0, Helpers.data_para_br(pedido_editar.data))
            
            if pedido_editar.observacoes: entry_obs.insert(0, pedido_editar.observacoes)
            if pedido_editar.cep: entry_cep.insert(0, pedido_editar.cep)
            if pedido_editar.unidade_federal: entry_uf.insert(0, pedido_editar.unidade_federal)
            if pedido_editar.cidade: entry_cidade.insert(0, pedido_editar.cidade)
            if pedido_editar.bairro: entry_bairro.insert(0, pedido_editar.bairro)
            if pedido_editar.rua: entry_rua.insert(0, pedido_editar.rua)
            if pedido_editar.numero: entry_num.insert(0, pedido_editar.numero)
            if pedido_editar.complemento: entry_comp.insert(0, pedido_editar.complemento)

            # Preenche Carrinho
            if itens_editar:
                for it in itens_editar:
                    carrinho_memoria.append(it)
                atualizar_tabela_carrinho()

        # 3. Botão Salvar Pedido Final
        def finalizar_pedido():
            # Empacota TUDO
            dados = {
                'cliente': entry_nome.get(),
                'cpf_cnpj': entry_cpf.get(),
                'telefone': entry_tel.get(),
                'data': entry_data.get(),
                'obs': entry_obs.get(),
                'cep': entry_cep.get(),
                'uf': entry_uf.get(),
                'cidade': entry_cidade.get(),
                'bairro': entry_bairro.get(),
                'rua': entry_rua.get(),
                'numero': entry_num.get(),
                'complemento': entry_comp.get()
            }
            # Se for edição, manda ID
            id_edit = pedido_editar.id if pedido_editar else None
            self.controller.salvar_pedido(dados, carrinho_memoria, toplevel, self.atualizar_tabela, id_edit)

        ctk.CTkButton(toplevel, text="FINALIZAR PEDIDO", fg_color="#2CC985", height=50, hover_color="#229E68",
                      font=("Roboto", 14, "bold"), command=finalizar_pedido).pack(fill="x", padx=20, pady=20)

    def acao_excluir(self):
        sel = self.tree.selection()
        if sel:
            id_ped = self.tree.item(sel[0], 'values')[0]
            self.controller.excluir_pedido(id_ped, self.atualizar_tabela)