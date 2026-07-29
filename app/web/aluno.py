"""Área do aluno: painel, jornada, aulas, questões, caderno de erros, simulados."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

from conteudo import TREINOS, edital, manual, modulos as catalogo_modulos
from conteudo import planos as catalogo_planos, simulados as conteudo_simulados, trilha
from conteudo.materias import IDS as MATERIAS_IDS
from conteudo.materias import POR_ID as MATERIAS_POR_ID
from conteudo.questoes import POR_MATERIA, questao as buscar_questao, selecionar

from .. import estudo, jornada, notificacoes, planos as servico_planos, srs
from ..config import config
from ..db import buscar_um, executar, sessao
from ..deps import bloqueio_por_plano, exigir_aluno, redirecionar, responder_template, validar_csrf
from ..gamificacao import estatisticas, extrato, medalhas_do_aluno, ranking, resumo_patente
from ..mailer import enviar_conclusao, enviar_dia_concluido
from ..security import agora_txt, conferir_senha, validar_senha
from ..alunos import definir_senha

router = APIRouter()


def _serializar_questao(q, resposta: Optional[dict] = None) -> dict:
    dados = {
        "id": q.id,
        "materia": q.materia,
        "materia_nome": MATERIAS_POR_ID[q.materia].nome,
        "cor": MATERIAS_POR_ID[q.materia].cor,
        "tema": q.tema,
        "nivel": q.nivel,
        "enunciado": q.enunciado,
        "alternativas": [{"letra": letra, "texto": texto} for letra, texto in q.alternativas],
    }
    if resposta:
        dados["respondida"] = resposta
    return dados


# --- painel ----------------------------------------------------------------


@router.get("/painel")
async def painel(request: Request, aluno=Depends(exigir_aluno), boasvindas: int = 0):
    aluno_id = int(aluno["id"])
    with sessao() as con:
        jornada.iniciar_jornada(con, aluno_id)
        resumo = jornada.resumo_jornada(con, aluno_id)
        stats = estatisticas(con, aluno_id)
        caderno = srs.resumo(con, aluno_id)
        prioridades = jornada.mapa_prioridades(con, aluno_id)[:4]
        evolucao = estudo.evolucao_semanal(con, aluno_id)
        historico = estudo.historico_simulados(con, aluno_id)
        medalhas = [m for m in medalhas_do_aluno(con, aluno_id) if m["conquistada"]][-6:]

    # cada treino declara o recurso que exige; sem recurso, é livre para todos
    treinos = [
        {
            **t,
            "bloqueado": bool(t["recurso"])
            and not servico_planos.tem_recurso(aluno, t["recurso"]),
        }
        for t in TREINOS
    ]

    with sessao() as con:
        saldo = servico_planos.saldo_de_questoes(con, aluno)
        avisos = notificacoes.gerar(con, aluno_id)

    return responder_template(
        request,
        "painel.html",
        {
            "aluno": aluno,
            "edital": edital.resumo(),
            "saldo": saldo,
            "modulos": catalogo_modulos.ordenados(),
            "modulos_liberados": servico_planos.tem_recurso(aluno, "avancado"),
            "resumo": resumo,
            "stats": stats,
            "caderno": caderno,
            "prioridades": prioridades,
            "evolucao": evolucao,
            "historico": historico,
            "medalhas": medalhas,
            "treinos": treinos,
            "plano": servico_planos.resumo(aluno),
            "boasvindas": bool(boasvindas),
            "avisos": avisos,
            "patente": resumo_patente(int(aluno["pontos"])),
        },
    )


@router.get("/jornada")
async def ver_jornada(request: Request, aluno=Depends(exigir_aluno)):
    with sessao() as con:
        resumo = jornada.resumo_jornada(con, int(aluno["id"]))
    return responder_template(
        request,
        "jornada.html",
        {"aluno": aluno, "resumo": resumo, "fases": trilha.FASES, "custo": config.custo_chave_antecipacao},
    )


@router.post("/jornada/antecipar/{numero}")
async def antecipar(request: Request, numero: int, csrf_token: str = Form(""), aluno=Depends(exigir_aluno)):
    validar_csrf(request, csrf_token)
    with sessao() as con:
        ok, mensagem = jornada.antecipar(con, int(aluno["id"]), numero)
    destino = f"/dia/{numero}" if ok else "/jornada?aviso=" + mensagem.replace(" ", "+")
    return redirecionar(destino)


# --- dia da trilha ---------------------------------------------------------


@router.get("/dia/{numero}")
async def ver_dia(request: Request, numero: int, aluno=Depends(exigir_aluno)):
    d = trilha.dia(numero)
    if d is None:
        raise HTTPException(status_code=404, detail="Dia não encontrado")
    aluno_id = int(aluno["id"])
    with sessao() as con:
        item = jornada.acesso_ao_dia(con, aluno_id, numero)
        if item is None:
            return responder_template(
                request,
                "bloqueado.html",
                {"aluno": aluno, "dia": d, "custo": config.custo_chave_antecipacao},
                status_code=403,
            )
        questoes = jornada.questoes_da_missao(con, aluno_id, numero)
        respondidas = estudo.respondidas_do_dia(con, aluno_id, numero)
        anotacao = jornada.ler_diario(con, aluno_id, numero)
        caderno = srs.resumo(con, aluno_id)

    simulado = conteudo_simulados.simulado(d.missao.simulado_id) if d.missao.simulado_id else None
    return responder_template(
        request,
        "dia.html",
        {
            "aluno": aluno,
            "d": d,
            "fase": trilha.FASES_POR_ID[d.fase],
            "item": item,
            "questoes": [
                _serializar_questao(q, respondidas.get(q.id)) for q in questoes
            ],
            "total_questoes": len(questoes),
            "respondidas": respondidas,
            "anotacao": anotacao,
            "caderno": caderno,
            "simulado": simulado,
            "meta": config.meta_acerto_missao,
        },
    )


@router.post("/dia/{numero}/aula-lida")
async def aula_lida(request: Request, numero: int, csrf_token: str = Form(""), aluno=Depends(exigir_aluno)):
    validar_csrf(request, csrf_token)
    with sessao() as con:
        jornada.marcar_aula_lida(con, int(aluno["id"]), numero)
    return redirecionar(f"/dia/{numero}#missao")


@router.post("/dia/{numero}/diario")
async def salvar_diario(
    request: Request, numero: int, texto: str = Form(""), csrf_token: str = Form(""), aluno=Depends(exigir_aluno)
):
    validar_csrf(request, csrf_token)
    with sessao() as con:
        jornada.salvar_diario(con, int(aluno["id"]), numero, texto)
    return redirecionar(f"/dia/{numero}#diario")


# --- API de estudo ---------------------------------------------------------


class RespostaEntrada(BaseModel):
    questao_id: str
    alternativa: str
    origem: str = "treino"
    dia: Optional[int] = None
    tempo_seg: int = 0
    sessao_id: Optional[int] = None


@router.post("/api/responder")
async def api_responder(dados: RespostaEntrada, aluno=Depends(exigir_aluno)):
    q = buscar_questao(dados.questao_id)
    if q is None:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    if dados.alternativa not in {letra for letra, _ in q.alternativas}:
        raise HTTPException(status_code=400, detail="Alternativa inválida")
    with sessao() as con:
        saldo = servico_planos.saldo_de_questoes(con, aluno)
        if saldo["esgotado"]:
            raise HTTPException(
                status_code=402,
                detail=(
                    f"Você chegou ao limite de {saldo['limite']} questões por dia do seu plano. "
                    "Faça upgrade para treinar sem limite."
                ),
            )
        resultado = estudo.responder(
            con,
            int(aluno["id"]),
            q,
            dados.alternativa,
            origem=dados.origem,
            dia=dados.dia,
            tempo_seg=dados.tempo_seg,
            sessao_id=dados.sessao_id,
        )
        resultado["pontos_totais"] = int(
            buscar_um(con, "SELECT pontos FROM alunos WHERE id=?", (aluno["id"],))["pontos"]
        )
        atualizado = servico_planos.saldo_de_questoes(con, aluno)
        resultado["restantes_hoje"] = atualizado["restantes"]
    return JSONResponse(resultado)


class ClassificacaoEntrada(BaseModel):
    questao_id: str
    categoria: str
    anotacao: str = ""


@router.post("/api/classificar")
async def api_classificar(dados: ClassificacaoEntrada, aluno=Depends(exigir_aluno)):
    with sessao() as con:
        resultado = estudo.classificar_erro(
            con, int(aluno["id"]), dados.questao_id, dados.categoria, dados.anotacao
        )
    if not resultado["ok"]:
        raise HTTPException(status_code=400, detail="Não foi possível classificar esse erro.")
    return JSONResponse(resultado)


class ConclusaoEntrada(BaseModel):
    dia: int


@router.post("/api/concluir-dia")
async def api_concluir_dia(dados: ConclusaoEntrada, aluno=Depends(exigir_aluno)):
    aluno_id = int(aluno["id"])
    with sessao() as con:
        item = jornada.acesso_ao_dia(con, aluno_id, dados.dia)
        if item is None:
            raise HTTPException(status_code=403, detail="Dia bloqueado")
        questoes = jornada.questoes_da_missao(con, aluno_id, dados.dia)
        respondidas = estudo.respondidas_do_dia(con, aluno_id, dados.dia)
        ids = {q.id for q in questoes}
        feitas = {qid: r for qid, r in respondidas.items() if qid in ids}
        acertos = sum(1 for r in feitas.values() if r["correta"])
        if len(feitas) < len(ids):
            raise HTTPException(
                status_code=400,
                detail=f"Faltam {len(ids) - len(feitas)} questões para concluir a missão.",
            )
        resultado = jornada.concluir_dia(con, aluno_id, dados.dia, acertos, len(ids))
        if resultado.get("concluido") and not resultado.get("ja_estava"):
            atualizado = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
            if resultado.get("proximo"):
                enviar_dia_concluido(
                    con,
                    atualizado,
                    dados.dia,
                    resultado.get("titulo_proximo", ""),
                    resultado.get("pontos", 0),
                )
            if resultado.get("final"):
                enviar_conclusao(con, atualizado)
    return JSONResponse(resultado)


# --- treino livre ----------------------------------------------------------


@router.get("/questoes")
async def treino(
    request: Request,
    aluno=Depends(exigir_aluno),
    materia: str = "",
    nivel: str = "",
    quantidade: int = 10,
):
    aluno_id = int(aluno["id"])
    quantidade = max(5, min(quantidade, 30))
    materias = [materia] if materia in MATERIAS_POR_ID else list(MATERIAS_IDS)
    with sessao() as con:
        total_feitas = estudo.total_respostas(con, aluno_id)
        questoes = selecionar(
            materias,
            quantidade=quantidade,
            nivel=nivel or None,
            semente=aluno_id * 7 + total_feitas,
        )
        caderno = srs.resumo(con, aluno_id)
    return responder_template(
        request,
        "questoes.html",
        {
            "aluno": aluno,
            "questoes": [_serializar_questao(q) for q in questoes],
            "materia": materia,
            "nivel": nivel,
            "quantidade": quantidade,
            "por_materia": {mid: len(lista) for mid, lista in POR_MATERIA.items()},
            "caderno": caderno,
        },
    )


# --- caderno de erros ------------------------------------------------------


@router.get("/erros")
async def caderno(request: Request, aluno=Depends(exigir_aluno), materia: str = ""):
    aluno_id = int(aluno["id"])
    with sessao() as con:
        resumo = srs.resumo(con, aluno_id)
        linhas = srs.abertas(con, aluno_id, materia if materia in MATERIAS_POR_ID else "")
        vencidas = {linha["questao_id"] for linha in srs.vencidas(con, aluno_id, limite=999)}
    itens = []
    for linha in linhas:
        q = buscar_questao(linha["questao_id"])
        if q is None:
            continue
        itens.append(
            {
                "questao": _serializar_questao(q),
                "categoria": linha["categoria"],
                "anotacao": linha["anotacao"],
                "nivel": linha["nivel_srs"],
                "proxima": linha["proxima_revisao"],
                "vencida": linha["questao_id"] in vencidas,
                "acertos_seguidos": linha["acertos_seguidos"],
            }
        )
    return responder_template(
        request,
        "erros.html",
        {"aluno": aluno, "resumo": resumo, "itens": itens, "materia": materia},
    )


@router.get("/erros/revisar")
async def revisar(request: Request, aluno=Depends(exigir_aluno)):
    aluno_id = int(aluno["id"])
    with sessao() as con:
        pendentes = srs.vencidas(con, aluno_id, limite=20)
        questoes = [
            q for q in (buscar_questao(linha["questao_id"]) for linha in pendentes) if q is not None
        ]
        resumo = srs.resumo(con, aluno_id)
    return responder_template(
        request,
        "revisar.html",
        {
            "aluno": aluno,
            "questoes": [_serializar_questao(q) for q in questoes],
            "resumo": resumo,
        },
    )


# --- simulados -------------------------------------------------------------


@router.get("/simulados")
async def lista_simulados(request: Request, aluno=Depends(exigir_aluno)):
    # a lista abre para todos: é ela que mostra o que o upgrade libera.
    # o bloqueio real acontece ao abrir cada simulado, pelo recurso dele.
    aluno_id = int(aluno["id"])
    with sessao() as con:
        resumo = jornada.resumo_jornada(con, aluno_id)
        historico = estudo.historico_simulados(con, aluno_id)
    concluidos = {i["numero"] for i in resumo["dias"] if i["concluido"]}
    liberados = {i["numero"] for i in resumo["dias"] if i["liberado"]}
    itens = []
    for s in conteudo_simulados.SIMULADOS:
        feitos = [h for h in historico if h["simulado_id"] == s.id]
        no_plano = servico_planos.tem_recurso(aluno, s.recurso)
        itens.append(
            {
                "simulado": s,
                "no_plano": no_plano,
                "liberado": no_plano
                and (s.dia_liberacao in liberados or s.dia_liberacao in concluidos),
                "tentativas": feitos,
                "melhor": max((f["pct"] for f in feitos), default=None),
            }
        )
    return responder_template(
        request,
        "simulados.html",
        {"aluno": aluno, "itens": itens, "historico": historico},
    )


@router.get("/simulado/{simulado_id}")
async def abrir_simulado(request: Request, simulado_id: str, aluno=Depends(exigir_aluno)):
    s = conteudo_simulados.simulado(simulado_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Simulado não encontrado")
    # cada simulado diz o recurso que exige — o diagnóstico entra no plano de entrada
    bloqueio = bloqueio_por_plano(request, aluno, s.recurso)
    if bloqueio is not None:
        return bloqueio
    aluno_id = int(aluno["id"])
    with sessao() as con:
        item = jornada.acesso_ao_dia(con, aluno_id, s.dia_liberacao)
        if item is None:
            return responder_template(
                request,
                "bloqueado.html",
                {"aluno": aluno, "dia": trilha.dia(s.dia_liberacao), "custo": config.custo_chave_antecipacao},
                status_code=403,
            )
        sessao_id = estudo.iniciar_simulado(con, aluno_id, simulado_id)
        respostas = estudo.respostas_da_sessao(con, aluno_id, sessao_id) if sessao_id else {}
    questoes = conteudo_simulados.montar(simulado_id)
    return responder_template(
        request,
        "simulado.html",
        {
            "aluno": aluno,
            "s": s,
            "sessao_id": sessao_id,
            "questoes": [_serializar_questao(q) for q in questoes],
            "respostas": respostas,
        },
    )


class FinalizarEntrada(BaseModel):
    sessao_id: int
    duracao_seg: int = 0


@router.post("/api/simulado/finalizar")
async def api_finalizar(dados: FinalizarEntrada, aluno=Depends(exigir_aluno)):
    with sessao() as con:
        resultado = estudo.finalizar_simulado(
            con, int(aluno["id"]), dados.sessao_id, dados.duracao_seg
        )
    if not resultado:
        raise HTTPException(status_code=404, detail="Sessão de simulado não encontrada")
    return JSONResponse(resultado)


@router.get("/simulado/{simulado_id}/relatorio/{sessao_id}")
async def relatorio(request: Request, simulado_id: str, sessao_id: int, aluno=Depends(exigir_aluno)):
    aluno_id = int(aluno["id"])
    with sessao() as con:
        historico = estudo.historico_simulados(con, aluno_id)
    atual = next((h for h in historico if h["id"] == sessao_id), None)
    if atual is None:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    anteriores = [h for h in historico if h["id"] != sessao_id]
    with sessao() as con:
        correcao = estudo.correcao_da_sessao(con, aluno_id, sessao_id)
    return responder_template(
        request,
        "relatorio.html",
        {
            "aluno": aluno,
            "atual": atual,
            "anteriores": anteriores,
            "correcao": correcao,
            "erradas": [i for i in correcao if not i["acertou"]],
            "materias": MATERIAS_POR_ID,
        },
    )


# --- pontos, manual, certificado e conta -----------------------------------


@router.get("/pontos")
async def pontos(request: Request, aluno=Depends(exigir_aluno)):
    aluno_id = int(aluno["id"])
    with sessao() as con:
        medalhas = medalhas_do_aluno(con, aluno_id)
        historico = extrato(con, aluno_id)
        tabela = ranking(con) if servico_planos.tem_recurso(aluno, "ranking") else []
        stats = estatisticas(con, aluno_id)
    return responder_template(
        request,
        "pontos.html",
        {
            "aluno": aluno,
            "medalhas": medalhas,
            "extrato": historico,
            "ranking": tabela,
            "stats": stats,
            "patente": resumo_patente(int(aluno["pontos"])),
        },
    )


@router.get("/manual")
async def ver_manual(request: Request, aluno=Depends(exigir_aluno)):
    bloqueio = bloqueio_por_plano(request, aluno, "manual")
    if bloqueio is not None:
        return bloqueio
    return responder_template(
        request,
        "manual.html",
        {"aluno": aluno, "capitulos": manual.CAPITULOS, "novos": manual.NOVOS},
    )


@router.get("/manual/download")
async def baixar_manual(request: Request, aluno=Depends(exigir_aluno)):
    # o download é a apostila inteira: gatear só a tela de leitura deixaria a
    # porta dos fundos aberta para quem não tem o recurso
    bloqueio = bloqueio_por_plano(request, aluno, "manual")
    if bloqueio is not None:
        return bloqueio
    return PlainTextResponse(
        manual.markdown(),
        headers={
            "Content-Disposition": 'attachment; filename="apostila-edital-pmsp-2026.md"'
        },
    )


@router.get("/certificado")
async def certificado(request: Request, aluno=Depends(exigir_aluno)):
    bloqueio = bloqueio_por_plano(request, aluno, "certificado")
    if bloqueio is not None:
        return bloqueio
    aluno_id = int(aluno["id"])
    with sessao() as con:
        resumo = jornada.resumo_jornada(con, aluno_id)
        stats = estatisticas(con, aluno_id)
    return responder_template(
        request,
        "certificado.html",
        {
            "aluno": aluno,
            "resumo": resumo,
            "stats": stats,
            "liberado": resumo["concluidos"] >= trilha.TOTAL_DIAS,
        },
    )


@router.get("/modulos")
async def lista_modulos(request: Request, aluno=Depends(exigir_aluno)):
    liberado = servico_planos.tem_recurso(aluno, "avancado")
    return responder_template(
        request,
        "modulos.html",
        {
            "aluno": aluno,
            "modulos": catalogo_modulos.ordenados(),
            "liberado": liberado,
            "plano": servico_planos.resumo(aluno),
        },
    )


@router.get("/modulos/{modulo_id}")
async def ver_modulo(request: Request, modulo_id: str, aluno=Depends(exigir_aluno)):
    m = catalogo_modulos.modulo(modulo_id)
    if m is None:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    bloqueio = bloqueio_por_plano(request, aluno, m.recurso)
    if bloqueio is not None:
        return bloqueio
    return responder_template(request, "modulo.html", {"aluno": aluno, "m": m})


# --- notificações e lembretes ----------------------------------------------


@router.get("/avisos")
async def central_de_avisos(request: Request, aluno=Depends(exigir_aluno)):
    with sessao() as con:
        avisos = notificacoes.gerar(con, int(aluno["id"]))
    return responder_template(
        request, "avisos.html", {"aluno": aluno, "avisos": avisos}
    )


class DispensaEntrada(BaseModel):
    chave: str = ""
    todas: bool = False


@router.post("/api/avisos/dispensar")
async def api_dispensar_aviso(dados: DispensaEntrada, aluno=Depends(exigir_aluno)):
    aluno_id = int(aluno["id"])
    with sessao() as con:
        if dados.todas:
            notificacoes.dispensar_todas(con, aluno_id)
        elif dados.chave:
            notificacoes.dispensar(con, aluno_id, dados.chave)
        else:
            raise HTTPException(status_code=400, detail="Informe a chave ou peça todas.")
        restantes = notificacoes.contar(con, aluno_id)
    return JSONResponse({"ok": True, "restantes": restantes})


@router.get("/planos")
async def meus_planos(request: Request, aluno=Depends(exigir_aluno)):
    resumo = servico_planos.resumo(aluno)
    return responder_template(
        request,
        "upgrade.html",
        {
            "aluno": aluno,
            "recurso": "",
            "recurso_nome": "Planos e assinatura",
            "meu_plano": resumo["plano"],
            "vencido": resumo["vencido"],
            "expira_em": resumo["expira_em"],
            "planos": catalogo_planos.PLANOS,
            "checkouts": servico_planos.checkouts(),
        },
    )


@router.get("/conta")
async def conta(request: Request, aluno=Depends(exigir_aluno), aviso: str = ""):
    return responder_template(
        request,
        "conta.html",
        {"aluno": aluno, "aviso": aviso, "plano": servico_planos.resumo(aluno)},
    )


@router.post("/conta/senha")
async def trocar_senha(
    request: Request,
    atual: str = Form(""),
    nova: str = Form(""),
    confirmacao: str = Form(""),
    csrf_token: str = Form(""),
    aluno=Depends(exigir_aluno),
):
    validar_csrf(request, csrf_token)
    if not conferir_senha(atual, aluno["senha_hash"]):
        return redirecionar("/conta?aviso=Senha atual incorreta.")
    if nova != confirmacao:
        return redirecionar("/conta?aviso=As senhas não conferem.")
    problema = validar_senha(nova)
    if problema:
        return redirecionar(f"/conta?aviso={problema}")
    with sessao() as con:
        definir_senha(con, int(aluno["id"]), nova)
    return redirecionar("/entrar?erro=Senha alterada. Entre novamente.")


@router.post("/conta/lembretes")
async def lembretes(
    request: Request, ativo: str = Form(""), csrf_token: str = Form(""), aluno=Depends(exigir_aluno)
):
    validar_csrf(request, csrf_token)
    with sessao() as con:
        executar(
            con,
            "UPDATE alunos SET lembretes_email=? WHERE id=?",
            (1 if ativo == "1" else 0, aluno["id"]),
        )
    return redirecionar("/conta?aviso=Preferência salva.")
