"""Manual do Mapa — o e-book original revisado e ampliado (versão 2).

Mantém a história e o método do autor e acrescenta os capítulos que faltavam:
anatomia do erro, revisão espaçada, gestão de tempo na prova, rotina real,
corpo e sono, e protocolo de ansiedade.
"""

from __future__ import annotations

from dataclasses import dataclass, field


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


CAPITULOS: tuple[Capitulo, ...] = (
    Capitulo(
        id="introducao",
        numero="Abertura",
        titulo="A verdade que ninguém te conta",
        resumo="Três reprovações, uma decisão e 60 dias que viraram método.",
        paragrafos=(
            "Meu nome é Rafael Andrade. Se você está lendo isto, provavelmente já sentiu o que eu "
            "senti três vezes: abrir a lista de aprovados e não encontrar o seu nome.",
            "Não foi uma vez. Foram três. Três vezes eu estudei, três vezes me dediquei, e três "
            "vezes saí da sala achando que tinha feito o suficiente — e não tinha. Cada reprovação "
            "doía mais que a anterior, porque a cada tentativa eu via minha família esperando uma "
            "notícia diferente.",
            "Venho de família humilde. Não tive cursinho caro, nem mentor, nem tempo de sobra. "
            "Casei jovem, tive filhos, e a rotina que antes era 'só' trabalho virou trabalho, casa, "
            "filhos, contas — e uma vontade cada vez mais distante de vestir a farda.",
            "Na quarta tentativa, faltando 60 dias para a prova, tomei a decisão que mudou tudo: "
            "parar de estudar do jeito errado. Este manual é o mapa que eu queria ter recebido "
            "antes da primeira tentativa. E nesta segunda versão ele vem com o que faltava: o "
            "passo a passo em 30 dias e as ferramentas que, na época, eu fazia na mão.",
        ),
        destaque="Não faltou esforço nas três primeiras tentativas. Faltou direção.",
    ),
    Capitulo(
        id="erro",
        numero="Capítulo 1",
        titulo="O erro que me custou três reprovações",
        resumo="Confundir esforço com direção é a armadilha mais cara do concurseiro.",
        paragrafos=(
            "Durante anos eu acreditei numa equação simples: quanto mais eu estudasse, mais "
            "chances teria. Parece lógico — e é uma das maiores mentiras do universo dos concursos.",
            "Eu lia apostilas inteiras, assistia horas de videoaula, fazia resumos bonitos e "
            "organizados. E no dia da prova, travava. Por quê? Porque estudava teoria demais e "
            "treinava de menos. Eu conhecia o conteúdo 'por cima', mas não sabia responder do jeito "
            "que a banca cobra.",
            "Pior: eu estudava assuntos que quase nunca caem, só porque 'pareciam importantes', "
            "enquanto negligenciava os pontos que aparecem prova após prova. Eu estava remando "
            "forte, mas para o lado errado.",
            "Depois da terceira reprovação, me fiz a pergunta que mudou minha trajetória: 'Se eu "
            "tivesse só 60 dias e uma única chance, o que eu estudaria?' A resposta virou este método.",
        ),
        lista=(
            "❌ Jeito errado: teoria em excesso, resumos bonitos, videoaulas longas — sem treinar questões.",
            "✅ Jeito certo: foco no que cai, resolução de questões como método principal, correção ativa dos erros.",
        ),
    ),
    Capitulo(
        id="virada",
        numero="Capítulo 2",
        titulo="A virada: foco total e resolução de questões",
        resumo="Os dois pilares que sustentam tudo o que vem depois.",
        paragrafos=(
            "O método que apliquei nos meus dias decisivos se apoia em dois pilares. O primeiro é "
            "o <strong>foco total no que cai em prova</strong>. A banca tem padrão: repete temas, "
            "repete estilos de pergunta, repete pegadinhas. Mapear esse padrão e estudar só o que "
            "tem alta chance de cair foi o que me devolveu o tempo que eu não tinha.",
            "O segundo é a <strong>resolução de questões como método principal</strong>. Eu "
            "inverti a lógica: em vez de estudar teoria e 'depois' fazer questões, passei a estudar "
            "através das questões. Cada questão errada virava uma aula. Cada padrão de erro virava "
            "um ponto de atenção.",
            "Isso não é atalho — é economia de esforço. Questão resolvida obriga o cérebro a "
            "recuperar a informação, e recuperação é o que fixa memória em quem tem pouco tempo. "
            "Ler de novo dá sensação de aprendizado; responder dá aprendizado de verdade.",
        ),
        destaque="Teoria vira ponto quando passa por uma questão.",
    ),
    Capitulo(
        id="mapa30",
        numero="Capítulo 3",
        titulo="O Mapa em 30 dias",
        resumo="As quatro fases originais, recomprimidas para quem tem um mês.",
        paragrafos=(
            "O mapa original dividia 60 dias em quatro fases. Nesta versão, as mesmas quatro fases "
            "cabem em 30 dias — não porque o conteúdo encolheu, mas porque a plataforma faz por "
            "você o trabalho braçal que eu fazia à mão: escolher as questões certas, guardar os "
            "erros, lembrar a hora de revisar.",
            "Cada fase tem um objetivo único. Nada de tentar fazer tudo ao mesmo tempo — é assim "
            "que se perde o mês inteiro.",
        ),
        lista=(
            "Fase 1 · Dias 1–6 — Diagnóstico e priorização",
            "Fase 2 · Dias 7–18 — Imersão em questões com correção ativa",
            "Fase 3 · Dias 19–26 — Simulados cronometrados e ajuste fino",
            "Fase 4 · Dias 27–30 — Revisão enxuta e blindagem mental",
        ),
        destaque="Se você tem 60 dias, faça o mapa em 30 e repita a Fase 2 e 3 no segundo mês.",
    ),
    Capitulo(
        id="fase1",
        numero="Capítulo 4",
        titulo="Fase 1 — Diagnóstico e priorização",
        resumo="Parar de estudar no escuro.",
        paragrafos=(
            "O primeiro passo foi parar de adivinhar. Peguei os últimos editais e as últimas provas "
            "e mapeei: quais matérias mais aparecem e com que peso, quais temas se repetem dentro "
            "de cada matéria e quais eram, na prática, minhas maiores dificuldades reais — não as "
            "que eu 'achava' que tinha, mas as que os resultados mostravam.",
            "O diagnóstico foi feito resolvendo um bloco de questões de cada matéria <em>antes</em> "
            "de estudar teoria. Os erros dessa fase viraram meu mapa de prioridades.",
            "Prioridade real é o cruzamento de duas coisas: o quanto a matéria cai e o quanto você "
            "erra nela. Matéria que cai muito e você acerta é patrimônio — só manutenção. Matéria "
            "que cai pouco e você erra é armadilha de perfeccionista. O ponto que decide aprovação "
            "está na interseção: peso alto e acerto baixo.",
        ),
        destaque="Um diagnóstico ruim não é o que mostra muitos erros — é o que mostra erros mentirosos.",
    ),
    Capitulo(
        id="fase2",
        numero="Capítulo 5",
        titulo="Fase 2 — Imersão em questões",
        resumo="A fase que mais transforma candidato.",
        paragrafos=(
            "A regra era simples: todos os dias, sem exceção, um bloco de questões nas matérias "
            "priorizadas. Minha rotina, encaixada entre trabalho e família, era esta: manhã de "
            "30–40 minutos antes do trabalho com uma matéria de exatas; 20 minutos no intervalo "
            "revisando os erros do dia anterior; 50–60 minutos à noite, depois dos filhos dormirem, "
            "com Direito ou Português e correção comentada de cada erro.",
            "O segredo não estava na quantidade de horas — eu não tinha muitas — e sim na "
            "consistência e na correção ativa. Toda questão errada eu anotava o motivo do erro. "
            "Esse hábito simples foi o que mais acelerou minha evolução, e virou um capítulo "
            "inteiro nesta edição.",
        ),
        destaque="Dois blocos de 40 minutos por dia batem uma maratona de seis horas no domingo.",
    ),
    Capitulo(
        id="anatomia",
        numero="Capítulo 6",
        titulo="A anatomia do erro: as três categorias",
        resumo="Cada tipo de erro pede um remédio diferente.",
        novo=True,
        paragrafos=(
            "Este capítulo não existia na primeira edição, e é o que mais mudou meus resultados. "
            "Todo erro cabe em uma de três categorias — e tratar todas do mesmo jeito é o que faz "
            "o candidato estudar muito e evoluir pouco.",
            "Quem trata desatenção estudando mais teoria fica cansado e continua errando. Quem "
            "trata falta de conteúdo com 'mais atenção' continua sem saber a regra. Categorizar "
            "leva dez segundos por questão e muda o plano da semana inteira.",
            "Na plataforma, essa classificação alimenta automaticamente a sua fila de revisão. Na "
            "mão, use três símbolos na margem do caderno: 📚, 🎯 e ⏱.",
        ),
        lista=(
            "📚 Falta de conteúdo — você não sabia a regra. Ação: revisar aquele tema específico, e só ele.",
            "🎯 Pegadinha de interpretação — você sabia, mas caiu no jeito como a banca escreveu. Ação: reler grifando o comando.",
            "⏱ Desatenção — você sabia e errou por pressa. Ação: desacelerar na hora de marcar, não estudar mais.",
        ),
        destaque="Errar duas vezes pelo mesmo motivo é falha de método, não de memória.",
    ),
    Capitulo(
        id="revisao",
        numero="Capítulo 7",
        titulo="Revisão espaçada: por que 1, 3, 7 e 15 dias",
        resumo="O intervalo certo entre revisões vale mais que o tempo total de estudo.",
        novo=True,
        paragrafos=(
            "A memória não funciona por acúmulo, funciona por resgate. Cada vez que você recupera "
            "uma informação prestes a ser esquecida, ela fica mais resistente. Revisar cedo demais "
            "é desperdício; revisar tarde demais é recomeçar do zero.",
            "Por isso a fila de revisão trabalha com intervalos crescentes: a questão errada volta "
            "em 1 dia, depois 3, depois 7, depois 15. Acertou? Sobe de nível. Errou de novo? Volta "
            "para o começo do ciclo. Depois de três acertos seguidos, ela sai da fila como dominada.",
            "Na prática, isso significa que 20 erros recorrentes transformados em acertos valem "
            "mais, na folha de respostas, do que 20 temas novos que talvez não caiam.",
        ),
        destaque="A questão que você errou vale mais que a questão nova.",
    ),
    Capitulo(
        id="fase3",
        numero="Capítulo 8",
        titulo="Fase 3 — Simulados e ajuste fino",
        resumo="Treinar prova, não conteúdo.",
        paragrafos=(
            "Com a base mais sólida, chegou a hora de simular a prova de verdade: cronometrada, nas "
            "mesmas condições. O objetivo aqui não é mais aprender conteúdo novo — é treinar gestão "
            "de tempo, estratégia de execução, controle da ansiedade e resistência mental para as "
            "últimas questões.",
            "Depois de cada simulado, a mesma correção ativa da Fase 2. Simulado sem autópsia é só "
            "um dia cansado: leia acerto por matéria, tempo por questão e distribuição das "
            "categorias de erro. As questões caras e erradas — muito tempo e resposta errada — são "
            "as primeiras a mudar de lugar na sua estratégia.",
        ),
        destaque="Simulado é ensaio geral, não avaliação de valor pessoal.",
    ),
    Capitulo(
        id="tempo",
        numero="Capítulo 9",
        titulo="Gestão de tempo: a estratégia das três passadas",
        resumo="Como não deixar pontos fáceis para trás.",
        novo=True,
        paragrafos=(
            "Existe candidato que sabe mais e passa menos, porque administra mal o relógio. A "
            "estratégia das três passadas resolve a maior parte disso.",
            "<strong>Primeira passada:</strong> responda só o que você sabe de imediato; marque o "
            "que exigir conta ou releitura e siga. <strong>Segunda passada:</strong> volte às "
            "marcadas, agora com noção do tempo disponível. <strong>Terceira passada:</strong> "
            "feche o restante por eliminação, sem deixar nada em branco quando não há penalidade.",
            "Duas regras inegociáveis: nenhuma questão vale mais que outra — nunca gaste cinco "
            "minutos numa só; e transcreva o gabarito em blocos de dez, nunca só no final.",
        ),
        lista=(
            "Elimine alternativas com termos absolutos (sempre, nunca, exclusivamente) quando o tema admite exceção.",
            "Desconfie da alternativa que inventa prazo ou requisito que a lei não pede.",
            "Sobrando duas, decida em 15 segundos. Indecisão custa mais que erro.",
        ),
    ),
    Capitulo(
        id="rotina",
        numero="Capítulo 10",
        titulo="A rotina de quem trabalha e tem filhos",
        resumo="O plano que sobrevive à vida real.",
        novo=True,
        paragrafos=(
            "Sei que você provavelmente não tem seis horas por dia. Eu não tinha. O modelo que "
            "funciona para quem tem rotina cheia é o de blocos curtos e fixos, com um plano mínimo "
            "para os dias que dão errado — e eles vão dar.",
            "Plano mínimo é o seguinte: no pior dia possível, 15 minutos de revisão dos erros. Não "
            "é o ideal, mas mantém a corrente viva. Um dia zerado custa mais do que quatro dias "
            "medianos, porque quebrar a sequência é o começo do abandono silencioso.",
        ),
        lista=(
            "Prefira 2 ou 3 blocos de 30 a 50 minutos ao dia a uma maratona no domingo.",
            "Toda sessão termina com questões, nunca só com leitura passiva.",
            "Use os tempos mortos do dia para revisar questões já respondidas, não conteúdo novo.",
            "Reserve um dia de descanso por semana — ele é estratégico, não é preguiça.",
        ),
    ),
    Capitulo(
        id="corpo",
        numero="Capítulo 11",
        titulo="Corpo, sono e as outras etapas do concurso",
        resumo="Aprovação não termina na prova objetiva.",
        novo=True,
        paragrafos=(
            "Carreira policial cobra mais do que a prova escrita: costuma haver teste físico, "
            "avaliação documental e etapas de saúde. Deixar isso para depois da objetiva é comum — "
            "e é como preparar metade do caminho.",
            "Sobre o sono, um ponto que candidato ignora e depois lamenta: privação de sono derruba "
            "atenção sustentada e memória de trabalho, exatamente as funções que uma prova longa "
            "exige. Dormir bem nas noites anteriores rende mais que duas horas de revisão exausta.",
            "Na última semana: horário fixo para dormir, tela longe da cama, álcool fora, cafeína "
            "só até o meio da tarde. E na véspera, nada de virar a noite garantindo conteúdo.",
        ),
        destaque="Sono não é preguiça. É preparação técnica.",
    ),
    Capitulo(
        id="mental",
        numero="Capítulo 12",
        titulo="Blindagem mental: protocolo para a hora H",
        resumo="Ter o que fazer quando o nervosismo chegar.",
        novo=True,
        paragrafos=(
            "Ansiedade na prova não é sinal de despreparo — é o corpo se preparando para algo que "
            "importa. O problema não é sentir; é não ter plano para quando sentir.",
            "Monte seu protocolo de três gatilhos e treine nos simulados, não só na prova: se "
            "travar numa questão, marque, pule e siga; se o coração acelerar, faça quatro "
            "respirações lentas (quatro tempos para inspirar, seis para soltar) e volte; se der "
            "branco geral, feche os olhos por dez segundos, releia a última questão que você "
            "acertou com facilidade e retome dali.",
            "E lembre do que sustenta tudo: você não entra na sala achando que estudou. Entra "
            "sabendo seu percentual, sabendo onde está forte e onde precisa de cuidado. Foi "
            "exatamente isso que me fez entrar calmo na quarta tentativa.",
        ),
        destaque="Não é ausência de medo. É ter o que fazer quando ele chega.",
    ),
    Capitulo(
        id="fase4",
        numero="Capítulo 13",
        titulo="Fase 4 — Revisão final e reta de chegada",
        resumo="Menos volume, mais precisão.",
        paragrafos=(
            "Nos últimos dias resisti à tentação mais perigosa de todo candidato: aprender conteúdo "
            "novo de última hora. O foco passou a ser revisar apenas os pontos que eu ainda errava "
            "com frequência, reduzir aos poucos o volume para chegar descansado, cuidar do sono e "
            "revisar meus próprios erros já registrados.",
            "Reduza o curso inteiro a uma folha: dez regras que mais te derrubaram, uma linha cada. "
            "É o único material que você deve reler nos últimos dias e na manhã da prova.",
            "Na véspera eu praticamente não estudei: descansei, revisei por alto minhas anotações "
            "mais recorrentes e fui dormir cedo. No dia da prova, entrei calmo — porque eu sabia, "
            "com dados reais das minhas semanas de treino, exatamente onde estava forte.",
        ),
        lista=(
            "Kit da véspera: documento oficial com foto, comprovante de inscrição, canetas pretas transparentes, água, lanche.",
            "Confira endereço e tempo de deslocamento com folga real.",
            "Evite rodas de conversa sobre conteúdo na porta do local de prova.",
            "Transcreva o gabarito a cada dez questões e revise as marcadas antes de entregar.",
        ),
    ),
    Capitulo(
        id="sacrificio",
        numero="Capítulo 14",
        titulo="Sonho exige sacrifício",
        resumo="A parte que dói falar.",
        paragrafos=(
            "Preciso ser honesto: aprovação não veio de graça, e não veio fácil. Eu tive que abrir "
            "mão de coisas. Excluí minhas redes sociais nos últimos meses — não porque eu tivesse "
            "muito tempo livre nelas, mas porque cada minuto de distração ali era um minuto a menos "
            "com meus filhos ou de estudo direcionado. Reduzi encontros com amigos. Dormi menos em "
            "algumas semanas. Abri mão de descanso que eu sentia que merecia.",
            "E ainda assim, no meio do caminho, cheguei a pensar que não seria suficiente. A "
            "diferença, dessa vez, não foi só o sacrifício — foi o sacrifício certo, direcionado ao "
            "que realmente importava.",
            "Se você está numa fase corrida da vida, saiba: sonho grande sempre vai pedir um preço. "
            "A pergunta não é se você vai precisar sacrificar algo. A pergunta é se você está "
            "disposto a trocar o que é fácil agora pelo que você mais quer para o seu futuro e o da "
            "sua família.",
        ),
        destaque="Eu troquei. E hoje, vestindo a farda, sei que cada sacrifício valeu cada segundo.",
    ),
    Capitulo(
        id="conclusao",
        numero="Encerramento",
        titulo="Da reprovação à farda",
        resumo="O que fazer a partir de agora.",
        paragrafos=(
            "Eu reprovei três vezes antes de entender que o problema nunca foi minha capacidade — "
            "era meu método. No dia em que troquei 'estudar mais' por 'estudar certo', com foco "
            "total e resolução de questões, minha trajetória mudou completamente.",
            "Se você aplicar o Mapa da Aprovação com disciplina, respeitando as quatro fases, "
            "treinando com questões no estilo da banca e aceitando que sonho grande exige "
            "sacrifício, eu acredito genuinamente que você pode ser o próximo aprovado.",
            "Comece agora pelo Dia 1: o diagnóstico. Trinta dias atrás eu também não tinha mapa — "
            "tinha vontade. Hoje você tem os dois.",
        ),
        destaque="O caminho é possível. Eu sou a prova disso. — Rafael Andrade",
    ),
)

POR_ID = {c.id: c for c in CAPITULOS}
TOTAL_CAPITULOS = len(CAPITULOS)
NOVOS = sum(1 for c in CAPITULOS if c.novo)


def markdown() -> str:
    """Exporta o manual completo em Markdown (usado no download do aluno)."""
    linhas = [
        "# O Mapa da Aprovação — 2ª edição",
        "",
        "*Como fui aprovado Soldado PM 2ª Classe depois de reprovar 3 vezes — agora em 30 dias*",
        "",
        "Por Rafael Andrade",
        "",
        "---",
        "",
    ]
    for capitulo in CAPITULOS:
        marca = " *(novo nesta edição)*" if capitulo.novo else ""
        linhas.append(f"## {capitulo.numero} — {capitulo.titulo}{marca}")
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
