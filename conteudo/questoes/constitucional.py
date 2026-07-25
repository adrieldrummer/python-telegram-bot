"""Direito Constitucional — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="const-001",
        materia="constitucional",
        tema="Segurança pública (art. 144)",
        nivel="facil",
        enunciado=(
            "Segundo a Constituição Federal, a segurança pública é exercida por meio de diversos "
            "órgãos. Às polícias militares cabe:"
        ),
        alternativas=(
            ("A", "a apuração de infrações penais contra a ordem política e social."),
            ("B", "o policiamento ostensivo e a preservação da ordem pública."),
            ("C", "as funções de polícia judiciária da União."),
            ("D", "a execução de atividades de defesa civil, com exclusividade."),
            ("E", "o patrulhamento ostensivo das rodovias federais."),
        ),
        correta="B",
        comentario=(
            "O art. 144, § 5º, da CF atribui às polícias militares a polícia ostensiva e a "
            "preservação da ordem pública; aos corpos de bombeiros militares cabe, além das "
            "atribuições definidas em lei, a execução de atividades de defesa civil."
        ),
        armadilha="As alternativas (A) e (C) descrevem a Polícia Federal; a (E) descreve a PRF.",
    ),
    Questao(
        id="const-002",
        materia="constitucional",
        tema="Subordinação das polícias militares",
        nivel="medio",
        enunciado=(
            "As polícias militares e os corpos de bombeiros militares, conforme a Constituição "
            "Federal, são forças auxiliares e reserva do Exército e subordinam-se:"
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
            "O art. 144, § 6º, da CF estabelece que as polícias militares e os corpos de bombeiros "
            "militares, forças auxiliares e reserva do Exército, subordinam-se aos Governadores "
            "dos Estados, do Distrito Federal e dos Territórios."
        ),
        armadilha="Ser 'reserva do Exército' não significa subordinação ao Exército no dia a dia.",
    ),
    Questao(
        id="const-003",
        materia="constitucional",
        tema="Direitos e garantias fundamentais",
        nivel="medio",
        enunciado=(
            "De acordo com o art. 5º da Constituição Federal, assinale a alternativa correta sobre "
            "a inviolabilidade do domicílio."
        ),
        alternativas=(
            ("A", "A casa é asilo inviolável, não se admitindo o ingresso em nenhuma hipótese sem "
                  "autorização do morador."),
            ("B", "O ingresso é permitido a qualquer hora, desde que haja ordem judicial."),
            ("C", "É permitido o ingresso sem consentimento em caso de flagrante delito, desastre "
                  "ou para prestar socorro, a qualquer hora."),
            ("D", "Somente durante o dia é possível ingressar em caso de flagrante delito."),
            ("E", "A inviolabilidade não se aplica a imóveis alugados."),
        ),
        correta="C",
        comentario=(
            "O art. 5º, XI, da CF garante a inviolabilidade do domicílio, ressalvando o ingresso "
            "sem consentimento em caso de flagrante delito, desastre ou para prestar socorro — "
            "essas três hipóteses valem a qualquer hora — e, durante o dia, por determinação "
            "judicial."
        ),
        armadilha="A restrição de horário ('durante o dia') vale para a ordem judicial, não para o flagrante.",
    ),
    Questao(
        id="const-004",
        materia="constitucional",
        tema="Remédios constitucionais",
        nivel="medio",
        enunciado=(
            "O remédio constitucional cabível para assegurar o conhecimento de informações "
            "relativas à pessoa do impetrante, constantes de registros de entidades governamentais "
            "ou de caráter público, é:"
        ),
        alternativas=(
            ("A", "o habeas corpus."),
            ("B", "o mandado de segurança."),
            ("C", "o habeas data."),
            ("D", "o mandado de injunção."),
            ("E", "a ação popular."),
        ),
        correta="C",
        comentario=(
            "Art. 5º, LXXII: o habeas data assegura o conhecimento ou a retificação de informações "
            "relativas ao próprio impetrante. Habeas corpus protege a liberdade de locomoção; o "
            "mandado de injunção supre falta de norma regulamentadora."
        ),
        armadilha="Confundir habeas data (dados do próprio impetrante) com direito de petição ou certidão.",
    ),
    Questao(
        id="const-005",
        materia="constitucional",
        tema="Princípio da legalidade e presunção de inocência",
        nivel="facil",
        enunciado="Assinale a alternativa que reproduz corretamente uma garantia do art. 5º da CF.",
        alternativas=(
            ("A", "Ninguém será considerado culpado até a lavratura do auto de prisão em flagrante."),
            ("B", "Ninguém será obrigado a fazer ou deixar de fazer alguma coisa senão em virtude de lei."),
            ("C", "A lei penal retroagirá sempre, para beneficiar ou prejudicar o réu."),
            ("D", "É garantido o sigilo da fonte, ainda que necessário ao exercício profissional."),
            ("E", "A prisão de qualquer pessoa independe de comunicação ao juiz competente."),
        ),
        correta="B",
        comentario=(
            "Art. 5º, II — princípio da legalidade. A presunção de inocência vai até o trânsito em "
            "julgado da sentença penal condenatória (inciso LVII); a lei penal só retroage para "
            "beneficiar (inciso XL); e toda prisão deve ser comunicada imediatamente ao juiz "
            "(inciso LXII)."
        ),
        armadilha="Alternativas que trocam 'trânsito em julgado' por qualquer marco anterior.",
    ),
    Questao(
        id="const-006",
        materia="constitucional",
        tema="Direitos sociais",
        nivel="facil",
        enunciado="São direitos sociais expressamente previstos no art. 6º da Constituição Federal:",
        alternativas=(
            ("A", "educação, saúde, alimentação, trabalho, moradia, transporte, lazer e segurança."),
            ("B", "propriedade, herança, livre iniciativa e sigilo bancário."),
            ("C", "voto, elegibilidade, iniciativa popular e plebiscito."),
            ("D", "liberdade de expressão, reunião e associação."),
            ("E", "nacionalidade, cidadania e dignidade da pessoa humana."),
        ),
        correta="A",
        comentario=(
            "O art. 6º relaciona os direitos sociais: educação, saúde, alimentação, trabalho, "
            "moradia, transporte, lazer, segurança, previdência social, proteção à maternidade e "
            "à infância e assistência aos desamparados."
        ),
        armadilha="(E) lista fundamentos da República (art. 1º), não direitos sociais.",
    ),
    Questao(
        id="const-007",
        materia="constitucional",
        tema="Fundamentos da República",
        nivel="medio",
        enunciado="NÃO constitui fundamento da República Federativa do Brasil (art. 1º da CF):",
        alternativas=(
            ("A", "a soberania."),
            ("B", "a cidadania."),
            ("C", "a dignidade da pessoa humana."),
            ("D", "a erradicação da pobreza."),
            ("E", "o pluralismo político."),
        ),
        correta="D",
        comentario=(
            "A erradicação da pobreza é OBJETIVO fundamental (art. 3º, III), não fundamento. Os "
            "fundamentos do art. 1º são soberania, cidadania, dignidade da pessoa humana, valores "
            "sociais do trabalho e da livre iniciativa e pluralismo político."
        ),
        armadilha="Questão com 'NÃO' no enunciado: leia duas vezes o comando antes de marcar.",
    ),
    Questao(
        id="const-008",
        materia="constitucional",
        tema="Prisão e direitos do preso",
        nivel="medio",
        enunciado="Sobre os direitos do preso, conforme o art. 5º da CF, é correto afirmar:",
        alternativas=(
            ("A", "O preso não tem direito à identificação dos responsáveis por sua prisão."),
            ("B", "É assegurado ao preso o respeito à integridade física e moral."),
            ("C", "A prisão ilegal deve ser comunicada ao juiz em até 72 horas."),
            ("D", "O preso somente será informado de seus direitos após o interrogatório."),
            ("E", "A assistência da família é vedada durante a custódia."),
        ),
        correta="B",
        comentario=(
            "Art. 5º, XLIX: é assegurado aos presos o respeito à integridade física e moral. O "
            "inciso LXIV garante a identificação dos responsáveis pela prisão e pelo interrogatório; "
            "a prisão ilegal deve ser imediatamente relaxada (LXV) e a prisão comunicada "
            "imediatamente ao juiz e à família (LXII)."
        ),
        armadilha="Prazos inventados ('72 horas') em incisos que falam em comunicação imediata.",
    ),
    Questao(
        id="const-009",
        materia="constitucional",
        tema="Nacionalidade",
        nivel="dificil",
        enunciado="São brasileiros natos, nos termos do art. 12 da CF:",
        alternativas=(
            ("A", "os nascidos no estrangeiro, de pais estrangeiros, que residam no Brasil há mais de 15 anos."),
            ("B", "os nascidos na República Federativa do Brasil, ainda que de pais estrangeiros, "
                  "desde que estes não estejam a serviço de seu país."),
            ("C", "os originários de países de língua portuguesa que residam há um ano ininterrupto no Brasil."),
            ("D", "os estrangeiros naturalizados após 15 anos de residência ininterrupta."),
            ("E", "os nascidos no exterior, de pai ou mãe brasileiros, que jamais tenham vindo ao Brasil."),
        ),
        correta="B",
        comentario=(
            "Art. 12, I, 'a': aplica-se o critério do território (ius soli), com a ressalva dos "
            "filhos de estrangeiros a serviço de seu país. As alternativas (C) e (D) tratam de "
            "naturalização, e não de nacionalidade originária."
        ),
        armadilha="Misturar as hipóteses de naturalizado com as de nato — é o ponto favorito da banca.",
    ),
    Questao(
        id="const-010",
        materia="constitucional",
        tema="Organização dos Poderes",
        nivel="medio",
        enunciado="Sobre a organização do Estado brasileiro, assinale a alternativa correta.",
        alternativas=(
            ("A", "A República Federativa do Brasil é formada pela união indissolúvel dos Estados, "
                  "Municípios e do Distrito Federal."),
            ("B", "Os Territórios Federais integram a União apenas para fins tributários."),
            ("C", "Os Municípios não possuem autonomia política."),
            ("D", "Os Estados podem se desmembrar independentemente de consulta às populações interessadas."),
            ("E", "O Distrito Federal pode ser dividido em Municípios."),
        ),
        correta="A",
        comentario=(
            "Art. 1º, caput: a República é formada pela união indissolúvel dos Estados e Municípios "
            "e do Distrito Federal. Os Municípios têm autonomia (art. 18), a criação/desmembramento "
            "de Estados exige consulta plebiscitária (art. 18, § 3º) e o DF não pode ser dividido "
            "em Municípios (art. 32)."
        ),
        armadilha="'União indissolúvel' aparece com frequência trocada por 'dissolúvel mediante lei'.",
    ),
    Questao(
        id="const-011",
        materia="constitucional",
        tema="Militares dos Estados",
        nivel="dificil",
        enunciado=(
            "De acordo com a Constituição Federal, ao militar estadual em atividade é vedado:"
        ),
        alternativas=(
            ("A", "exercer o direito de voto."),
            ("B", "a sindicalização e a greve."),
            ("C", "receber remuneração por subsídio."),
            ("D", "prestar concurso público de qualquer natureza."),
            ("E", "obter licença para tratamento de saúde."),
        ),
        correta="B",
        comentario=(
            "O art. 142, § 3º, IV, aplicável aos militares dos Estados por força do art. 42, veda "
            "a sindicalização e a greve. O direito de voto é assegurado; a remuneração por subsídio "
            "é admitida."
        ),
        armadilha="Confundir vedação de filiação sindical com vedação de qualquer associação.",
    ),
    Questao(
        id="const-012",
        materia="constitucional",
        tema="Aplicação imediata dos direitos fundamentais",
        nivel="medio",
        enunciado=(
            "Segundo o art. 5º, § 1º, da Constituição Federal, as normas definidoras dos direitos "
            "e garantias fundamentais:"
        ),
        alternativas=(
            ("A", "dependem sempre de lei regulamentadora para produzir efeitos."),
            ("B", "têm aplicação imediata."),
            ("C", "produzem efeitos apenas após decisão do Supremo Tribunal Federal."),
            ("D", "aplicam-se somente aos brasileiros natos."),
            ("E", "podem ser suspensas por decreto do Poder Executivo."),
        ),
        correta="B",
        comentario=(
            "Art. 5º, § 1º: as normas definidoras dos direitos e garantias fundamentais têm "
            "aplicação imediata. O caput assegura tais direitos a brasileiros e estrangeiros "
            "residentes no País."
        ),
        armadilha="A palavra 'sempre' na alternativa (A) já denuncia o exagero típico de distrator.",
    ),
]
