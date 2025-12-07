import customtkinter as ctk

class HomeView(ctk.CTkFrame):
    def __init__(self, parent, controller_main):
        super().__init__(parent)
        self.controller_main = controller_main # Referência para trocar de tela
        self.pack(fill="both", expand=True)

        # --- Layout Centralizado ---
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) # Espaço antes do titulo
        self.rowconfigure(10, weight=1) # Espaço depois dos botões

        # Título (Baseado no PPT)
        lbl_titulo = ctk.CTkLabel(self, 
                                  text="Sistema de Gerenciamento\nde Estoque", 
                                  font=("Roboto", 26, "bold"),
                                  text_color=("gray10", "white"))
        lbl_titulo.grid(row=1, column=0, pady=(0, 40))

        # --- Botões do Menu ---
        # Definindo um estilo padrão para os botões do menu
        btn_params = {
            "width": 300,
            "height": 50,
            "font": ("Roboto", 16, "bold"),
            "corner_radius": 8
        }

        # 1. Botão Estoque de Insumos
        btn_insumos = ctk.CTkButton(self, text="Estoque de Insumos", 
                                    fg_color="#1f6aa5", hover_color="#144870",
                                    command=lambda: self.controller_main.mostrar_insumos(),
                                    **btn_params)
        btn_insumos.grid(row=2, column=0, pady=10)

        # 2. Botão Registros de Compras (Ainda não implementado)
        btn_compras = ctk.CTkButton(self, text="Registros de Compras", 
                                    fg_color="#1f6aa5", hover_color="#144870",
                                    command=lambda: self.controller_main.mostrar_compras(),
                                    **btn_params)
        btn_compras.grid(row=3, column=0, pady=10)

        # 3. Botão Fichas Técnicas (Ainda não implementado)
        btn_fichas = ctk.CTkButton(self, text="Fichas Técnicas", 
                                   fg_color="#555", state="disabled", 
                                   **btn_params)
        btn_fichas.grid(row=4, column=0, pady=10)

        # 4. Botão Pedidos (Ainda não implementado)
        btn_pedidos = ctk.CTkButton(self, text="Pedidos", 
                                    fg_color="#555", state="disabled", 
                                    **btn_params)
        btn_pedidos.grid(row=5, column=0, pady=10)

        # 5. Botão Relatórios (Ainda não implementado)
        btn_relatorios = ctk.CTkButton(self, text="Relatórios", 
                                       fg_color="#555", state="disabled", 
                                       **btn_params)
        btn_relatorios.grid(row=6, column=0, pady=10)

        # Rodapé
        lbl_creditos = ctk.CTkLabel(self, text="Stock Manager v1.0", text_color="gray50")
        lbl_creditos.grid(row=9, column=0, pady=(40, 0))