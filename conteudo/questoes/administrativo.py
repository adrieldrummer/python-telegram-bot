"""Direito Administrativo — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="adm-001",
        materia="administrativo",
        tema="Princípios da Administração Pública",
        nivel="facil",
        enunciado=(
            "O art. 37, caput, da Constituição Federal impõe à Administração Pública direta e "
            "indireta a observância dos princípios de:"
        ),
        alternativas=(
            ("A", "legalidade, impessoalidade, moralidade, publicidade e eficiência."),
            ("B", "legalidade, isonomia, motivação, proporcionalidade e economicidade."),
            ("C", "supremacia do interesse público, autotutela, especialidade e continuidade."),
            ("D", "hierarquia, disciplina, moralidade, celeridade e transparência."),
            ("E", "legalidade, publicidade, oportunidade, conveniência e eficácia."),
        ),
        correta="A",
        comentario=(
            "São os cinco princípios expressos, lembrados pela sigla LIMPE. Os demais citados "
            "existem, mas como princípios implícitos ou infraconstitucionais."
        ),
        armadilha="Distratores misturam princípios implícitos verdadeiros com os expressos.",
    ),
    Questao(
        id="adm-002",
        materia="administrativo",
        tema="Anulação e revogação",
        nivel="medio",
        enunciado="Sobre o desfazimento dos atos administrativos, é correto afirmar:",
        alternativas=(
            ("A", "A anulação decorre de conveniência e oportunidade e opera efeitos ex nunc."),
            ("B", "A revogação atinge ato ilegal e opera efeitos ex tunc."),
            ("C", "A anulação atinge ato ilegal e, em regra, opera efeitos retroativos (ex tunc)."),
            ("D", "Somente o Poder Judiciário pode anular atos da Administração."),
            ("E", "Atos vinculados podem ser revogados a qualquer tempo."),
        ),
        correta="C",
        comentario=(
            "Anulação = vício de legalidade, efeitos retroativos (ex tunc). Revogação = ato "
            "legal que se tornou inconveniente ou inoportuno, efeitos a partir da decisão (ex "
            "nunc). Pela autotutela (Súmula 473 do STF), a própria Administração anula e revoga "
            "seus atos. Atos vinculados não comportam revogação."
        ),
        armadilha="Trocar os efeitos temporais é o erro mais frequente nesse tema.",
    ),
    Questao(
        id="adm-003",
        materia="administrativo",
        tema="Atributos do ato administrativo",
        nivel="medio",
        enunciado=(
            "O atributo que permite à Administração executar diretamente suas decisões, sem "
            "necessidade de prévia autorização judicial, denomina-se:"
        ),
        alternativas=(
            ("A", "presunção de legitimidade."),
            ("B", "imperatividade."),
            ("C", "autoexecutoriedade."),
            ("D", "tipicidade."),
            ("E", "discricionariedade."),
        ),
        correta="C",
        comentario=(
            "Autoexecutoriedade é a possibilidade de execução direta e imediata pela própria "
            "Administração. Imperatividade é a imposição unilateral de obrigações; presunção de "
            "legitimidade é a presunção relativa de validade e veracidade."
        ),
        armadilha="Imperatividade e autoexecutoriedade parecem sinônimos, mas uma impõe e a outra executa.",
    ),
    Questao(
        id="adm-004",
        materia="administrativo",
        tema="Elementos do ato administrativo",
        nivel="medio",
        enunciado="São elementos (requisitos) do ato administrativo:",
        alternativas=(
            ("A", "competência, finalidade, forma, motivo e objeto."),
            ("B", "sujeito, culpa, nexo causal, dano e resultado."),
            ("C", "legalidade, mérito, oportunidade, conveniência e eficácia."),
            ("D", "hierarquia, disciplina, polícia, regulamentar e vinculado."),
            ("E", "presunção, imperatividade, tipicidade, exigibilidade e coercibilidade."),
        ),
        correta="A",
        comentario=(
            "São cinco os elementos: competência, finalidade, forma, motivo e objeto. Competência, "
            "finalidade e forma são sempre vinculados; motivo e objeto podem ser discricionários — "
            "é aí que reside o mérito administrativo."
        ),
        armadilha="A alternativa (E) lista atributos, não elementos.",
    ),
    Questao(
        id="adm-005",
        materia="administrativo",
        tema="Poder de polícia",
        nivel="medio",
        enunciado="Sobre o poder de polícia administrativa, assinale a alternativa correta.",
        alternativas=(
            ("A", "Tem por objetivo punir o servidor faltoso."),
            ("B", "Condiciona e restringe o uso de bens, atividades e direitos individuais em "
                  "benefício do interesse público."),
            ("C", "Somente pode ser exercido mediante autorização judicial prévia."),
            ("D", "É privativo do Poder Legislativo."),
            ("E", "Aplica-se exclusivamente a servidores públicos federais."),
        ),
        correta="B",
        comentario=(
            "O poder de polícia limita o exercício de direitos individuais em favor da coletividade "
            "(ex.: fiscalização de trânsito, sanitária, ambiental). Punir servidor faltoso é poder "
            "disciplinar."
        ),
        armadilha="Confundir poder de polícia (dirigido ao particular) com poder disciplinar (interno).",
    ),
    Questao(
        id="adm-006",
        materia="administrativo",
        tema="Poder hierárquico e disciplinar",
        nivel="facil",
        enunciado=(
            "O poder que permite ao superior distribuir funções, fiscalizar, delegar e avocar "
            "atribuições dentro da estrutura administrativa é o poder:"
        ),
        alternativas=(
            ("A", "de polícia."),
            ("B", "regulamentar."),
            ("C", "disciplinar."),
            ("D", "hierárquico."),
            ("E", "vinculado."),
        ),
        correta="D",
        comentario=(
            "O poder hierárquico organiza a estrutura interna: ordenar, fiscalizar, rever, delegar "
            "e avocar. Do descumprimento das ordens nasce o poder disciplinar, que aplica sanções."
        ),
        armadilha="Delegar e avocar são hierárquicos; punir é disciplinar — a banca troca os dois.",
    ),
    Questao(
        id="adm-007",
        materia="administrativo",
        tema="Responsabilidade civil do Estado",
        nivel="dificil",
        enunciado=(
            "Conforme o art. 37, § 6º, da CF, a responsabilidade das pessoas jurídicas de direito "
            "público por danos causados por seus agentes a terceiros é:"
        ),
        alternativas=(
            ("A", "subjetiva, exigindo prova de dolo ou culpa do agente pela vítima."),
            ("B", "objetiva, assegurado o direito de regresso contra o agente responsável nos casos "
                  "de dolo ou culpa."),
            ("C", "objetiva, vedado o direito de regresso."),
            ("D", "solidária com o agente, em qualquer hipótese."),
            ("E", "inexistente quando o dano decorre de ato omissivo."),
        ),
        correta="B",
        comentario=(
            "A vítima não precisa provar dolo ou culpa: basta conduta, dano e nexo causal "
            "(responsabilidade objetiva, teoria do risco administrativo). O Estado, depois, pode "
            "cobrar do agente em ação de regresso, aí sim provando dolo ou culpa."
        ),
        armadilha="Trocar a relação Estado-vítima (objetiva) pela relação Estado-agente (subjetiva).",
    ),
    Questao(
        id="adm-008",
        materia="administrativo",
        tema="Administração direta e indireta",
        nivel="medio",
        enunciado="Integram a Administração Pública indireta:",
        alternativas=(
            ("A", "os Ministérios e as Secretarias de Estado."),
            ("B", "as autarquias, fundações públicas, empresas públicas e sociedades de economia mista."),
            ("C", "as organizações sociais e os cartórios extrajudiciais."),
            ("D", "os órgãos públicos sem personalidade jurídica própria."),
            ("E", "as concessionárias e permissionárias de serviço público."),
        ),
        correta="B",
        comentario=(
            "A Administração indireta é composta por entidades com personalidade jurídica própria: "
            "autarquias, fundações, empresas públicas e sociedades de economia mista. Ministérios e "
            "Secretarias são órgãos da Administração direta."
        ),
        armadilha="Concessionárias prestam serviço público, mas são particulares — não integram a indireta.",
    ),
    Questao(
        id="adm-009",
        materia="administrativo",
        tema="Servidores públicos",
        nivel="medio",
        enunciado=(
            "Sobre a investidura em cargo ou emprego público, a Constituição Federal determina que:"
        ),
        alternativas=(
            ("A", "depende sempre de aprovação prévia em concurso público, sem qualquer exceção."),
            ("B", "depende de aprovação prévia em concurso público, ressalvadas as nomeações para "
                  "cargo em comissão declarado em lei de livre nomeação e exoneração."),
            ("C", "pode ocorrer por indicação, desde que haja publicidade do ato."),
            ("D", "independe de concurso quando se tratar de emprego em empresa pública."),
            ("E", "exige concurso apenas para cargos de nível superior."),
        ),
        correta="B",
        comentario=(
            "Art. 37, II: a regra é o concurso público; a exceção constitucional expressa é o cargo "
            "em comissão de livre nomeação e exoneração (além de hipóteses como contratação "
            "temporária do inciso IX)."
        ),
        armadilha="A palavra 'sem qualquer exceção' invalida a alternativa (A), que parece certa.",
    ),
    Questao(
        id="adm-010",
        materia="administrativo",
        tema="Discricionariedade e arbitrariedade",
        nivel="dificil",
        enunciado="Sobre o ato discricionário, assinale a alternativa correta.",
        alternativas=(
            ("A", "É sinônimo de ato arbitrário, pois o administrador decide livremente."),
            ("B", "Permite juízo de conveniência e oportunidade nos limites da lei, sujeitando-se a "
                  "controle de legalidade pelo Judiciário."),
            ("C", "Não admite qualquer controle judicial."),
            ("D", "É aquele em que todos os elementos são fixados pela lei."),
            ("E", "Pode ser praticado por agente sem competência, se conveniente."),
        ),
        correta="B",
        comentario=(
            "Discricionariedade é liberdade dentro da lei; arbitrariedade é atuação fora dela. O "
            "Judiciário não substitui o mérito, mas controla legalidade, competência, forma, "
            "finalidade e razoabilidade."
        ),
        armadilha="'Livremente' e 'não admite controle' são exageros que a banca usa como isca.",
    ),
    Questao(
        id="adm-011",
        materia="administrativo",
        tema="Improbidade administrativa",
        nivel="medio",
        enunciado=(
            "Os atos de improbidade administrativa, nos termos do art. 37, § 4º, da CF, importarão:"
        ),
        alternativas=(
            ("A", "prisão automática do agente, independentemente de processo."),
            ("B", "suspensão dos direitos políticos, perda da função pública, indisponibilidade dos "
                  "bens e ressarcimento ao erário, na forma e gradação previstas em lei."),
            ("C", "apenas multa administrativa."),
            ("D", "cassação da nacionalidade do agente."),
            ("E", "perda automática de todos os bens do agente e de sua família."),
        ),
        correta="B",
        comentario=(
            "O § 4º prevê exatamente essas consequências, 'sem prejuízo da ação penal cabível' — "
            "ou seja, a sanção por improbidade é independente da esfera penal."
        ),
        armadilha="Improbidade não é crime por si só: quem prende é o processo penal, não o § 4º.",
    ),
    Questao(
        id="adm-012",
        materia="administrativo",
        tema="Princípio da publicidade",
        nivel="facil",
        enunciado=(
            "A publicidade dos atos administrativos, segundo a CF, admite restrição quando:"
        ),
        alternativas=(
            ("A", "o ato for considerado inconveniente pelo administrador."),
            ("B", "houver risco à imagem pessoal da autoridade."),
            ("C", "o sigilo for imprescindível à segurança da sociedade e do Estado."),
            ("D", "o custo de divulgação for elevado."),
            ("E", "a informação for de interesse apenas de particulares."),
        ),
        correta="C",
        comentario=(
            "Art. 5º, XXXIII: todos têm direito a informações de interesse coletivo ou geral, "
            "ressalvadas aquelas cujo sigilo seja imprescindível à segurança da sociedade e do "
            "Estado. Publicidade é a regra; sigilo, exceção fundamentada."
        ),
        armadilha="Conveniência do administrador nunca justifica sigilo — só a hipótese constitucional.",
    ),
]
