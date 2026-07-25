-- ============================================================
--  Esquema PostgreSQL (Supabase, Neon, RDS...).
--  Espelha app/schema.sql. Datas continuam TEXT para manter
--  idênticos os relatórios que fatiam a string (substr).
-- ============================================================

CREATE TABLE IF NOT EXISTS alunos (
    id                SERIAL PRIMARY KEY,
    nome              TEXT    NOT NULL,
    email             TEXT    NOT NULL UNIQUE,
    telefone          TEXT    DEFAULT '',
    senha_hash        TEXT    DEFAULT '',
    status            TEXT    NOT NULL DEFAULT 'pendente',
    admin             INTEGER NOT NULL DEFAULT 0,
    origem            TEXT    NOT NULL DEFAULT 'cakto',
    pontos            INTEGER NOT NULL DEFAULT 0,
    pontos_gastos     INTEGER NOT NULL DEFAULT 0,
    streak_atual      INTEGER NOT NULL DEFAULT 0,
    streak_recorde    INTEGER NOT NULL DEFAULT 0,
    ultimo_dia_estudo TEXT,
    diagnostico_em    TEXT,
    inicio_jornada    TEXT,
    concluido_em      TEXT,
    lembretes_email   INTEGER NOT NULL DEFAULT 1,
    criado_em         TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    ativado_em        TEXT,
    ultimo_login      TEXT,
    observacoes       TEXT    DEFAULT ''
);

CREATE TABLE IF NOT EXISTS tokens (
    id         SERIAL PRIMARY KEY,
    aluno_id   INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    tipo       TEXT    NOT NULL,
    token_hash TEXT    NOT NULL UNIQUE,
    expira_em  TEXT    NOT NULL,
    usado_em   TEXT,
    criado_em  TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS')
);
CREATE INDEX IF NOT EXISTS idx_tokens_aluno ON tokens(aluno_id, tipo);

CREATE TABLE IF NOT EXISTS sessoes (
    id         TEXT    PRIMARY KEY,
    aluno_id   INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    criado_em  TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    expira_em  TEXT    NOT NULL,
    revogada   INTEGER NOT NULL DEFAULT 0,
    user_agent TEXT    DEFAULT '',
    ip         TEXT    DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sessoes_aluno ON sessoes(aluno_id);

CREATE TABLE IF NOT EXISTS compras (
    id         SERIAL PRIMARY KEY,
    aluno_id   INTEGER REFERENCES alunos(id) ON DELETE SET NULL,
    provedor   TEXT    NOT NULL DEFAULT 'cakto',
    referencia TEXT,
    produto    TEXT    DEFAULT '',
    oferta     TEXT    DEFAULT '',
    valor      REAL    DEFAULT 0,
    status     TEXT    NOT NULL,
    email      TEXT    DEFAULT '',
    criado_em  TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS')
);
CREATE INDEX IF NOT EXISTS idx_compras_aluno ON compras(aluno_id);

CREATE TABLE IF NOT EXISTS webhooks (
    id            SERIAL PRIMARY KEY,
    provedor      TEXT    NOT NULL DEFAULT 'cakto',
    evento_id     TEXT    UNIQUE,
    tipo          TEXT    DEFAULT '',
    assinatura_ok INTEGER NOT NULL DEFAULT 0,
    payload       TEXT    NOT NULL,
    resultado     TEXT    DEFAULT '',
    criado_em     TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS')
);

CREATE TABLE IF NOT EXISTS progresso_dias (
    aluno_id        INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    dia             INTEGER NOT NULL,
    status          TEXT    NOT NULL DEFAULT 'liberado',
    liberado_em     TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    aula_lida_em    TEXT,
    missao_em       TEXT,
    concluido_em    TEXT,
    acerto_pct      INTEGER DEFAULT 0,
    questoes_feitas INTEGER NOT NULL DEFAULT 0,
    antecipado      INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (aluno_id, dia)
);

CREATE TABLE IF NOT EXISTS respostas (
    id          SERIAL PRIMARY KEY,
    aluno_id    INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    questao_id  TEXT    NOT NULL,
    materia     TEXT    NOT NULL DEFAULT '',
    alternativa TEXT    NOT NULL,
    correta     INTEGER NOT NULL,
    tempo_seg   INTEGER NOT NULL DEFAULT 0,
    origem      TEXT    NOT NULL,
    dia         INTEGER,
    sessao_id   INTEGER,
    criado_em   TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS')
);
CREATE INDEX IF NOT EXISTS idx_respostas_aluno ON respostas(aluno_id, criado_em);
CREATE INDEX IF NOT EXISTS idx_respostas_materia ON respostas(aluno_id, materia);

CREATE TABLE IF NOT EXISTS caderno_erros (
    id               SERIAL PRIMARY KEY,
    aluno_id         INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    questao_id       TEXT    NOT NULL,
    materia          TEXT    NOT NULL DEFAULT '',
    categoria        TEXT    DEFAULT '',
    anotacao         TEXT    DEFAULT '',
    status           TEXT    NOT NULL DEFAULT 'aberto',
    nivel_srs        INTEGER NOT NULL DEFAULT 0,
    acertos_seguidos INTEGER NOT NULL DEFAULT 0,
    proxima_revisao  TEXT,
    criado_em        TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    atualizado_em    TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    UNIQUE (aluno_id, questao_id)
);
CREATE INDEX IF NOT EXISTS idx_erros_revisao ON caderno_erros(aluno_id, status, proxima_revisao);

CREATE TABLE IF NOT EXISTS simulados_sessoes (
    id            SERIAL PRIMARY KEY,
    aluno_id      INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    simulado_id   TEXT    NOT NULL,
    iniciado_em   TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    finalizado_em TEXT,
    duracao_seg   INTEGER NOT NULL DEFAULT 0,
    acertos       INTEGER NOT NULL DEFAULT 0,
    total         INTEGER NOT NULL DEFAULT 0,
    relatorio     TEXT    DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_simulados_aluno ON simulados_sessoes(aluno_id);

CREATE TABLE IF NOT EXISTS eventos_pontos (
    id        SERIAL PRIMARY KEY,
    aluno_id  INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    tipo      TEXT    NOT NULL,
    pontos    INTEGER NOT NULL,
    descricao TEXT    DEFAULT '',
    criado_em TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS')
);
CREATE INDEX IF NOT EXISTS idx_pontos_aluno ON eventos_pontos(aluno_id, criado_em);

CREATE TABLE IF NOT EXISTS medalhas_aluno (
    aluno_id       INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    medalha_id     TEXT    NOT NULL,
    conquistada_em TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    PRIMARY KEY (aluno_id, medalha_id)
);

CREATE TABLE IF NOT EXISTS diario (
    id        SERIAL PRIMARY KEY,
    aluno_id  INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    dia       INTEGER NOT NULL,
    texto     TEXT    NOT NULL DEFAULT '',
    criado_em TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    UNIQUE (aluno_id, dia)
);

CREATE TABLE IF NOT EXISTS emails (
    id           SERIAL PRIMARY KEY,
    aluno_id     INTEGER REFERENCES alunos(id) ON DELETE SET NULL,
    destinatario TEXT    NOT NULL,
    assunto      TEXT    NOT NULL,
    corpo_html   TEXT    NOT NULL,
    corpo_texto  TEXT    NOT NULL DEFAULT '',
    tipo         TEXT    NOT NULL DEFAULT 'geral',
    status       TEXT    NOT NULL DEFAULT 'na_fila',
    tentativas   INTEGER NOT NULL DEFAULT 0,
    erro         TEXT    DEFAULT '',
    criado_em    TEXT    NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS'),
    enviado_em   TEXT
);
CREATE INDEX IF NOT EXISTS idx_emails_status ON emails(status, criado_em);

CREATE TABLE IF NOT EXISTS tentativas_login (
    id        SERIAL PRIMARY KEY,
    email     TEXT NOT NULL,
    ip        TEXT DEFAULT '',
    sucesso   INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT NOT NULL DEFAULT to_char(now(), 'YYYY-MM-DD HH24:MI:SS')
);
CREATE INDEX IF NOT EXISTS idx_tentativas ON tentativas_login(email, criado_em);
