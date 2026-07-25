"""Atualidades e Cidadania — questões autorais sobre temas estruturais (não notícia do dia)."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="atu-001",
        materia="atualidades",
        tema="Segurança pública: sistema",
        nivel="facil",
        enunciado=(
            "O Sistema Único de Segurança Pública (Susp) tem como característica principal:"
        ),
        alternativas=(
            ("A", "centralizar na União toda a atividade policial do País."),
            ("B", "integrar e coordenar as ações dos órgãos de segurança pública das três esferas "
                  "de governo, com diretrizes e metas comuns."),
            ("C", "substituir as polícias estaduais por uma guarda nacional."),
            ("D", "transferir a segurança pública para a iniciativa privada."),
            ("E", "extinguir os planos estaduais de segurança."),
        ),
        correta="B",
        comentario=(
            "O Susp organiza a atuação integrada de União, Estados, Distrito Federal e Municípios "
            "em segurança pública, com planejamento, metas e compartilhamento de informações — sem "
            "suprimir a autonomia das corporações estaduais."
        ),
        armadilha="Integração não é centralização: a alternativa (A) exagera o papel da União.",
    ),
    Questao(
        id="atu-002",
        materia="atualidades",
        tema="Cidadania e direitos",
        nivel="facil",
        enunciado="A Declaração Universal dos Direitos Humanos, de 1948, é um documento:",
        alternativas=(
            ("A", "aprovado pela Assembleia Geral das Nações Unidas, que estabelece direitos comuns "
                  "a todos os seres humanos."),
            ("B", "editado pelo Congresso Nacional brasileiro."),
            ("C", "de caráter militar, restrito a conflitos armados."),
            ("D", "que trata exclusivamente de direitos econômicos."),
            ("E", "revogado pela Constituição de 1988."),
        ),
        correta="A",
        comentario=(
            "A Declaração foi proclamada pela Assembleia Geral da ONU em 1948 e inspirou os "
            "tratados posteriores e boa parte do rol de direitos fundamentais da Constituição de 1988."
        ),
        armadilha="Confundir a Declaração da ONU com as Convenções de Genebra (direito humanitário).",
    ),
    Questao(
        id="atu-003",
        materia="atualidades",
        tema="Meio ambiente",
        nivel="medio",
        enunciado=(
            "Os Objetivos de Desenvolvimento Sustentável (ODS) da Agenda 2030 da ONU caracterizam-se por:"
        ),
        alternativas=(
            ("A", "tratar apenas de preservação de florestas."),
            ("B", "reunir metas globais em temas como pobreza, educação, saúde, igualdade, cidades "
                  "sustentáveis, paz e instituições eficazes."),
            ("C", "ser um tratado militar entre países da América do Sul."),
            ("D", "substituir as constituições nacionais."),
            ("E", "aplicar-se somente a países desenvolvidos."),
        ),
        correta="B",
        comentario=(
            "A Agenda 2030 reúne 17 objetivos e 169 metas, e é universal: vale para países ricos e "
            "pobres. O ODS 16 trata de paz, justiça e instituições eficazes — tema com relação "
            "direta com segurança pública."
        ),
        armadilha="Reduzir os ODS a 'meio ambiente' ignora as dimensões social e institucional.",
    ),
    Questao(
        id="atu-004",
        materia="atualidades",
        tema="Políticas públicas de segurança",
        nivel="medio",
        enunciado=(
            "O policiamento comunitário, adotado como diretriz por diversas corporações, "
            "caracteriza-se por:"
        ),
        alternativas=(
            ("A", "priorizar o confronto armado como estratégia principal."),
            ("B", "aproximar a polícia da comunidade, com foco na prevenção e na solução conjunta "
                  "de problemas locais."),
            ("C", "substituir o policiamento ostensivo por vigilância eletrônica."),
            ("D", "transferir o poder de polícia às associações de bairro."),
            ("E", "restringir a atuação policial a grandes eventos."),
        ),
        correta="B",
        comentario=(
            "A filosofia de polícia comunitária desloca o foco da reação para a prevenção, com "
            "vínculo permanente entre policiais e moradores, diagnóstico local e corresponsabilidade."
        ),
        armadilha="Aproximação com a comunidade não significa delegar poder de polícia a particulares.",
    ),
    Questao(
        id="atu-005",
        materia="atualidades",
        tema="Estatísticas de segurança",
        nivel="medio",
        enunciado=(
            "A taxa de homicídios por 100 mil habitantes é um indicador utilizado em segurança "
            "pública porque:"
        ),
        alternativas=(
            ("A", "mede o número absoluto de crimes registrados no ano."),
            ("B", "permite comparar realidades de populações de tamanhos diferentes."),
            ("C", "considera apenas os casos com autoria identificada."),
            ("D", "substitui os boletins de ocorrência."),
            ("E", "é calculada apenas em capitais."),
        ),
        correta="B",
        comentario=(
            "Taxas por 100 mil habitantes normalizam os números pelo tamanho da população, o que "
            "torna possível comparar municípios e estados diferentes. Números absolutos, sozinhos, "
            "distorcem a comparação."
        ),
        armadilha="Número absoluto x taxa: a diferença entre os dois é a pegadinha do tema.",
    ),
    Questao(
        id="atu-006",
        materia="atualidades",
        tema="Transformação digital e sociedade",
        nivel="medio",
        enunciado="A Lei Geral de Proteção de Dados (LGPD) tem por objetivo:",
        alternativas=(
            ("A", "proibir o uso de dados pessoais por qualquer instituição."),
            ("B", "proteger os direitos fundamentais de liberdade e privacidade, disciplinando o "
                  "tratamento de dados pessoais por pessoas físicas e jurídicas."),
            ("C", "regular exclusivamente redes sociais estrangeiras."),
            ("D", "substituir o Marco Civil da Internet."),
            ("E", "vedar o compartilhamento de dados entre órgãos públicos em qualquer hipótese."),
        ),
        correta="B",
        comentario=(
            "A LGPD (Lei 13.709/2018) disciplina o tratamento de dados pessoais, estabelecendo "
            "bases legais, direitos do titular e deveres de segurança da informação — inclusive "
            "para o poder público, com regras próprias."
        ),
        armadilha="A LGPD não proíbe o uso de dados: ela exige base legal e finalidade determinada.",
    ),
    Questao(
        id="atu-007",
        materia="atualidades",
        tema="Sistema de justiça",
        nivel="facil",
        enunciado="No processo penal brasileiro, cabe ao Ministério Público, em regra:",
        alternativas=(
            ("A", "julgar o acusado."),
            ("B", "promover, privativamente, a ação penal pública."),
            ("C", "presidir o inquérito policial."),
            ("D", "defender o réu hipossuficiente."),
            ("E", "executar mandados de prisão nas ruas."),
        ),
        correta="B",
        comentario=(
            "Art. 129, I, da CF. Julgar é função do Judiciário; presidir o inquérito é atribuição "
            "da autoridade policial; a defesa do hipossuficiente cabe à Defensoria Pública."
        ),
        armadilha="Trocar as funções das instituições do sistema de justiça é cobrança recorrente.",
    ),
    Questao(
        id="atu-008",
        materia="atualidades",
        tema="Saúde e sociedade",
        nivel="facil",
        enunciado="O Sistema Único de Saúde (SUS) é orientado, entre outros, pelos princípios de:",
        alternativas=(
            ("A", "universalidade, integralidade e equidade."),
            ("B", "exclusividade, onerosidade e seletividade."),
            ("C", "privatização, terceirização e concessão."),
            ("D", "centralização absoluta na União."),
            ("E", "atendimento restrito a contribuintes da previdência."),
        ),
        correta="A",
        comentario=(
            "O SUS é universal (para todos), integral (do preventivo ao curativo) e busca equidade "
            "(tratar desigualmente os desiguais). É organizado de forma descentralizada, com "
            "direção única em cada esfera de governo."
        ),
        armadilha="Confundir equidade com igualdade formal — não são a mesma coisa.",
    ),
    Questao(
        id="atu-009",
        materia="atualidades",
        tema="Desinformação",
        nivel="medio",
        enunciado=(
            "No enfrentamento à desinformação, a checagem de uma notícia recebida por aplicativo de "
            "mensagens deve começar por:"
        ),
        alternativas=(
            ("A", "compartilhar com os contatos para pedir opinião."),
            ("B", "verificar a fonte original, a data da publicação e a existência do fato em "
                  "veículos e órgãos oficiais."),
            ("C", "confiar quando a mensagem tem muitos encaminhamentos."),
            ("D", "aceitar a informação se houver imagem anexada."),
            ("E", "avaliar apenas se o texto tem erros de português."),
        ),
        correta="B",
        comentario=(
            "Fonte, data e confirmação independente são os três primeiros filtros. Volume de "
            "compartilhamentos e presença de imagem não atestam veracidade — imagens antigas fora "
            "de contexto são o formato mais comum de desinformação."
        ),
        armadilha="Encaminhamento em massa é indício de viralização, não de veracidade.",
    ),
    Questao(
        id="atu-010",
        materia="atualidades",
        tema="Federalismo e competências",
        nivel="medio",
        enunciado="Em matéria de segurança pública no Brasil, é correto afirmar que:",
        alternativas=(
            ("A", "a responsabilidade é exclusiva da União."),
            ("B", "a segurança pública é dever do Estado, direito e responsabilidade de todos, "
                  "exercida para a preservação da ordem pública e da incolumidade das pessoas e do "
                  "patrimônio."),
            ("C", "os Municípios não podem constituir guardas municipais."),
            ("D", "os Estados não têm competência para organizar suas polícias."),
            ("E", "a atuação preventiva é vedada às polícias militares."),
        ),
        correta="B",
        comentario=(
            "É a redação do caput do art. 144 da CF. Os Municípios podem constituir guardas "
            "municipais destinadas à proteção de seus bens, serviços e instalações (§ 8º)."
        ),
        armadilha="'Responsabilidade de todos' costuma ser suprimido nos distratores.",
    ),
    Questao(
        id="atu-011",
        materia="atualidades",
        tema="Trabalho e sociedade",
        nivel="facil",
        enunciado="A inclusão de pessoas com deficiência no serviço público é assegurada, entre outras formas, por:",
        alternativas=(
            ("A", "reserva de percentual de vagas em concursos públicos, na forma da lei."),
            ("B", "dispensa da comprovação de aptidão para o exercício do cargo."),
            ("C", "nomeação independentemente de aprovação em concurso."),
            ("D", "vedação de exames médicos admissionais."),
            ("E", "restrição a cargos administrativos."),
        ),
        correta="A",
        comentario=(
            "Art. 37, VIII, da CF: a lei reservará percentual dos cargos e empregos públicos para "
            "pessoas com deficiência. A reserva não afasta a exigência de aprovação no concurso nem "
            "a compatibilidade entre a deficiência e as atribuições do cargo."
        ),
        armadilha="Reserva de vagas não é nomeação automática — o concurso continua obrigatório.",
    ),
    Questao(
        id="atu-012",
        materia="atualidades",
        tema="Ética no serviço público",
        nivel="medio",
        enunciado=(
            "Um agente público que utiliza informação sigilosa obtida no exercício do cargo para "
            "obter vantagem pessoal viola diretamente o princípio da:"
        ),
        alternativas=(
            ("A", "eficiência."),
            ("B", "moralidade."),
            ("C", "celeridade."),
            ("D", "anterioridade."),
            ("E", "autotutela."),
        ),
        correta="B",
        comentario=(
            "A moralidade administrativa exige atuação honesta, leal e de boa-fé, para além da "
            "simples legalidade formal. A conduta descrita também viola impessoalidade e pode "
            "configurar improbidade e crime."
        ),
        armadilha="Eficiência trata de resultado; o que está em jogo aqui é a honestidade do meio.",
    ),
]
