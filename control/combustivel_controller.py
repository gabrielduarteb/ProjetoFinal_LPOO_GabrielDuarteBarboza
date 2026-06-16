from dao.combustivel_dao import CombustivelDAO
from model.combustivel import Combustivel, TipoCombustivel
from model.ExcecoesPersonalizadas import ValorInvalidoError


class CombustivelController:
    def __init__(self):
        self.dao = CombustivelDAO()

    def salvar(self, tipo_str: str, preco_str: str, estoque_str: str):
        if not tipo_str or not preco_str:
            return False, "Preencha todos os campos obrigatorios."
        try:
            tipo       = TipoCombustivel(tipo_str)
            preco      = float(preco_str.replace(",", "."))
            estoque    = float(estoque_str.replace(",", ".")) if estoque_str else 0.0

            if preco <= 0:
                return False, "O preco por litro deve ser maior que zero."
            if estoque < 0:
                return False, "O estoque nao pode ser negativo."

            # Verifica duplicidade
            existente = self.dao.buscar_por_tipo(tipo_str)
            if existente:
                return False, f"Combustivel '{tipo_str}' ja esta cadastrado."

            combustivel = Combustivel(tipo, preco, estoque)
            return self.dao.salvar(combustivel)
        except ValueError as e:
            return False, f"Valor invalido: {e}"
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def atualizar(self, combustivel_id: int, tipo_str: str, preco_str: str, estoque_str: str):
        if not tipo_str or not preco_str:
            return False, "Preencha todos os campos obrigatorios."
        try:
            tipo    = TipoCombustivel(tipo_str)
            preco   = float(preco_str.replace(",", "."))
            estoque = float(estoque_str.replace(",", ".")) if estoque_str else 0.0

            if preco <= 0:
                return False, "O preco por litro deve ser maior que zero."
            if estoque < 0:
                return False, "O estoque nao pode ser negativo."

            combustivel = Combustivel(tipo, preco, estoque)
            combustivel.combustivel_id = combustivel_id
            return self.dao.atualizar(combustivel)
        except ValueError as e:
            return False, f"Valor invalido: {e}"
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def remover(self, combustivel_id: int):
        try:
            return self.dao.remover(combustivel_id)
        except Exception as e:
            return False, f"Erro ao remover: {e}"

    def listar(self):
        try:
            return self.dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar combustiveis: {e}")
            return []

    def buscar_por_id(self, combustivel_id: int):
        try:
            return self.dao.buscar_por_id(combustivel_id)
        except Exception as e:
            print(f"Erro ao buscar combustivel: {e}")
            return None
