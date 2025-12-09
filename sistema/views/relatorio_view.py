import customtkinter as ctk
from tkinter import ttk
from sistema.controllers.relatorio_controller import RelatorioController
from sistema.utils.helpers import Helpers

class RelatorioView(ctk.CTkFrame):
    def __init__(self, parent, controller_main):
        super().__init__(parent)
        self.controller = RelatorioController()
        self.controller_main = controller_main
        self.pack(fill="both", expand=True)

        # --- Cabeçalho ---
        frame_head = ctk.CTkFrame(self, fg_color="transparent")
        frame_head.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(frame_head, text="← Voltar", width=60, fg_color="transparent", border_width=1, 
                      text_color=("gray10", "white"), command=self.controller_main.mostrar_home).pack(side="left")
        
        ctk.CTkLabel(frame_head, text="RELATÓRIOS GERENCIAIS", font=("Roboto", 20, "bold")).pack(side="left", padx=20)

        # --- Filtros ---
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_filtros, text="Período:").pack(side="left", padx=10, pady=10)
        
        self.entry_ini = ctk.CTkEntry(frame_filtros, width=100, placeholder_text="DD/MM/AAAA")
        self.entry_ini.pack(side="left", padx=5)
        self.entry_ini.insert(0, self.controller.data_inicio_mes())

        ctk.CTkLabel(frame_filtros, text="até").pack(side="left", padx=5)

        self.entry_fim = ctk.CTkEntry(frame_filtros, width=100, placeholder_text="DD/MM/AAAA")
        self.entry_fim.pack(side="left", padx=5)
        self.entry_fim.insert(0, self.controller.data_hoje())

        ctk.CTkButton(frame_filtros, text="Gerar Relatório", fg_color="#1f6aa5", 
                      command=self.gerar).pack(side="left", padx=20)

        # --- Área de Conteúdo (Cards + Abas) ---
        self.frame_content = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_content.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Cards de Resumo (Criados dinamicamente)
        self.frame_cards = ctk.CTkFrame(self.frame_content, fg_color="transparent")
        self.frame_cards.pack(fill="x", pady=(0, 20))
        
        # Abas
        self.tabview = ctk.CTkTabview(self.frame_content)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_prod = self.tabview.add("Produtos Vendidos")
        self.tab_insumo = self.tabview.add("Consumo de Insumos")
        
        # Inicializa tabelas vazias
        self.criar_tabelas()

    def criar_card(self, parent, titulo, valor, cor_texto):
        card = ctk.CTkFrame(parent)
        card.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkLabel(card, text=titulo, font=("Roboto", 12)).pack(pady=(10,0))
        ctk.CTkLabel(card, text=valor, font=("Roboto", 22, "bold"), text_color=cor_texto).pack(pady=(0,10))

    def criar_tabelas(self):
        # Tabela Produtos
        cols_prod = ("nome", "qtd", "total")
        self.tree_prod = ttk.Treeview(self.tab_prod, columns=cols_prod, show="headings")
        self.tree_prod.heading("nome", text="Produto")
        self.tree_prod.heading("qtd", text="Qtd Vendida")
        self.tree_prod.heading("total", text="Faturamento Total")
        self.tree_prod.column("nome", width=300)
        self.tree_prod.column("qtd", width=100, anchor="center")
        self.tree_prod.column("total", width=150, anchor="center")
        self.tree_prod.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabela Insumos
        cols_ins = ("nome", "qtd", "un")
        self.tree_ins = ttk.Treeview(self.tab_insumo, columns=cols_ins, show="headings")
        self.tree_ins.heading("nome", text="Insumo")
        self.tree_ins.heading("qtd", text="Qtd Consumida")
        self.tree_ins.heading("un", text="Unidade")
        self.tree_ins.column("nome", width=300)
        self.tree_ins.column("qtd", width=150, anchor="center")
        self.tree_ins.column("un", width=100, anchor="center")
        self.tree_ins.pack(fill="both", expand=True, padx=10, pady=10)

    def gerar(self):
        # Busca dados
        dados = self.controller.gerar_relatorio(self.entry_ini.get(), self.entry_fim.get())
        if not dados: return

        # 1. Atualizar Cards
        for widget in self.frame_cards.winfo_children(): widget.destroy()
        
        fin = dados['financeiro']
        self.criar_card(self.frame_cards, "Faturamento", Helpers.formatar_moeda(fin['faturamento']), "#2CC985")
        self.criar_card(self.frame_cards, "Custos (Compras)", Helpers.formatar_moeda(fin['custos']), "#E74C3C")
        
        cor_lucro = "#2CC985" if fin['lucro'] >= 0 else "#E74C3C"
        self.criar_card(self.frame_cards, "Lucro Líquido", Helpers.formatar_moeda(fin['lucro']), cor_lucro)

        # 2. Atualizar Tabela Produtos
        for i in self.tree_prod.get_children(): self.tree_prod.delete(i)
        for p in dados['produtos']:
            val_fmt = Helpers.formatar_moeda(p['total'])
            self.tree_prod.insert("", "end", values=(p['nome'], p['qtd'], val_fmt))

        # 3. Atualizar Tabela Insumos
        for i in self.tree_ins.get_children(): self.tree_ins.delete(i)
        for ins in dados['insumos']:
            self.tree_ins.insert("", "end", values=(ins['nome'], f"{ins['qtd']:.3f}", ins['unidade']))