"""Tradução do SQL para Postgres — o mesmo código roda nos dois bancos."""

from __future__ import annotations

from app.db import traduzir


def test_placeholders_viram_percent_s():
    assert traduzir("SELECT * FROM alunos WHERE id = ?") == "SELECT * FROM alunos WHERE id = %s"


def test_insert_or_ignore_vira_on_conflict():
    saida = traduzir("INSERT OR IGNORE INTO medalhas_aluno (aluno_id, medalha_id) VALUES (?,?)")
    assert saida.startswith("INSERT INTO medalhas_aluno")
    assert saida.endswith("ON CONFLICT DO NOTHING")
    assert "OR IGNORE" not in saida


def test_datetime_now_vira_to_char():
    assert "to_char(now()" in traduzir("UPDATE alunos SET ultimo_login=datetime('now') WHERE id=?")


def test_datetime_relativo_vira_interval():
    saida = traduzir("SELECT 1 FROM respostas WHERE criado_em > datetime('now','-7 day')")
    assert "interval '-7 day'" in saida


def test_like_vira_ilike():
    assert "ILIKE" in traduzir("SELECT * FROM alunos WHERE nome LIKE ?")


def test_on_conflict_existente_nao_e_duplicado():
    entrada = (
        "INSERT INTO diario (aluno_id, dia, texto) VALUES (?,?,?) "
        "ON CONFLICT(aluno_id, dia) DO UPDATE SET texto=excluded.texto"
    )
    saida = traduzir(entrada)
    assert saida.count("ON CONFLICT") == 1


def test_sql_sem_dialeto_passa_intacto():
    entrada = "SELECT COUNT(*) FROM alunos WHERE status = 'ativo'"
    assert traduzir(entrada) == entrada
