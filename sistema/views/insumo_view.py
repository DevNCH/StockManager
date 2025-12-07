import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from sistema.controllers.insumo_controller import InsumoController

class InsumoView(ctk.CTkFrame):
    def __init__(self, parent, controller_main=None): # Adicione controller_main
        super().__init__(parent)
        self.controller = InsumoController()
        self.controller_main = controller_main # Guarda a referência
        self.pack(fill="both", expand=True)


    # --- Botão Voltar (Seta) ---
        if self.controller_main:
            btn_voltar = ctk.CTkButton(self, text="← Voltar", width=60, fg_color="transparent", border_width=1, border_color="#ccc",
                                       text_color=("gray10", "white"), command=self.controller_main.mostrar_home)
            btn_voltar.pack(anchor="w", padx=20, pady=(10, 0))

        # --- Configuração de Estilo da Tabela (Treeview) ---
        # Como o CTk não tem tabela, estilizamos a nativa para parecer moderna
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # --- Cabeçalho ---
        lbl_titulo = ctk.CTkLabel(self, text="ESTOQUE DE INSUMOS", 
                                  font=("Roboto", 24, "bold"),
                                  text_color=("#333", "white"))
        lbl_titulo.pack(pady=(20, 10))

        # --- Área de Busca e Botão Novo ---
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=20, pady=10)

        # Campo de Busca (CTkEntry já tem placeholder nativo!)
        self.entry_busca = ctk.CTkEntry(frame_topo, 
                                        placeholder_text="Pesquisar por nome ou ID...",
                                        width=300,
                                        height=35)
        self.entry_busca.pack(side="left", padx=(0, 10))
        self.entry_busca.bind("<Return>", self.realizar_pesquisa)

        btn_buscar = ctk.CTkButton(frame_topo, text="Buscar", width=80, height=35,
                                   command=self.realizar_pesquisa)
        btn_buscar.pack(side="left")

        # Botão Novo (Verde)
        btn_novo = ctk.CTkButton(frame_topo, text="+ Novo Insumo", 
                                 fg_color="#2CC985", hover_color="#229E68",
                                 height=35, font=("Roboto", 12, "bold"),
                                 command=self.abrir_modal_novo)
        btn_novo.pack(side="right")

        # --- Tabela (Treeview) ---
        # Container para a tabela e scrollbar
        frame_tabela = ctk.CTkFrame(self, fg_color="transparent")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        colunas = ("id", "nome", "quantidade", "medida")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")
        
        # Cabeçalhos
        self.tree.heading("id", text="Código")
        self.tree.heading("nome", text="Insumo")
        self.tree.heading("quantidade", text="Quantidade")
        self.tree.heading("medida", text="Unidade")

        # Colunas
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=300, anchor="w")
        self.tree.column("quantidade", width=100, anchor="center")
        self.tree.column("medida", width=100, anchor="center")

        # Scrollbar (Scrollbar nativa estilizada ou CTkScrollbar n funciona bem com treeview direto)
        # Usaremos a nativa mas alinhada
        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Botões de Ação (Editar e Excluir) ---
        frame_acoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_acoes.pack(pady=20)

        btn_editar = ctk.CTkButton(frame_acoes, text="Editar Selecionado", 
                                   fg_color="#F1C40F", hover_color="#D4AC0D", text_color="black",
                                   command=self.abrir_modal_editar)
        btn_editar.pack(side="left", padx=10)

        btn_excluir = ctk.CTkButton(frame_acoes, text="Excluir Selecionado", 
                                    fg_color="#C0392B", hover_color="#922B21",
                                    command=self.acao_excluir)
        btn_excluir.pack(side="left", padx=10)

        # Carregar dados iniciais
        self.atualizar_tabela()

    # --- Métodos de Lógica (Iguais, mas adaptados visualmente) ---

    def realizar_pesquisa(self, event=None):
        texto = self.entry_busca.get()
        # Limpa tabela
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Busca
        insumos_filtrados = self.controller.pesquisar_insumos(texto)
        # Preenche
        for insumo in insumos_filtrados:
            self.tree.insert("", "end", values=(insumo.id, insumo.nome, insumo.quantidade, insumo.unidade_medida))

    def atualizar_tabela(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        insumos = self.controller.buscar_todos()
        for insumo in insumos:
            self.tree.insert("", "end", values=(insumo.id, insumo.nome, insumo.quantidade, insumo.unidade_medida))

    def abrir_modal_novo(self):
        self._criar_modal("Novo Insumo", is_edit=False)

    def abrir_modal_editar(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um insumo na tabela para editar.")
            return
        
        valores = self.tree.item(item_selecionado[0], 'values')
        self._criar_modal("Editar Insumo", is_edit=True, dados=valores)

    def _criar_modal(self, titulo, is_edit, dados=None):
        # Janela TopLevel do CTk
        toplevel = ctk.CTkToplevel(self)
        toplevel.title(titulo)
        toplevel.geometry("400x350")
        
        # Garante que a janela fique na frente e tenha foco
        toplevel.transient(self) 
        toplevel.lift()
        toplevel.focus_force()
        # O grab_set bloqueia a janela principal, impedindo cliques fora
        toplevel.grab_set()

        # --- Campos do Formulário ---
        # Usamos padding (pady) no pack para dar espaço vertical
        
        ctk.CTkLabel(toplevel, text="Nome do Insumo:", font=("Roboto", 14)).pack(anchor="w", padx=20, pady=(20, 5))
        entry_nome = ctk.CTkEntry(toplevel)
        entry_nome.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(toplevel, text="Quantidade:", font=("Roboto", 14)).pack(anchor="w", padx=20, pady=(10, 5))
        entry_qtd = ctk.CTkEntry(toplevel)
        entry_qtd.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(toplevel, text="Unidade de Medida:", font=("Roboto", 14)).pack(anchor="w", padx=20, pady=(10, 5))
        combo_medida = ctk.CTkComboBox(toplevel, values=["kg", "L", "unidade"])
        combo_medida.pack(fill="x", padx=20, pady=5)

        # Se for edição, preenche os campos com os dados atuais
        if is_edit and dados:
            id_atual, nome_atual, qtd_atual, unidade_atual = dados
            entry_nome.insert(0, nome_atual)
            entry_qtd.insert(0, qtd_atual)
            combo_medida.set(unidade_atual)

        # --- Botões ---
        frame_btns = ctk.CTkFrame(toplevel, fg_color="transparent")
        frame_btns.pack(pady=30)

        # Função interna para chamar a controller
        def confirmar():
            nome = entry_nome.get()
            qtd = entry_qtd.get()
            unidade = combo_medida.get()
            
            if is_edit:
                # Passa o ID (dados[0]) para atualizar
                self.controller.atualizar_insumo(dados[0], nome, qtd, unidade, toplevel, self.atualizar_tabela)
            else:
                self.controller.salvar_insumo(nome, qtd, unidade, toplevel, self.atualizar_tabela)

        ctk.CTkButton(frame_btns, text="Cancelar", fg_color="transparent", border_width=1, 
                      text_color=("gray10", "gray90"), command=toplevel.destroy).pack(side="left", padx=10)

        ctk.CTkButton(frame_btns, text="Salvar", fg_color="#2CC985", hover_color="#229E68",
                      command=confirmar).pack(side="left", padx=10)

    def acao_excluir(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            return
        valores = self.tree.item(item_selecionado[0], 'values')
        self.controller.excluir_insumo(valores[0], self.atualizar_tabela)