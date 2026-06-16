from .combustivel import Combustivel, TipoCombustivel
from .bomba import Bomba
from .abastecimento import Abastecimento, StatusAbastecimento
from .AbastecimentoStrategy import (
    AbastecimentoStrategy,
    PrecoCheioStrategy,
    DescontoFrotaStrategy,
    DescontoFidelidadeStrategy,
)
from .ExcecoesPersonalizadas import (
    CombustivelInvalidoError,
    EstoqueInsuficienteError,
    ValorInvalidoError,
)