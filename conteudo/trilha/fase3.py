"""Fase 3 — Simulados e Ajuste Fino (dias 19 a 26)."""

from __future__ import annotations

from . import Dia, Missao

DIAS: list[Dia] = [
    Dia(
        numero=19,
        fase="fase3",
        titulo="Como se faz uma prova (e o primeiro simulado)",
        promessa="Aprender a estratégia de execução antes de executar.",
        tempo_min=75,
        aula=(
            "Saber conteúdo e fazer prova são habilidades diferentes. Existe candidato que sabe "
            "mais e passa menos, porque administra mal o relógio e a cabeça.",
            "A estratégia das três passadas resolve a maior parte disso. <strong>Primeira passada:</strong> "
            "responda apenas o que você sabe de imediato, sem hesitar; marque com um traço o que "
            "exigir conta ou releitura e siga. <strong>Segunda passada:</strong> volte às marcadas "
            "e resolva com calma — agora você já tem noção do tempo disponível. <strong>Terceira "
            "passada:</strong> feche as restantes com eliminação de alternativas, sem deixar nada "
            "em branco quando não há penalidade por erro.",
            "Duas regras de ouro: nenhuma questão vale mais que outra, então nunca gaste cinco "
            "minutos numa só; e transcreva para o gabarito em blocos (a cada 10 questões), nunca "
            "só no final — é assim que se evita a tragédia de acabar o tempo com a folha em branco.",
            "Hoje você faz o Simulado 1: 30 questões, 60 minutos, cronômetro rodando. Não pause. "
            "Se o telefone tocar, o simulado continua — porque na prova real também continuaria.",
        ),
        chave="Prova é execução sob relógio. Isso se treina, não se improvisa.",
        tarefas=(
            "Separar 60 minutos ininterruptos",
            "Aplicar a estratégia das três passadas",
            "Não consultar nada durante o simulado",
        ),
        missao=Missao(
            tipo="simulado",
            titulo="Simulado 1 — 30 questões em 60 minutos",
            simulado_id="sim-1",
            descricao="Cronometrado, misto, no formato da prova.",
        ),
        frase="A prova não premia quem sabe mais. Premia quem entrega mais em 3 horas.",
        pontos_base=150,
    ),
    Dia(
        numero=20,
        fase="fase3",
        titulo="Autópsia do Simulado 1",
        promessa="Extrair do simulado tudo o que ele tem a dizer sobre você.",
        tempo_min=50,
        aula=(
            "Fazer simulado sem autópsia é desperdício caro. O relatório da plataforma já te "
            "entregou três informações: acerto por matéria, tempo médio por questão e distribuição "
            "dos erros por categoria.",
            "Leia nessa ordem. Primeiro, <strong>matéria</strong>: qual delas sozinha derrubou mais "
            "pontos? Segundo, <strong>tempo</strong>: em quais questões você gastou acima da média "
            "e ainda assim errou? (esse é o pior tipo de questão — cara e improdutiva; na próxima "
            "prova ela vai para a segunda passada). Terceiro, <strong>categoria de erro</strong>: se "
            "desatenção passou de um terço dos erros, seu problema hoje é ritmo, não conteúdo.",
            "Anote no diário de bordo as duas matérias que mais tiraram pontos. Elas serão o alvo "
            "dos dias 21 e 22.",
        ),
        chave="Simulado sem autópsia é só um dia cansado.",
        tarefas=(
            "Ler o relatório completo do Simulado 1",
            "Classificar no caderno todos os erros do simulado",
            "Registrar as duas matérias-alvo no diário",
        ),
        missao=Missao(
            tipo="revisao",
            titulo="Autópsia: revisar os erros do simulado",
            quantidade=12,
        ),
        frase="Errar num simulado é barato. Errar na prova custa um ano.",
        diario="Quais foram as duas matérias que mais te tiraram pontos? E a categoria de erro dominante?",
    ),
    Dia(
        numero=21,
        fase="fase3",
        titulo="Ajuste fino I: atacar a matéria que mais custa",
        promessa="Converter o ponto fraco número 1 em pontos na folha.",
        tempo_min=55,
        aula=(
            "Hoje é bloco cirúrgico. A plataforma seleciona questões concentradas na sua pior "
            "matéria do simulado — não em todas, não nas que você gosta.",
            "Trabalhe com uma regra simples: para cada questão errada, escreva uma frase curta que "
            "explique a regra que você não sabia. Uma frase. Se você não consegue explicar em uma "
            "frase, o tema ainda não está entendido, e aí sim vale ler a teoria específica daquele "
            "ponto — cinco minutos, não uma apostila.",
            "É normal a nota cair um pouco em blocos concentrados no ponto fraco. Não é retrocesso: "
            "é o custo de estar treinando exatamente o que você evitava.",
        ),
        chave="Quem treina só o que acerta chega na prova com a mesma nota de sempre.",
        tarefas=("Fazer o bloco na matéria-alvo", "Escrever uma frase-regra para cada erro"),
        missao=Missao(
            tipo="questoes",
            titulo="18 questões na sua matéria mais fraca",
            quantidade=18,
            usar_prioridades=True,
        ),
        frase="Ponto fraco não some por vergonha. Some por repetição.",
    ),
    Dia(
        numero=22,
        fase="fase3",
        titulo="Ajuste fino II: eliminação e chute inteligente",
        promessa="Transformar dúvida em probabilidade a seu favor.",
        tempo_min=50,
        aula=(
            "Em prova objetiva sem penalidade por erro, deixar em branco é jogar ponto fora. Mas "
            "chutar às cegas rende 20%. Chutar bem rende o dobro.",
            "Técnicas que funcionam: elimine alternativas com <strong>termos absolutos</strong> "
            "(sempre, nunca, exclusivamente, em qualquer hipótese) quando o tema admite exceção; "
            "desconfie da alternativa que <strong>acrescenta requisito</strong> que a lei não pede "
            "(prazos inventados são o exemplo clássico); elimine as duas que dizem a mesma coisa "
            "com palavras diferentes — se ambas fossem certas, a questão seria anulada.",
            "E o mais importante: quando sobrarem duas, não fique. Escolha e siga. O tempo gasto "
            "empatado entre duas alternativas é o tempo que faltaria para duas questões fáceis "
            "no fim da prova.",
        ),
        chave="Entre duas alternativas, decida em 15 segundos. O relógio cobra caro pela indecisão.",
        tarefas=(
            "Fazer o bloco aplicando eliminação consciente",
            "Anotar quantas questões você acertou por eliminação",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="18 questões — treino de eliminação",
            quantidade=18,
        ),
        frase="Não existe questão difícil. Existe questão que custa mais tempo do que vale.",
    ),
    Dia(
        numero=23,
        fase="fase3",
        titulo="Simulado 2: mais longo, mais parecido com a prova",
        promessa="Testar a estratégia sob um pouco mais de pressão.",
        tempo_min=90,
        aula=(
            "Segundo simulado: 40 questões em 80 minutos. Agora com estratégia definida e ponto de "
            "fadiga conhecido.",
            "Três instruções operacionais: cronometre de verdade e não pause; use o mesmo tipo de "
            "caneta e papel que usará na prova, se puder; e faça no horário mais próximo possível "
            "do horário real da sua prova — o corpo tem ritmo, e treinar de madrugada para uma "
            "prova das 9h é treinar outro corpo.",
            "Ao terminar, não corrija de imediato. Levante, beba água, respire cinco minutos. "
            "Corrigir no cansaço distorce a leitura do resultado.",
        ),
        chave="Simulado é ensaio geral, não avaliação de valor pessoal.",
        tarefas=("Fazer o Simulado 2 sem pausar", "Corrigir só depois de uma pausa de 5 minutos"),
        missao=Missao(
            tipo="simulado",
            titulo="Simulado 2 — 40 questões em 80 minutos",
            simulado_id="sim-2",
        ),
        frase="Você já é um candidato diferente daquele do dia 1. O número vai mostrar.",
        pontos_base=170,
    ),
    Dia(
        numero=24,
        fase="fase3",
        titulo="Autópsia do Simulado 2 e comparação de curva",
        promessa="Ver a evolução em número e corrigir o que ainda sangra.",
        tempo_min=50,
        aula=(
            "Compare os dois simulados lado a lado no painel: acerto geral, acerto por matéria e "
            "distribuição das categorias de erro.",
            "Três leituras possíveis. Se o acerto subiu e a desatenção caiu, sua execução melhorou — "
            "mantenha. Se o acerto subiu mas a desatenção também, você está indo rápido demais: no "
            "próximo simulado, ganhe 20 segundos por questão nas fáceis. Se o acerto não subiu, "
            "olhe se a dificuldade concentrou-se nas mesmas matérias — se sim, o plano dos dias "
            "seguintes é claro; se não, o problema é constância, não conteúdo.",
            "Nada aqui é motivo para desanimar. Você ainda tem seis dias, e é justamente nesses "
            "seis dias que a maioria dos candidatos ganha ou perde os pontos que separam a lista "
            "de aprovados da lista de espera.",
        ),
        chave="Curva importa mais que ponto isolado.",
        tarefas=(
            "Comparar Simulado 1 e 2 no painel",
            "Revisar os erros do Simulado 2",
            "Definir a meta do Simulado 3",
        ),
        missao=Missao(
            tipo="revisao",
            titulo="Autópsia e revisão dirigida",
            quantidade=15,
        ),
        frase="Dado bom é o que muda a próxima decisão.",
        diario="Sua curva subiu? Qual meta você define para o Simulado 3 do dia 26?",
    ),
    Dia(
        numero=25,
        fase="fase3",
        titulo="Faxina no caderno de erros",
        promessa="Reduzir a lista de coisas que ainda te derrubam.",
        tempo_min=55,
        aula=(
            "Hoje o objetivo é numérico: diminuir a quantidade de questões abertas no seu Caderno "
            "de Erros. Cada questão que sai do caderno como <strong>dominada</strong> é um erro a "
            "menos que você pode cometer na prova.",
            "Faça a revisão em duas rodadas. Primeiro, as questões marcadas como falta de conteúdo "
            "— elas exigem um minuto de teoria antes de refazer. Depois, pegadinha e desatenção, "
            "que se resolvem com leitura mais lenta do comando.",
            "Se uma questão te derrubar pela terceira vez, ela é uma <strong>questão-âncora</strong>: "
            "escreva a regra dela em uma folha à parte e cole em algum lugar que você olha todo dia. "
            "Cinco âncoras bem escolhidas valem mais que cinquenta páginas de resumo.",
        ),
        chave="Sua nota na prova é o inverso do tamanho do seu caderno de erros.",
        tarefas=(
            "Revisar o máximo de questões vencidas",
            "Escrever até 5 questões-âncora",
        ),
        missao=Missao(
            tipo="revisao",
            titulo="Faxina: revisão espaçada ampliada",
            quantidade=20,
        ),
        frase="Reduzir erro é mais rápido que aumentar conhecimento.",
    ),
    Dia(
        numero=26,
        fase="fase3",
        titulo="Simulado 3: o ensaio geral",
        promessa="Fazer a prova antes da prova.",
        tempo_min=110,
        aula=(
            "Último simulado, o mais longo: 50 questões em 100 minutos. Este é o número que você "
            "vai levar para a prova como referência — e a última oportunidade de ajustar execução.",
            "Reproduza as condições reais tanto quanto der: acorde no horário, tome o mesmo café, "
            "vista roupa parecida, sente-se com a mesa limpa, celular longe e silencioso. Quanto "
            "mais parecido o ensaio, menos novidade no dia.",
            "E preste atenção ao trecho final: as últimas dez questões são onde a resistência "
            "mental decide. Se o rendimento cair ali, na prova real você vai precisar de uma pausa "
            "técnica de 60 segundos por volta da questão 40 — respirar fundo, alongar os ombros, "
            "voltar. Custa um minuto e devolve três questões.",
        ),
        chave="No ensaio geral, treine também o cansaço.",
        tarefas=(
            "Reproduzir as condições da prova real",
            "Fazer as 50 questões sem pausa longa",
            "Registrar como se sentiu nas últimas 10 questões",
        ),
        missao=Missao(
            tipo="simulado",
            titulo="Simulado 3 — 50 questões em 100 minutos",
            simulado_id="sim-3",
        ),
        frase="Fase 3 concluída. Agora é blindagem.",
        pontos_base=200,
        diario="Como foi seu rendimento nas últimas 10 questões? O que fará diferente na prova?",
    ),
]
