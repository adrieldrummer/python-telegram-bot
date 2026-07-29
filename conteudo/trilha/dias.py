"""Os 7 dias da apostila explicativa do edital PM-SP 2026.

Cada dia cobre uma grande área do edital: primeiro a explicação — para o aluno
entender o assunto, e não decorar em excesso — e depois a missão de questões,
que é o que fixa. Esta é a trilha do plano de entrada; os aprofundamentos ficam
nos módulos avançados.
"""

from __future__ import annotations

from . import Dia, Missao

DIAS: list[Dia] = [
    Dia(
        numero=1,
        fase="base",
        titulo="Língua Portuguesa — o terço mais caro da prova",
        promessa="Entender os pontos de português que a VUNESP cobra, sem gramática inteira.",
        tempo_min=60,
        aula=(
            "Português vale <strong>20 das 60 questões</strong>. Sozinha, essa matéria pesa mais "
            "que Informática e Administração Pública somadas. Se você só tivesse um dia para "
            "estudar, seria este.",
            "<strong>Interpretação de texto.</strong> Interpretar é entender o que o autor quis "
            "dizer, não apenas decodificar palavras. Textos literários (crônica, poema, conto) "
            "têm função estética e linguagem livre; textos não literários (notícia, edital, texto "
            "informativo) comunicam um fato ou uma regra de forma objetiva. Na prova: leia o texto "
            "inteiro antes de responder, identifique a ideia central e separe-a dos detalhes.",
            "<strong>Sinônimos e antônimos</strong> testam vocabulário: trocar a palavra sem mudar "
            "o sentido da frase. <strong>Sentido próprio</strong> (denotativo) é o literal, do "
            "dicionário; <strong>sentido figurado</strong> (conotativo) é simbólico — 'coração de "
            "pedra' não fala do órgão, fala de insensibilidade.",
            "<strong>Pontuação.</strong> A vírgula separa enumeração, isola aposto e marca termo "
            "deslocado. O erro mais cobrado: separar sujeito e verbo com vírgula — isso quase "
            "sempre está errado.",
            "<strong>Classes de palavras.</strong> Substantivo nomeia; adjetivo qualifica; numeral "
            "indica quantidade ou ordem; pronome substitui ou acompanha; verbo indica ação, estado "
            "ou fenômeno; advérbio modifica verbo, adjetivo ou outro advérbio; preposição liga "
            "termos; conjunção liga orações.",
            "<strong>Concordância</strong> é harmonia: verbal entre sujeito e verbo ('os alunos "
            "estudam'), nominal entre o substantivo e o que o acompanha ('as provas difíceis'). "
            "<strong>Regência</strong> é a preposição que o verbo ou o nome exige ('obedecer AO "
            "superior', 'apto PARA o serviço').",
            "<strong>Colocação pronominal:</strong> próclise (antes — 'não me diga'), ênclise "
            "(depois — 'diga-me') e mesóclise (no meio, com futuro — 'dir-me-á'). "
            "<strong>Crase</strong> é a fusão da preposição 'a' com o artigo 'a': 'vou à escola', "
            "'às vezes', 'às 14h'. Nunca antes de palavra masculina ou de verbo.",
        ),
        chave="Leia o comando duas vezes. Só depois leia as alternativas.",
        tarefas=(
            "Ler a explicação inteira sem pular",
            "Fazer o diagnóstico de 20 questões, sem consultar nada",
            "Classificar cada erro no Caderno de Erros",
        ),
        missao=Missao(
            tipo="diagnostico",
            titulo="Diagnóstico: 20 questões de todo o edital",
            quantidade=20,
            simulado_id="sim-diagnostico",
            descricao=(
                "Antes de estudar mais seis dias, você precisa saber onde está. Errar aqui é "
                "esperado — o resultado é o que monta o seu mapa de prioridades."
            ),
        ),
        frase="Vinte questões. Nenhuma outra matéria te dá tanto retorno por hora estudada.",
        pontos_base=80,
        diario="Qual ponto de português você percebeu que nunca tinha entendido de verdade?",
    ),
    Dia(
        numero=2,
        fase="base",
        titulo="Matemática I — números, porcentagem e regra de três",
        promessa="Dominar os temas de cálculo que se repetem em toda prova da banca.",
        tempo_min=60,
        aula=(
            "Matemática vale <strong>15 questões</strong> e é a matéria mais previsível do edital: "
            "poucos temas, sempre os mesmos. Hoje ficamos na parte de números e operações.",
            "<strong>Inteiros:</strong> positivos, negativos e zero. Atenção às regras de sinal — "
            "sinais iguais dão positivo, diferentes dão negativo, na multiplicação e na divisão. "
            "<strong>Racionais:</strong> tudo que se escreve como fração (1/2) ou decimal (0,5); "
            "saiba converter de um para o outro e operar com frações.",
            "<strong>MMC</strong> é o menor número múltiplo de dois ou mais ao mesmo tempo. Serve "
            "para igualar denominadores antes de somar frações — e cai também em problema de "
            "encontro ('a cada 4 e a cada 6 dias, quando coincidem?').",
            "<strong>Razão</strong> é a comparação entre duas grandezas (2 para 4 = 2/4). "
            "<strong>Proporção</strong> é a igualdade entre duas razões. Daí saem escala, mapa e "
            "receita. <strong>Porcentagem</strong> é uma razão com denominador 100: 20% de um "
            "valor é o valor × 0,20. A banca adora aumento e desconto sucessivos.",
            "<strong>Regra de três simples:</strong> antes de montar, pergunte se as grandezas são "
            "diretamente proporcionais (uma sobe, a outra sobe) ou inversamente (uma sobe, a outra "
            "desce — mais operários, menos dias). Errar essa identificação inverte o resultado "
            "inteiro. <strong>Média aritmética</strong> é a soma dividida pela quantidade.",
            "Dica de execução: em prova cronometrada, descarte alternativas absurdas por ordem de "
            "grandeza antes de fazer a conta. Eliminar duas opções em dez segundos vale mais que a "
            "conta perfeita em quatro minutos.",
        ),
        chave="Identifique se a proporção é direta ou inversa ANTES de montar o cálculo.",
        tarefas=("Ler a explicação", "Fazer as 15 questões", "Refazer no papel cada questão errada"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões de Matemática — números e operações",
            quantidade=15,
            materias=("matematica",),
        ),
        frase="Você não precisa ser bom em matemática. Precisa ser rápido nos seis temas que caem.",
        pontos_base=80,
    ),
    Dia(
        numero=3,
        fase="calculo",
        titulo="Matemática II — geometria, medidas e raciocínio lógico",
        promessa="Fechar a parte de cálculo com equações, geometria e lógica.",
        tempo_min=60,
        aula=(
            "<strong>Equação do 1º grau</strong> é uma igualdade com uma incógnita elevada à "
            "primeira potência (2x + 3 = 7): resolver é achar o valor de x que torna a igualdade "
            "verdadeira. <strong>Sistema</strong> é um conjunto de equações resolvidas ao mesmo "
            "tempo, por substituição (isolar uma variável) ou adição (somar para eliminar uma).",
            "<strong>Sistema métrico:</strong> tempo, comprimento, superfície e capacidade. Saber "
            "converter é meio caminho — quilômetro para metro, hora para minuto, litro para "
            "mililitro. Questão de conversão mal feita é ponto perdido por desatenção, não por "
            "falta de conhecimento.",
            "<strong>Tabelas e gráficos:</strong> a prova mostra dados em barras, linhas ou pizza e "
            "pede para extrair uma informação ou calcular a partir dela. Leia primeiro o título e "
            "a legenda; metade dos erros vem de ler o eixo errado.",
            "<strong>Geometria:</strong> perímetro é a soma dos lados (o contorno); área é o espaço "
            "que a figura ocupa (quadrado = lado × lado); volume é o espaço de um objeto "
            "tridimensional (cubo = lado³). <strong>Teorema de Pitágoras:</strong> no triângulo "
            "retângulo, a² = b² + c² — a hipotenusa ao quadrado é a soma dos quadrados dos catetos. "
            "Aparece em problema de distância e de altura.",
            "<strong>Raciocínio lógico</strong> não é fórmula: é organizar informação, achar padrão "
            "em sequência e concluir a partir de premissas. E <strong>situação-problema</strong> é "
            "a aplicação de tudo. O método são quatro passos, nesta ordem: ler com calma → "
            "identificar o que se pede → organizar os dados → calcular. Pular o segundo passo é o "
            "erro mais caro da prova.",
        ),
        chave="Ler com calma, identificar o que pede, organizar os dados, calcular. Nessa ordem.",
        tarefas=("Ler a explicação", "Fazer as 15 questões", "Anotar as fórmulas que faltaram"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — geometria, medidas e lógica",
            quantidade=15,
            materias=("matematica",),
        ),
        frase="Metade da prova de exatas se resolve sabendo o que a questão está pedindo.",
        pontos_base=80,
        diario="Em qual dos quatro passos (ler, identificar, organizar, calcular) você mais escorrega?",
    ),
    Dia(
        numero=4,
        fase="calculo",
        titulo="História — do século 20 à Constituição de 1988",
        promessa="Montar a linha do tempo que responde a maioria das questões de História.",
        tempo_min=55,
        aula=(
            "História e Geografia formam os <strong>15 pontos de Conhecimentos Gerais</strong>. O "
            "recorte é fechado e se repete: século 20, com foco em guerras, Guerra Fria e Brasil "
            "republicano. Estude por linha do tempo — data solta some da memória, encadeamento não.",
            "<strong>Primeira Guerra (1914–1918):</strong> disputas territoriais, corrida "
            "armamentista e alianças (Tríplice Aliança × Tríplice Entente); estopim no assassinato "
            "do arquiduque Francisco Ferdinando. A derrota alemã e o Tratado de Versalhes, com "
            "punições severas, prepararam o terreno para a Segunda.",
            "<strong>Nazifascismo e Segunda Guerra (1939–1945):</strong> nazismo na Alemanha "
            "(Hitler) e fascismo na Itália (Mussolini) — nacionalismo extremo, culto ao líder e "
            "perseguição a minorias, com o Holocausto. A guerra começa com a invasão da Polônia e "
            "termina com a derrota do Eixo.",
            "<strong>Guerra Fria (1947–1991):</strong> tensão sem confronto direto entre EUA "
            "(capitalismo) e União Soviética (socialismo): corrida armamentista e espacial, divisão "
            "da Alemanha, conflitos indiretos como Coreia e Vietnã. Depois dela vêm a "
            "<strong>globalização</strong> e as políticas neoliberais — menos Estado na economia, "
            "privatizações e abertura de mercados.",
            "<strong>Brasil.</strong> A Revolução de 1930 encerra a República Velha das oligarquias "
            "e leva Vargas ao poder: leis trabalhistas, industrialização e o Estado Novo "
            "(1937–1945), autoritário. O <strong>regime militar (1964–1985)</strong> traz censura, "
            "perseguição e o AI-5 (1968). A abertura vem com a Lei da Anistia (1979), as Diretas Já "
            "(1984), Tancredo Neves (1985) e a <strong>Constituição de 1988</strong>, a 'Constituição "
            "Cidadã'.",
            "<strong>Constituições republicanas</strong> em ordem: 1891, 1934, 1937 (outorgada por "
            "Vargas), 1946, 1967 (regime militar) e 1988 (atual). A banca gosta de trocar a ordem "
            "ou o contexto de cada uma.",
        ),
        chave="Decore encadeamento, não data solta: o que causou o quê.",
        tarefas=("Ler a explicação", "Fazer as 12 questões", "Escrever a linha do tempo de memória"),
        missao=Missao(
            tipo="questoes",
            titulo="12 questões de História",
            quantidade=12,
            materias=("historia",),
        ),
        frase="História de concurso é história com endereço: século 20, Brasil e mundo.",
        pontos_base=70,
    ),
    Dia(
        numero=5,
        fase="mundo",
        titulo="Geografia e Atualidades — Brasil, meio ambiente e o que está no noticiário",
        promessa="Cobrir a metade de Conhecimentos Gerais que muda a cada prova.",
        tempo_min=55,
        aula=(
            "<strong>Nova ordem mundial:</strong> com o fim da Guerra Fria, o mundo deixou de ser "
            "bipolar — EUA como potência dominante, ascensão da China e blocos regionais como a "
            "União Europeia ganhando peso.",
            "<strong>Natureza brasileira.</strong> Relevo: predominam planaltos e depressões, com "
            "poucas áreas de grande altitude. Hidrografia: uma das maiores redes do mundo, com "
            "destaque para a Bacia Amazônica. Clima: tropical e equatorial, com semiárido no "
            "Nordeste e subtropical no Sul.",
            "<strong>Biomas:</strong> Amazônia (maior floresta tropical, Norte), Mata Atlântica "
            "(litoral, muito desmatada), Cerrado (savana brasileira, Centro-Oeste, árvores de "
            "troncos retorcidos), Caatinga (semiárido nordestino, vegetação adaptada à seca), Pampa "
            "(campos do Sul) e Pantanal (maior planície alagável do mundo).",
            "<strong>População:</strong> crescimento demográfico desacelerando, concentração no "
            "litoral e nas regiões Sudeste e Nordeste, envelhecimento da população e migrações — do "
            "êxodo rural do século 20 aos deslocamentos internos de hoje.",
            "<strong>Economia:</strong> industrialização e urbanização se intensificam no século 20, "
            "concentradas no Sudeste; energia hidrelétrica e petróleo, com avanço de eólica e solar; "
            "agropecuária forte, com soja, cana e pecuária. <strong>Meio ambiente:</strong> "
            "aquecimento global, desmatamento, poluição e perda de biodiversidade.",
            "<strong>Atualidades</strong> cobram fatos dos <strong>últimos seis meses</strong> antes "
            "da prova, com atenção a São Paulo. Não estude notícia solta: acompanhe temas "
            "recorrentes (segurança pública, meio ambiente, economia e políticas sociais) em "
            "resumos semanais, nas semanas mais próximas da prova.",
        ),
        chave="Atualidades é assinatura de tema, não colecionar manchete.",
        tarefas=("Ler a explicação", "Fazer as 12 questões", "Escolher uma fonte semanal de atualidades"),
        missao=Missao(
            tipo="questoes",
            titulo="12 questões de Geografia e Atualidades",
            quantidade=12,
            materias=("geografia",),
        ),
        frase="O mapa do Brasil cai todo ano. A manchete de ontem, quase nunca.",
        pontos_base=70,
    ),
    Dia(
        numero=6,
        fase="mundo",
        titulo="Informática — cinco pontos baratos",
        promessa="Garantir as 5 questões que quase ninguém estuda direito.",
        tempo_min=45,
        aula=(
            "São <strong>5 questões</strong> de conteúdo repetitivo e previsível. Todo mundo estuda "
            "Português; poucos fecham Informática. É aqui que se ganha posição na classificação.",
            "<strong>Windows 10:</strong> organização em pastas e arquivos, atalhos, área de "
            "trabalho e área de transferência (copiar e colar), gerenciamento de programas.",
            "<strong>Word 2016:</strong> formatação de fontes, cabeçalho e rodapé, parágrafos e "
            "colunas, tabelas, quebras, numeração de páginas, índices e inserção de objetos. "
            "<strong>Excel 2016:</strong> células, linhas e colunas, tabelas e gráficos, fórmulas e "
            "funções (soma, média), macros, importação e classificação de dados. "
            "<strong>PowerPoint 2016:</strong> anotações do apresentador, réguas e guias, cabeçalho "
            "e rodapé, animação, transição e botões de ação.",
            "<strong>E-mail:</strong> preparo e envio de mensagens e anexação de arquivos — e a "
            "diferença entre Cc (todos veem) e Cco (cópia oculta). <strong>Internet:</strong> URL, "
            "links, busca e impressão de páginas.",
            "<strong>Google Workspace:</strong> Gmail, Agenda, Meet, Chat, Drive, Documentos, "
            "Planilhas, Apresentações e Formulários. <strong>Microsoft Teams:</strong> chat, "
            "chamadas, equipes e colaboração em tempo real nos arquivos do Office.",
            "Regra prática: entenda o que a função faz antes de decorar o atalho. A banca pergunta "
            "o efeito, não a tecla.",
        ),
        chave="Toda questão vale o mesmo ponto. Só o custo de acertar é diferente.",
        tarefas=("Ler a explicação", "Fazer as 10 questões", "Abrir o Excel e testar SOMA e MÉDIA"),
        missao=Missao(
            tipo="questoes",
            titulo="10 questões de Informática",
            quantidade=10,
            materias=("informatica",),
        ),
        frase="Ninguém reprova por Informática. Muita gente reprova por 2 pontos.",
        pontos_base=60,
    ),
    Dia(
        numero=7,
        fase="fechamento",
        titulo="Administração Pública e revisão final",
        promessa="Fechar o edital com a parte institucional — e revisar o mapa inteiro.",
        tempo_min=60,
        aula=(
            "<strong>5 questões</strong>, e a matéria mais 'decorável' do edital. Vem de quatro "
            "fontes: Constituição Federal, Constituição do Estado de São Paulo, Lei de Acesso à "
            "Informação e o Decreto estadual 68.155/2023.",
            "<strong>Constituição Federal.</strong> Título II — direitos e deveres individuais e "
            "coletivos (vida, liberdade, igualdade, segurança) e direitos políticos. Título III, "
            "Capítulo VII — regras da Administração Pública e situação dos militares dos Estados. "
            "Título V, Capítulo III — segurança pública como dever do Estado e direito de todos, "
            "com a Polícia Militar responsável pelo policiamento ostensivo e pela preservação da "
            "ordem pública.",
            "<strong>Os cinco princípios (LIMPE):</strong> Legalidade, Impessoalidade, Moralidade, "
            "Publicidade e Eficiência. Essa sigla cai em praticamente toda prova de concurso.",
            "<strong>Constituição do Estado de São Paulo.</strong> Organização do Executivo estadual "
            "e do Judiciário — incluindo a <strong>Justiça Militar do Estado</strong>, que julga "
            "crimes militares; regras da Administração estadual e a diferença entre servidor civil "
            "e servidor militar; e a seção específica sobre segurança pública e a Polícia Militar.",
            "<strong>Lei de Acesso à Informação (12.527/2011):</strong> qualquer cidadão pode pedir "
            "informação produzida ou guardada por órgão público, com prazo para resposta; o sigilo "
            "é exceção prevista em lei. O <strong>Decreto estadual 68.155/2023</strong> regulamenta "
            "como os órgãos paulistas aplicam essa lei.",
            "<strong>Revisão final.</strong> Agora que você entendeu o porquê de cada assunto, o "
            "próximo passo é resolver questão e revisar erro — não reler tudo de novo. A partir de "
            "amanhã, sua rotina é: bloco diário de questões nas matérias de maior peso e revisão do "
            "Caderno de Erros.",
        ),
        chave="Entendeu o assunto? Então pare de reler e comece a resolver.",
        tarefas=(
            "Ler a explicação",
            "Fazer o bloco final de 12 questões",
            "Montar seu plano até o dia da prova",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="12 questões — Administração Pública e revisão",
            quantidade=12,
            materias=("administracao", "portugues", "matematica"),
        ),
        frase="Sete dias para entender o edital inteiro. O resto é repetição — e ela começa agora.",
        pontos_base=120,
        diario="Escreva seu plano dos próximos dias: quantos blocos por dia e em quais matérias.",
    ),
]
