from enum import Enum
from .ExcecoesPersonalizadas import ValorInvalidoError, EstoqueInsuficienteError


class TipoCombustivel(Enum):
    GASOLINA_COMUM  = "Gasolina Comum"
    GASOLINA_ADITIVADA = "Gasolina Aditivada"
    ETANOL          = "Etanol"
    DIESEL          = "Diesel"
    DIESEL_S10      = "Diesel S10"
    GNV             = "GNV"


class Combustivel:
    def __init__(self, tipo: TipoCombustivel, preco_litro: float, estoque_litros: float = 0.0, combustivel_id: int = None):
        self.__tipo = None
        self.__preco_litro = 0.0
        self.__estoque_litros = 0.0

        self.combustivel_id  = combustivel_id
        self.tipo            = tipo
        self.preco_litro     = preco_litro
        self.estoque_litros  = estoque_litros

    # ── tipo ──────────────────────────────────────────────────────────
    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: TipoCombustivel):
        if not isinstance(tipo, TipoCombustivel):
            raise CombustivelInvalidoError(f"Tipo de combustivel invalido: {tipo}")
        self.__tipo = tipo

    # ── preco_litro ───────────────────────────────────────────────────
    @property
    def preco_litro(self):
        return self.__preco_litro

    @preco_litro.setter
    def preco_litro(self, valor: float):
        if valor is None or valor <= 0:
            raise ValorInvalidoError("O preco por litro deve ser maior que zero.")
        self.__preco_litro = float(valor)

    # ── estoque_litros ────────────────────────────────────────────────
    @property
    def estoque_litros(self):
        return self.__estoque_litros

    @estoque_litros.setter
    def estoque_litros(self, valor: float):
        if valor is None or valor < 0:
            raise ValorInvalidoError("O estoque nao pode ser negativo.")
        self.__estoque_litros = float(valor)

    # ── metodos de negocio ────────────────────────────────────────────
    def abastecer_estoque(self, litros: float):
        """Adiciona litros ao estoque (reabastecimento do tanque)."""
        if litros <= 0:
            raise ValorInvalidoError("A quantidade de litros deve ser maior que zero.")
        self.__estoque_litros += litros

    def retirar_estoque(self, litros: float):
        """Retira litros do estoque (consumo no abastecimento)."""
        if litros <= 0:
            raise ValorInvalidoError("A quantidade de litros deve ser maior que zero.")
        if litros > self.__estoque_litros:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente. Disponivel: {self.__estoque_litros:.2f}L, Solicitado: {litros:.2f}L"
            )
        self.__estoque_litros -= litros

    def calcular_valor(self, litros: float) -> float:
        """Calcula o valor total para uma quantidade de litros."""
        if litros <= 0:
            raise ValorInvalidoError("A quantidade de litros deve ser maior que zero.")
        return round(self.__preco_litro * litros, 2)

    def __str__(self):
        return (
            f"Combustivel: {self.__tipo.value}\n"
            f"Preco/Litro: R$ {self.__preco_litro:.2f}\n"
            f"Estoque:     {self.__estoque_litros:.2f} L"
        )
