"""Apostila Explicativa — Edital PM-SP 2026 em 7 dias, em formato de leitura.

Os capítulos são montados a partir da própria trilha: o texto que o aluno lê no
Dia 3 é exatamente o texto do capítulo 3 da apostila. Isso evita a armadilha
clássica de manter dois conteúdos parecidos que, com o tempo, divergem.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import edital, trilha


@dataclass(frozen=True)
class Capitulo:
    id: str
    numero: str
    titulo: str
    resumo: str
    paragrafos: tuple[str, ...]
    destaque: str = ""
    novo: bool = False
    lista: tuple[str, ...] = field(default_factory=tuple)


def _reais(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


ABERTURA = Capitulo(
    id="abertura",
    numero="Abertura",
    titulo="Como usar esta apostila",
    resumo="Entender o assunto vale mais do que memorizar conteúdo em excesso.",
    paragrafos=(
        "Esta apostila explica cada tópico do edital do concurso de "
        f"<strong>{edital.CONCURSO}</strong> de forma clara e didática. O objetivo é que você "
        "<strong>entenda</strong> o assunto — e não decore conteúdo em excesso, correndo o risco "
        "de esquecer tudo antes mesmo de terminar a leitura.",
        f"São <strong>{edital.VAGAS} vagas</strong>, banca {edital.BANCA} e salário inicial de "
        f"R$ {_reais(edital.SALARIO_INICIAL)}. A prova objetiva tem "
        f"<strong>{edital.TOTAL_QUESTOES_PROVA} questões</strong> e exige no mínimo "
        f"{edital.NOTA_MINIMA} pontos para o candidato seguir no concurso.",
        "Cada dia cobre uma grande área do edital. Leia a explicação completa e depois volte aos "
        "tópicos que achar mais difíceis antes de seguir para o próximo dia. Nesta reta final, "
        "foque em resolver questões e revisar aquelas que errou — é isso que fixa.",
    ),
    destaque="Entenda primeiro. Depois resolva questão. Só então revise o erro.",
    lista=tuple(f"{nome} — {q} questões na prova" for _, nome, q in edital.PROVA_OBJETIVA),
)

FECHAMENTO = Capitulo(
    id="revisao-final",
    numero="Encerramento",
    titulo="Revisão final e próximos passos",
    resumo="Agora que você entendeu o porquê de cada assunto, o que fixa é a prática.",
    paragrafos=(
        "Você percorreu o edital inteiro. O próximo passo não é reler tudo: é resolver questões "
        "sobre cada tópico e revisar as que errou. Reler dá sensação de aprendizado; responder dá "
        "aprendizado.",
        "Volte a este material sempre que tiver dúvida sobre um conceito específico — ele é "
        "referência de consulta, não leitura corrida. E use o Caderno de Erros: cada questão que "
        "sai de lá como dominada é um erro a menos no dia da prova.",
        "A prova objetiva é só a primeira etapa. Depois dela vêm redação, teste físico, exames de "
        "saúde, avaliação psicológica e investigação social — todas eliminatórias. Quem se organiza "
        "para elas desde agora não é pego de surpresa.",
    ),
    destaque="Boa prova. Com método e disciplina, a vaga é consequência do processo.",
    lista=tuple(f"{e.nome} — {e.descricao}" for e in edital.ETAPAS),
)


def _capitulo_do_dia(dia: trilha.Dia) -> Capitulo:
    return Capitulo(
        id=f"dia-{dia.numero}",
        numero=f"Dia {dia.numero}",
        titulo=dia.titulo,
        resumo=dia.promessa,
        paragrafos=dia.aula,
        destaque=dia.chave,
    )


CAPITULOS: tuple[Capitulo, ...] = (
    (ABERTURA,) + tuple(_capitulo_do_dia(d) for d in trilha.DIAS) + (FECHAMENTO,)
)

POR_ID = {c.id: c for c in CAPITULOS}
TOTAL_CAPITULOS = len(CAPITULOS)
NOVOS = 0


def markdown() -> str:
    """Exporta a apostila completa em Markdown (download do aluno)."""
    linhas = [
        "# Apostila Explicativa — Edital PM-SP 2026 em 7 Dias",
        "",
        f"*{edital.CONCURSO}*",
        "",
        f"Banca: {edital.BANCA} · {edital.VAGAS} vagas · prova em "
        f"{edital.DATA_PROVA.strftime('%d/%m/%Y')}",
        "",
        "---",
        "",
    ]
    for capitulo in CAPITULOS:
        linhas.append(f"## {capitulo.numero} — {capitulo.titulo}")
        linhas.append("")
        linhas.append(f"*{capitulo.resumo}*")
        linhas.append("")
        for paragrafo in capitulo.paragrafos:
            texto = (
                paragrafo.replace("<strong>", "**")
                .replace("</strong>", "**")
                .replace("<em>", "*")
                .replace("</em>", "*")
            )
            linhas.extend([texto, ""])
        for item in capitulo.lista:
            linhas.append(f"- {item}")
        if capitulo.lista:
            linhas.append("")
        if capitulo.destaque:
            linhas.extend([f"> {capitulo.destaque}", ""])
        linhas.extend(["---", ""])
    return "\n".join(linhas)
