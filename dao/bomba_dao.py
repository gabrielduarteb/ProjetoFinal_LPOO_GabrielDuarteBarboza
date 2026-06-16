import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.bomba import Bomba
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from dao.combustivel_dao import CombustivelDAO


class BombaDAO(GenericDAO):
    def __init__(self):
        self.conexao      = DatabaseConfig.get_connection()
        self.comb_dao     = CombustivelDAO()

    def salvar(self, bomba: Bomba):
        if not self.conexao:
            raise Exception("Sem conexao com o BD")
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_bombas (bomb_numero, bomb_comb_id, bomb_ativa)
                VALUES (%s, %s, %s)
                RETURNING bomb_id
            """
            cursor.execute(query, (
                bomba.numero,
                bomba.combustivel.combustivel_id,
                bomba.ativa,
            ))
            bomba.bomba_id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Bomba cadastrada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao salvar bomba: {e}"
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                SELECT b.bomb_id, b.bomb_numero, b.bomb_comb_id, b.bomb_ativa
                FROM tb_bombas b
                ORDER BY b.bomb_numero
            """
            cursor.execute(query)
            bombas = []
            for linha in cursor.fetchall():
                bombas.append(self._montar(linha))
            return bombas
        except Exception as e:
            print(f"Erro ao listar bombas: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_objeto: int):
        if not self.conexao:
            raise Exception("Sem conexao com o BD")
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM tb_bombas WHERE bomb_id = %s", (id_objeto,))
            self.conexao.commit()
            return True, "Bomba removida com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover bomba: {e}"
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, bomba: Bomba):
        if not self.conexao:
            raise Exception("Sem conexao com o BD")
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_bombas
                SET bomb_numero  = %s,
                    bomb_comb_id = %s,
                    bomb_ativa   = %s
                WHERE bomb_id = %s
            """
            cursor.execute(query, (
                bomba.numero,
                bomba.combustivel.combustivel_id,
                bomba.ativa,
                bomba.bomba_id,
            ))
            self.conexao.commit()
            return True, "Bomba atualizada com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar bomba: {e}"
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, bomba_id: int):
        if not self.conexao:
            return None
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT bomb_id, bomb_numero, bomb_comb_id, bomb_ativa FROM tb_bombas WHERE bomb_id = %s",
                (bomba_id,)
            )
            linha = cursor.fetchone()
            return self._montar(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar bomba: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def _montar(self, linha) -> Bomba:
        bomb_id, numero, comb_id, ativa = linha
        combustivel = self.comb_dao.buscar_por_id(comb_id)
        b = Bomba(numero, combustivel, bool(ativa))
        b.bomba_id = bomb_id
        return b
