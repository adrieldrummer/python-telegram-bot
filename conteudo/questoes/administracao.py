"""Noções de Administração Pública — CF, Constituição paulista e Lei de Acesso à Informação."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="adm-001",
        materia="administracao",
        tema="Princípios da Administração Pública",
        nivel="facil",
        enunciado=(
            "O art. 37, caput, da Constituição Federal impõe à Administração Pública direta e "
            "indireta a observância dos princípios de:"
        ),
        alternativas=(
            ("A", "legalidade, impessoalidade, moralidade, publicidade e eficiência."),
            ("B", "legalidade, isonomia, motivação, proporcionalidade e economicidade."),
            ("C", "hierarquia, disciplina, celeridade, transparência e oportunidade."),
            ("D", "supremacia do interesse público, autotutela, especialidade e continuidade."),
            ("E", "legalidade, publicidade, conveniência, eficácia e discricionariedade."),
        ),
        correta="A",
        comentario=(
            "São os cinco princípios expressos, lembrados pela sigla LIMPE. Os demais citados "
            "existem no Direito Administrativo, mas como princípios implícitos ou "
            "infraconstitucionais."
        ),
        armadilha="Decore LIMPE: é a sigla que mais cai em prova de concurso público.",
    ),
    Questao(
        id="adm-002",
        materia="administracao",
        tema="Segurança pública (CF, art. 144)",
        nivel="facil",
        enunciado="Segundo a Constituição Federal, cabe às polícias militares:",
        alternativas=(
            ("A", "a apuração de infrações penais contra a ordem política e social."),
            ("B", "o policiamento ostensivo e a preservação da ordem pública."),
            ("C", "as funções de polícia judiciária da União."),
            ("D", "o patrulhamento ostensivo das rodovias federais."),
            ("E", "a execução, com exclusividade, das atividades de defesa civil."),
        ),
        correta="B",
        comentario=(
            "Art. 144, § 5º: às polícias militares cabem a polícia ostensiva e a preservação da "
            "ordem pública; aos corpos de bombeiros militares, a defesa civil. As alternativas (A) "
            "e (C) descrevem a Polícia Federal e a (D), a Polícia Rodoviária Federal."
        ),
        armadilha="Cada órgão do art. 144 tem atribuição própria — a banca troca uma pela outra.",
    ),
    Questao(
        id="adm-003",
        materia="administracao",
        tema="Segurança pública: dever e direito",
        nivel="facil",
        enunciado="De acordo com o caput do art. 144 da Constituição Federal, a segurança pública é:",
        alternativas=(
            ("A", "dever exclusivo das forças policiais, sem participação da sociedade."),
            ("B", "dever do Estado, direito e responsabilidade de todos, exercida para a "
                  "preservação da ordem pública e da incolumidade das pessoas e do patrimônio."),
            ("C", "atribuição privativa da União."),
            ("D", "serviço público delegável à iniciativa privada."),
            ("E", "competência exclusiva dos municípios."),
        ),
        correta="B",
        comentario=(
            "A redação constitucional é literal: 'dever do Estado, direito e responsabilidade de "
            "todos'. A parte final — responsabilidade de todos — é justamente a que costuma ser "
            "suprimida nos distratores."
        ),
        armadilha="Se a alternativa exclui a sociedade, ela contraria o texto da Constituição.",
    ),
    Questao(
        id="adm-004",
        materia="administracao",
        tema="Militares dos Estados",
        nivel="medio",
        enunciado=(
            "As polícias militares e os corpos de bombeiros militares são forças auxiliares e "
            "reserva do Exército e subordinam-se:"
        ),
        alternativas=(
            ("A", "ao Ministro da Defesa."),
            ("B", "ao Comandante do Exército da respectiva região militar."),
            ("C", "aos Governadores dos Estados, do Distrito Federal e dos Territórios."),
            ("D", "ao Presidente da República, em qualquer hipótese."),
            ("E", "aos Prefeitos dos municípios onde estão sediadas."),
        ),
        correta="C",
        comentario=(
            "Art. 144, § 6º. Ser 'força auxiliar e reserva do Exército' não significa subordinação "
            "cotidiana ao Exército: o comando é do Governador do Estado."
        ),
        armadilha="A expressão 'reserva do Exército' é a isca para marcar a alternativa (B).",
    ),
    Questao(
        id="adm-005",
        materia="administracao",
        tema="Direitos e garantias fundamentais",
        nivel="medio",
        enunciado=(
            "De acordo com o art. 5º da Constituição Federal, sobre a inviolabilidade do "
            "domicílio, é correto afirmar:"
        ),
        alternativas=(
            ("A", "A casa é asilo inviolável, não se admitindo ingresso em nenhuma hipótese sem "
                  "consentimento do morador."),
            ("B", "É permitido o ingresso sem consentimento em caso de flagrante delito, desastre "
                  "ou para prestar socorro, a qualquer hora do dia ou da noite."),
            ("C", "O ingresso por determinação judicial pode ocorrer a qualquer hora."),
            ("D", "Somente durante o dia é possível ingressar em caso de flagrante delito."),
            ("E", "A garantia não se aplica a imóveis alugados."),
        ),
        correta="B",
        comentario=(
            "Art. 5º, XI: flagrante delito, desastre e prestação de socorro autorizam o ingresso a "
            "qualquer hora; a determinação judicial, apenas durante o dia."
        ),
        armadilha="A restrição de horário vale para a ordem judicial, não para o flagrante.",
    ),
    Questao(
        id="adm-006",
        materia="administracao",
        tema="Direitos e garantias fundamentais",
        nivel="facil",
        enunciado="Assinale a alternativa que reproduz corretamente uma garantia do art. 5º da CF.",
        alternativas=(
            ("A", "Ninguém será obrigado a fazer ou deixar de fazer alguma coisa senão em virtude de lei."),
            ("B", "Ninguém será considerado culpado até a lavratura do auto de prisão em flagrante."),
            ("C", "A lei penal retroagirá sempre, para beneficiar ou prejudicar o réu."),
            ("D", "A prisão de qualquer pessoa independe de comunicação ao juiz competente."),
            ("E", "É vedado o direito de reunião pacífica em locais públicos."),
        ),
        correta="A",
        comentario=(
            "Art. 5º, II — princípio da legalidade. A presunção de inocência vai até o trânsito em "
            "julgado (inciso LVII); a lei penal só retroage para beneficiar (XL); toda prisão deve "
            "ser comunicada imediatamente ao juiz (LXII); e a reunião pacífica é assegurada (XVI)."
        ),
        armadilha="Alternativas que antecipam a culpa para antes do trânsito em julgado.",
    ),
    Questao(
        id="adm-007",
        materia="administracao",
        tema="Direitos políticos",
        nivel="medio",
        enunciado="Sobre os direitos políticos na Constituição Federal, é correto afirmar:",
        alternativas=(
            ("A", "O voto é facultativo para todos os brasileiros."),
            ("B", "O alistamento e o voto são obrigatórios para os maiores de 18 e menores de 70 "
                  "anos, e facultativos para analfabetos, maiores de 70 e jovens de 16 e 17 anos."),
            ("C", "O voto é vedado aos maiores de 65 anos."),
            ("D", "Estrangeiros têm direito de votar em eleições municipais."),
            ("E", "Conscritos, durante o serviço militar obrigatório, são obrigados a votar."),
        ),
        correta="B",
        comentario=(
            "Art. 14, § 1º. A obrigatoriedade vale dos 18 aos 70 anos; é facultativo para "
            "analfabetos, maiores de 70 e maiores de 16 e menores de 18. Conscritos, durante o "
            "serviço militar obrigatório, não podem se alistar (§ 2º)."
        ),
        armadilha="Facultativo não é o mesmo que proibido — a banca embaralha os dois.",
    ),
    Questao(
        id="adm-008",
        materia="administracao",
        tema="Investidura em cargo público",
        nivel="medio",
        enunciado="Sobre a investidura em cargo ou emprego público, a Constituição Federal determina que:",
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
            "Art. 37, II: a regra é o concurso público; a exceção expressa é o cargo em comissão de "
            "livre nomeação e exoneração, além da contratação temporária do inciso IX."
        ),
        armadilha="A expressão 'sem qualquer exceção' já invalida a alternativa (A).",
    ),
    Questao(
        id="adm-009",
        materia="administracao",
        tema="Publicidade e sigilo",
        nivel="medio",
        enunciado="A publicidade dos atos administrativos admite restrição quando:",
        alternativas=(
            ("A", "o ato for considerado inconveniente pelo administrador."),
            ("B", "houver risco à imagem pessoal da autoridade."),
            ("C", "o sigilo for imprescindível à segurança da sociedade e do Estado."),
            ("D", "o custo de divulgação for elevado."),
            ("E", "a informação for antiga."),
        ),
        correta="C",
        comentario=(
            "Art. 5º, XXXIII: todos têm direito a receber informações de interesse coletivo ou "
            "geral, ressalvadas aquelas cujo sigilo seja imprescindível à segurança da sociedade e "
            "do Estado. Publicidade é a regra; sigilo é exceção fundamentada em lei."
        ),
        armadilha="Conveniência do administrador nunca justifica sigilo.",
    ),
    Questao(
        id="adm-010",
        materia="administracao",
        tema="Lei de Acesso à Informação (Lei 12.527/2011)",
        nivel="medio",
        enunciado="Sobre a Lei de Acesso à Informação, é correto afirmar:",
        alternativas=(
            ("A", "Só advogados e jornalistas podem solicitar informações a órgãos públicos."),
            ("B", "Qualquer pessoa pode solicitar informações a órgãos públicos, com prazos "
                  "definidos para resposta, sendo o sigilo exceção prevista em lei."),
            ("C", "O pedido de informação exige a apresentação de motivo determinado."),
            ("D", "Os órgãos públicos podem simplesmente ignorar pedidos considerados inoportunos."),
            ("E", "A lei se aplica apenas aos órgãos federais."),
        ),
        correta="B",
        comentario=(
            "A Lei 12.527/2011 assegura o acesso como regra, a qualquer interessado, sem exigir "
            "motivação do pedido, com prazos de resposta e possibilidade de recurso. Aplica-se à "
            "União, aos Estados, ao Distrito Federal e aos Municípios."
        ),
        armadilha="Exigir motivo para o pedido é justamente o que a lei proíbe.",
    ),
    Questao(
        id="adm-011",
        materia="administracao",
        tema="Decreto estadual 68.155/2023",
        nivel="dificil",
        enunciado=(
            "No Estado de São Paulo, o Decreto estadual nº 68.155/2023 tem por objeto:"
        ),
        alternativas=(
            ("A", "criar novo imposto estadual sobre serviços."),
            ("B", "regulamentar, no âmbito estadual, a aplicação da Lei de Acesso à Informação, "
                  "definindo procedimentos e responsabilidades no atendimento aos pedidos."),
            ("C", "reorganizar a carreira dos servidores civis federais."),
            ("D", "instituir o Código de Trânsito do Estado de São Paulo."),
            ("E", "revogar a Lei de Acesso à Informação no território paulista."),
        ),
        correta="B",
        comentario=(
            "O decreto estadual regulamenta como os órgãos e entidades paulistas cumprem a Lei "
            "12.527/2011 — prazos, fluxos e responsáveis. Decreto regulamenta lei; não a revoga."
        ),
        armadilha="Decreto não revoga lei federal — hierarquia das normas resolve a questão.",
    ),
    Questao(
        id="adm-012",
        materia="administracao",
        tema="Constituição do Estado de São Paulo",
        nivel="medio",
        enunciado=(
            "A Justiça Militar do Estado, prevista na Constituição do Estado de São Paulo, é "
            "responsável por:"
        ),
        alternativas=(
            ("A", "julgar todas as ações cíveis envolvendo o Estado."),
            ("B", "julgar os crimes militares definidos em lei, praticados por militares estaduais."),
            ("C", "julgar exclusivamente crimes eleitorais."),
            ("D", "fiscalizar as contas do Poder Executivo estadual."),
            ("E", "processar e julgar o Governador por crime de responsabilidade."),
        ),
        correta="B",
        comentario=(
            "A Justiça Militar estadual julga os crimes militares definidos em lei cometidos por "
            "policiais e bombeiros militares. Contas do Executivo são do Tribunal de Contas; "
            "crimes eleitorais, da Justiça Eleitoral."
        ),
        armadilha="Militar que comete crime comum não vai para a Justiça Militar.",
    ),
    Questao(
        id="adm-013",
        materia="administracao",
        tema="Servidores civis e militares (CE-SP)",
        nivel="medio",
        enunciado=(
            "Sobre os servidores públicos estaduais na Constituição do Estado de São Paulo, é "
            "correto afirmar:"
        ),
        alternativas=(
            ("A", "Servidores civis e militares submetem-se exatamente ao mesmo regime jurídico."),
            ("B", "A Constituição estadual diferencia servidores públicos civis de servidores "
                  "públicos militares, com regras próprias de ingresso, direitos e deveres."),
            ("C", "Não há previsão de servidores militares na Constituição estadual."),
            ("D", "Os militares estaduais são regidos pela Consolidação das Leis do Trabalho."),
            ("E", "O ingresso na carreira militar independe de concurso público."),
        ),
        correta="B",
        comentario=(
            "A Constituição paulista trata separadamente as duas categorias. Os militares estaduais "
            "têm regime próprio — inclusive quanto a hierarquia, disciplina e vedações, como a "
            "sindicalização e a greve."
        ),
        armadilha="Servidor militar não é celetista nem tem o mesmo regime do servidor civil.",
    ),
    Questao(
        id="adm-014",
        materia="administracao",
        tema="Responsabilidade do Estado",
        nivel="dificil",
        enunciado=(
            "Conforme o art. 37, § 6º, da Constituição Federal, a responsabilidade das pessoas "
            "jurídicas de direito público por danos causados por seus agentes a terceiros é:"
        ),
        alternativas=(
            ("A", "subjetiva, exigindo que a vítima prove dolo ou culpa do agente."),
            ("B", "objetiva, assegurado o direito de regresso contra o agente responsável nos casos "
                  "de dolo ou culpa."),
            ("C", "objetiva, vedado o direito de regresso."),
            ("D", "inexistente quando o dano decorre de ato omissivo."),
            ("E", "solidária com o agente em qualquer hipótese."),
        ),
        correta="B",
        comentario=(
            "Para a vítima, basta demonstrar conduta, dano e nexo causal — responsabilidade "
            "objetiva. Já a ação de regresso do Estado contra o agente depende de comprovar dolo ou "
            "culpa."
        ),
        armadilha="Trocar a relação Estado-vítima (objetiva) pela Estado-agente (subjetiva).",
    ),
    Questao(
        id="adm-015",
        materia="administracao",
        tema="Direitos sociais",
        nivel="facil",
        enunciado="São direitos sociais expressamente previstos no art. 6º da Constituição Federal:",
        alternativas=(
            ("A", "educação, saúde, alimentação, trabalho, moradia, transporte, lazer e segurança."),
            ("B", "propriedade, herança, livre iniciativa e sigilo bancário."),
            ("C", "voto, elegibilidade, iniciativa popular e plebiscito."),
            ("D", "nacionalidade, cidadania e dignidade da pessoa humana."),
            ("E", "liberdade de expressão, reunião e associação."),
        ),
        correta="A",
        comentario=(
            "O art. 6º lista os direitos sociais, incluindo ainda previdência social, proteção à "
            "maternidade e à infância e assistência aos desamparados. A alternativa (D) traz "
            "fundamentos da República (art. 1º)."
        ),
        armadilha="Direitos sociais (art. 6º) x fundamentos da República (art. 1º).",
    ),
]
