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
            ("B", "a polícia ostensiva e a preservação da ordem pública."),
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
            ("B", "atribuição privativa da União."),
            ("C", "dever do Estado, direito e responsabilidade de todos, exercida para a "
                  "preservação da ordem pública e da incolumidade das pessoas e do patrimônio."),
            ("D", "serviço público delegável à iniciativa privada."),
            ("E", "competência exclusiva dos municípios."),
        ),
        correta="C",
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
            ("C", "ao Presidente da República, em qualquer hipótese."),
            ("D", "aos Governadores dos Estados, do Distrito Federal e dos Territórios."),
            ("E", "aos Prefeitos dos municípios onde estão sediadas."),
        ),
        correta="D",
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
            ("B", "A garantia não se aplica a imóveis alugados."),
            ("C", "O ingresso por determinação judicial pode ocorrer a qualquer hora."),
            ("D", "Somente durante o dia é possível ingressar em caso de flagrante delito."),
            ("E", "É permitido o ingresso sem consentimento em caso de flagrante delito, desastre "
                  "ou para prestar socorro, a qualquer hora do dia ou da noite."),
        ),
        correta="E",
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
            ("B", "pode ocorrer por indicação, desde que haja publicidade do ato."),
            ("C", "depende de aprovação prévia em concurso público, ressalvadas as nomeações para "
                  "cargo em comissão declarado em lei de livre nomeação e exoneração."),
            ("D", "independe de concurso quando se tratar de emprego em empresa pública."),
            ("E", "exige concurso apenas para cargos de nível superior."),
        ),
        correta="C",
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
            ("C", "o custo de divulgação for elevado."),
            ("D", "o sigilo for imprescindível à segurança da sociedade e do Estado."),
            ("E", "a informação for antiga."),
        ),
        correta="D",
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
            ("B", "A lei se aplica apenas aos órgãos federais."),
            ("C", "O pedido de informação exige a apresentação de motivo determinado."),
            ("D", "Os órgãos públicos podem simplesmente ignorar pedidos considerados inoportunos."),
            ("E", "Qualquer pessoa pode solicitar informações a órgãos públicos, com prazos "
                  "definidos para resposta, sendo o sigilo exceção prevista em lei."),
        ),
        correta="E",
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
            ("A", "regulamentar, no âmbito estadual, a aplicação da Lei de Acesso à Informação, "
                  "definindo procedimentos e responsabilidades no atendimento aos pedidos."),
            ("B", "criar novo imposto estadual sobre serviços."),
            ("C", "reorganizar a carreira dos servidores civis federais."),
            ("D", "instituir o Código de Trânsito do Estado de São Paulo."),
            ("E", "revogar a Lei de Acesso à Informação no território paulista."),
        ),
        correta="A",
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
            ("B", "Não há previsão de servidores militares na Constituição estadual."),
            ("C", "A Constituição estadual diferencia servidores públicos civis de servidores "
                  "públicos militares, com regras próprias de ingresso, direitos e deveres."),
            ("D", "Os militares estaduais são regidos pela Consolidação das Leis do Trabalho."),
            ("E", "O ingresso na carreira militar independe de concurso público."),
        ),
        correta="C",
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
            ("B", "inexistente quando o dano decorre de ato omissivo."),
            ("C", "objetiva, vedado o direito de regresso."),
            ("D", "objetiva, assegurado o direito de regresso contra o agente responsável nos casos "
                  "de dolo ou culpa."),
            ("E", "solidária com o agente em qualquer hipótese."),
        ),
        correta="D",
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
            ("A", "liberdade de expressão, reunião e associação."),
            ("B", "propriedade, herança, livre iniciativa e sigilo bancário."),
            ("C", "voto, elegibilidade, iniciativa popular e plebiscito."),
            ("D", "nacionalidade, cidadania e dignidade da pessoa humana."),
            ("E", "educação, saúde, alimentação, trabalho, moradia, transporte, lazer e segurança."),
        ),
        correta="E",
        comentario=(
            "O art. 6º lista os direitos sociais, incluindo ainda previdência social, proteção à "
            "maternidade e à infância e assistência aos desamparados. A alternativa (D) traz "
            "fundamentos da República (art. 1º)."
        ),
        armadilha="Direitos sociais (art. 6º) x fundamentos da República (art. 1º).",
    ),
    Questao(
        id="adm-016",
        materia="administracao",
        tema="Direitos e garantias fundamentais",
        nivel="medio",
        enunciado=(
            "Sobre os direitos e garantias fundamentais do art. 5º da Constituição Federal, é "
            "correto afirmar que:"
        ),
        alternativas=(
            ("A", "a liberdade de associação é plena, inclusive para associações de caráter "
                  "paramilitar."),
            ("B", "é assegurada, nos termos da lei, a prestação de assistência religiosa nas "
                  "entidades civis e militares de internação coletiva."),
            ("C", "ninguém pode ser compelido a associar-se, mas a saída da associação depende de "
                  "autorização judicial."),
            ("D", "a criação de associações depende de autorização prévia do poder público."),
            ("E", "as associações só podem ser dissolvidas por ato do Poder Executivo."),
        ),
        correta="B",
        comentario=(
            "Art. 5º, VII: a assistência religiosa é assegurada em entidades de internação coletiva "
            "— presídios, hospitais e quartéis, entre outras. Sobre associações: é plena a liberdade "
            "<strong>para fins lícitos, vedada a de caráter paramilitar</strong> (XVII); a criação "
            "independe de autorização (XVIII); ninguém é obrigado a associar-se nem a permanecer "
            "associado (XX); e a dissolução compulsória exige decisão judicial transitada em julgado "
            "(XIX)."
        ),
        armadilha=(
            "A palavra 'plena' aparece no texto constitucional, mas vem sempre acompanhada de "
            "'para fins lícitos' e da vedação ao caráter paramilitar. Alternativa que só diz 'plena' "
            "está incompleta de propósito."
        ),
    ),
    Questao(
        id="adm-017",
        materia="administracao",
        tema="Militares: perda de posto e patente",
        nivel="dificil",
        enunciado=(
            "Um oficial da Polícia Militar foi condenado pela Justiça comum, por sentença transitada "
            "em julgado, a pena privativa de liberdade superior a dois anos. Conforme a Constituição "
            "Federal, esse oficial:"
        ),
        alternativas=(
            ("A", "perde automaticamente o posto e a patente com o trânsito em julgado da sentença."),
            ("B", "não pode sofrer qualquer consequência na esfera militar, por se tratar de "
                  "condenação na Justiça comum."),
            ("C", "será submetido a julgamento por tribunal militar de caráter permanente, que "
                  "decidirá sobre a perda do posto e da patente."),
            ("D", "é exonerado por ato do Governador, sem necessidade de julgamento."),
            ("E", "perde apenas a remuneração, mantendo posto e patente."),
        ),
        correta="C",
        comentario=(
            "Art. 142, § 3º, VI e VII (aplicável aos militares estaduais por força do art. 42): o "
            "oficial só perde o posto e a patente se for <strong>julgado indigno do oficialato ou "
            "com ele incompatível</strong>, por decisão de tribunal militar de caráter permanente. "
            "A condenação superior a dois anos na Justiça comum ou militar é o que "
            "<em>desencadeia</em> esse julgamento — ela não produz a perda sozinha."
        ),
        armadilha=(
            "Repare no 'superior a dois anos'. Condenação de exatamente dois anos não aciona o "
            "dispositivo — é o tipo de detalhe numérico que a banca usa para separar quem leu o "
            "texto de quem leu o resumo."
        ),
    ),
    Questao(
        id="adm-018",
        materia="administracao",
        tema="Organização da PM-SP",
        nivel="medio",
        enunciado=(
            "Sobre o Comandante Geral da Polícia Militar do Estado de São Paulo, é correto afirmar "
            "que o cargo é:"
        ),
        alternativas=(
            ("A", "ocupado por eleição direta entre os integrantes da corporação."),
            ("B", "privativo de oficial da reserva remunerada."),
            ("C", "provido por concurso público específico."),
            ("D", "ocupado por oficial do Exército designado pelo Ministério da Defesa."),
            ("E", "de livre nomeação do Governador do Estado, escolhido entre os coronéis da ativa "
                  "do Quadro de Oficiais Policiais Militares."),
        ),
        correta="E",
        comentario=(
            "A Polícia Militar subordina-se ao Governador (CF, art. 144, § 6º), e é ele quem nomeia "
            "o Comandante Geral entre os coronéis da ativa do QOPM. Não há eleição, concurso "
            "específico para o posto nem indicação federal — este último ponto é justamente o que "
            "distingue força auxiliar de força federal."
        ),
        armadilha=(
            "'Reserva e força auxiliar do Exército' induz à ideia de nomeação militar federal. O "
            "comando é estadual, e civil: quem nomeia é o Governador."
        ),
    ),
    Questao(
        id="adm-019",
        materia="administracao",
        tema="Atendimento ao cidadão",
        nivel="facil",
        enunciado=(
            "Canais oficiais de ouvidoria e atendimento ao cidadão, como os mantidos pelo Governo do "
            "Estado de São Paulo, têm por finalidade principal:"
        ),
        alternativas=(
            ("A", "substituir o registro de boletim de ocorrência policial."),
            ("B", "receber e encaminhar solicitações, reclamações, denúncias e pedidos de "
                  "informação, com acompanhamento do protocolo pelo cidadão."),
            ("C", "julgar administrativamente os servidores denunciados."),
            ("D", "divulgar campanhas publicitárias do governo."),
            ("E", "arrecadar taxas e tributos estaduais."),
        ),
        correta="B",
        comentario=(
            "A ouvidoria é porta de entrada e encaminhamento: registra a manifestação, gera "
            "protocolo e cobra resposta do órgão competente, em prazo. Ela não julga servidor — isso "
            "é da corregedoria e do processo administrativo disciplinar — nem substitui o boletim de "
            "ocorrência, que é ato de polícia judiciária."
        ),
        armadilha=(
            "Ouvidoria encaminha e acompanha; corregedoria apura e pune. Trocar as duas é o erro "
            "clássico do tema."
        ),
    ),
    Questao(
        id="adm-020",
        materia="administracao",
        tema="Segurança pública: atuação federal",
        nivel="dificil",
        enunciado=(
            "Diante de grave comprometimento da ordem pública em um Estado, a Constituição Federal "
            "admite a atuação das Forças Armadas na garantia da lei e da ordem. Essa atuação:"
        ),
        alternativas=(
            ("A", "dispensa qualquer provocação, podendo ser iniciada pelo comando militar local."),
            ("B", "transfere em definitivo o comando da polícia militar para o Exército."),
            ("C", "ocorre por iniciativa do Presidente da República, após iniciativa de qualquer dos "
                  "poderes constitucionais, e tem caráter episódico e temporário."),
            ("D", "substitui a competência estadual em matéria de segurança pública."),
            ("E", "só é possível mediante decretação de estado de sítio."),
        ),
        correta="C",
        comentario=(
            "Art. 142: as Forças Armadas destinam-se à defesa da Pátria, à garantia dos poderes "
            "constitucionais e, <strong>por iniciativa de qualquer destes</strong>, à garantia da lei "
            "e da ordem. Quem determina o emprego é o Presidente da República, e a operação é "
            "episódica e por tempo determinado — não anula a competência estadual nem exige, "
            "necessariamente, estado de sítio ou intervenção federal."
        ),
        armadilha=(
            "GLO, intervenção federal, estado de defesa e estado de sítio são institutos diferentes, "
            "com requisitos próprios. A banca mistura os quatro na mesma questão."
        ),
    ),
]
