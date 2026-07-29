-- ============================================================
--  Esquema do banco (SQLite). Somente dados de alunos:
--  o conteúdo do curso vive em /conteudo, versionado no git.
-- ============================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS alunos (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    nome              TEXT    NOT NULL,
    email             TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    telefone          TEXT    DEFAULT '',
    senha_hash        TEXT    DEFAULT '',
    -- pendente: comprou e recebeu e-mail de aprovação, ainda não criou senha
    -- ativo: acesso liberado | suspenso: reembolso/chargeback | cancelado
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
    plano             TEXT    NOT NULL DEFAULT 'recruta',
    plano_ate         TEXT,
    criado_em         TEXT    NOT NULL DEFAULT (datetime('now')),
    ativado_em        TEXT,
    ultimo_login      TEXT,
    observacoes       TEXT    DEFAULT ''
);

CREATE TABLE IF NOT EXISTS tokens (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id   INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    tipo       TEXT    NOT NULL,              -- ativacao | recuperacao
    token_hash TEXT    NOT NULL UNIQUE,
    expira_em  TEXT    NOT NULL,
    usado_em   TEXT,
    criado_em  TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_tokens_aluno ON tokens(aluno_id, tipo);

CREATE TABLE IF NOT EXISTS sessoes (
    id         TEXT    PRIMARY KEY,
    aluno_id   INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    criado_em  TEXT    NOT NULL DEFAULT (datetime('now')),
    expira_em  TEXT    NOT NULL,
    revogada   INTEGER NOT NULL DEFAULT 0,
    user_agent TEXT    DEFAULT '',
    ip         TEXT    DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sessoes_aluno ON sessoes(aluno_id);

CREATE TABLE IF NOT EXISTS compras (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id   INTEGER REFERENCES alunos(id) ON DELETE SET NULL,
    provedor   TEXT    NOT NULL DEFAULT 'cakto',
    referencia TEXT,                          -- id da transação na Cakto
    produto    TEXT    DEFAULT '',
    oferta     TEXT    DEFAULT '',
    valor      REAL    DEFAULT 0,
    status     TEXT    NOT NULL,              -- aprovada | reembolsada | chargeback | cancelada
    email      TEXT    DEFAULT '',
    criado_em  TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_compras_aluno ON compras(aluno_id);

CREATE TABLE IF NOT EXISTS webhooks (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    provedor       TEXT    NOT NULL DEFAULT 'cakto',
    evento_id      TEXT    UNIQUE,
    tipo           TEXT    DEFAULT '',
    assinatura_ok  INTEGER NOT NULL DEFAULT 0,
    payload        TEXT    NOT NULL,
    resultado      TEXT    DEFAULT '',
    criado_em      TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS progresso_dias (
    aluno_id       INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    dia            INTEGER NOT NULL,
    status         TEXT    NOT NULL DEFAULT 'liberado',   -- liberado | concluido
    liberado_em    TEXT    NOT NULL DEFAULT (datetime('now')),
    aula_lida_em   TEXT,
    missao_em      TEXT,
    concluido_em   TEXT,
    acerto_pct     INTEGER DEFAULT 0,
    questoes_feitas INTEGER NOT NULL DEFAULT 0,
    antecipado     INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (aluno_id, dia)
);

CREATE TABLE IF NOT EXISTS respostas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id    INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    questao_id  TEXT    NOT NULL,
    materia     TEXT    NOT NULL DEFAULT '',
    alternativa TEXT    NOT NULL,
    correta     INTEGER NOT NULL,
    tempo_seg   INTEGER NOT NULL DEFAULT 0,
    origem      TEXT    NOT NULL,             -- diagnostico | missao | treino | simulado | revisao
    dia         INTEGER,
    sessao_id   INTEGER,                      -- id da sessão de simulado, quando houver
    criado_em   TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_respostas_aluno ON respostas(aluno_id, criado_em);
CREATE INDEX IF NOT EXISTS idx_respostas_materia ON respostas(aluno_id, materia);

CREATE TABLE IF NOT EXISTS caderno_erros (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id        INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    questao_id      TEXT    NOT NULL,
    materia         TEXT    NOT NULL DEFAULT '',
    categoria       TEXT    DEFAULT '',       -- conteudo | pegadinha | desatencao
    anotacao        TEXT    DEFAULT '',
    status          TEXT    NOT NULL DEFAULT 'aberto',   -- aberto | dominado
    nivel_srs       INTEGER NOT NULL DEFAULT 0,
    acertos_seguidos INTEGER NOT NULL DEFAULT 0,
    proxima_revisao TEXT,
    criado_em       TEXT    NOT NULL DEFAULT (datetime('now')),
    atualizado_em   TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (aluno_id, questao_id)
);
CREATE INDEX IF NOT EXISTS idx_erros_revisao ON caderno_erros(aluno_id, status, proxima_revisao);

CREATE TABLE IF NOT EXISTS simulados_sessoes (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id     INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    simulado_id  TEXT    NOT NULL,
    iniciado_em  TEXT    NOT NULL DEFAULT (datetime('now')),
    finalizado_em TEXT,
    duracao_seg  INTEGER NOT NULL DEFAULT 0,
    acertos      INTEGER NOT NULL DEFAULT 0,
    total        INTEGER NOT NULL DEFAULT 0,
    relatorio    TEXT    DEFAULT ''            -- JSON com desempenho por matéria
);
CREATE INDEX IF NOT EXISTS idx_simulados_aluno ON simulados_sessoes(aluno_id);

CREATE TABLE IF NOT EXISTS eventos_pontos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id   INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    tipo       TEXT    NOT NULL,
    pontos     INTEGER NOT NULL,
    descricao  TEXT    DEFAULT '',
    criado_em  TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_pontos_aluno ON eventos_pontos(aluno_id, criado_em);

CREATE TABLE IF NOT EXISTS medalhas_aluno (
    aluno_id      INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    medalha_id    TEXT    NOT NULL,
    conquistada_em TEXT   NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (aluno_id, medalha_id)
);

CREATE TABLE IF NOT EXISTS diario (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id  INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    dia       INTEGER NOT NULL,
    texto     TEXT    NOT NULL DEFAULT '',
    criado_em TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (aluno_id, dia)
);

CREATE TABLE IF NOT EXISTS emails (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id     INTEGER REFERENCES alunos(id) ON DELETE SET NULL,
    destinatario TEXT    NOT NULL,
    assunto      TEXT    NOT NULL,
    corpo_html   TEXT    NOT NULL,
    corpo_texto  TEXT    NOT NULL DEFAULT '',
    tipo         TEXT    NOT NULL DEFAULT 'geral',
    status       TEXT    NOT NULL DEFAULT 'na_fila',   -- na_fila | enviado | erro | caixa_saida
    tentativas   INTEGER NOT NULL DEFAULT 0,
    erro         TEXT    DEFAULT '',
    criado_em    TEXT    NOT NULL DEFAULT (datetime('now')),
    enviado_em   TEXT
);
CREATE INDEX IF NOT EXISTS idx_emails_status ON emails(status, criado_em);

CREATE TABLE IF NOT EXISTS tentativas_login (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    email     TEXT NOT NULL,
    ip        TEXT DEFAULT '',
    sucesso   INTEGER NOT NULL DEFAULT 0,
    criado_em TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_tentativas ON tentativas_login(email, criado_em);

CREATE TABLE IF NOT EXISTS assinaturas (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id     INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    provedor     TEXT    NOT NULL DEFAULT 'cakto',
    referencia   TEXT,
    plano        TEXT    NOT NULL,
    ciclo        TEXT    NOT NULL DEFAULT 'único',
    status       TEXT    NOT NULL DEFAULT 'ativa',   -- ativa | cancelada | expirada | atrasada
    inicio       TEXT    NOT NULL DEFAULT (datetime('now')),
    renova_em    TEXT,
    cancelada_em TEXT,
    atualizado_em TEXT   NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_assinaturas_aluno ON assinaturas(aluno_id, status);
