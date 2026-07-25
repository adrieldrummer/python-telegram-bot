"""Fase 1 — Diagnóstico e Prioridade (dias 1 a 6)."""

from __future__ import annotations

from . import Dia, Missao

DIAS: list[Dia] = [
    Dia(
        numero=1,
        fase="fase1",
        titulo="O diagnóstico honesto",
        promessa="Em 40 minutos você vai saber, com número, onde está perdendo pontos.",
        tempo_min=45,
        aula=(
            "Antes de estudar qualquer coisa, você precisa parar de estudar no escuro. A maioria "
            "dos candidatos começa pelo que gosta, não pelo que precisa — e descobre tarde demais "
            "que passou dois meses reforçando o que já sabia.",
            "O autor deste método reprovou três vezes antes de entender isso. Ele lia apostila "
            "inteira, fazia resumo bonito, assistia horas de videoaula, e no dia da prova travava. "
            "Não era falta de esforço: era esforço sem direção. Ele estava remando forte para o "
            "lado errado.",
            "O diagnóstico de hoje inverte a lógica: você vai responder um bloco de questões de "
            "todas as matérias ANTES de revisar qualquer teoria. Vai errar — e é exatamente isso "
            "que queremos. Cada erro aqui é informação. Ao final, a plataforma monta o seu Mapa de "
            "Prioridades: a ordem em que as matérias devem consumir o seu tempo nos próximos 29 dias.",
            "Regra de ouro do dia: <strong>não pesquise, não consulte, não chute com calma.</strong> "
            "Responda como responderia na prova. Um diagnóstico maquiado gera um plano inútil.",
        ),
        chave="Um diagnóstico ruim não é o que mostra muitos erros. É o que mostra erros mentirosos.",
        tarefas=(
            "Reservar 40 minutos sem interrupção",
            "Responder as 24 questões do diagnóstico sem consultar nada",
            "Ler o seu Mapa de Prioridades ao final",
        ),
        missao=Missao(
            tipo="diagnostico",
            titulo="Diagnóstico inicial — 24 questões",
            quantidade=24,
            descricao=(
                "Três questões de cada uma das oito matérias. Sem consulta, sem pausa longa. "
                "O resultado define a sua trilha."
            ),
        ),
        frase="Você não está começando do zero. Está começando do real.",
        pontos_base=120,
        diario="Antes de ver o resultado: em quais duas matérias você acha que foi pior?",
    ),
    Dia(
        numero=2,
        fase="fase1",
        titulo="Lendo o seu mapa: prioridade não é preferência",
        promessa="Escolher onde o seu tempo vai doer menos e render mais.",
        tempo_min=40,
        aula=(
            "Você já tem números. Agora vem a parte que quase ninguém faz direito: interpretar.",
            "Prioridade real é o cruzamento de duas coisas — <strong>o quanto a matéria cai</strong> "
            "e <strong>o quanto você erra nela</strong>. Uma matéria em que você acerta 90% e que "
            "cai muito não é prioridade: é patrimônio, você só mantém. Uma matéria em que você "
            "acerta 30% e que quase não cai também não é prioridade: é armadilha de perfeccionista.",
            "O ponto que decide aprovação é a interseção: peso alto e acerto baixo. É lá que cada "
            "hora investida devolve mais pontos na folha de respostas. A plataforma já calculou "
            "isso para você e ordenou as matérias — as três primeiras são as suas prioritárias e "
            "vão dominar as próximas duas semanas.",
            "Hoje o bloco é curto de propósito. Depois do diagnóstico, o cérebro precisa de uma "
            "sessão de confirmação: questões só nas suas três prioritárias, para você sentir na "
            "prática o tamanho do buraco.",
        ),
        chave="Estude o que dói e cai. O resto é conforto disfarçado de estudo.",
        tarefas=(
            "Abrir o Mapa de Prioridades e ler as três primeiras matérias",
            "Fazer o bloco de 12 questões nas prioritárias",
            "Classificar cada erro no Caderno de Erros",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="12 questões nas suas 3 matérias prioritárias",
            quantidade=12,
            usar_prioridades=True,
            descricao="A plataforma seleciona automaticamente pelas suas piores matérias do diagnóstico.",
        ),
        frase="Não existe matéria chata. Existe matéria que você evita porque ela te expõe.",
        diario="Qual das suas três prioridades você mais evitava até hoje? Por quê?",
    ),
    Dia(
        numero=3,
        fase="fase1",
        titulo="A rotina possível: três blocos, não seis horas",
        promessa="Montar uma grade que sobrevive a trabalho, casa e filhos.",
        tempo_min=40,
        aula=(
            "O autor do método tinha trabalho, casa, contas e filhos pequenos. A rotina que o "
            "aprovou não tinha seis horas de estudo — tinha três encaixes:",
            "🌅 <strong>Manhã (30–40 min)</strong>: antes do trabalho, um bloco de exatas, quando "
            "a cabeça está mais fria. ☕ <strong>Intervalo (20 min)</strong>: revisão rápida dos "
            "erros do dia anterior. 🌙 <strong>Noite (50–60 min)</strong>: depois das crianças "
            "dormirem, um bloco de Direito ou Português com correção comentada de cada erro.",
            "O que faz esse modelo funcionar não é a soma das horas — é a distribuição. Três "
            "contatos curtos com o conteúdo em um dia fixam mais do que uma maratona de domingo, "
            "porque cada retomada obriga o cérebro a recuperar a informação, e é a recuperação "
            "que consolida a memória.",
            "Hoje você define os seus três horários. Não os ideais: os possíveis. Um bloco que "
            "existe às 5h40 da manhã vale mais do que dois blocos imaginários às 14h.",
        ),
        chave="Dois blocos de 40 minutos por dia batem uma maratona de 6 horas no domingo. Sempre.",
        tarefas=(
            "Escrever no diário os três horários reais dos seus blocos",
            "Definir o que fazer no bloco quando o dia der errado (plano mínimo de 15 minutos)",
            "Fazer o bloco de 12 questões nas prioritárias",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="12 questões + definição da sua grade",
            quantidade=12,
            usar_prioridades=True,
        ),
        frase="Consistência é o que sobra quando a motivação acaba — e ela acaba sempre.",
        diario="Escreva seus três horários de estudo e o seu 'plano mínimo' para dias caóticos.",
    ),
    Dia(
        numero=4,
        fase="fase1",
        titulo="Correção ativa: transformar erro em aula",
        promessa="Aprender a técnica que mais acelerou a evolução do autor.",
        tempo_min=45,
        aula=(
            "Aqui está o segredo mais barato e mais ignorado do método: toda questão errada recebe "
            "uma etiqueta. Sempre uma destas três:",
            "📚 <strong>Falta de conteúdo</strong> — você não sabia a regra. A ação é revisar aquele "
            "tema específico, e só ele. 🎯 <strong>Pegadinha de interpretação</strong> — você sabia, "
            "mas caiu no jeito como a banca escreveu. A ação é reler grifando o comando. "
            "⏱ <strong>Desatenção</strong> — você sabia e errou por pressa. A ação não é estudar "
            "mais: é desacelerar na hora de marcar.",
            "Por que isso funciona? Porque cada categoria pede um remédio diferente. Quem trata "
            "desatenção estudando mais teoria fica cansado e continua errando. Quem trata falta de "
            "conteúdo com 'mais atenção' continua sem saber a regra.",
            "A partir de hoje, cada erro seu entra no Caderno de Erros com a etiqueta e uma "
            "anotação de uma linha. A plataforma vai devolver essas questões para você em 1, 3, 7 "
            "e 15 dias — revisão espaçada automática. Você não precisa lembrar de revisar: o "
            "sistema lembra por você.",
        ),
        chave="Errar duas vezes pelo mesmo motivo é falha de método, não de memória.",
        tarefas=(
            "Fazer o bloco de 12 questões",
            "Classificar TODOS os erros do bloco",
            "Escrever uma anotação de uma linha em pelo menos 3 erros",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="12 questões com correção ativa obrigatória",
            quantidade=12,
            usar_prioridades=True,
            descricao="Ao errar, classifique o motivo. É isso que alimenta a sua revisão espaçada.",
        ),
        frase="O erro é caro só quando você o joga fora.",
        diario="Qual foi a categoria de erro mais frequente hoje? O que isso diz sobre você?",
    ),
    Dia(
        numero=5,
        fase="fase1",
        titulo="O que realmente cai — e o que você pode ignorar",
        promessa="Cortar do plano o que não paga o tempo investido.",
        tempo_min=45,
        aula=(
            "Existe um vício comum: estudar assunto que 'parece importante'. Parecer importante e "
            "cair em prova são coisas diferentes. O autor perdeu três tentativas estudando temas "
            "que quase nunca eram cobrados, enquanto negligenciava os que se repetiam prova após "
            "prova.",
            "Na plataforma, cada matéria carrega um peso de 1 a 5, baseado na leitura estatística "
            "das provas anteriores. Português e Direito Constitucional puxam a fila; Informática e "
            "Atualidades valem menos, mas são pontos baratos — pouca teoria, alta repetição.",
            "A estratégia da reta curta é esta: <strong>peso alto + acerto baixo</strong> recebe "
            "bloco diário. <strong>Peso alto + acerto alto</strong> recebe manutenção duas vezes "
            "por semana. <strong>Peso baixo + acerto baixo</strong> recebe um bloco semanal focado, "
            "porque são pontos que se compram rápido. <strong>Peso baixo + acerto alto</strong> "
            "você só encosta no fim.",
            "Importante e honesto: peso é orientação estatística, não edital. Sempre confira o "
            "edital vigente do seu concurso — se ele mudar a distribuição, a prioridade muda junto.",
        ),
        chave="Não existe tempo curto. Existe tempo mal distribuído.",
        tarefas=(
            "Conferir o quadro de pesos por matéria",
            "Fazer o bloco de 15 questões nas matérias de maior peso",
            "Classificar os erros",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="15 questões nas matérias de maior peso",
            quantidade=15,
            materias=("portugues", "constitucional", "matematica", "penal"),
        ),
        frase="Direção primeiro. Velocidade depois.",
    ),
    Dia(
        numero=6,
        fase="fase1",
        titulo="Fechamento da Fase 1: sua linha de base",
        promessa="Registrar o número de onde você está partindo.",
        tempo_min=50,
        aula=(
            "Hoje encerramos o diagnóstico com um bloco misto — o mesmo tipo de mistura que a "
            "prova real faz. O objetivo é registrar a sua linha de base: o percentual de acerto "
            "com que você entra na fase de imersão.",
            "Esse número não é para julgar você. É para comparar. Daqui a duas semanas, no primeiro "
            "simulado, ele volta. E no dia 26, no simulado final, volta de novo. Ver a curva subir "
            "com dado real é o que sustenta a disciplina quando a motivação some — e ela vai sumir "
            "por volta do dia 12, como some com todo mundo.",
            "Antes de virar a chave para a Fase 2, faça um acerto de contas com você mesmo: os "
            "blocos que você definiu no dia 3 aconteceram? Se não, o problema é o horário escolhido "
            "ou o tamanho do bloco. Ajuste agora — não na terceira semana.",
            "A partir de amanhã muda o jogo: menos leitura, mais questão. Você vai estudar através "
            "das questões, e a teoria vira consequência da correção, não o ponto de partida.",
        ),
        chave="O que não é medido vira opinião. E opinião não passa em concurso.",
        tarefas=(
            "Fazer o bloco misto de 15 questões",
            "Comparar com o resultado do diagnóstico",
            "Ajustar seus horários de estudo, se necessário",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="Bloco misto de 15 questões (linha de base)",
            quantidade=15,
        ),
        frase="Fase 1 concluída. Você saiu do escuro.",
        pontos_base=90,
        diario="Sua linha de base é qual percentual? Que meta você assume para o dia 30?",
    ),
]
