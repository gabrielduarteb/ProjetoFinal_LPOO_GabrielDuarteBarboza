# Sistema de Posto de Combustível

Sistema desktop de gerenciamento de posto de combustível, desenvolvido em Python com Tkinter e PostgreSQL, seguindo a arquitetura MVC (Model-View-Controller).

## Descrição Geral

O sistema permite gerenciar os combustíveis disponíveis no posto, as bombas de abastecimento e os registros de abastecimentos realizados. O controle de estoque é atualizado automaticamente a cada abastecimento concluído, e o cálculo do valor cobrado varia conforme a modalidade escolhida (preço cheio, desconto frota ou desconto fidelidade).

## Funcionalidades

- Cadastro, edição e remoção de combustíveis (tipo, preço por litro e estoque)
- Cadastro, edição e remoção de bombas (número, combustível associado e status)
- Registro de abastecimentos com cálculo automático de valor em tempo real
- Listagem de abastecimentos com filtro por combustível
- Controle automático de estoque ao concluir um abastecimento
- Validações em todos os formulários (campos obrigatórios, valores numéricos, estoque disponível)
- Menu de navegação entre todas as telas do sistema
- Tela Sobre com informações do sistema e do autor

## Tecnologias

- Python 3.13
- Tkinter (interface gráfica)
- PostgreSQL 18 (banco de dados)
- psycopg 3 (driver de conexão)

## Como Executar

### 1. Instalar dependência

```bash
python -m pip install psycopg[binary]
```

### 2. Criar o banco de dados no pgAdmin

```sql
CREATE DATABASE lpoo_projeto_gabrielduarte;
```

### 3. Criar as tabelas

Execute o script `create_tables.sql` no Query Tool do pgAdmin, conectado ao banco `lpoo_projeto_gabrielduarte`.

### 4. Executar o sistema

```bash
python main.py
```

## Estrutura do Projeto

```
ProjetoFinal_LPOO_GabrielDuarteBarboza/
├── main.py                             # Janela principal com menu
├── create_tables.sql                   # Script de criação das tabelas
├── model/
│   ├── combustivel.py                  # Combustivel, TipoCombustivel
│   ├── bomba.py                        # Bomba
│   ├── abastecimento.py                # Abastecimento, StatusAbastecimento
│   ├── AbastecimentoStrategy.py        # Padrão Strategy
│   └── ExcecoesPersonalizadas.py       # Exceções do sistema
├── dao/
│   ├── db_config.py                    # Conexão com PostgreSQL
│   ├── generic_dao.py                  # Classe base abstrata DAO
│   ├── combustivel_dao.py              # CRUD de combustíveis
│   ├── bomba_dao.py                    # CRUD de bombas
│   └── abastecimento_dao.py            # CRUD de abastecimentos
├── control/
│   ├── combustivel_controller.py       # Regras de negócio de combustíveis
│   ├── bomba_controller.py             # Regras de negócio de bombas
│   └── abastecimento_controller.py     # Regras de negócio de abastecimentos
└── view/
    ├── combustivel_view.py             # Formulário de combustível
    ├── combustivel_list_view.py        # Listagem de combustíveis
    ├── bomba_view.py                   # Formulário de bomba
    ├── bomba_list_view.py              # Listagem de bombas
    ├── abastecimento_view.py           # Formulário de abastecimento
    ├── abastecimento_list_view.py      # Listagem com filtro
    └── sobre_view.py                   # Tela Sobre
```

## Modelagem do Banco de Dados

### Tabelas

| Tabela | Descrição |
|---|---|
| `tb_combustiveis` | Tipos de combustível, preço por litro e estoque |
| `tb_bombas` | Bombas de abastecimento, vinculadas a um combustível |
| `tb_abastecimentos` | Registros de abastecimento, vinculados a uma bomba |

### Relacionamentos

- `tb_bombas` → `tb_combustiveis` (N para 1): cada bomba distribui um único tipo de combustível
- `tb_abastecimentos` → `tb_bombas` (N para 1): cada abastecimento é realizado em uma única bomba

### Diagrama de Classes

![Diagrama de Classes](docs/classe_projeto.png)

## Documentação do Projeto

[Clique aqui para acessar a Documentação Completa](Documentação%20do%20Projeto.md)

## Padrões de Projeto Utilizados

| Padrão | Categoria | Onde é usado |
|---|---|---|
| DAO | Estrutural | `CombustivelDAO`, `BombaDAO` e `AbastecimentoDAO` isolam totalmente o acesso ao banco de dados das demais camadas |
| Strategy | Comportamental | `PrecoCheioStrategy`, `DescontoFrotaStrategy` e `DescontoFidelidadeStrategy` calculam o valor do abastecimento de formas diferentes, intercambiáveis em tempo de execução |

### Strategy — Detalhamento

A classe `Abastecimento` recebe uma estratégia de cálculo no momento da criação, sem precisar conhecer os detalhes de como o valor é calculado:

- **PrecoCheioStrategy** — cliente comum, paga o preço integral por litro
- **DescontoFrotaStrategy** — cliente frota, 10% de desconto no preço por litro
- **DescontoFidelidadeStrategy** — cliente fidelidade, 5% de desconto no preço por litro

---

## Detalhamento de Aprendizado

**Dificuldades Encontradas:**
- Configurar a conexão com PostgreSQL no Windows, pois o psycopg2 apresentava erro de decodificação relacionado a caracteres especiais no caminho de instalação do sistema
- Estruturar a hierarquia de janelas com `Toplevel` e garantir o recarregamento automático dos dados após o fechamento de uma janela filha
- Implementar o cálculo de valor em tempo real no formulário de abastecimento, reagindo a mudanças nos campos sem travar a interface

**Como resolvi:**
- Substituição do psycopg2 pelo psycopg3, que resolveu o problema de codificação no Windows
- Estudo da documentação do Tkinter sobre `Toplevel` e `wait_window()` para entender o fluxo correto entre janelas pai e filha
- Uso do evento `<KeyRelease>` do Tkinter associado a uma função de recálculo, atualizando o valor exibido a cada tecla digitada

**Principal Aprendizado:**
- Compreendi como o padrão Strategy permite trocar algoritmos de cálculo em tempo de execução sem alterar a classe principal
- Entendi como a camada DAO isola completamente o acesso ao banco de dados, deixando o restante do sistema independente da tecnologia de persistência utilizada
- Aprendi a modelar relacionamentos N-1 entre entidades, refletindo isso tanto nas classes Python quanto nas chaves estrangeiras das tabelas

---

## Declaração de Uso de IA

- [x] **Utilizei IA** como ferramenta de apoio.
- **Ferramenta:** Claude Sonnet 4.6 (Anthropic)
- **Finalidade:** Auxílio na configuração da conexão com o banco de dados PostgreSQL e geração de código para os arquivos de DAO, Controller e View, principalmente no View.
- **Validação:** Declaro que todo o código gerado foi lido, testado e compreendido antes da entrega.

---

**Autor:** Gabriel Duarte Barboza  
**Curso:** Bacharelado em Ciência da Computação  
**Disciplina:** Linguagem de Programação Orientada a Objetos (LPOO)  
**Professora:** Vanessa Lago Machado  
**Período:** 2026/1
