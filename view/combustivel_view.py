import tkinter as tk
from tkinter import ttk, messagebox
from model.combustivel import TipoCombustivel
from control.combustivel_controller import CombustivelController


class CombustivelView(tk.Toplevel):
    """Formulario de cadastro e edicao de combustivel."""

    TIPOS = [t.value for t in TipoCombustivel]

    def __init__(self, parent, combustivel_obj=None):
        super().__init__(parent)
        self.resizable(False, False)
        self.grab_set()

        self.controller    = CombustivelController()
        self._comb_obj     = combustivel_obj
        self._modo_edicao  = combustivel_obj is not None

        self.title("Editar Combustivel" if self._modo_edicao else "Novo Combustivel")
        self._construir_tela()

        if self._modo_edicao:
            self._preencher_campos()

    def _construir_tela(self):
        titulo = "Editar Combustivel" if self._modo_edicao else "Novo Combustivel"
        tk.Label(self, text=titulo, font=("Arial", 13, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        tk.Label(self, text="Tipo:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self._var_tipo = tk.StringVar(value=self.TIPOS[0])
        ttk.Combobox(
            self, textvariable=self._var_tipo,
            values=self.TIPOS, state="readonly", width=25,
        ).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self, text="Preco por Litro (R$):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self._entry_preco = tk.Entry(self, width=27)
        self._entry_preco.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Estoque (Litros):").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self._entry_estoque = tk.Entry(self, width=27)
        self._entry_estoque.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self, text="Salvar", width=15, command=self._salvar).grid(
            row=4, column=0, columnspan=2, pady=15
        )

    def _preencher_campos(self):
        self._var_tipo.set(self._comb_obj.tipo.value)
        self._entry_preco.insert(0, str(self._comb_obj.preco_litro))
        self._entry_estoque.insert(0, str(self._comb_obj.estoque_litros))

    def _salvar(self):
        tipo_str    = self._var_tipo.get()
        preco_str   = self._entry_preco.get().strip()
        estoque_str = self._entry_estoque.get().strip()

        if self._modo_edicao:
            sucesso, msg = self.controller.atualizar(
                self._comb_obj.combustivel_id, tipo_str, preco_str, estoque_str
            )
        else:
            sucesso, msg = self.controller.salvar(tipo_str, preco_str, estoque_str)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
