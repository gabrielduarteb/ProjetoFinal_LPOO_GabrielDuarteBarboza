import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
from view.combustivel_list_view import CombustivelListView
from view.bomba_list_view import BombaListView
from view.abastecimento_list_view import AbastecimentoListView
from view.sobre_view import SobreView


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Posto de Combustivel")
        self.geometry("480x280")
        self.resizable(False, False)
        self._construir_menu()
        self._construir_tela()

    def _construir_menu(self):
        menubar = tk.Menu(self)

        # Menu Cadastro
        menu_cadastro = tk.Menu(menubar, tearoff=0)
        menu_cadastro.add_command(label="Combustiveis", command=self._abrir_combustiveis)
        menu_cadastro.add_command(label="Bombas",       command=self._abrir_bombas)
        menubar.add_cascade(label="Cadastro", menu=menu_cadastro)

        # Menu Operacoes
        menu_op = tk.Menu(menubar, tearoff=0)
        menu_op.add_command(label="Abastecimentos", command=self._abrir_abastecimentos)
        menubar.add_cascade(label="Operacoes", menu=menu_op)

        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=self._abrir_sobre)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.config(menu=menubar)

    def _construir_tela(self):
        tk.Label(self, text="Posto de Combustivel",
                 font=("Arial", 18, "bold")).pack(expand=True)
        tk.Label(self, text="Use o menu acima para navegar pelo sistema.",
                 font=("Arial", 10), fg="gray").pack()
        tk.Label(self, text="Gabriel Duarte Barboza — LPOO 2026/1",
                 font=("Arial", 9), fg="gray").pack(pady=(0, 20))

    def _abrir_combustiveis(self):
        CombustivelListView(self)

    def _abrir_bombas(self):
        BombaListView(self)

    def _abrir_abastecimentos(self):
        AbastecimentoListView(self)

    def _abrir_sobre(self):
        SobreView(self)


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()
