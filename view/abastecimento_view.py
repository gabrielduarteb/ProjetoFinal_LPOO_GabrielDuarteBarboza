import tkinter as tk
from tkinter import ttk, messagebox
from control.abastecimento_controller import AbastecimentoController
from control.bomba_controller import BombaController


class AbastecimentoView(tk.Toplevel):
    """Formulario para registrar um novo abastecimento."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Abastecimento")
        self.resizable(False, False)
        self.grab_set()

        self.controller      = AbastecimentoController()
        self.bomba_controller = BombaController()
        self._bombas         = self.bomba_controller.listar()

        self._construir_tela()

    def _construir_tela(self):
        tk.Label(self, text="Registrar Abastecimento", font=("Arial", 13, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        # Bomba
        tk.Label(self, text="Bomba:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self._var_bomba = tk.StringVar()
        opcoes = [f"#{b.numero} - {b.combustivel.tipo.value} ({b.combustivel.estoque_litros:.0f}L disp.)"
                  for b in self._bombas if b.ativa]
        self._bombas_ativas = [b for b in self._bombas if b.ativa]
        self._combo_bomba = ttk.Combobox(
            self, textvariable=self._var_bomba,
            values=opcoes, state="readonly", width=35,
        )
        self._combo_bomba.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        if opcoes:
            self._combo_bomba.current(0)

        # Litros
        tk.Label(self, text="Litros:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self._entry_litros = tk.Entry(self, width=27)
        self._entry_litros.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Modalidade
        tk.Label(self, text="Modalidade:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self._var_modalidade = tk.StringVar()
        modalidades = self.controller.modalidades()
        self._combo_modalidade = ttk.Combobox(
            self, textvariable=self._var_modalidade,
            values=modalidades, state="readonly", width=35,
        )
        self._combo_modalidade.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self._combo_modalidade.current(0)

        # Valor estimado
        tk.Label(self, text="Valor Estimado:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self._lbl_valor = tk.Label(self, text="R$ 0.00", font=("Arial", 11, "bold"))
        self._lbl_valor.grid(row=4, column=1, sticky="w", padx=10)

        # Binds para calcular valor em tempo real
        self._entry_litros.bind("<KeyRelease>", self._calcular_valor)
        self._combo_bomba.bind("<<ComboboxSelected>>", self._calcular_valor)
        self._combo_modalidade.bind("<<ComboboxSelected>>", self._calcular_valor)

        tk.Button(self, text="Confirmar Abastecimento", width=25, command=self._salvar).grid(
            row=5, column=0, columnspan=2, pady=15
        )

    def _calcular_valor(self, event=None):
        try:
            sel = self._combo_bomba.current()
            if sel < 0 or not self._bombas_ativas:
                return
            bomba    = self._bombas_ativas[sel]
            litros   = float(self._entry_litros.get().replace(",", "."))
            from model.AbastecimentoStrategy import PrecoCheioStrategy, DescontoFrotaStrategy, DescontoFidelidadeStrategy
            estrategias = {
                "Preco Cheio":              PrecoCheioStrategy(),
                "Desconto Frota (10%)":     DescontoFrotaStrategy(),
                "Desconto Fidelidade (5%)": DescontoFidelidadeStrategy(),
            }
            estrategia = estrategias.get(self._var_modalidade.get(), PrecoCheioStrategy())
            valor = estrategia.calcular(bomba.combustivel.preco_litro, litros)
            self._lbl_valor.config(text=f"R$ {valor:.2f}")
        except (ValueError, ZeroDivisionError):
            self._lbl_valor.config(text="R$ 0.00")

    def _salvar(self):
        sel = self._combo_bomba.current()
        if sel < 0 or not self._bombas_ativas:
            messagebox.showwarning("Aviso", "Selecione uma bomba.", parent=self)
            return

        bomba_id     = self._bombas_ativas[sel].bomba_id
        litros_str   = self._entry_litros.get().strip()
        modalidade   = self._var_modalidade.get()

        sucesso, msg = self.controller.registrar(bomba_id, litros_str, modalidade)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
