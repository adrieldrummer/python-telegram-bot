"""Fase 2 — Imersão em Questões (dias 7 a 18)."""

from __future__ import annotations

from . import Dia, Missao

DIAS: list[Dia] = [
    Dia(
        numero=7,
        fase="fase2",
        titulo="Português: o comando manda mais que o texto",
        promessa="Parar de perder ponto em questão que você sabia responder.",
        tempo_min=50,
        aula=(
            "Interpretação não é opinião sobre o texto: é conferência. A banca cobra o que está "
            "escrito, e o candidato responde o que ficou na cabeça depois da leitura rápida. Entre "
            "uma coisa e outra mora a maior sangria de pontos da prova.",
            "Adote hoje o protocolo dos três grifos: <strong>1)</strong> grife o comando (o que ele "
            "quer: 'é correto', 'NÃO é correto', 'exceto', 'respectivamente'); <strong>2)</strong> "
            "grife no texto o trecho que responde; <strong>3)</strong> elimine as alternativas que "
            "acrescentam informação que o texto não deu. Distrator bom quase sempre é verdadeiro no "
            "mundo, mas ausente no texto.",
            "Palavras absolutas — sempre, nunca, exclusivamente, em qualquer hipótese — são pistas. "
            "Não são gabarito automático, mas exigem prova. Se você não achar essa prova no texto "
            "ou na lei, desconfie.",
        ),
        chave="Leia o comando duas vezes. Só depois leia as alternativas.",
        tarefas=(
            "Aplicar o protocolo dos três grifos em todas as questões do bloco",
            "Classificar cada erro",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Português em foco",
            quantidade=15,
            materias=("portugues",),
        ),
        frase="A banca não te derruba com o que você não sabe. Ela derruba com o que você leu rápido.",
    ),
    Dia(
        numero=8,
        fase="fase2",
        titulo="Constitucional: art. 5º e segurança pública",
        promessa="Dominar o bloco que mais cai na sua prova.",
        tempo_min=50,
        aula=(
            "Direito Constitucional em concurso de praça se concentra em três ilhas: direitos e "
            "garantias fundamentais (art. 5º), organização do Estado e segurança pública (art. 144). "
            "Quem domina essas três responde a maioria das questões sem ter lido a Constituição inteira.",
            "No art. 5º, memorize por lógica, não por número: o que é inviolável, o que é garantido, "
            "o que é vedado, e as exceções. A banca vive nas exceções — casa é inviolável, <em>mas</em> "
            "flagrante, desastre e socorro entram a qualquer hora; ordem judicial, só durante o dia.",
            "No art. 144, saiba de cor quem faz o quê: PM faz polícia ostensiva e preserva a ordem "
            "pública; bombeiro militar executa defesa civil; PF apura infrações contra a União; PRF "
            "patrulha rodovias federais. E as PMs subordinam-se ao Governador, ainda que sejam "
            "forças auxiliares e reserva do Exército.",
        ),
        chave="Decore a exceção. A regra você acerta por bom senso; a exceção é onde caem os pontos.",
        tarefas=(
            "Fazer o bloco de Constitucional",
            "Anotar no caderno toda exceção que te pegou",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Direito Constitucional",
            quantidade=15,
            materias=("constitucional",),
        ),
        frase="Você não precisa saber toda a Constituição. Precisa saber a que cai.",
    ),
    Dia(
        numero=9,
        fase="fase2",
        titulo="Matemática: os três temas que pagam a conta",
        promessa="Resolver porcentagem e proporção sem travar.",
        tempo_min=50,
        aula=(
            "Matemática de prova de praça é repetitiva: porcentagem, regra de três, razão e "
            "proporção, equação do 1º grau, média e sequências resolvem a grande maioria. Não é "
            "hora de estudar matemática — é hora de estudar <em>essas</em> matemáticas.",
            "Três reflexos para hoje: aumento e desconto do mesmo percentual não se anulam (200 → "
            "+10% → 220 → −10% → 198); grandeza inversamente proporcional inverte a fração (mais "
            "gente, menos tempo); e antes de calcular, traduza a frase em equação — 'o triplo de um "
            "número diminuído de 8' é 3x − 8, não 3(x − 8).",
            "Se você trava em cálculo, use a estimativa: descarte alternativas absurdas por ordem "
            "de grandeza antes de fazer a conta. Em prova cronometrada, eliminar duas alternativas "
            "em 10 segundos vale mais do que a conta perfeita em 4 minutos.",
        ),
        chave="Em exatas, o inimigo é o relógio — não a fórmula.",
        tarefas=("Fazer o bloco de exatas", "Refazer, no papel, cada questão errada"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Matemática e Raciocínio Lógico",
            quantidade=15,
            materias=("matematica",),
        ),
        frase="Você não precisa ser bom em matemática. Precisa ser rápido nos seis temas que caem.",
    ),
    Dia(
        numero=10,
        fase="fase2",
        titulo="Penal: separar o que a banca gosta de confundir",
        promessa="Nunca mais trocar furto, roubo e extorsão.",
        tempo_min=50,
        aula=(
            "Direito Penal cai por pares confundíveis. A banca raramente pergunta 'o que é furto'. "
            "Ela descreve uma cena e espera que você escolha entre dois tipos parecidos.",
            "Fixe as fronteiras: furto x roubo — o divisor é violência ou grave ameaça à pessoa. "
            "Roubo x extorsão — no roubo o agente pega; na extorsão a vítima precisa colaborar. "
            "Peculato x concussão x corrupção passiva — apropriar-se, exigir, solicitar/receber. "
            "Resistência x desobediência x desacato — com violência, sem violência, ofendendo.",
            "Outra fronteira que cai muito: excludente de ilicitude (art. 23 — legítima defesa, "
            "estado de necessidade, estrito cumprimento de dever legal, exercício regular de direito) "
            "não é a mesma coisa que excludente de culpabilidade (coação irresistível, obediência "
            "hierárquica, doença mental). Na primeira, não há crime; na segunda, há crime sem "
            "reprovação ao agente.",
        ),
        chave="Estude penal em pares. É assim que a banca cobra.",
        tarefas=("Fazer o bloco de Penal", "Escrever, com suas palavras, três pares confundíveis"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Direito Penal",
            quantidade=15,
            materias=("penal",),
        ),
        frase="Quem confunde o par erra a questão inteira, mesmo sabendo os dois crimes.",
    ),
    Dia(
        numero=11,
        fase="fase2",
        titulo="Primeira revisão espaçada: o retorno dos seus erros",
        promessa="Fechar buracos antes que eles virem hábito.",
        tempo_min=40,
        aula=(
            "Hoje a plataforma devolve as questões que você errou nos últimos dias — as que já "
            "venceram o prazo de revisão. Esse é o mecanismo que o autor do método fazia à mão, "
            "revisando o caderno de erros nos 20 minutos do intervalo do trabalho.",
            "O ciclo é 1 → 3 → 7 → 15 dias. Acertou uma questão do caderno? Ela sobe de nível e "
            "volta mais tarde. Errou de novo? Ela cai para o começo do ciclo e volta amanhã. "
            "Depois de três acertos seguidos, ela sai do caderno como <strong>dominada</strong>.",
            "Não pule este dia achando que é 'só revisão'. Estatisticamente, é o bloco que mais "
            "aumenta a nota final: transformar 20 erros recorrentes em acertos vale mais do que "
            "aprender 20 temas novos que talvez não caiam.",
        ),
        chave="A questão que você errou vale mais que a questão nova.",
        tarefas=("Revisar todas as questões vencidas", "Reclassificar o erro se ele mudou de motivo"),
        missao=Missao(
            tipo="revisao",
            titulo="Revisão espaçada do Caderno de Erros",
            quantidade=12,
            descricao="A plataforma seleciona as questões vencidas do seu caderno.",
        ),
        frase="Ninguém passa aprendendo tudo. Passa quem para de errar o mesmo.",
        diario="Alguma questão voltou a te enganar? O que exatamente te enganou de novo?",
    ),
    Dia(
        numero=12,
        fase="fase2",
        titulo="Administrativo: princípios, atos e o que é exceção",
        promessa="Ganhar as questões de LIMPE e de atos administrativos.",
        tempo_min=50,
        aula=(
            "Administrativo tem duas famílias que caem sempre: princípios (LIMPE — legalidade, "
            "impessoalidade, moralidade, publicidade, eficiência) e atos administrativos (elementos, "
            "atributos, anulação x revogação).",
            "Grave os cinco elementos — competência, finalidade, forma, motivo, objeto — e lembre "
            "que competência, finalidade e forma são sempre vinculados. O mérito (conveniência e "
            "oportunidade) mora apenas em motivo e objeto. E os atributos: presunção de legitimidade, "
            "imperatividade, autoexecutoriedade e tipicidade — imperatividade impõe, "
            "autoexecutoriedade executa.",
            "A dupla que mais derruba: anulação (vício de legalidade, efeito retroativo/ex tunc) e "
            "revogação (ato legal, inconveniente, efeito ex nunc). Pela autotutela, a própria "
            "Administração faz as duas.",
        ),
        chave="Anulação olha para trás. Revogação olha para frente.",
        tarefas=("Fazer o bloco de Administrativo", "Reescrever de memória os 5 elementos do ato"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Direito Administrativo",
            quantidade=15,
            materias=("administrativo",),
        ),
        frase="Administrativo é decoreba com lógica. Entenda a lógica e a decoreba encolhe.",
    ),
    Dia(
        numero=13,
        fase="fase2",
        titulo="Português II: concordância, crase e regência",
        promessa="Fechar a parte gramatical que cai todo ano.",
        tempo_min=50,
        aula=(
            "Gramática de prova se resolve com poucos gatilhos. Crase: só existe diante de palavra "
            "feminina que aceite artigo; teste trocando por palavra masculina — se virar 'ao', tem "
            "crase. Antes de verbo, de pronome pessoal e de palavra masculina, não tem.",
            "Concordância: 'haver' no sentido de existir é impessoal e não vai para o plural — "
            "'houve muitas ocorrências'. Já 'existir' concorda normalmente. E as expressões 'é "
            "proibido', 'é necessário' só flexionam quando há determinante: 'é proibida <em>a</em> "
            "entrada'.",
            "Regência: assistir (ver) pede 'a'; obedecer pede 'a'; chegar pede 'a', não 'em'; "
            "preferir não aceita 'mais do que'. São meia dúzia de verbos que respondem quase todas "
            "as questões do tema.",
        ),
        chave="Gramática de concurso é lista curta de gatilhos, não a gramática inteira.",
        tarefas=("Fazer o bloco de Português", "Anotar os gatilhos que você errou"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Português (gramática)",
            quantidade=15,
            materias=("portugues",),
        ),
        frase="Ponto de gramática é ponto barato — se você tratar como lista, não como matéria.",
    ),
    Dia(
        numero=14,
        fase="fase2",
        titulo="Legislação especial: drogas, ECA, Maria da Penha",
        promessa="Dominar as leis que aparecem na rotina policial e na prova.",
        tempo_min=50,
        aula=(
            "Legislação especial tem peso menor, mas é a matéria mais 'comprável' da lista: são "
            "poucos artigos, cobrados quase sempre no mesmo recorte.",
            "Lei de Drogas: o art. 28 (porte para consumo) gera advertência, prestação de serviços e "
            "medida educativa — não prisão. E a distinção entre uso e tráfico não é só quantidade: "
            "o § 2º manda considerar natureza, quantidade, local, condições da ação, circunstâncias "
            "sociais e pessoais, conduta e antecedentes. ECA: criança é até 12 anos incompletos "
            "(medida de proteção); adolescente, de 12 a 18 (medida socioeducativa).",
            "Maria da Penha: violência doméstica não é só física — inclui psicológica, sexual, "
            "patrimonial e moral, e não exige coabitação. Abuso de autoridade: exige finalidade "
            "específica de prejudicar ou favorecer; divergência na interpretação da lei não configura abuso.",
        ),
        chave="Leis especiais caem em recorte fixo. Estude o recorte, não a lei inteira.",
        tarefas=("Fazer o bloco de Legislação", "Listar as três leis que mais te derrubaram"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Legislação Especial",
            quantidade=15,
            materias=("legislacao",),
        ),
        frase="Pontos baratos existem. Ignorá-los é caro.",
    ),
    Dia(
        numero=15,
        fase="fase2",
        titulo="Informática e Atualidades: o troco que decide a classificação",
        promessa="Comprar pontos rápidos nas matérias de menor peso.",
        tempo_min=45,
        aula=(
            "Essas duas matérias costumam ser tratadas como sobra — e é justamente por isso que "
            "elas decidem posições na lista de classificação. Todo mundo estuda Direito; poucos "
            "fecham Informática.",
            "Informática cai em quatro blocos: pacote de escritório (fórmulas e referências), "
            "navegadores e internet (HTTPS, cookies, DNS), segurança (phishing, ransomware, backup, "
            "senha forte) e conceitos de hardware/software. É repetição pura.",
            "Atualidades e cidadania: não estude notícia solta. Estude tema recorrente — segurança "
            "pública e sistema de justiça, direitos humanos, políticas sociais, meio ambiente e "
            "LGPD/desinformação. Uma questão de atualidade bem estudada vale o mesmo que uma de "
            "Direito Penal.",
        ),
        chave="Toda questão vale o mesmo ponto. Só o custo de acertar é diferente.",
        tarefas=("Fazer o bloco misto", "Classificar erros por categoria"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Informática + Atualidades",
            quantidade=15,
            materias=("informatica", "atualidades"),
        ),
        frase="Ninguém reprova por causa de Informática. Muita gente reprova por 2 pontos.",
    ),
    Dia(
        numero=16,
        fase="fase2",
        titulo="Segunda revisão espaçada + ajuste de rota",
        promessa="Confirmar o que já virou domínio e o que ainda resiste.",
        tempo_min=45,
        aula=(
            "Metade do caminho. Hoje é dia de olhar para trás com frieza: quais matérias subiram "
            "desde o diagnóstico e quais teimam em ficar embaixo?",
            "Se uma matéria continua abaixo de 50% mesmo depois de um bloco dedicado, o problema "
            "raramente é 'estudar mais'. Olhe a categoria dos seus erros nela: se predomina falta "
            "de conteúdo, você precisa de teoria curta e específica antes das questões; se predomina "
            "pegadinha, o problema é leitura; se predomina desatenção, é ritmo.",
            "Este é o dia em que a maioria dos candidatos desiste em silêncio — não abandonando, mas "
            "afrouxando. O bloco de hoje é curto por decisão de método: manter a corrente viva vale "
            "mais do que um dia heroico seguido de três dias parados.",
        ),
        chave="Se a matéria não sobe, mude o remédio — não a dose.",
        tarefas=("Revisar as questões vencidas", "Comparar o painel com a sua linha de base"),
        missao=Missao(
            tipo="revisao",
            titulo="Revisão espaçada + leitura do painel",
            quantidade=15,
        ),
        frase="Metade do mapa percorrida. Ninguém percorre metade por acaso.",
        diario="Qual matéria mais evoluiu? Qual resiste? Que remédio ela pede?",
    ),
    Dia(
        numero=17,
        fase="fase2",
        titulo="Raciocínio lógico: negar proposição sem errar",
        promessa="Ganhar as questões de lógica que quase todo mundo chuta.",
        tempo_min=50,
        aula=(
            "Lógica proposicional é o tema mais 'mecânico' da prova: quem sabe as três negações "
            "acerta praticamente todas.",
            "Negação de 'todo A é B' → 'existe pelo menos um A que não é B' (nunca 'nenhum A é B'). "
            "Negação de 'se p então q' → 'p e não q' (nunca a contrapositiva, nunca a recíproca). "
            "Negação de 'p e q' → 'não p ou não q'; de 'p ou q' → 'não p e não q' (leis de De Morgan).",
            "Repare que a banca sempre oferece o 'contrário extremo' como distrator, porque ele soa "
            "natural. Negar não é inverter — é apenas afirmar que aquilo não acontece.",
        ),
        chave="Negar ≠ contrariar. Essa distinção vale pontos todo ano.",
        tarefas=("Fazer o bloco de lógica", "Escrever as três regras de negação de memória"),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões — Raciocínio Lógico e exatas",
            quantidade=15,
            materias=("matematica",),
        ),
        frase="Lógica é a matéria mais justa da prova: ou você sabe a regra, ou não.",
    ),
    Dia(
        numero=18,
        fase="fase2",
        titulo="Fechamento da imersão: bloco grande e misto",
        promessa="Provar para você mesmo que a curva subiu.",
        tempo_min=60,
        aula=(
            "Último dia da fase mais pesada. O bloco de hoje é maior e misturado — 25 questões de "
            "todas as matérias, na sequência em que a prova costuma embaralhar.",
            "Preste atenção em algo além do acerto: o cansaço. A partir de qual questão a sua "
            "atenção caiu? Esse é o seu 'ponto de fadiga', e ele é uma informação valiosa para a "
            "Fase 3, quando você vai treinar prova completa. Quem conhece o próprio ponto de fadiga "
            "sabe onde precisa de uma pausa técnica de 30 segundos.",
            "A partir de amanhã, o jogo muda de novo: menos aprender, mais executar. Simulado é "
            "treino de prova, não de conteúdo.",
        ),
        chave="Você não vai fazer a prova sabendo tudo. Vai fazer sabendo o que treinou.",
        tarefas=("Fazer o bloco de 25 questões", "Anotar em que questão a atenção caiu"),
        missao=Missao(
            tipo="questoes",
            titulo="Bloco misto de 25 questões",
            quantidade=25,
        ),
        frase="Fase 2 concluída. Agora você treina prova.",
        pontos_base=90,
        diario="Em que número de questão sua atenção caiu? O que você fez a respeito?",
    ),
]
