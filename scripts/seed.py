"""Prepara o banco: cria o admin, contas de teste e (opcionalmente) progresso de demonstração.

Uso:
    python scripts/seed.py              # cria admin + contas de teste
    python scripts/seed.py --demo       # também simula progresso do aluno de teste
    python scripts/seed.py --limpar     # apaga o banco antes (cuidado)
"""

from __future__ import annotations

import os
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app import alunos as servico_alunos  # noqa: E402
from app import estudo, jornada  # noqa: E402
from app.db import buscar_um, caminho_banco, criar_esquema, executar, sessao  # noqa: E402
from app.security import agora_txt  # noqa: E402
from conteudo.questoes import questao as buscar_questao  # noqa: E402

CONTAS_TESTE = [
    {
        "nome": os.getenv("ADMIN_NOME", "Rafael Andrade"),
        "email": os.getenv("ADMIN_EMAIL", "admin@teste.com"),
        "senha": os.getenv("ADMIN_SENHA", "admin1234"),
        "admin": True,
    },
    {
        "nome": "Aluno de Teste",
        "email": "aluno@teste.com",
        "senha": "aluno1234",
        "admin": False,
    },
]


def criar_contas() -> list[dict]:
    criadas = []
    with sessao() as con:
        for conta in CONTAS_TESTE:
            existente = servico_alunos.por_email(con, conta["email"])
            if existente is None:
                aluno = servico_alunos.criar(
                    con,
                    conta["nome"],
                    conta["email"],
                    origem="seed",
                    admin=conta["admin"],
                    senha=conta["senha"],
                )
                executar(
                    con,
                    "UPDATE alunos SET ativado_em=?, status='ativo' WHERE id=?",
                    (agora_txt(), aluno["id"]),
                )
                estado = "criada"
            else:
                servico_alunos.definir_senha(con, int(existente["id"]), conta["senha"])
                executar(
                    con,
                    "UPDATE alunos SET admin=?, status='ativo' WHERE id=?",
                    (1 if conta["admin"] else 0, existente["id"]),
                )
                aluno = servico_alunos.por_email(con, conta["email"])
                estado = "atualizada"
            jornada.iniciar_jornada(con, int(aluno["id"]))
            criadas.append({**conta, "id": int(aluno["id"]), "estado": estado})
    return criadas


def simular_progresso(aluno_id: int, ate_dia: int = 4, acerto_alvo: float = 0.72) -> None:
    """Responde as missões dos primeiros dias para o painel nascer com dados."""
    rnd = random.Random(2026)
    with sessao() as con:
        jornada.iniciar_jornada(con, aluno_id)
        for numero in range(1, ate_dia + 1):
            item = jornada.acesso_ao_dia(con, aluno_id, numero)
            if item is None:
                print(f"  dia {numero} bloqueado — parando a simulação aqui")
                break
            jornada.marcar_aula_lida(con, aluno_id, numero)
            questoes = jornada.questoes_da_missao(con, aluno_id, numero)
            acertos = 0
            for q in questoes:
                acertou = rnd.random() < acerto_alvo
                letra = q.correta
                if not acertou:
                    outras = [alt for alt, _ in q.alternativas if alt != q.correta]
                    letra = rnd.choice(outras)
                resultado = estudo.responder(
                    con, aluno_id, q, letra, origem="missao", dia=numero, tempo_seg=rnd.randint(25, 95)
                )
                if resultado["correta"]:
                    acertos += 1
                else:
                    estudo.classificar_erro(
                        con,
                        aluno_id,
                        q.id,
                        rnd.choice(["conteudo", "pegadinha", "desatencao"]),
                        "erro simulado para demonstração",
                    )
            resultado = jornada.concluir_dia(con, aluno_id, numero, acertos, len(questoes))
            print(f"  dia {numero}: {acertos}/{len(questoes)} — {'concluído' if resultado.get('concluido') else resultado.get('motivo')}")

        # antecipa os dias seguintes para a demonstração ficar navegável
        for numero in range(ate_dia + 1, ate_dia + 2):
            jornada.liberar_proximo(con, aluno_id, numero - 1, antecipado=True)


def main() -> int:
    if "--limpar" in sys.argv:
        alvo = caminho_banco()
        for sufixo in ("", "-wal", "-shm"):
            arquivo = Path(str(alvo) + sufixo)
            if arquivo.exists():
                arquivo.unlink()
        print(f"Banco removido: {alvo}")

    criar_esquema()
    print(f"Banco pronto em {caminho_banco()}\n")

    contas = criar_contas()
    print("Contas de acesso:")
    for c in contas:
        papel = "ADMIN" if c["admin"] else "ALUNO"
        print(f"  [{papel}] {c['email']}  senha: {c['senha']}  ({c['estado']})")

    if "--demo" in sys.argv:
        aluno = next(c for c in contas if not c["admin"])
        print("\nSimulando progresso do aluno de teste:")
        simular_progresso(aluno["id"])

    with sessao() as con:
        total = buscar_um(con, "SELECT COUNT(*) AS n FROM alunos")
    print(f"\nTotal de contas no banco: {total['n']}")
    print("\nSuba a aplicação com:  python run.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
