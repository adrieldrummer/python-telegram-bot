"""Lembretes diários e resgate de alunos parados. Feito para rodar em cron.

    # todo dia às 19h
    0 19 * * *  cd /opt/mapa && /opt/mapa/.venv/bin/python scripts/enviar_lembretes.py

Também processa a fila de e-mails, então serve como worker único da máquina.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app import mailer  # noqa: E402
from app.db import buscar_todos, sessao  # noqa: E402
from app.jornada import dia_atual  # noqa: E402
from app.security import hoje_txt  # noqa: E402


def alunos_para_lembrar(con):
    """Ativos, com lembretes ligados e que ainda não estudaram hoje."""
    return buscar_todos(
        con,
        """SELECT * FROM alunos
           WHERE status = 'ativo' AND admin = 0 AND lembretes_email = 1
             AND concluido_em IS NULL
             AND (ultimo_dia_estudo IS NULL OR ultimo_dia_estudo <> ?)""",
        (hoje_txt(),),
    )


def mensagem_para(con, aluno) -> str:
    item = dia_atual(con, int(aluno["id"]))
    dia = item["dia"]
    streak = int(aluno["streak_atual"] or 0)
    if streak >= 3:
        abertura = f"Você está com {streak} dias seguidos — não quebre hoje."
    elif aluno["ultimo_dia_estudo"] is None:
        abertura = "Sua jornada está esperando o primeiro bloco."
    else:
        abertura = "Faz um tempo desde o seu último bloco."
    return (
        f"{abertura} O próximo passo é o <strong>Dia {dia.numero} — {dia.titulo}</strong>: "
        f"{dia.promessa} São {dia.tempo_min} minutos."
    )


def main() -> int:
    enviados = 0
    with sessao() as con:
        for aluno in alunos_para_lembrar(con):
            mailer.enviar_lembrete(con, aluno, mensagem_para(con, aluno))
            enviados += 1
    resumo = mailer.processar_fila(limite=200)
    print(f"Lembretes enfileirados: {enviados}")
    print(f"Fila processada: {resumo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
