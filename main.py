import customtkinter as ctk
from tkinter import ttk
from sistema.views.insumo_view import InsumoView
from sistema.views.home_view import HomeView
from sistema.views.compra_view import CompraView
from sistema.views.ficha_tecnica_view import FichaTecnicaView
from sistema.views.pedido_view import PedidoView
from sistema.views.relatorio_view import RelatorioView

# Configuração Global
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Stock Manager")
        self.geometry("1024x768")
        
        # --- CONFIGURAÇÃO DE ESTILO GLOBAL DAS TABELAS ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Cores do Modo Escuro
        bg_color = "#2b2b2b"
        fg_color = "white"
        header_bg = "#1f6aa5"
        header_fg = "white"
        
        # Configura o corpo da tabela
        style.configure("Treeview", 
                        background=bg_color, 
                        foreground=fg_color, 
                        fieldbackground=bg_color,
                        rowheight=30,
                        borderwidth=0)
        
        # Configura a cor de seleção (azul mais escuro)
        style.map("Treeview", background=[("selected", "#1f538d")])
        
        # Configura o cabeçalho
        style.configure("Treeview.Heading", 
                        background=header_bg, 
                        foreground=header_fg,
                        font=("Roboto", 10, "bold"),
                        borderwidth=0)
        # -------------------------------------------------

        self.tela_atual = None
        self.mostrar_home()

    def _limpar_tela(self):
        if self.tela_atual is not None:
            self.tela_atual.destroy()

    def mostrar_home(self):
        self._limpar_tela()
        self.tela_atual = HomeView(parent=self, controller_main=self)

    def mostrar_insumos(self):
        self._limpar_tela()
        self.tela_atual = InsumoView(parent=self, controller_main=self)

    def mostrar_compras(self):
        self._limpar_tela()
        self.tela_atual = CompraView(parent=self, controller_main=self)

    def mostrar_fichas(self):
        self._limpar_tela()
        self.tela_atual = FichaTecnicaView(parent=self, controller_main=self)

    def mostrar_pedidos(self):
        self._limpar_tela()
        self.tela_atual = PedidoView(parent=self, controller_main=self)

    def mostrar_relatorios(self):
        self._limpar_tela()
        self.tela_atual = RelatorioView(parent=self, controller_main=self)

if __name__ == "__main__":
    app = App()
    app.mainloop()