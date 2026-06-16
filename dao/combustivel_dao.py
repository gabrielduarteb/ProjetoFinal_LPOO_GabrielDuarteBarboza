import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.combustivel import Combustivel, TipoCombustivel
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO


class CombustivelDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, combustivel: Combustivel):
        if not self.conexao:
            raise Exception("Sem conexao com o BD")
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_combustiveis (comb_tipo, comb_preco, comb_estoque)
                VALUES (%s, %s, %s)
                RETURNING comb_id
            """
            cursor.execute(query, (
                combustivel.tipo.value,
                combustivel.preco_litro,
                combustivel.estoque_litros,
            ))
            combustivel.combustivel_id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Combustivel cadastrado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao salvar combustivel: {e}"
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT comb_id, comb_tipo, comb_preco, comb_estoque FROM tb_combustiveis ORDER BY comb_id")
            return [self._montar(linha) for linha in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao listar combustiveis: {e}")
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
            cursor.execute("DELETE FROM tb_combustiveis WHERE comb_id = %s", (id_objeto,))
            self.conexao.commit()
            return True, "Combustivel removido com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover combustivel: {e}"
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, combustivel: Combustivel):
        if not self.conexao:
            raise Exception("Sem conexao com o BD")
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_combustiveis
                SET comb_tipo    = %s,
                    comb_preco   = %s,
                    comb_estoque = %s
                WHERE comb_id = %s
            """
            cursor.execute(query, (
                combustivel.tipo.value,
                combustivel.preco_litro,
                combustivel.estoque_litros,
                combustivel.combustivel_id,
            ))
            self.conexao.commit()
            return True, "Combustivel atualizado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar combustivel: {e}"
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, comb_id: int):
        if not self.conexao:
            return None
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT comb_id, comb_tipo, comb_preco, comb_estoque FROM tb_combustiveis WHERE comb_id = %s",
                (comb_id,)
            )
            linha = cursor.fetchone()
            return self._montar(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar combustivel: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def buscar_por_tipo(self, tipo: str):
        if not self.conexao:
            return None
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT comb_id, comb_tipo, comb_preco, comb_estoque FROM tb_combustiveis WHERE comb_tipo = %s",
                (tipo,)
            )
            linha = cursor.fetchone()
            return self._montar(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar combustivel por tipo: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def _montar(self, linha) -> Combustivel:
        comb_id, tipo_str, preco, estoque = linha
        tipo = TipoCombustivel(tipo_str)
        c = Combustivel(tipo, float(preco), float(estoque))
        c.combustivel_id = comb_id
        return c
