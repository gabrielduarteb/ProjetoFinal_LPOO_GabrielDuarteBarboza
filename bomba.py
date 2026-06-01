from .combustivel import Combustivel
from .ExcecoesPersonalizadas import ValorInvalidoError


class Bomba:
    def __init__(self, numero: int, combustivel: Combustivel, ativa: bool = True, bomba_id: int = None):
        self.__numero     = None
        self.__combustivel = None
        self.__ativa      = True

        self.bomba_id    = bomba_id
        self.numero      = numero
        self.combustivel = combustivel
        self.ativa       = ativa

    # ── numero ────────────────────────────────────────────────────────
    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, valor: int):
        if valor is None or valor <= 0:
            raise ValorInvalidoError("O numero da bomba deve ser maior que zero.")
        self.__numero = int(valor)

    # ── combustivel ───────────────────────────────────────────────────
    @property
    def combustivel(self):
        return self.__combustivel

    @combustivel.setter
    def combustivel(self, obj: Combustivel):
        if obj is None:
            raise ValueError("A bomba deve ter um combustivel associado.")
        self.__combustivel = obj

    # ── ativa ─────────────────────────────────────────────────────────
    @property
    def ativa(self):
        return self.__ativa

    @ativa.setter
    def ativa(self, valor: bool):
        self.__ativa = bool(valor)

    # ── metodos de negocio ────────────────────────────────────────────
    def esta_disponivel(self) -> bool:
        """Retorna True se a bomba esta ativa e tem estoque disponivel."""
        return self.__ativa and self.__combustivel.estoque_litros > 0

    def __str__(self):
        status = "Ativa" if self.__ativa else "Inativa"
        return (
            f"Bomba #{self.__numero}\n"
            f"Combustivel: {self.__combustivel.tipo.value}\n"
            f"Status: {status}"
        )
