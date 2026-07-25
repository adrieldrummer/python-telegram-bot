"""Fase 4 — Blindagem e Reta Final (dias 27 a 30)."""

from __future__ import annotations

from . import Dia, Missao

DIAS: list[Dia] = [
    Dia(
        numero=27,
        fase="fase4",
        titulo="Autópsia final e as 10 âncoras",
        promessa="Reduzir todo o curso a uma folha que você revisa em 10 minutos.",
        tempo_min=50,
        aula=(
            "A partir de hoje vale uma regra inegociável: <strong>nada de conteúdo novo</strong>. "
            "Aprender tema novo na última semana rende pouco e custa muito — atrapalha o que já "
            "estava consolidado e alimenta a sensação de que falta tudo.",
            "O trabalho de hoje é de síntese. Olhe o seu caderno de erros e escolha as dez regras "
            "que mais te derrubaram no mês. Escreva cada uma em uma linha, com suas palavras. Essa "
            "é a sua folha de âncoras — o único material que você vai revisar nos dias 28, 29 e na "
            "manhã da prova.",
            "Se você tem dificuldade em escolher dez, use o critério da frequência: as regras que "
            "voltaram três vezes ou mais no caderno. Elas não voltaram por acaso.",
        ),
        chave="Na reta final, sintetizar vale mais que acrescentar.",
        tarefas=(
            "Revisar as questões vencidas do caderno",
            "Escrever a folha das 10 âncoras no diário",
        ),
        missao=Missao(
            tipo="revisao",
            titulo="Revisão final dirigida",
            quantidade=15,
        ),
        frase="Você não vai lembrar de tudo. Vai lembrar do que repetiu.",
        diario="Escreva aqui suas 10 âncoras — uma linha cada. Esta é a sua folha de revisão final.",
    ),
    Dia(
        numero=28,
        fase="fase4",
        titulo="Corpo: sono, comida e o teste físico",
        promessa="Chegar inteiro — porque a prova é do corpo também.",
        tempo_min=40,
        aula=(
            "Concurso de carreira policial não termina na prova objetiva: costuma haver etapas "
            "físicas, documentais e de saúde. Duas providências práticas para hoje, enquanto sobra "
            "cabeça: confira a lista de documentos exigidos pelo edital e comece (ou retome) o "
            "preparo físico de forma regular — corrida leve, abdominais, barra, conforme as provas "
            "previstas para o seu certame.",
            "Sobre o sono, um dado que candidato ignora e depois lamenta: privação de sono derruba "
            "atenção sustentada e memória de trabalho — exatamente as duas funções que uma prova "
            "de três horas exige. Dormir bem nas noites que antecedem a prova rende mais do que "
            "duas horas extras de revisão exausta.",
            "Nesta semana: horário de dormir fixo, tela longe da cama, álcool fora, cafeína só até "
            "o meio da tarde. E na véspera, nada de virar a noite 'garantindo' conteúdo. Quem vira "
            "a noite entra na sala com metade do cérebro disponível.",
        ),
        chave="Sono não é preguiça. É preparação técnica.",
        tarefas=(
            "Conferir a lista de documentos do edital",
            "Definir horário fixo de dormir até o dia da prova",
            "Fazer o bloco leve de manutenção",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="Bloco leve de manutenção — 12 questões",
            quantidade=12,
        ),
        frase="Corpo descansado responde melhor do que cabeça cheia.",
    ),
    Dia(
        numero=29,
        fase="fase4",
        titulo="Blindagem mental: a cabeça na hora H",
        promessa="Ter um plano para quando o nervosismo aparecer — porque ele vai aparecer.",
        tempo_min=40,
        aula=(
            "Ansiedade na prova não é sinal de despreparo: é o corpo se preparando para algo que "
            "importa. O problema não é sentir — é não ter plano para quando sentir.",
            "Monte o seu protocolo agora, com três gatilhos. <strong>Se travar numa questão:</strong> "
            "marque, pule, siga — você volta depois. <strong>Se o coração acelerar:</strong> quatro "
            "respirações lentas, contando quatro tempos para inspirar e seis para soltar; ombros "
            "para baixo; volte. <strong>Se der branco geral:</strong> feche os olhos por dez "
            "segundos, releia a última questão que você acertou com facilidade e retome dali — "
            "retomar do sucesso reancora a confiança.",
            "E lembre do que sustenta tudo: você tem dado. Não está entrando na sala achando que "
            "estudou; está entrando sabendo o seu percentual, sabendo onde está forte e onde vai "
            "precisar de mais cuidado. Foi exatamente isso que fez o autor deste método entrar "
            "calmo na quarta tentativa depois de três reprovações.",
            "Sobre sacrifício, uma última verdade: você abriu mão de coisas nestes 30 dias. Redes "
            "sociais, descanso, encontros. Não foi só sacrifício — foi sacrifício direcionado. E "
            "isso é o que separa quem tenta de quem passa.",
        ),
        chave="Não é ausência de medo. É ter o que fazer quando ele chega.",
        tarefas=(
            "Escrever seu protocolo de três gatilhos",
            "Reler a folha das 10 âncoras",
            "Fazer o bloco leve",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="Bloco leve de confiança — 12 questões",
            quantidade=12,
            descricao="Bloco calibrado para você terminar acertando. Confiança também se treina.",
        ),
        frase="Sonho grande sempre cobra um preço. Você já vem pagando.",
        diario="Escreva seu protocolo: o que fazer se travar, se acelerar, se der branco.",
    ),
    Dia(
        numero=30,
        fase="fase4",
        titulo="Véspera e dia da prova: o checklist final",
        promessa="Sair de casa sem nenhuma decisão pendente.",
        tempo_min=35,
        aula=(
            "Hoje o estudo é mínimo por decisão de método. Trinta minutos de leitura das âncoras, "
            "um bloco curto de questões só para o cérebro entrar no ritmo — e ponto.",
            "<strong>Na véspera:</strong> separe documento oficial com foto, comprovante de "
            "inscrição, canetas esferográficas pretas de corpo transparente, água e um lanche "
            "simples. Confira o endereço do local e o tempo de deslocamento com folga real (trânsito "
            "de dia de prova é sempre pior). Roupa separada. Despertador duplo. Durma cedo.",
            "<strong>No dia:</strong> chegue com antecedência, evite rodas de conversa sobre "
            "conteúdo na porta — elas só espalham insegurança. Na sala, antes de começar, respire "
            "quatro vezes e lembre da estratégia das três passadas. Transcreva o gabarito em blocos "
            "de dez. Não saia antes do tempo para 'não pensar demais': revise as marcadas.",
            "E quando entregar a folha, entregue sabendo que você fez o percurso inteiro. Trinta "
            "dias atrás você não tinha mapa — tinha vontade. Hoje você tem os dois.",
        ),
        chave="Prova se ganha na véspera, quando não sobra nenhuma decisão para o dia seguinte.",
        tarefas=(
            "Montar o kit da prova (documentos, canetas, água, lanche)",
            "Conferir local e horário com folga",
            "Ler as âncoras e dormir cedo",
        ),
        missao=Missao(
            tipo="questoes",
            titulo="Bloco final — 10 questões de ritmo",
            quantidade=10,
        ),
        frase="Mapa concluído. Agora é você e a farda. Vá buscar.",
        pontos_base=250,
        diario="Escreva uma mensagem para você mesmo ler na manhã da prova.",
    ),
]
