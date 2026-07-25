"""Direito Penal — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="pen-001",
        materia="penal",
        tema="Princípio da legalidade",
        nivel="facil",
        enunciado=(
            "«Não há crime sem lei anterior que o defina, nem pena sem prévia cominação legal.» "
            "Esse enunciado, previsto no art. 1º do Código Penal, consagra o princípio da:"
        ),
        alternativas=(
            ("A", "insignificância."),
            ("B", "legalidade (ou reserva legal)."),
            ("C", "adequação social."),
            ("D", "intervenção mínima."),
            ("E", "territorialidade."),
        ),
        correta="B",
        comentario=(
            "É o princípio da legalidade, também chamado de reserva legal, previsto no art. 1º do "
            "CP e no art. 5º, XXXIX, da CF. Dele decorre a anterioridade da lei penal."
        ),
        armadilha="Insignificância e intervenção mínima são princípios reais, mas de outro conteúdo.",
    ),
    Questao(
        id="pen-002",
        materia="penal",
        tema="Lei penal no tempo",
        nivel="medio",
        enunciado="Sobre a aplicação da lei penal no tempo, é correto afirmar:",
        alternativas=(
            ("A", "A lei posterior mais severa aplica-se a fatos anteriores à sua vigência."),
            ("B", "A lei penal nunca retroage."),
            ("C", "A lei posterior que de qualquer modo favorece o agente aplica-se aos fatos "
                  "anteriores, ainda que decididos por sentença condenatória transitada em julgado."),
            ("D", "A retroatividade benéfica depende de pedido do Ministério Público."),
            ("E", "A abolição do crime não afeta condenações já em execução."),
        ),
        correta="C",
        comentario=(
            "Art. 2º, parágrafo único, do CP: a lei mais benéfica retroage e alcança inclusive a "
            "coisa julgada. Já a lei mais severa é irretroativa (art. 5º, XL, da CF)."
        ),
        armadilha="A alternativa (B) parece um princípio, mas ignora a exceção benéfica.",
    ),
    Questao(
        id="pen-003",
        materia="penal",
        tema="Furto e roubo",
        nivel="medio",
        enunciado=(
            "A diferença essencial entre os crimes de furto (art. 155 do CP) e roubo (art. 157 do "
            "CP) está:"
        ),
        alternativas=(
            ("A", "no valor da coisa subtraída."),
            ("B", "no emprego de grave ameaça ou violência à pessoa, presente no roubo."),
            ("C", "no local em que ocorre a subtração."),
            ("D", "na quantidade de agentes envolvidos."),
            ("E", "no fato de o roubo exigir arrombamento de obstáculo."),
        ),
        correta="B",
        comentario=(
            "Furto é a subtração de coisa alheia móvel sem violência ou grave ameaça à pessoa. O "
            "roubo acrescenta violência, grave ameaça ou qualquer meio que reduza a capacidade de "
            "resistência da vítima."
        ),
        armadilha="Rompimento de obstáculo é qualificadora do FURTO, não elemento do roubo.",
    ),
    Questao(
        id="pen-004",
        materia="penal",
        tema="Extorsão",
        nivel="dificil",
        enunciado=(
            "Agente constrange a vítima, mediante grave ameaça, a entregar a senha do cartão para "
            "que ele mesmo realize saques posteriores. A conduta, em regra, configura:"
        ),
        alternativas=(
            ("A", "furto qualificado."),
            ("B", "roubo próprio."),
            ("C", "extorsão."),
            ("D", "estelionato."),
            ("E", "apropriação indébita."),
        ),
        correta="C",
        comentario=(
            "Na extorsão (art. 158), a vítima é constrangida a fazer, tolerar que se faça ou deixar "
            "de fazer algo — a colaboração dela é imprescindível. No roubo, o agente subtrai "
            "diretamente o bem; a participação da vítima é dispensável."
        ),
        armadilha="Roubo x extorsão: pergunte-se se a vítima precisou colaborar para o crime se consumar.",
    ),
    Questao(
        id="pen-005",
        materia="penal",
        tema="Excludentes de ilicitude",
        nivel="medio",
        enunciado="Não há crime quando o agente pratica o fato (art. 23 do CP):",
        alternativas=(
            ("A", "em estado de necessidade, legítima defesa, estrito cumprimento de dever legal ou "
                  "exercício regular de direito."),
            ("B", "sob coação moral irresistível ou obediência hierárquica."),
            ("C", "em erro de proibição inevitável."),
            ("D", "por inimputabilidade decorrente de doença mental."),
            ("E", "em razão de arrependimento posterior."),
        ),
        correta="A",
        comentario=(
            "O art. 23 traz as excludentes de ILICITUDE. Coação moral irresistível, obediência "
            "hierárquica, erro de proibição inevitável e doença mental excluem a CULPABILIDADE — "
            "o crime existe, mas o agente não é reprovável."
        ),
        armadilha="Excludente de ilicitude ≠ excludente de culpabilidade. A banca vive nessa troca.",
    ),
    Questao(
        id="pen-006",
        materia="penal",
        tema="Legítima defesa",
        nivel="medio",
        enunciado="Age em legítima defesa quem:",
        alternativas=(
            ("A", "repele agressão futura e incerta, usando qualquer meio."),
            ("B", "usando moderadamente dos meios necessários, repele injusta agressão, atual ou "
                  "iminente, a direito seu ou de outrem."),
            ("C", "revida agressão já cessada, para punir o agressor."),
            ("D", "provoca a agressão para depois revidar."),
            ("E", "utiliza meios desproporcionais, desde que a agressão seja injusta."),
        ),
        correta="B",
        comentario=(
            "Art. 25 do CP. São requisitos cumulativos: agressão injusta, atual ou iminente; "
            "direito próprio ou de terceiro; meios necessários; e moderação no uso. Faltando a "
            "moderação, há excesso punível."
        ),
        armadilha="Agressão 'já cessada' transforma defesa em vingança — e vingança é crime.",
    ),
    Questao(
        id="pen-007",
        materia="penal",
        tema="Crimes contra a Administração",
        nivel="dificil",
        enunciado=(
            "O funcionário público que se apropria de dinheiro de que tem a posse em razão do cargo "
            "comete:"
        ),
        alternativas=(
            ("A", "concussão."),
            ("B", "corrupção passiva."),
            ("C", "peculato."),
            ("D", "prevaricação."),
            ("E", "advocacia administrativa."),
        ),
        correta="C",
        comentario=(
            "Peculato (art. 312). Concussão é exigir vantagem indevida; corrupção passiva é "
            "solicitar ou receber; prevaricação é retardar ou deixar de praticar ato de ofício "
            "para satisfazer interesse ou sentimento pessoal."
        ),
        armadilha="Exigir (concussão) x solicitar/receber (corrupção passiva) x apropriar-se (peculato).",
    ),
    Questao(
        id="pen-008",
        materia="penal",
        tema="Desacato, resistência e desobediência",
        nivel="medio",
        enunciado=(
            "O particular que se opõe à execução de ato legal, mediante violência ou ameaça a "
            "funcionário competente, comete o crime de:"
        ),
        alternativas=(
            ("A", "desobediência."),
            ("B", "desacato."),
            ("C", "resistência."),
            ("D", "constrangimento ilegal."),
            ("E", "ameaça."),
        ),
        correta="C",
        comentario=(
            "Resistência (art. 329) exige violência ou ameaça contra funcionário. Desobediência "
            "(art. 330) é o descumprimento de ordem legal sem violência. Desacato (art. 331) é "
            "ofender a dignidade ou o decoro do funcionário no exercício da função."
        ),
        armadilha="Sem violência ou ameaça, não é resistência: é desobediência.",
    ),
    Questao(
        id="pen-009",
        materia="penal",
        tema="Territorialidade",
        nivel="medio",
        enunciado="Sobre a aplicação da lei penal no espaço, é correto afirmar:",
        alternativas=(
            ("A", "Adota-se a territorialidade absoluta, sem exceções."),
            ("B", "Adota-se a territorialidade temperada, aplicando-se a lei brasileira ao crime "
                  "cometido no território nacional, sem prejuízo de convenções e tratados."),
            ("C", "A lei brasileira jamais se aplica a crime cometido no exterior."),
            ("D", "Aeronaves e embarcações brasileiras no exterior nunca são consideradas extensão "
                  "do território nacional."),
            ("E", "Aplica-se apenas a lei do país de nacionalidade do autor."),
        ),
        correta="B",
        comentario=(
            "Art. 5º do CP: aplica-se a lei brasileira ao crime cometido no território nacional, "
            "'sem prejuízo de convenções, tratados e regras de direito internacional' — daí a "
            "expressão territorialidade temperada. O art. 7º prevê hipóteses de extraterritorialidade."
        ),
        armadilha="A palavra 'absoluta' na alternativa (A) é o sinal de alerta.",
    ),
    Questao(
        id="pen-010",
        materia="penal",
        tema="Crimes contra a pessoa",
        nivel="facil",
        enunciado=(
            "Ofender a integridade corporal ou a saúde de outrem configura o crime de:"
        ),
        alternativas=(
            ("A", "homicídio tentado."),
            ("B", "lesão corporal."),
            ("C", "vias de fato."),
            ("D", "maus-tratos."),
            ("E", "periclitação da vida."),
        ),
        correta="B",
        comentario=(
            "É a definição literal do art. 129 do CP (lesão corporal). Vias de fato é contravenção "
            "penal, quando não há lesão; o homicídio tentado exige o dolo de matar."
        ),
        armadilha="O que separa lesão de tentativa de homicídio é a intenção (dolo), não o resultado.",
    ),
    Questao(
        id="pen-011",
        materia="penal",
        tema="Tentativa",
        nivel="medio",
        enunciado="Sobre a tentativa (art. 14, II, do CP), assinale a alternativa correta.",
        alternativas=(
            ("A", "Ocorre quando o agente desiste voluntariamente de prosseguir na execução."),
            ("B", "Ocorre quando, iniciada a execução, o crime não se consuma por circunstâncias "
                  "alheias à vontade do agente."),
            ("C", "É punida sempre com a mesma pena do crime consumado."),
            ("D", "Aplica-se a todos os crimes, inclusive aos culposos."),
            ("E", "Depende de confissão do agente."),
        ),
        correta="B",
        comentario=(
            "A tentativa exige início de execução e não consumação por causas alheias à vontade do "
            "agente; a pena é a do crime consumado reduzida de um a dois terços. Se a interrupção "
            "for voluntária, há desistência voluntária (art. 15). Crimes culposos não admitem tentativa."
        ),
        armadilha="Desistência voluntária x tentativa: a diferença está em quem interrompeu a execução.",
    ),
    Questao(
        id="pen-012",
        materia="penal",
        tema="Concurso de pessoas",
        nivel="dificil",
        enunciado="Quanto ao concurso de pessoas, é correto afirmar:",
        alternativas=(
            ("A", "Todos os que concorrem para o crime respondem sempre com penas idênticas."),
            ("B", "Quem, de qualquer modo, concorre para o crime incide nas penas a este cominadas, "
                  "na medida de sua culpabilidade."),
            ("C", "A participação de menor importância impede a punição do partícipe."),
            ("D", "O ajuste e a instigação são puníveis mesmo que o crime não chegue a ser tentado."),
            ("E", "Somente o autor material responde pelo delito."),
        ),
        correta="B",
        comentario=(
            "Art. 29 do CP. A responsabilidade é individualizada pela culpabilidade; a participação "
            "de menor importância reduz a pena de um sexto a um terço (§ 1º). O ajuste, a "
            "determinação ou a instigação não são puníveis se o crime não chega ao menos a ser "
            "tentado (art. 31)."
        ),
        armadilha="'Sempre penas idênticas' ignora a individualização — palavra absoluta, alternativa falsa.",
    ),
]
