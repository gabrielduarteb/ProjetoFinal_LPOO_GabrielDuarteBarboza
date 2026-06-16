import tkinter as tk
from tkinter import ttk, messagebox
from control.bomba_controller import BombaController
from control.combustivel_controller import CombustivelController


class BombaView(tk.Toplevel):
    """Formulario de cadastro e edicao de bomba."""

    def __init__(self, parent, bomba_obj=None):
        super().__init__(parent)
        self.resizable(False, False)
        self.grab_set()

        self.controller      = BombaController()
        self.comb_controller = CombustivelController()
        self._bomba_obj      = bomba_obj
        self._modo_edicao    = bomba_obj is not None
        self._combustiveis   = self.comb_controller.listar()

        self.title("Editar Bomba" if self._modo_edicao else "Nova Bomba")
        self._construir_tela()

        if self._modo_edicao:
            self._preencher_campos()

    def _construir_tela(self):
        titulo = "Editar Bomba" if self._modo_edicao else "Nova Bomba"
        tk.Label(self, text=titulo, font=("Arial", 13, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        tk.Label(self, text="Numero da Bomba:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self._entry_numero = tk.Entry(self, width=27)
        self._entry_numero.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Combustivel:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self._var_comb = tk.StringVar()
        opcoes = [f"{c.combustivel_id} - {c.tipo.value}" for c in self._combustiveis]
        self._combo_comb = ttk.Combobox(
            self, textvariable=self._var_comb,
            values=opcoes, state="readonly", width=25,
        )
        self._combo_comb.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        if opcoes:
            self._combo_comb.current(0)

        tk.Label(self, text="Status:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self._var_ativa = tk.BooleanVar(value=True)
        frame_status = tk.Frame(self)
        frame_status.grid(row=3, column=1, sticky="w", padx=10)
        tk.Radiobutton(frame_status, text="Ativa",   variable=self._var_ativa, value=True).pack(side="left")
        tk.Radiobutton(frame_status, text="Inativa", variable=self._var_ativa, value=False).pack(side="left")

        tk.Button(self, text="Salvar", width=15, command=self._salvar).grid(
            row=4, column=0, columnspan=2, pady=15
        )

    def _preencher_campos(self):
        self._entry_numero.insert(0, str(self._bomba_obj.numero))
        for i, c in enumerate(self._combustiveis):
            if c.combustivel_id == self._bomba_obj.combustivel.combustivel_id:
                self._combo_comb.current(i)
                break
        self._var_ativa.set(self._bomba_obj.ativa)

    def _salvar(self):
        numero_str = self._entry_numero.get().strip()
        ativa      = self._var_ativa.get()

        sel = self._combo_comb.current()
        if sel < 0 or not self._combustiveis:
            messagebox.showwarning("Aviso", "Selecione um combustivel.", parent=self)
            return
        comb_id = self._combustiveis[sel].combustivel_id

        if self._modo_edicao:
            sucesso, msg = self.controller.atualizar(
                self._bomba_obj.bomba_id, numero_str, comb_id, ativa
            )
        else:
            sucesso, msg = self.controller.salvar(numero_str, comb_id, ativa)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
