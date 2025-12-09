import customtkinter as ctk
from tkinter import ttk, messagebox
from sistema.controllers.ficha_tecnica_controller import FichaTecnicaController
from sistema.utils.helpers import Helpers

class FichaTecnicaView(ctk.CTkFrame):
    def __init__(self, parent, controller_main):
        super().__init__(parent)
        self.controller = FichaTecnicaController()
        self.controller_main = controller_main
        self.pack(fill="both", expand=True)

        # --- Cabeçalho ---
        frame_head = ctk.CTkFrame(self, fg_color="transparent")
        frame_head.pack(fill="x", padx=20, pady=10)
        
        btn_voltar = ctk.CTkButton(frame_head, text="← Voltar", width=60, 
                                   fg_color="transparent", border_width=1, text_color=("gray10", "white"),
                                   command=self.controller_main.mostrar_home)
        btn_voltar.pack(side="left")
        
        ctk.CTkLabel(frame_head, text="FICHAS TÉCNICAS (PRODUTOS)", 
                     font=("Roboto", 20, "bold")).pack(side="left", padx=20)

        ctk.CTkButton(frame_head, text="+ Novo Produto", fg_color="#2CC985", hover_color="#229E68",
                      command=self.abrir_modal_novo).pack(side="right")

        # --- Tabela de Produtos ---
        frame_tabela = ctk.CTkFrame(self, fg_color="transparent")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        colunas = ("id", "nome", "valor")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="Cód")
        self.tree.heading("nome", text="Nome do Produto")
        self.tree.heading("valor", text="Preço de Venda")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=400)
        self.tree.column("valor", width=150, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Botões de Ação ---
        frame_acoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_acoes.pack(pady=10)

        ctk.CTkButton(frame_acoes, text="Editar Receita", fg_color="#F1C40F", text_color="black", hover_color="#D4AC0D",
                      command=self.abrir_modal_editar).pack(side="left", padx=10)

        ctk.CTkButton(frame_acoes, text="Excluir Produto", fg_color="#C0392B", hover_color="#922B21",
                      command=self.acao_excluir).pack(side="left", padx=10)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        fichas = self.controller.buscar_todas()
        for f in fichas:
            val = Helpers.formatar_moeda(f.valor)
            self.tree.insert("", "end", values=(f.id, f.nome, val))

    def abrir_modal_novo(self):
        self._criar_modal("Novo Produto")

    def abrir_modal_editar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto para editar.")
            return
        id_ficha = self.tree.item(sel[0], 'values')[0]
        ficha_obj, itens = self.controller.buscar_ficha_completa(id_ficha)
        self._criar_modal("Editar Produto", ficha_obj, itens)

    def _criar_modal(self, titulo, ficha_editar=None, itens_editar=None):
        toplevel = ctk.CTkToplevel(self)
        toplevel.title(titulo)
        toplevel.geometry("600x700")
        
        toplevel.transient(self)
        toplevel.lift()
        toplevel.focus_force()
        toplevel.wait_visibility()
        toplevel.grab_set()

        # 1. Dados do Produto
        frame_top = ctk.CTkFrame(toplevel, fg_color="transparent")
        frame_top.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_top, text="Nome do Produto:").pack(anchor="w")
        entry_nome = ctk.CTkEntry(frame_top)
        entry_nome.pack(fill="x", pady=5)

        ctk.CTkLabel(frame_top, text="Preço de Venda (R$):").pack(anchor="w")
        entry_valor = ctk.CTkEntry(frame_top)
        entry_valor.pack(fill="x", pady=5)

        # 2. Área de Ingredientes
        frame_ing = ctk.CTkFrame(toplevel)
        frame_ing.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(frame_ing, text="Ingredientes da Receita", font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        # Controles para adicionar ingrediente
        frame_add = ctk.CTkFrame(frame_ing, fg_color="transparent")
        frame_add.pack(fill="x", padx=5)

        # Carrega lista de insumos do banco
        lista_opcoes = self.controller.buscar_insumos_combobox()
        combo_insumo = ctk.CTkComboBox(frame_add, values=lista_opcoes, width=250)
        combo_insumo.pack(side="left", padx=5)
        combo_insumo.set("Selecione o Ingrediente...")

        entry_qtd = ctk.CTkEntry(frame_add, placeholder_text="Qtd", width=80)
        entry_qtd.pack(side="left", padx=5)

        lista_memoria = []

        # Tabela Pequena de Ingredientes
        tree_itens = ttk.Treeview(frame_ing, columns=("nome", "qtd"), show="headings", height=8)
        tree_itens.heading("nome", text="Ingrediente")
        tree_itens.heading("qtd", text="Quantidade Necessária")
        
        tree_itens.column("nome", width=250)
        tree_itens.column("qtd", width=100, anchor="center")
        tree_itens.pack(fill="both", expand=True, padx=5, pady=5)

        def atualizar_lista_visual():
            for i in tree_itens.get_children(): tree_itens.delete(i)
            for item in lista_memoria:
                tree_itens.insert("", "end", values=(item['nome_visual'], item['qtd']))

        def add_item():
            sel = combo_insumo.get()
            qtd_str = entry_qtd.get()
            
            if "Selecione" in sel or not qtd_str: return
            
            try:
                qtd_float = Helpers.ler_dinheiro(qtd_str)
                id_insumo = int(sel.split(" - ")[0])
                nome_insumo = sel.split(" - ")[1]
                
                # Adiciona na memória
                lista_memoria.append({
                    "id_insumo": id_insumo,
                    "nome_visual": nome_insumo, # Apenas para mostrar na tabela
                    "qtd": qtd_float
                })
                atualizar_lista_visual()
                entry_qtd.delete(0, "end")
            except Exception as e:
                print(e)

        ctk.CTkButton(frame_add, text="+", width=40, command=add_item).pack(side="left", padx=5)

        # Botão Remover Item da Lista
        def remover_item():
            sel = tree_itens.selection()
            if sel:
                idx = tree_itens.index(sel[0])
                lista_memoria.pop(idx)
                atualizar_lista_visual()
        
        ctk.CTkButton(frame_ing, text="Remover Selecionado", fg_color="#C0392B", height=25, 
                      command=remover_item).pack(pady=5)

        # Preencher se for Edição
        if ficha_editar:
            entry_nome.insert(0, ficha_editar.nome)
            entry_valor.insert(0, Helpers.formatar_moeda(ficha_editar.valor))
            
            if itens_editar:
                for it in itens_editar:
                    lista_memoria.append({
                        "id_insumo": it['id_insumo'],
                        "nome_visual": it['nome'],
                        "qtd": it['qtd']
                    })
                atualizar_lista_visual()

        # Botão Salvar
        def salvar():
            nome = entry_nome.get()
            valor = entry_valor.get()
            
            id_edit = ficha_editar.id if ficha_editar else None
            self.controller.salvar_ficha(nome, valor, lista_memoria, toplevel, self.atualizar_tabela, id_edit)

        ctk.CTkButton(toplevel, text="SALVAR FICHA TÉCNICA", fg_color="#2CC985", height=50, font=("Roboto", 14, "bold"),
                      command=salvar).pack(fill="x", padx=20, pady=20)

    def acao_excluir(self):
        sel = self.tree.selection()
        if sel:
            id_ficha = self.tree.item(sel[0], 'values')[0]
            self.controller.excluir_ficha(id_ficha, self.atualizar_tabela)