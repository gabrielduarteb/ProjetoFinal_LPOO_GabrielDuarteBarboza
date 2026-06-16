from abc import ABC, abstractmethod


class AbastecimentoStrategy(ABC):
    """Strategy base para calculo do valor do abastecimento."""

    @abstractmethod
    def calcular(self, preco_litro: float, litros: float) -> float:
        pass

    @abstractmethod
    def descricao(self) -> str:
        pass


class PrecoCheioStrategy(AbastecimentoStrategy):
    """Cliente comum — paga o preco cheio."""

    def calcular(self, preco_litro: float, litros: float) -> float:
        return round(preco_litro * litros, 2)

    def descricao(self) -> str:
        return "Preco Cheio"


class DescontoFrotaStrategy(AbastecimentoStrategy):
    """Cliente frota — 10% de desconto no preco por litro."""

    DESCONTO = 0.10

    def calcular(self, preco_litro: float, litros: float) -> float:
        preco_com_desconto = preco_litro * (1 - self.DESCONTO)
        return round(preco_com_desconto * litros, 2)

    def descricao(self) -> str:
        return "Desconto Frota (10%)"


class DescontoFidelidadeStrategy(AbastecimentoStrategy):
    """Cliente fidelidade — 5% de desconto no preco por litro."""

    DESCONTO = 0.05

    def calcular(self, preco_litro: float, litros: float) -> float:
        preco_com_desconto = preco_litro * (1 - self.DESCONTO)
        return round(preco_com_desconto * litros, 2)

    def descricao(self) -> str:
        return "Desconto Fidelidade (5%)"
