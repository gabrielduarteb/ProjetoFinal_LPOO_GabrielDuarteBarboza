-- Banco: lpoo_projeto_gabrielduarte
-- Sistema: Posto de Combustivel

CREATE TABLE tb_combustiveis (
    comb_id      SERIAL PRIMARY KEY,
    comb_tipo    VARCHAR(30)   UNIQUE NOT NULL,
    comb_preco   NUMERIC(10,2) NOT NULL CHECK (comb_preco > 0),
    comb_estoque NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (comb_estoque >= 0)
);

CREATE TABLE tb_bombas (
    bomb_id      SERIAL PRIMARY KEY,
    bomb_numero  INTEGER       UNIQUE NOT NULL CHECK (bomb_numero > 0),
    bomb_comb_id INTEGER       NOT NULL,
    bomb_ativa   BOOLEAN       NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_bomba_combustivel
        FOREIGN KEY (bomb_comb_id)
        REFERENCES tb_combustiveis(comb_id)
        ON DELETE RESTRICT
);

CREATE TABLE tb_abastecimentos (
    abast_id         SERIAL PRIMARY KEY,
    abast_bomb_id    INTEGER        NOT NULL,
    abast_litros     NUMERIC(10,2)  NOT NULL CHECK (abast_litros > 0),
    abast_valor      NUMERIC(10,2)  NOT NULL CHECK (abast_valor > 0),
    abast_modalidade VARCHAR(30)    NOT NULL,
    abast_data_hora  TIMESTAMP      NOT NULL DEFAULT NOW(),
    abast_status     VARCHAR(20)    NOT NULL DEFAULT 'concluido',
    CONSTRAINT fk_abast_bomba
        FOREIGN KEY (abast_bomb_id)
        REFERENCES tb_bombas(bomb_id)
        ON DELETE RESTRICT,
    CONSTRAINT chk_abast_status
        CHECK (abast_status IN ('pendente', 'concluido', 'cancelado'))
);
