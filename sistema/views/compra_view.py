
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from sistema.controllers.compra_controller import CompraController
from sistema.utils.helpers import Helpers

class CompraView(ctk.CTkFrame):
    def __init__(self, parent, controller_main):
        super().__init__(parent)
        self.controller = CompraController()
        self.controller_main = controller_main
        self.pack(fill="both", expand=True)

        # --- Cabeçalho ---
        frame_head = ctk.CTkFrame(self, fg_color="transparent")
        frame_head.pack(fill="x", padx=20, pady=10)
        
        btn_voltar = ctk.CTkButton(frame_head, text="← Voltar", width=60, 
                                   fg_color="transparent", border_width=1, text_color=("gray10", "white"),
                                   command=self.controller_main.mostrar_home)
        btn_voltar.pack(side="left")
        
        ctk.CTkLabel(frame_head, text="REGISTRO DE COMPRAS", font=("Roboto", 20, "bold")).pack(side="left", padx=20)

        ctk.CTkButton(frame_head, text="+ Nova Nota Fiscal", fg_color="#2CC985", 
                      command=self.abrir_modal_novo).pack(side="right")

        # --- Tabela ---
        frame_tabela = ctk.CTkFrame(self, fg_color="transparent")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        colunas = ("id", "fornecedor", "data", "valor")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="Código")
        self.tree.heading("fornecedor", text="Fornecedor")
        self.tree.heading("data", text="Data")
        self.tree.heading("valor", text="Total")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("fornecedor", width=300)
        self.tree.column("data", width=100, anchor="center")
        self.tree.column("valor", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)
        
        # --- Botões de Ação ---
        frame_acoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_acoes.pack(pady=10)

        ctk.CTkButton(frame_acoes, text="Editar / Ver Detalhes", fg_color="#F1C40F", text_color="black",
                      command=self.abrir_modal_editar).pack(side="left", padx=10)

        ctk.CTkButton(frame_acoes, text="Excluir Nota", fg_color="#C0392B",
                      command=self.acao_excluir).pack(side="left", padx=10)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        notas = self.controller.buscar_todas_notas()
        for n in notas:
            dt = Helpers.data_para_br(n.data_emissao)
            val = Helpers.formatar_moeda(n.valor)
            self.tree.insert("", "end", values=(n.id, n.nome_fornecedor, dt, val))

    def abrir_modal_novo(self):
        self._criar_modal("Nova Nota Fiscal")

    def abrir_modal_editar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma nota para editar.")
            return
        id_nota = self.tree.item(sel[0], 'values')[0]
        # Busca dados completos do banco
        nota_obj, itens = self.controller.buscar_nota_completa(id_nota)
        self._criar_modal("Editar Nota Fiscal", nota_obj, itens)

    def _criar_modal(self, titulo, nota_editar=None, itens_editar=None):
        toplevel = ctk.CTkToplevel(self)
        toplevel.title(titulo)
        toplevel.geometry("800x650")
        
        # --- CORREÇÃO DO ERRO DE TELA PRETA/GRAB FAILED ---
        toplevel.transient(self)
        toplevel.lift()
        toplevel.focus_force()
        # O segredo: esperar a janela ficar visível antes de bloquear
        toplevel.wait_visibility() 
        toplevel.grab_set()

        # 1. Cabeçalho
        frame_top = ctk.CTkFrame(toplevel, fg_color="transparent")
        frame_top.pack(fill="x", padx=20, pady=10)

        # Campos
        ctk.CTkLabel(frame_top, text="Fornecedor:").grid(row=0, column=0, sticky="w")
        entry_forn = ctk.CTkEntry(frame_top, width=250)
        entry_forn.grid(row=1, column=0, padx=5, pady=5)

        ctk.CTkLabel(frame_top, text="CNPJ:").grid(row=0, column=1, sticky="w")
        entry_cnpj = ctk.CTkEntry(frame_top, width=150)
        entry_cnpj.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frame_top, text="Data (dd/mm/aaaa):").grid(row=0, column=2, sticky="w")
        entry_data = ctk.CTkEntry(frame_top, width=120)
        entry_data.grid(row=1, column=2, padx=5, pady=5)

        data_hoje = datetime.now().strftime("%d/%m/%Y")
        entry_data.insert(0, data_hoje)

        ctk.CTkLabel(frame_top, text="NFCe:").grid(row=2, column=0, sticky="w")
        entry_nfce = ctk.CTkEntry(frame_top, width=150)
        entry_nfce.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(frame_top, text="Série:").grid(row=2, column=1, sticky="w")
        entry_serie = ctk.CTkEntry(frame_top, width=100)
        entry_serie.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # 2. Itens
        frame_itens = ctk.CTkFrame(toplevel)
        frame_itens.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(frame_itens, text="Insumos da Nota", font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Controles de Adição
        frame_add = ctk.CTkFrame(frame_itens, fg_color="transparent")
        frame_add.pack(fill="x", padx=5)

        combo_insumos = ctk.CTkComboBox(frame_add, values=self.controller.buscar_insumos_para_combobox(), width=250)
        combo_insumos.pack(side="left", padx=5)
        combo_insumos.set("Selecione o Insumo...")
        
        entry_qtd = ctk.CTkEntry(frame_add, placeholder_text="Qtd", width=80)
        entry_qtd.pack(side="left", padx=5)
        
        entry_val = ctk.CTkEntry(frame_add, placeholder_text="Valor R$", width=80)
        entry_val.pack(side="left", padx=5)

        lista_itens_memoria = []

        # Tabela de Itens (Pequena)
        tree_itens = ttk.Treeview(frame_itens, columns=("nome", "qtd", "valor"), show="headings", height=8)
        tree_itens.heading("nome", text="Insumo")
        tree_itens.heading("qtd", text="Qtd")
        tree_itens.heading("valor", text="Total R$")
        tree_itens.pack(fill="both", expand=True, padx=5, pady=5)

        def atualizar_lista_visual():
            for i in tree_itens.get_children(): tree_itens.delete(i)
            for item in lista_itens_memoria:
                tree_itens.insert("", "end", values=(item['nome'], item['qtd'], f"R$ {item['valor']}"))

        def add_item():
            sel = combo_insumos.get()
            q = entry_qtd.get()
            v = entry_val.get()
            if "Selecione" in sel or not q or not v: return
            
            try:
                lista_itens_memoria.append({
                    "id_insumo": int(sel.split(" - ")[0]),
                    "nome": sel.split(" - ")[1],
                    "qtd": Helpers.ler_dinheiro(q),
                    "valor": Helpers.ler_dinheiro(v)
                })
                atualizar_lista_visual()
                entry_qtd.delete(0, "end")
                entry_val.delete(0, "end")
            except: pass

        ctk.CTkButton(frame_add, text="+", width=40, command=add_item).pack(side="left", padx=5)
        
        # Botão para remover item da lista (Opcional, mas útil)
        def remover_item_visual():
            sel = tree_itens.selection()
            if sel:
                idx = tree_itens.index(sel[0])
                lista_itens_memoria.pop(idx)
                atualizar_lista_visual()
        
        ctk.CTkButton(frame_itens, text="Remover Item", fg_color="#C0392B", height=25, command=remover_item_visual).pack(pady=5)

        # PREENCHIMENTO SE FOR EDIÇÃO
        if nota_editar:
            entry_forn.insert(0, nota_editar.nome_fornecedor)
            entry_cnpj.insert(0, nota_editar.cnpj_fornecedor)
            entry_nfce.insert(0, nota_editar.nfce)
            entry_serie.insert(0, nota_editar.serie)
            
            # Limpa a data de hoje antes de colocar a data da nota salva
            entry_data.delete(0, "end") 
            entry_data.insert(0, Helpers.data_para_br(nota_editar.data_emissao))
            
            # Carrega itens
            if itens_editar:
                for it in itens_editar:
                    lista_itens_memoria.append(it)
                atualizar_lista_visual()

        # Botão Salvar Final
        def salvar():
            cabecalho = {
                "fornecedor": entry_forn.get(), "cnpj": entry_cnpj.get(),
                "nfce": entry_nfce.get(), "serie": entry_serie.get(), "data": entry_data.get()
            }
            # Se tiver nota_editar, manda o ID dela para atualizar
            id_edit = nota_editar.id if nota_editar else None
            self.controller.salvar_nota_completa(cabecalho, lista_itens_memoria, toplevel, self.atualizar_tabela, id_edit)

        ctk.CTkButton(toplevel, text="SALVAR LANÇAMENTO", fg_color="#2CC985", height=50, font=("Roboto", 14, "bold"),
                      command=salvar).pack(fill="x", padx=20, pady=20)

    def acao_excluir(self):
        sel = self.tree.selection()
        if sel:
            id_nota = self.tree.item(sel[0], 'values')[0]
            self.controller.excluir_nota(id_nota, self.atualizar_tabela)
