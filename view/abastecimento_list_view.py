import tkinter as tk
from tkinter import ttk, messagebox
from control.abastecimento_controller import AbastecimentoController
from control.combustivel_controller import CombustivelController
from view.abastecimento_view import AbastecimentoView


class AbastecimentoListView(tk.Toplevel):
    """Tela de listagem de abastecimentos com filtro por combustivel."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Abastecimentos")
        self.geometry("860x480")

        self.controller      = AbastecimentoController()
        self.comb_controller = CombustivelController()
        self._construir_tela()
        self.carregar_dados()

    def _construir_tela(self):
        tk.Label(self, text="Abastecimentos", font=("Arial", 14, "bold")).pack(pady=8)

        # Filtro por combustivel
        frame_filtro = tk.Frame(self)
        frame_filtro.pack(padx=10, pady=4, fill="x")

        tk.Label(frame_filtro, text="Filtrar por Combustivel:").pack(side="left", padx=5)
        self._combustiveis = self.comb_controller.listar()
        opcoes = ["Todos"] + [c.tipo.value for c in self._combustiveis]
        self._var_filtro = tk.StringVar(value="Todos")
        ttk.Combobox(
            frame_filtro, textvariable=self._var_filtro,
            values=opcoes, state="readonly", width=25,
        ).pack(side="left", padx=5)
        tk.Button(frame_filtro, text="Filtrar", command=self._filtrar).pack(side="left", padx=5)
        tk.Button(frame_filtro, text="Limpar",  command=self.carregar_dados).pack(side="left", padx=5)

        # Tabela
        colunas = ("id", "bomba", "combustivel", "litros", "valor", "modalidade", "data_hora", "status")
        self._tree = ttk.Treeview(self, columns=colunas, show="headings", height=13)

        cabecalhos = {
            "id":          ("ID",         40),
            "bomba":       ("Bomba",      70),
            "combustivel": ("Combustivel",160),
            "litros":      ("Litros",     80),
            "valor":       ("Valor",      90),
            "modalidade":  ("Modalidade", 170),
            "data_hora":   ("Data/Hora",  130),
            "status":      ("Status",     80),
        }
        for col, (titulo, larg) in cabecalhos.items():
            self._tree.heading(col, text=titulo)
            self._tree.column(col, width=larg, anchor="center")
        self._tree.pack(padx=10, pady=5, fill="both", expand=True)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=8)
        tk.Button(frame_botoes, text="Novo Abastecimento", width=18, command=self._novo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Remover",            width=14, command=self._remover).grid(row=0, column=1, padx=5)

    def carregar_dados(self):
        self._var_filtro.set("Todos")
        self._abastecimentos = self.controller.listar()
        self._preencher_tabela(self._abastecimentos)

    def _filtrar(self):
        filtro = self._var_filtro.get()
        if filtro == "Todos":
            self.carregar_dados()
            return
        comb = next((c for c in self._combustiveis if c.tipo.value == filtro), None)
        if comb:
            self._abastecimentos = self.controller.listar_por_combustivel(comb.combustivel_id)
            self._preencher_tabela(self._abastecimentos)

    def _preencher_tabela(self, lista):
        for item in self._tree.get_children():
            self._tree.delete(item)
        for a in lista:
            self._tree.insert("", "end", values=(
                a.abastecimento_id,
                f"#{a.bomba.numero}",
                a.bomba.combustivel.tipo.value,
                f"{a.litros:.2f}L",
                f"R$ {a.calcular_valor():.2f}",
                a.estrategia.descricao(),
                a.data_hora.strftime("%d/%m/%Y %H:%M"),
                a.status.value,
            ))

    def _selecionado(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um abastecimento.", parent=self)
            return None
        return self._abastecimentos[self._tree.index(sel[0])]

    def _novo(self):
        janela = AbastecimentoView(self)
        self.wait_window(janela)
        self.carregar_dados()

    def _remover(self):
        obj = self._selecionado()
        if not obj:
            return
        if not messagebox.askyesno("Confirmar", f"Remover abastecimento #{obj.abastecimento_id}?", parent=self):
            return
        sucesso, msg = self.controller.remover(obj.abastecimento_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.carregar_dados()
        else:
            messagebox.showerror("Erro", msg, parent=self)
