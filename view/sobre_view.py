import tkinter as tk


class SobreView(tk.Toplevel):
    """Tela Sobre — informacoes do sistema e do autor."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sobre")
        self.resizable(False, False)
        self.grab_set()
        self._construir_tela()

    def _construir_tela(self):
        tk.Label(self, text="Sistema de Posto de Combustivel",
                 font=("Arial", 14, "bold")).pack(pady=(20, 5))

        tk.Label(self, text="Versao 1.0", font=("Arial", 10), fg="gray").pack()

        tk.Label(self, text=(
            "\nGerenciamento de combustiveis, bombas e abastecimentos\n"
            "com controle de estoque e multiplas modalidades de preco.\n"
        ), font=("Arial", 10), justify="center").pack(padx=20)

        tk.Label(self, text="Padroes de Projeto Utilizados:",
                 font=("Arial", 10, "bold")).pack(pady=(10, 2))
        tk.Label(self, text="DAO — isolamento do acesso ao banco de dados",
                 font=("Arial", 10)).pack()
        tk.Label(self, text="Strategy — calculo do valor do abastecimento",
                 font=("Arial", 10)).pack()

        tk.Frame(self, height=1, bg="gray").pack(fill="x", padx=20, pady=15)

        tk.Label(self, text="Autor: Gabriel Duarte Barboza",
                 font=("Arial", 10, "bold")).pack()
        tk.Label(self, text="Disciplina: Linguagem de Programacao Orientada a Objetos (LPOO)",
                 font=("Arial", 9), fg="gray").pack()
        tk.Label(self, text="Professora: Vanessa Lago Machado",
                 font=("Arial", 9), fg="gray").pack()
        tk.Label(self, text="Bacharelado em Ciencia da Computacao — IFSul 2026/1",
                 font=("Arial", 9), fg="gray").pack(pady=(0, 5))

        tk.Button(self, text="Fechar", width=12, command=self.destroy).pack(pady=15)
