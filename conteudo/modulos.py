"""Módulos avançados — o que fica além da trilha de 7 dias.

A trilha explica o edital e cabe no plano de entrada. Os módulos daqui cobrem
o que decide aprovação depois da objetiva: redação, teste físico, etapas
eliminatórias, aprofundamento por matéria e reta final. Cada módulo exige um
**recurso** de plano — quem não tem, vê a capa com cadeado e a tela de upgrade.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Aula:
    id: str
    titulo: str
    resumo: str
    paragrafos: tuple[str, ...]
    chave: str = ""
    lista: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Modulo:
    id: str
    titulo: str
    chamada: str
    descricao: str
    recurso: str
    capa: str
    etiqueta: str
    ordem: int
    aulas: tuple[Aula, ...]
    materias: tuple[str, ...] = ()


MODULOS: tuple[Modulo, ...] = (
    Modulo(
        id="redacao",
        titulo="Redação que não elimina",
        chamada="A prova dissertativa reprova quem passou na objetiva. Não seja essa pessoa.",
        descricao=(
            "Estrutura, critérios de correção e três modelos comentados para escrever com "
            "segurança no dia da prova."
        ),
        recurso="avancado",
        capa="redacao",
        etiqueta="Etapa eliminatória",
        ordem=1,
        aulas=(
            Aula(
                id="redacao-estrutura",
                titulo="A estrutura que a banca espera",
                resumo="Introdução, desenvolvimento e conclusão — com função definida.",
                paragrafos=(
                    "Prova dissertativa de concurso não pede literatura: pede clareza. A banca "
                    "avalia se você entendeu o tema, se defendeu uma posição e se escreve dentro da "
                    "norma-padrão. Texto bonito e vazio perde para texto simples e organizado.",
                    "<strong>Introdução (4 a 5 linhas):</strong> apresente o tema e anuncie a sua "
                    "tese — a posição que você vai defender. Nada de rodeio: quem lê 300 textos por "
                    "dia decide em três linhas se o seu está organizado.",
                    "<strong>Desenvolvimento (dois parágrafos):</strong> um argumento por parágrafo, "
                    "cada um com fundamentação — dado, exemplo, referência legal ou consequência "
                    "prática. Evite frases de efeito; prefira frases que provem algo.",
                    "<strong>Conclusão (4 a 5 linhas):</strong> retome a tese e proponha "
                    "encaminhamento. Em tema de segurança pública, uma proposta viável vale mais "
                    "que um apelo emocional.",
                ),
                chave="Uma ideia por parágrafo. Parágrafo com duas ideias é parágrafo confuso.",
                lista=(
                    "Não use primeira pessoa do singular ('eu acho').",
                    "Não copie trechos do enunciado como se fossem seus.",
                    "Respeite o limite de linhas: passar ou faltar custa nota.",
                    "Letra legível é critério, não detalhe.",
                ),
            ),
            Aula(
                id="redacao-criterios",
                titulo="Como a nota é calculada",
                resumo="O que pesa na correção e onde se perde ponto sem perceber.",
                paragrafos=(
                    "A correção costuma olhar quatro eixos: adequação ao tema e ao gênero, "
                    "coerência e coesão, argumentação e domínio da norma-padrão. Fugir do tema "
                    "zera; os demais eixos descontam.",
                    "Erros que mais custam: fuga parcial do tema (falar de segurança em geral quando "
                    "o tema é específico), parágrafos sem conector, repetição da mesma palavra em "
                    "todo o texto e desvio grave de concordância ou crase — justamente o que você "
                    "estudou no Dia 1.",
                    "Prática que resolve: escreva três textos completos, cronometrados, e releia "
                    "cada um no dia seguinte com uma caneta na mão. Reler no mesmo dia não mostra o "
                    "erro; reler depois, sim.",
                ),
                chave="Fuga ao tema zera. Antes de escrever, sublinhe o comando duas vezes.",
            ),
            Aula(
                id="redacao-temas",
                titulo="Temas prováveis e repertório",
                resumo="O que costuma cair em concurso de carreira policial — e o que citar.",
                paragrafos=(
                    "Temas recorrentes: segurança pública e policiamento comunitário, violência "
                    "doméstica, drogas e políticas públicas, uso da força e direitos humanos, "
                    "tecnologia na segurança (câmeras corporais, monitoramento), juventude e "
                    "oportunidades.",
                    "Repertório que sustenta argumento sem exigir decoreba: a Constituição de 1988 "
                    "(segurança pública como dever do Estado e responsabilidade de todos), o papel "
                    "da PM no policiamento ostensivo, dados de fontes públicas e a lógica de "
                    "prevenção versus repressão.",
                    "Monte três 'blocos' prontos de repertório e treine encaixá-los. Não é decorar "
                    "texto: é ter três referências firmes que você sabe explicar em duas linhas.",
                ),
                chave="Repertório é ferramenta, não enfeite: cite o que você sabe explicar.",
            ),
        ),
    ),
    Modulo(
        id="taf",
        titulo="TAF sem susto",
        chamada="O teste físico elimina candidato aprovado na prova escrita todos os anos.",
        descricao=(
            "Plano de 8 semanas para corrida, força e abdominal, com progressão semanal e "
            "orientação para o dia do teste."
        ),
        recurso="avancado",
        capa="capa-taf",
        etiqueta="Etapa eliminatória",
        ordem=2,
        aulas=(
            Aula(
                id="taf-o-que-cai",
                titulo="O que o TAF cobra",
                resumo="Provas de resistência e força, com índice mínimo por sexo e idade.",
                paragrafos=(
                    "O teste de aptidão física costuma reunir corrida de resistência (12 minutos ou "
                    "distância fixa), flexão na barra ou apoio de frente, abdominal em tempo e, em "
                    "alguns certames, natação ou impulsão. Os índices variam por sexo e faixa "
                    "etária, e estão no edital — leia a tabela antes de treinar.",
                    "A lógica é simples e implacável: é etapa eliminatória, e não adianta 'ser "
                    "forte' em uma prova e zerar em outra. O treino precisa cobrir resistência "
                    "aeróbica e força localizada ao mesmo tempo.",
                    "Regra de ouro: quem começa oito semanas antes chega; quem começa duas semanas "
                    "antes se machuca. Progressão gradual não é conselho de saúde — é estratégia "
                    "para não ser eliminado por lesão.",
                ),
                chave="Confira no edital a tabela de índices do SEU sexo e da SUA faixa etária.",
            ),
            Aula(
                id="taf-plano",
                titulo="Plano de 8 semanas",
                resumo="Três treinos por semana, com progressão previsível.",
                paragrafos=(
                    "<strong>Semanas 1-2 — base.</strong> Três sessões: 25 a 30 minutos de corrida "
                    "leve ou caminhada rápida alternada; 3 séries de abdominais até 60% do máximo; "
                    "3 séries de apoio de frente (pode ser com joelhos apoiados no início).",
                    "<strong>Semanas 3-5 — carga.</strong> Corrida contínua de 30 a 40 minutos, "
                    "somando um tiro semanal de 6 × 400 m com pausa curta; abdominais em séries "
                    "cronometradas de 1 minuto; barra assistida ou remada, 4 séries.",
                    "<strong>Semanas 6-7 — específico.</strong> Simule o teste completo uma vez por "
                    "semana, na ordem e no ritmo do TAF, e anote os números. É aqui que você "
                    "descobre qual prova é seu gargalo — e ela vira prioridade.",
                    "<strong>Semana 8 — afinamento.</strong> Reduza volume pela metade, mantenha a "
                    "intensidade, durma bem e não faça nada novo. Chegar descansado vale mais que "
                    "um treino heroico na véspera.",
                ),
                chave="Simule o teste inteiro antes do dia oficial. Surpresa no TAF custa a vaga.",
                lista=(
                    "Tênis usado e confortável — nada de estrear calçado no dia.",
                    "Hidratação nas 24 horas anteriores, não só na hora.",
                    "Aquecimento de 10 minutos antes de qualquer avaliação.",
                    "Dor aguda não é 'garra': é sinal para parar e procurar avaliação.",
                ),
            ),
        ),
    ),
    Modulo(
        id="etapas",
        titulo="Etapas eliminatórias sem mistério",
        chamada="Saúde, psicológico e investigação social reprovam mais por desorganização que por mérito.",
        descricao=(
            "O que cada etapa avalia, os documentos exigidos e os erros que eliminam candidato "
            "bem preparado."
        ),
        recurso="avancado",
        capa="documentos",
        etiqueta="Etapa eliminatória",
        ordem=3,
        aulas=(
            Aula(
                id="etapas-saude",
                titulo="Exames de saúde",
                resumo="A etapa em que se perde vaga por prazo, não por doença.",
                paragrafos=(
                    "A avaliação de saúde reúne exames laboratoriais, de imagem, avaliação clínica "
                    "e odontológica. O edital lista exatamente quais exames apresentar e em qual "
                    "validade — normalmente poucos meses.",
                    "O erro mais comum não é reprovação clínica: é chegar sem um exame, com laudo "
                    "vencido ou sem assinatura e carimbo do profissional. Monte uma pasta física e "
                    "uma digital, com checklist do edital marcado item a item.",
                    "Se você tem alguma condição de saúde controlada, leve relatório médico "
                    "atualizado explicando o quadro e o tratamento. Documentação clara evita "
                    "interpretação desfavorável.",
                ),
                chave="Faça o checklist do edital e marque item por item. Prazo vencido elimina.",
            ),
            Aula(
                id="etapas-psicologico",
                titulo="Avaliação psicológica",
                resumo="Não existe gabarito — existe coerência.",
                paragrafos=(
                    "A avaliação psicológica verifica se o candidato tem o perfil exigido para a "
                    "função: controle emocional, capacidade de seguir normas, tolerância à "
                    "frustração e relacionamento interpessoal. Costuma combinar testes objetivos, "
                    "projetivos e entrevista.",
                    "Não tente 'adivinhar a resposta certa'. Os testes têm escalas de validade que "
                    "detectam respostas montadas para agradar — e o resultado disso é justamente a "
                    "inaptidão. Responda com sinceridade e coerência.",
                    "O que ajuda de verdade: dormir bem na véspera, chegar com antecedência, ler "
                    "cada instrução até o fim e responder no ritmo pedido. Cansaço e pressa "
                    "produzem contradições que o teste captura.",
                ),
                chave="Responder o que 'parece bonito' é o caminho mais rápido para ser considerado inapto.",
            ),
            Aula(
                id="etapas-investigacao",
                titulo="Investigação social",
                resumo="Comece a juntar certidões hoje, não quando for convocado.",
                paragrafos=(
                    "A investigação social analisa vida pregressa e conduta: certidões criminais e "
                    "cíveis das comarcas onde você morou, antecedentes, situação eleitoral e "
                    "militar, dados profissionais e, em alguns casos, informações de vizinhança e "
                    "redes sociais públicas.",
                    "Duas causas frequentes de eliminação: omitir informação no formulário — a "
                    "omissão pesa mais que o fato em si — e não conseguir reunir certidões a tempo, "
                    "porque algumas comarcas demoram semanas.",
                    "Ação prática para esta semana: liste todas as cidades onde você morou nos "
                    "últimos cinco anos e solicite as certidões. Guarde tudo digitalizado, com data.",
                ),
                chave="Omitir é pior que declarar. Transparência é critério de conduta.",
                lista=(
                    "Certidões criminais estadual e federal das comarcas de residência",
                    "Certidão de distribuição cível",
                    "Quitação eleitoral e situação militar",
                    "Comprovantes de vínculos empregatícios anteriores",
                ),
            ),
        ),
    ),
    Modulo(
        id="portugues-avancado",
        titulo="Português avançado — as pegadinhas da VUNESP",
        chamada="Vinte questões. Aqui estão os padrões que se repetem prova após prova.",
        descricao="Interpretação sob pressão, gramática de alta incidência e treino dirigido.",
        recurso="avancado",
        capa="capa-fase1",
        etiqueta="Aprofundamento",
        ordem=4,
        materias=("portugues",),
        aulas=(
            Aula(
                id="port-av-interpretacao",
                titulo="Interpretação: o protocolo dos três grifos",
                resumo="Como não perder ponto em questão que você sabia responder.",
                paragrafos=(
                    "Interpretação não é opinião sobre o texto: é conferência. A banca cobra o que "
                    "está escrito; o candidato responde o que ficou na cabeça depois da leitura "
                    "rápida. Entre uma coisa e outra mora a maior sangria de pontos da prova.",
                    "<strong>Protocolo:</strong> 1) grife o comando (o que ele quer: 'é correto', "
                    "'NÃO é correto', 'exceto', 'respectivamente'); 2) grife no texto o trecho que "
                    "responde; 3) elimine alternativas que acrescentam informação que o texto não "
                    "deu — distrator bom costuma ser verdadeiro no mundo, mas ausente no texto.",
                    "Palavras absolutas — sempre, nunca, exclusivamente — exigem prova explícita. "
                    "Se você não achar essa prova no texto, desconfie.",
                ),
                chave="Distrator bom é verdadeiro no mundo e ausente no texto.",
            ),
            Aula(
                id="port-av-gramatica",
                titulo="Gramática de alta incidência",
                resumo="A lista curta de gatilhos que resolve a maioria das questões.",
                paragrafos=(
                    "Crase: teste trocando por palavra masculina — virou 'ao', tem crase. Antes de "
                    "verbo, de pronome pessoal e de palavra masculina, não tem.",
                    "Concordância: 'haver' no sentido de existir é impessoal e não vai ao plural; "
                    "'fazer' indicando tempo também. 'É proibido' só flexiona com determinante: "
                    "'é proibida A entrada'.",
                    "Regência: assistir (ver) pede 'a'; obedecer pede 'a'; chegar pede 'a', não "
                    "'em'; preferir não aceita 'mais do que'. Colocação: palavra negativa, advérbio "
                    "e pronome relativo atraem o pronome para antes do verbo (próclise).",
                ),
                chave="Gramática de concurso é lista curta de gatilhos, não a gramática inteira.",
            ),
        ),
    ),
    Modulo(
        id="matematica-avancada",
        titulo="Matemática em 90 segundos por questão",
        chamada="Quinze questões, três horas de prova. Tempo é a variável que decide.",
        descricao="Atalhos de cálculo, estimativa e eliminação para resolver rápido e sem erro.",
        recurso="avancado",
        capa="capa-fase2",
        etiqueta="Aprofundamento",
        ordem=5,
        materias=("matematica",),
        aulas=(
            Aula(
                id="mat-av-atalhos",
                titulo="Atalhos que economizam minutos",
                resumo="Porcentagem, proporção e média resolvidas de cabeça.",
                paragrafos=(
                    "<strong>Porcentagem:</strong> 10% é dividir por 10; 5% é metade disso; 20% é o "
                    "dobro. Combinando esses três, você monta quase qualquer percentual mentalmente "
                    "— 35% é 20% + 10% + 5%.",
                    "<strong>Aumento e desconto:</strong> use fator multiplicador. Aumento de 15% é "
                    "× 1,15; desconto de 15% é × 0,85. Sucessivos se multiplicam: 1,10 × 0,90 = "
                    "0,99, ou seja, queda de 1%.",
                    "<strong>Estimativa antes da conta:</strong> descarte alternativas absurdas por "
                    "ordem de grandeza. Eliminar duas opções em dez segundos vale mais que a conta "
                    "perfeita em quatro minutos.",
                ),
                chave="Fator multiplicador transforma três contas em uma.",
            ),
            Aula(
                id="mat-av-logica",
                titulo="Lógica: as três negações",
                resumo="Quem sabe negar corretamente acerta praticamente todas.",
                paragrafos=(
                    "Negação de 'todo A é B' → 'existe pelo menos um A que não é B'. Nunca 'nenhum "
                    "A é B'.",
                    "Negação de 'se p então q' → 'p e não q'. Nunca a contrapositiva, nunca a "
                    "recíproca.",
                    "Leis de De Morgan: negação de 'p e q' → 'não p ou não q'; negação de 'p ou q' "
                    "→ 'não p e não q'. A banca sempre oferece o 'contrário extremo' como distrator, "
                    "porque ele soa natural.",
                ),
                chave="Negar não é contrariar — é afirmar que aquilo não acontece.",
            ),
        ),
    ),
    Modulo(
        id="reta-final",
        titulo="Reta final — os 7 dias antes da prova",
        chamada="O que fazer (e o que não fazer) na semana que decide o ano.",
        descricao="Revisão enxuta, logística, controle de ansiedade e checklist da véspera.",
        recurso="avancado",
        capa="bota",
        etiqueta="Reta final",
        ordem=6,
        aulas=(
            Aula(
                id="reta-revisao",
                titulo="Revisão que cabe em uma folha",
                resumo="Nada de conteúdo novo: só o que você ainda erra.",
                paragrafos=(
                    "Regra inegociável da última semana: <strong>nada de conteúdo novo</strong>. "
                    "Aprender tema novo agora rende pouco e atrapalha o que já estava consolidado.",
                    "Abra seu Caderno de Erros e escolha as dez regras que mais te derrubaram. "
                    "Escreva cada uma em uma linha, com suas palavras. Essa folha é o único material "
                    "que você revisa na véspera e na manhã da prova.",
                    "Continue resolvendo questões — em volume menor, mas todo dia. Parar de resolver "
                    "na última semana esfria o reflexo de leitura do enunciado.",
                ),
                chave="Na reta final, sintetizar vale mais que acrescentar.",
            ),
            Aula(
                id="reta-vespera",
                titulo="Véspera e dia da prova",
                resumo="Sair de casa sem nenhuma decisão pendente.",
                paragrafos=(
                    "<strong>Véspera:</strong> documento oficial com foto, comprovante de inscrição, "
                    "canetas esferográficas pretas de corpo transparente, água e lanche simples. "
                    "Confira endereço e tempo de deslocamento com folga real. Roupa separada, "
                    "despertador duplo, dormir cedo.",
                    "<strong>No dia:</strong> chegue cedo, evite rodas de conversa sobre conteúdo na "
                    "porta — elas só espalham insegurança. Na sala, respire quatro vezes antes de "
                    "começar.",
                    "<strong>Execução:</strong> três passadas. Primeira, o que você sabe de "
                    "imediato; segunda, o que exige conta ou releitura; terceira, eliminação nas "
                    "restantes. Transcreva o gabarito a cada dez questões — nunca só no fim.",
                    "Se travar: marque, pule, siga. Se acelerar: quatro respirações lentas, ombros "
                    "para baixo, volte. Se der branco: releia a última questão que você acertou com "
                    "facilidade e retome dali.",
                ),
                chave="Prova se ganha na véspera, quando não sobra decisão para o dia seguinte.",
            ),
        ),
    ),
)

POR_ID = {m.id: m for m in MODULOS}
TOTAL_AULAS = sum(len(m.aulas) for m in MODULOS)


def modulo(mid: str) -> Modulo | None:
    return POR_ID.get(mid)


def aula(mid: str, aid: str) -> Aula | None:
    m = POR_ID.get(mid)
    if m is None:
        return None
    return next((a for a in m.aulas if a.id == aid), None)


def ordenados() -> list[Modulo]:
    return sorted(MODULOS, key=lambda m: m.ordem)
