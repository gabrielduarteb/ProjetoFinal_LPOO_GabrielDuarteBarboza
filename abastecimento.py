from datetime import datetime
from enum import Enum
from .bomba import Bomba
from .AbastecimentoStrategy import AbastecimentoStrategy, PrecoCheioStrategy
from .ExcecoesPersonalizadas import ValorInvalidoError, EstoqueInsuficienteError


class StatusAbastecimento(Enum):
    PENDENTE   = "pendente"
    CONCLUIDO  = "concluido"
    CANCELADO  = "cancelado"


class Abastecimento:
    def __init__(
        self,
        bomba: Bomba,
        litros: float,
        estrategia: AbastecimentoStrategy = None,
        data_hora: datetime = None,
        status: StatusAbastecimento = StatusAbastecimento.PENDENTE,
        abastecimento_id: int = None,
    ):
        self.__bomba   = None
        self.__litros  = 0.0

        if estrategia is None:
            estrategia = PrecoCheioStrategy()
        if data_hora is None:
            data_hora = datetime.now()

        self.abastecimento_id = abastecimento_id
        self.bomba            = bomba
        self.litros           = litros
        self.estrategia       = estrategia
        self.data_hora        = data_hora
        self.status           = status

    # ── bomba ─────────────────────────────────────────────────────────
    @property
    def bomba(self):
        return self.__bomba

    @bomba.setter
    def bomba(self, obj: Bomba):
        if obj is None:
            raise ValueError("A bomba e obrigatoria.")
        self.__bomba = obj

    # ── litros ────────────────────────────────────────────────────────
    @property
    def litros(self):
        return self.__litros

    @litros.setter
    def litros(self, valor: float):
        if valor is None or valor <= 0:
            raise ValorInvalidoError("A quantidade de litros deve ser maior que zero.")
        self.__litros = float(valor)

    # ── calcular valor ────────────────────────────────────────────────
    def calcular_valor(self) -> float:
        """Calcula o valor total usando a estrategia configurada."""
        return self.estrategia.calcular(self.__bomba.combustivel.preco_litro, self.__litros)

    # ── concluir abastecimento ────────────────────────────────────────
    def concluir(self):
        """Confirma o abastecimento, retirando do estoque do combustivel."""
        if self.status != StatusAbastecimento.PENDENTE:
            raise ValueError("Apenas abastecimentos pendentes podem ser concluidos.")
        if self.__litros > self.__bomba.combustivel.estoque_litros:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente. Disponivel: {self.__bomba.combustivel.estoque_litros:.2f}L"
            )
        self.__bomba.combustivel.retirar_estoque(self.__litros)
        self.status = StatusAbastecimento.CONCLUIDO

    # ── cancelar abastecimento ────────────────────────────────────────
    def cancelar(self):
        """Cancela o abastecimento."""
        if self.status != StatusAbastecimento.PENDENTE:
            raise ValueError("Apenas abastecimentos pendentes podem ser cancelados.")
        self.status = StatusAbastecimento.CANCELADO

    def __str__(self):
        return (
            f"Abastecimento #{self.abastecimento_id}\n"
            f"Bomba:       #{self.__bomba.numero}\n"
            f"Combustivel: {self.__bomba.combustivel.tipo.value}\n"
            f"Litros:      {self.__litros:.2f} L\n"
            f"Valor:       R$ {self.calcular_valor():.2f}\n"
            f"Modalidade:  {self.estrategia.descricao()}\n"
            f"Data/Hora:   {self.data_hora.strftime('%d/%m/%Y %H:%M')}\n"
            f"Status:      {self.status.value}"
        )
