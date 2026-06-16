import tkinter as tk
from tkinter import ttk, messagebox
from control.bomba_controller import BombaController
from view.bomba_view import BombaView


class BombaListView(tk.Toplevel):
    """Tela de listagem e CRUD de bombas."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bombas")
        self.geometry("680x420")

        self.controller = BombaController()
        self._construir_tela()
        self.carregar_dados()

    def _construir_tela(self):
        tk.Label(self, text="Bombas Cadastradas", font=("Arial", 14, "bold")).pack(pady=8)

        colunas = ("id", "numero", "combustivel", "estoque", "status")
        self._tree = ttk.Treeview(self, columns=colunas, show="headings", height=12)
        self._tree.heading("id",          text="ID")
        self._tree.heading("numero",      text="Numero")
        self._tree.heading("combustivel", text="Combustivel")
        self._tree.heading("estoque",     text="Estoque (L)")
        self._tree.heading("status",      text="Status")
        self._tree.column("id",          width=40,  anchor="center")
        self._tree.column("numero",      width=80,  anchor="center")
        self._tree.column("combustivel", width=200, anchor="center")
        self._tree.column("estoque",     width=120, anchor="center")
        self._tree.column("status",      width=100, anchor="center")
        self._tree.pack(padx=10, pady=5)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)
        tk.Button(frame_botoes, text="Nova",    width=14, command=self._novo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Editar",  width=14, command=self._editar).grid(row=0, column=1, padx=5)
        tk.Button(frame_botoes, text="Remover", width=14, command=self._remover).grid(row=0, column=2, padx=5)

    def carregar_dados(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._bombas = self.controller.listar()
        for b in self._bombas:
            self._tree.insert("", "end", values=(
                b.bomba_id,
                f"#{b.numero}",
                b.combustivel.tipo.value,
                f"{b.combustivel.estoque_litros:.2f}",
                "Ativa" if b.ativa else "Inativa",
            ))

    def _selecionado(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma bomba.", parent=self)
            return None
        return self._bombas[self._tree.index(sel[0])]

    def _novo(self):
        janela = BombaView(self)
        self.wait_window(janela)
        self.carregar_dados()

    def _editar(self):
        obj = self._selecionado()
        if not obj:
            return
        janela = BombaView(self, bomba_obj=obj)
        self.wait_window(janela)
        self.carregar_dados()

    def _remover(self):
        obj = self._selecionado()
        if not obj:
            return
        if not messagebox.askyesno("Confirmar", f"Remover Bomba #{obj.numero}?", parent=self):
            return
        sucesso, msg = self.controller.remover(obj.bomba_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)
