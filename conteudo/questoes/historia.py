"""História Geral e do Brasil — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="hist-001",
        materia="historia",
        tema="Primeira Guerra Mundial",
        nivel="facil",
        enunciado="O estopim da Primeira Guerra Mundial (1914-1918) foi:",
        alternativas=(
            ("A", "a invasão da Polônia pela Alemanha."),
            ("B", "o ataque japonês a Pearl Harbor."),
            ("C", "o assassinato do arquiduque austríaco Francisco Ferdinando."),
            ("D", "a construção do Muro de Berlim."),
            ("E", "a queda da Bastilha."),
        ),
        correta="C",
        comentario=(
            "O assassinato do arquiduque Francisco Ferdinando, herdeiro do trono austro-húngaro, "
            "acionou o sistema de alianças (Tríplice Aliança × Tríplice Entente) e iniciou o "
            "conflito. A invasão da Polônia é o marco da Segunda Guerra."
        ),
        armadilha="Trocar o estopim da Primeira pelo da Segunda Guerra é o erro mais comum do tema.",
    ),
    Questao(
        id="hist-002",
        materia="historia",
        tema="Tratado de Versalhes",
        nivel="medio",
        enunciado=(
            "O Tratado de Versalhes, assinado ao fim da Primeira Guerra Mundial, é apontado como "
            "um dos fatores que levaram à Segunda Guerra porque:"
        ),
        alternativas=(
            ("A", "dividiu a Alemanha em Oriental e Ocidental."),
            ("B", "estabeleceu a aliança entre Alemanha, Itália e Japão."),
            ("C", "criou a Organização das Nações Unidas."),
            ("D", "impôs punições severas à Alemanha, gerando crise e ressentimento."),
            ("E", "garantiu reparações à Alemanha pelas perdas sofridas."),
        ),
        correta="D",
        comentario=(
            "As reparações e as perdas territoriais impostas à Alemanha aprofundaram a crise "
            "econômica e o ressentimento nacional, terreno em que o nazismo cresceu. A divisão da "
            "Alemanha veio depois da Segunda Guerra; a ONU foi criada em 1945."
        ),
        armadilha="Confundir consequências da Primeira com consequências da Segunda Guerra.",
    ),
    Questao(
        id="hist-003",
        materia="historia",
        tema="Nazifascismo",
        nivel="medio",
        enunciado="São características comuns ao nazismo alemão e ao fascismo italiano:",
        alternativas=(
            ("A", "pluripartidarismo, liberdade de imprensa e economia planificada."),
            ("B", "neutralidade nas relações internacionais e desarmamento."),
            ("C", "defesa do internacionalismo proletário e fim da propriedade privada."),
            ("D", "descentralização do poder e ampliação dos direitos civis."),
            ("E", "nacionalismo extremo, culto ao líder e perseguição a minorias."),
        ),
        correta="E",
        comentario=(
            "Nazismo (Hitler) e fascismo (Mussolini) são regimes autoritários marcados por "
            "nacionalismo extremo, culto ao líder, partido único e perseguição a minorias — no caso "
            "alemão, com o Holocausto contra os judeus."
        ),
        armadilha="A alternativa (C) descreve o comunismo, ideologia oposta à desses regimes.",
    ),
    Questao(
        id="hist-004",
        materia="historia",
        tema="Segunda Guerra Mundial",
        nivel="facil",
        enunciado="A Segunda Guerra Mundial (1939-1945) terminou com:",
        alternativas=(
            ("A", "a derrota do Eixo — Alemanha, Itália e Japão — pelos Aliados."),
            ("B", "a vitória do Eixo sobre os Aliados."),
            ("C", "um acordo de paz sem vencedores, assinado em Versalhes."),
            ("D", "a anexação da França pela União Soviética."),
            ("E", "a independência das colônias africanas."),
        ),
        correta="A",
        comentario=(
            "O Eixo (Alemanha, Itália e Japão) foi derrotado pelos Aliados. A rendição alemã "
            "ocorreu em maio de 1945 e a japonesa em setembro, após as bombas atômicas."
        ),
        armadilha="Versalhes encerrou a Primeira Guerra, não a Segunda.",
    ),
    Questao(
        id="hist-005",
        materia="historia",
        tema="Guerra Fria",
        nivel="medio",
        enunciado="A Guerra Fria (1947-1991) caracterizou-se por:",
        alternativas=(
            ("A", "confronto militar direto e permanente entre Estados Unidos e União Soviética."),
            ("B", "tensão entre EUA e URSS sem confronto militar direto, com corrida armamentista, "
                  "corrida espacial e conflitos indiretos."),
            ("C", "aliança militar entre Estados Unidos e União Soviética contra a China."),
            ("D", "isolamento econômico completo entre os países do bloco capitalista."),
            ("E", "predomínio de governos socialistas em toda a Europa Ocidental."),
        ),
        correta="B",
        comentario=(
            "A expressão 'fria' vem justamente da ausência de confronto direto entre as duas "
            "superpotências. A disputa se deu por armamentos, espaço, áreas de influência e "
            "conflitos indiretos, como as guerras da Coreia e do Vietnã."
        ),
        armadilha="Se houvesse guerra declarada entre EUA e URSS, não seria 'fria'.",
    ),
    Questao(
        id="hist-006",
        materia="historia",
        tema="Guerra Fria: Alemanha",
        nivel="medio",
        enunciado="A divisão da Alemanha em Oriental e Ocidental, no pós-guerra, resultou:",
        alternativas=(
            ("A", "do Tratado de Versalhes, em 1919."),
            ("B", "de um plebiscito realizado entre os alemães em 1961."),
            ("C", "da disputa entre os blocos capitalista e socialista após a Segunda Guerra."),
            ("D", "da unificação alemã promovida por Bismarck."),
            ("E", "da adesão da Alemanha à União Europeia."),
        ),
        correta="C",
        comentario=(
            "Derrotada, a Alemanha foi ocupada pelos vencedores e acabou dividida entre a República "
            "Federal (ocidental, capitalista) e a República Democrática (oriental, socialista). O "
            "Muro de Berlim (1961-1989) tornou-se o símbolo dessa divisão."
        ),
        armadilha="Bismarck unificou a Alemanha no século 19 — movimento oposto ao da divisão.",
    ),
    Questao(
        id="hist-007",
        materia="historia",
        tema="Revolução de 1930",
        nivel="medio",
        enunciado="A Revolução de 1930, que levou Getúlio Vargas ao poder, encerrou:",
        alternativas=(
            ("A", "o Império e a monarquia no Brasil."),
            ("B", "o regime militar iniciado em 1964."),
            ("C", "o Estado Novo e a ditadura varguista."),
            ("D", "a República Velha, dominada pelas oligarquias agrárias."),
            ("E", "o período colonial português."),
        ),
        correta="D",
        comentario=(
            "O movimento armado de 1930 encerrou a República Velha, marcada pelo domínio das "
            "oligarquias agrárias de São Paulo e Minas Gerais. O Estado Novo (1937-1945) veio "
            "depois, dentro da própria Era Vargas."
        ),
        armadilha="O Estado Novo é parte da Era Vargas, não algo que 1930 encerrou.",
    ),
    Questao(
        id="hist-008",
        materia="historia",
        tema="Era Vargas",
        nivel="medio",
        enunciado="São marcas da Era Vargas (1930-1945):",
        alternativas=(
            ("A", "criação da Constituição de 1988."),
            ("B", "abertura total da economia e privatização das estatais."),
            ("C", "eleições diretas ininterruptas e ampla liberdade de imprensa."),
            ("D", "fim do voto feminino e retorno da monarquia."),
            ("E", "leis trabalhistas, industrialização e o período autoritário do Estado Novo."),
        ),
        correta="E",
        comentario=(
            "A Era Vargas combinou avanços trabalhistas e industrialização com autoritarismo, "
            "sobretudo no Estado Novo (1937-1945), quando houve censura e fechamento do Congresso. "
            "O voto feminino, aliás, foi instituído em 1932, nesse período."
        ),
        armadilha="A alternativa (B) descreve políticas neoliberais dos anos 1990.",
    ),
    Questao(
        id="hist-009",
        materia="historia",
        tema="Constituições republicanas",
        nivel="dificil",
        enunciado="A Constituição de 1937, outorgada por Getúlio Vargas, caracterizou-se por:",
        alternativas=(
            ("A", "instaurar o regime autoritário do Estado Novo, com concentração de poder."),
            ("B", "ser a primeira constituição republicana do Brasil."),
            ("C", "restabelecer a democracia após o regime militar."),
            ("D", "ser conhecida como 'Constituição Cidadã'."),
            ("E", "criar o parlamentarismo como sistema de governo definitivo."),
        ),
        correta="A",
        comentario=(
            "A Carta de 1937 foi outorgada (imposta, não votada) e sustentou o Estado Novo. A "
            "primeira republicana é a de 1891; a 'Constituição Cidadã' é a de 1988."
        ),
        armadilha="Outorgada x promulgada: a banca cobra essa diferença com frequência.",
    ),
    Questao(
        id="hist-010",
        materia="historia",
        tema="Regime militar",
        nivel="medio",
        enunciado="O Ato Institucional nº 5 (AI-5), de 1968, ficou marcado por:",
        alternativas=(
            ("A", "convocar eleições diretas para presidente."),
            ("B", "suspender direitos civis, fechar o Congresso e ampliar a censura."),
            ("C", "conceder anistia aos exilados políticos."),
            ("D", "promulgar a Constituição de 1988."),
            ("E", "encerrar o regime militar."),
        ),
        correta="B",
        comentario=(
            "O AI-5 foi o mais duro dos atos institucionais: fechou o Congresso, suspendeu o habeas "
            "corpus para crimes políticos, cassou mandatos e institucionalizou a censura, abrindo o "
            "período mais repressivo do regime."
        ),
        armadilha="A anistia veio em 1979, mais de dez anos depois, já na abertura política.",
    ),
    Questao(
        id="hist-011",
        materia="historia",
        tema="Redemocratização",
        nivel="medio",
        enunciado="Assinale a alternativa que apresenta fatos da abertura política brasileira em ordem cronológica:",
        alternativas=(
            ("A", "Diretas Já (1984) → Lei da Anistia (1979) → Constituição de 1988."),
            ("B", "Constituição de 1988 → Lei da Anistia (1979) → Diretas Já (1984)."),
            ("C", "Lei da Anistia (1979) → Diretas Já (1984) → Constituição de 1988."),
            ("D", "Lei da Anistia (1979) → Constituição de 1988 → Diretas Já (1984)."),
            ("E", "Diretas Já (1984) → Constituição de 1988 → Lei da Anistia (1979)."),
        ),
        correta="C",
        comentario=(
            "A sequência é: Lei da Anistia (1979), movimento das Diretas Já (1984), eleição indireta "
            "de Tancredo Neves (1985) e promulgação da Constituição de 1988."
        ),
        armadilha="Questão de ordenação: fixe a linha do tempo e ela se resolve sozinha.",
    ),
    Questao(
        id="hist-012",
        materia="historia",
        tema="Globalização e neoliberalismo",
        nivel="medio",
        enunciado="As políticas neoliberais, associadas ao avanço da globalização, defendem:",
        alternativas=(
            ("A", "ampliação da intervenção do Estado e estatização de empresas."),
            ("B", "controle estatal dos preços em todos os setores."),
            ("C", "fechamento das fronteiras ao comércio internacional."),
            ("D", "redução da intervenção estatal na economia, privatizações e abertura de mercados."),
            ("E", "coletivização da propriedade rural."),
        ),
        correta="D",
        comentario=(
            "O receituário neoliberal, difundido a partir dos anos 1980-1990, propõe Estado menor "
            "na economia, privatizações, desregulamentação e abertura comercial — movimento que "
            "acompanhou a intensificação da globalização."
        ),
        armadilha="Globalização não é sinônimo de neoliberalismo: uma é processo, o outro é política.",
    ),
    Questao(
        id="hist-013",
        materia="historia",
        tema="Nova República",
        nivel="medio",
        enunciado=(
            "Eleito presidente pelo Colégio Eleitoral em 1985, marcando o fim do regime militar, "
            "adoeceu na véspera da posse e morreu sem assumir o cargo, que foi ocupado por seu vice. "
            "O texto refere-se a:"
        ),
        alternativas=(
            ("A", "Juscelino Kubitschek."),
            ("B", "Tancredo Neves."),
            ("C", "João Goulart."),
            ("D", "Ulysses Guimarães."),
            ("E", "Fernando Collor de Mello."),
        ),
        correta="B",
        comentario=(
            "<strong>Tancredo Neves</strong> foi eleito indiretamente em janeiro de 1985 e morreu em "
            "21 de abril, sem tomar posse. Assumiu o vice, <strong>José Sarney</strong>, iniciando a "
            "Nova República. Ulysses Guimarães presidiu a Assembleia Constituinte de 1988; Collor foi "
            "o primeiro presidente eleito por voto direto depois do regime militar, em 1989."
        ),
        armadilha=(
            "A eleição de Tancredo foi indireta, pelo Colégio Eleitoral — a primeira direta para "
            "presidente só veio em 1989. Confundir as duas é o erro mais comum do período."
        ),
    ),
    Questao(
        id="hist-014",
        materia="historia",
        tema="Movimentos sociais nos anos 1970",
        nivel="dificil",
        enunciado=(
            "Durante a década de 1970, sob o regime militar, surgiram movimentos populares "
            "organizados a partir de clubes de mães e de comunidades eclesiais de base, que "
            "denunciavam a alta dos preços e a perda do poder de compra. Esses movimentos:"
        ),
        alternativas=(
            ("A", "eram promovidos pelo próprio governo, para apoiar o milagre econômico."),
            ("B", "restringiram-se ao meio rural e não tiveram expressão nas periferias urbanas."),
            ("C", "defendiam o retorno da monarquia como solução para a crise."),
            ("D", "expressaram, na periferia urbana, a insatisfação com a carestia e ajudaram a "
                  "reorganizar a sociedade civil no processo de abertura política."),
            ("E", "foram criados após a Constituição de 1988, já em plena democracia."),
        ),
        correta="D",
        comentario=(
            "Com partidos e sindicatos sob forte controle, a mobilização encontrou espaço nas igrejas "
            "e nas associações de bairro. O <strong>Movimento do Custo de Vida</strong>, nascido na "
            "periferia de São Paulo, é o exemplo mais conhecido: reuniu assinaturas contra a carestia "
            "e formou lideranças que depois atuariam em partidos e sindicatos da redemocratização."
        ),
        armadilha=(
            "A data importa: são movimentos <em>anteriores</em> à abertura, e parte da causa dela — "
            "não uma consequência da Constituição de 1988."
        ),
    ),
]
