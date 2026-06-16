import tkinter as tk
from tkinter import ttk, messagebox
from control.combustivel_controller import CombustivelController
from view.combustivel_view import CombustivelView


class CombustivelListView(tk.Toplevel):
    """Tela de listagem e CRUD de combustiveis."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Combustiveis")
        self.geometry("700x420")

        self.controller = CombustivelController()
        self._construir_tela()
        self.carregar_dados()

    def _construir_tela(self):
        tk.Label(self, text="Combustiveis Cadastrados", font=("Arial", 14, "bold")).pack(pady=8)

        colunas = ("id", "tipo", "preco", "estoque")
        self._tree = ttk.Treeview(self, columns=colunas, show="headings", height=12)
        self._tree.heading("id",      text="ID")
        self._tree.heading("tipo",    text="Tipo")
        self._tree.heading("preco",   text="Preco/Litro")
        self._tree.heading("estoque", text="Estoque (L)")
        self._tree.column("id",      width=50,  anchor="center")
        self._tree.column("tipo",    width=220, anchor="center")
        self._tree.column("preco",   width=150, anchor="center")
        self._tree.column("estoque", width=150, anchor="center")
        self._tree.pack(padx=10, pady=5)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)
        tk.Button(frame_botoes, text="Novo",    width=14, command=self._novo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Editar",  width=14, command=self._editar).grid(row=0, column=1, padx=5)
        tk.Button(frame_botoes, text="Remover", width=14, command=self._remover).grid(row=0, column=2, padx=5)

    def carregar_dados(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._combustiveis = self.controller.listar()
        for c in self._combustiveis:
            self._tree.insert("", "end", values=(
                c.combustivel_id,
                c.tipo.value,
                f"R$ {c.preco_litro:.2f}",
                f"{c.estoque_litros:.2f}",
            ))

    def _selecionado(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um combustivel.", parent=self)
            return None
        return self._combustiveis[self._tree.index(sel[0])]

    def _novo(self):
        janela = CombustivelView(self)
        self.wait_window(janela)
        self.carregar_dados()

    def _editar(self):
        obj = self._selecionado()
        if not obj:
            return
        janela = CombustivelView(self, combustivel_obj=obj)
        self.wait_window(janela)
        self.carregar_dados()

    def _remover(self):
        obj = self._selecionado()
        if not obj:
            return
        if not messagebox.askyesno("Confirmar", f"Remover '{obj.tipo.value}'?", parent=self):
            return
        sucesso, msg = self.controller.remover(obj.combustivel_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)
