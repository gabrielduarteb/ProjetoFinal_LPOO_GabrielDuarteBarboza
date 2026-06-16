import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from model.abastecimento import Abastecimento, StatusAbastecimento
from model.AbastecimentoStrategy import PrecoCheioStrategy, DescontoFrotaStrategy, DescontoFidelidadeStrategy
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO
from dao.bomba_dao import BombaDAO


class AbastecimentoDAO(GenericDAO):
    def __init__(self):
        self.conexao  = DatabaseConfig.get_connection()
        self.bomba_dao = BombaDAO()

    def salvar(self, abastecimento: Abastecimento):
        if not self.conexao:
            raise Exception("Sem conexao com o BD")
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_abastecimentos
                    (abast_bomb_id, abast_litros, abast_valor, abast_modalidade, abast_data_hora, abast_status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING abast_id
            """
            cursor.execute(query, (
                abastecimento.bomba.bomba_id,
                abastecimento.litros,
                abastecimento.calcular_valor(),
                abastecimento.estrategia.descricao(),
                abastecimento.data_hora,
                abastecimento.status.value,
            ))
            abastecimento.abastecimento_id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Abastecimento registrado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao salvar abastecimento: {e}"
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
                SELECT abast_id, abast_bomb_id, abast_litros, abast_valor,
                       abast_modalidade, abast_data_hora, abast_status
                FROM tb_abastecimentos
                ORDER BY abast_id DESC
            """
            cursor.execute(query)
            return [self._montar(linha) for linha in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao listar abastecimentos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def listar_por_combustivel(self, comb_id: int):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                SELECT a.abast_id, a.abast_bomb_id, a.abast_litros, a.abast_valor,
                       a.abast_modalidade, a.abast_data_hora, a.abast_status
                FROM tb_abastecimentos a
                JOIN tb_bombas b ON b.bomb_id = a.abast_bomb_id
                WHERE b.bomb_comb_id = %s
                ORDER BY a.abast_id DESC
            """
            cursor.execute(query, (comb_id,))
            return [self._montar(linha) for linha in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao filtrar abastecimentos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def listar_por_data(self, data_inicio: datetime, data_fim: datetime):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                SELECT abast_id, abast_bomb_id, abast_litros, abast_valor,
                       abast_modalidade, abast_data_hora, abast_status
                FROM tb_abastecimentos
                WHERE abast_data_hora BETWEEN %s AND %s
                ORDER BY abast_id DESC
            """
            cursor.execute(query, (data_inicio, data_fim))
            return [self._montar(linha) for linha in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao filtrar abastecimentos por data: {e}")
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
            cursor.execute("DELETE FROM tb_abastecimentos WHERE abast_id = %s", (id_objeto,))
            self.conexao.commit()
            return True, "Abastecimento removido com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover abastecimento: {e}"
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, abastecimento: Abastecimento):
        if not self.conexao:
            raise Exception("Sem conexao com o BD")
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_abastecimentos
                SET abast_bomb_id   = %s,
                    abast_litros    = %s,
                    abast_valor     = %s,
                    abast_modalidade = %s,
                    abast_status    = %s
                WHERE abast_id = %s
            """
            cursor.execute(query, (
                abastecimento.bomba.bomba_id,
                abastecimento.litros,
                abastecimento.calcular_valor(),
                abastecimento.estrategia.descricao(),
                abastecimento.status.value,
                abastecimento.abastecimento_id,
            ))
            self.conexao.commit()
            return True, "Abastecimento atualizado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar abastecimento: {e}"
        finally:
            if cursor:
                cursor.close()

    def _montar(self, linha) -> Abastecimento:
        abast_id, bomb_id, litros, valor, modalidade, data_hora, status_str = linha

        bomba    = self.bomba_dao.buscar_por_id(bomb_id)
        status   = StatusAbastecimento(status_str)

        # Reconstroi a estrategia pelo nome salvo
        estrategias = {
            "Preco Cheio":              PrecoCheioStrategy(),
            "Desconto Frota (10%)":     DescontoFrotaStrategy(),
            "Desconto Fidelidade (5%)": DescontoFidelidadeStrategy(),
        }
        estrategia = estrategias.get(modalidade, PrecoCheioStrategy())

        a = Abastecimento(
            bomba=bomba,
            litros=float(litros),
            estrategia=estrategia,
            data_hora=data_hora,
            status=status,
            abastecimento_id=abast_id,
        )
        return a
