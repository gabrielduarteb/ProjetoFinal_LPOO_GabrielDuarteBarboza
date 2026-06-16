from datetime import datetime
from dao.abastecimento_dao import AbastecimentoDAO
from dao.bomba_dao import BombaDAO
from model.abastecimento import Abastecimento, StatusAbastecimento
from model.AbastecimentoStrategy import PrecoCheioStrategy, DescontoFrotaStrategy, DescontoFidelidadeStrategy
from model.ExcecoesPersonalizadas import EstoqueInsuficienteError, ValorInvalidoError


ESTRATEGIAS = {
    "Preco Cheio":              PrecoCheioStrategy(),
    "Desconto Frota (10%)":     DescontoFrotaStrategy(),
    "Desconto Fidelidade (5%)": DescontoFidelidadeStrategy(),
}


class AbastecimentoController:
    def __init__(self):
        self.dao      = AbastecimentoDAO()
        self.bomba_dao = BombaDAO()

    def registrar(self, bomba_id: int, litros_str: str, modalidade_str: str):
        if not bomba_id or not litros_str or not modalidade_str:
            return False, "Preencha todos os campos obrigatorios."
        try:
            litros = float(litros_str.replace(",", "."))
            if litros <= 0:
                return False, "A quantidade de litros deve ser maior que zero."

            bomba = self.bomba_dao.buscar_por_id(bomba_id)
            if not bomba:
                return False, "Bomba nao encontrada."
            if not bomba.ativa:
                return False, "Esta bomba esta inativa."
            if bomba.combustivel.estoque_litros < litros:
                return False, f"Estoque insuficiente. Disponivel: {bomba.combustivel.estoque_litros:.2f}L"

            estrategia = ESTRATEGIAS.get(modalidade_str, PrecoCheioStrategy())

            abastecimento = Abastecimento(
                bomba=bomba,
                litros=litros,
                estrategia=estrategia,
                status=StatusAbastecimento.CONCLUIDO,
            )

            # Retira do estoque
            bomba.combustivel.retirar_estoque(litros)

            # Salva no banco
            sucesso, msg = self.dao.salvar(abastecimento)
            if sucesso:
                # Atualiza estoque no banco
                from dao.combustivel_dao import CombustivelDAO
                CombustivelDAO().atualizar(bomba.combustivel)

            return sucesso, msg

        except EstoqueInsuficienteError as e:
            return False, str(e)
        except ValorInvalidoError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao registrar abastecimento: {e}"

    def listar(self):
        try:
            return self.dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar abastecimentos: {e}")
            return []

    def listar_por_combustivel(self, comb_id: int):
        try:
            return self.dao.listar_por_combustivel(comb_id)
        except Exception as e:
            print(f"Erro ao filtrar abastecimentos: {e}")
            return []

    def listar_por_data(self, data_inicio: datetime, data_fim: datetime):
        try:
            return self.dao.listar_por_data(data_inicio, data_fim)
        except Exception as e:
            print(f"Erro ao filtrar por data: {e}")
            return []

    def remover(self, abastecimento_id: int):
        try:
            return self.dao.remover(abastecimento_id)
        except Exception as e:
            return False, f"Erro ao remover: {e}"

    def modalidades(self):
        return list(ESTRATEGIAS.keys())
