from dao.bomba_dao import BombaDAO
from dao.combustivel_dao import CombustivelDAO
from model.bomba import Bomba


class BombaController:
    def __init__(self):
        self.dao      = BombaDAO()
        self.comb_dao = CombustivelDAO()

    def salvar(self, numero_str: str, comb_id: int, ativa: bool = True):
        if not numero_str or not comb_id:
            return False, "Preencha todos os campos obrigatorios."
        try:
            numero = int(numero_str)
            if numero <= 0:
                return False, "O numero da bomba deve ser maior que zero."

            combustivel = self.comb_dao.buscar_por_id(comb_id)
            if not combustivel:
                return False, "Combustivel nao encontrado."

            bomba = Bomba(numero, combustivel, ativa)
            return self.dao.salvar(bomba)
        except ValueError as e:
            return False, f"Valor invalido: {e}"
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def atualizar(self, bomba_id: int, numero_str: str, comb_id: int, ativa: bool):
        if not numero_str or not comb_id:
            return False, "Preencha todos os campos obrigatorios."
        try:
            numero = int(numero_str)
            if numero <= 0:
                return False, "O numero da bomba deve ser maior que zero."

            combustivel = self.comb_dao.buscar_por_id(comb_id)
            if not combustivel:
                return False, "Combustivel nao encontrado."

            bomba = Bomba(numero, combustivel, ativa)
            bomba.bomba_id = bomba_id
            return self.dao.atualizar(bomba)
        except ValueError as e:
            return False, f"Valor invalido: {e}"
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def remover(self, bomba_id: int):
        try:
            return self.dao.remover(bomba_id)
        except Exception as e:
            return False, f"Erro ao remover: {e}"

    def listar(self):
        try:
            return self.dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar bombas: {e}")
            return []

    def buscar_por_id(self, bomba_id: int):
        try:
            return self.dao.buscar_por_id(bomba_id)
        except Exception as e:
            print(f"Erro ao buscar bomba: {e}")
            return None
