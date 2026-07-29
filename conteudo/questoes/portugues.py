"""Língua Portuguesa — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="port-001",
        materia="portugues",
        tema="Crase",
        nivel="facil",
        enunciado=(
            "Assinale a alternativa em que o sinal indicativo de crase foi empregado "
            "corretamente."
        ),
        alternativas=(
            ("A", "O policial dirigiu-se à pé até o local da ocorrência."),
            ("B", "A equipe permaneceu atenta à movimentação na esquina."),
            ("C", "Entregou o documento à ele ainda pela manhã."),
            ("D", "A viatura chegou à uma quadra do endereço informado."),
            ("E", "Começaremos o patrulhamento à partir das dez horas."),
        ),
        correta="B",
        comentario=(
            "Crase é a fusão da preposição 'a' com o artigo 'a(s)'. Em (B), 'atenta' exige "
            "preposição 'a' e 'movimentação' é palavra feminina que admite artigo: a + a = à. "
            "Antes de palavra masculina ('pé', 'partir'), de pronome pessoal ('ele') e antes de "
            "'uma' não há artigo feminino, logo não há crase."
        ),
        armadilha="A banca aposta que você marque 'à pé' por ouvir muito essa forma errada na fala.",
    ),
    Questao(
        id="port-002",
        materia="portugues",
        tema="Ortografia: mal x mau",
        nivel="facil",
        enunciado="Assinale a alternativa correta quanto ao emprego de 'mal' e 'mau'.",
        alternativas=(
            ("A", "O suspeito agiu de mau modo e respondeu mal ao questionamento."),
            ("B", "Ele é um mal exemplo para a turma."),
            ("C", "Foi um mau começo, mas o dia terminou mal."),
            ("D", "Mau chegou à unidade, iniciou o serviço."),
            ("E", "O relatório foi mau redigido."),
        ),
        correta="C",
        comentario=(
            "'Mau' é adjetivo e se opõe a 'bom' ('mau começo' / 'bom começo'). 'Mal' é advérbio "
            "(ou substantivo) e se opõe a 'bem' ('terminou mal' / 'terminou bem'). Em (C) as duas "
            "formas estão nas funções certas."
        ),
        armadilha="Troca de classe gramatical: se dá para trocar por 'bom', é 'mau'; por 'bem', é 'mal'.",
    ),
    Questao(
        id="port-003",
        materia="portugues",
        tema="Concordância verbal: verbo haver",
        nivel="medio",
        enunciado="Assinale a alternativa em que a concordância verbal está correta.",
        alternativas=(
            ("A", "Houveram muitas ocorrências no fim de semana."),
            ("B", "Haviam três viaturas no pátio."),
            ("C", "Existiu, no bairro, diversos casos semelhantes."),
            ("D", "Houve muitas ocorrências no fim de semana."),
            ("E", "Devem haver soluções melhores para o problema."),
        ),
        correta="D",
        comentario=(
            "O verbo 'haver' no sentido de 'existir' é impessoal: fica sempre na 3ª pessoa do "
            "singular ('Houve muitas ocorrências'). Já 'existir' é pessoal e concorda com o sujeito "
            "('Existiram diversos casos'). Em locução, a impessoalidade passa ao auxiliar: 'Deve "
            "haver soluções'."
        ),
        armadilha="'Houveram' soa natural e é justamente o erro mais cobrado na prova.",
    ),
    Questao(
        id="port-004",
        materia="portugues",
        tema="Emprego de por que / porque / por quê / porquê",
        nivel="medio",
        enunciado="Assinale a alternativa que completa corretamente as lacunas:\n"
        "«___ você desistiu do concurso? Desisti ___ perdi a confiança, e ninguém entendeu o ___.»",
        alternativas=(
            ("A", "Porquê — porque — por que"),
            ("B", "Porque — por que — por quê"),
            ("C", "Por quê — porque — por que"),
            ("D", "Por que — por quê — porquê"),
            ("E", "Por que — porque — porquê"),
        ),
        correta="E",
        comentario=(
            "Pergunta direta no início: 'Por que' (separado, sem acento). Resposta/causa: 'porque' "
            "(junto). Precedido de artigo, vira substantivo: 'o porquê' (junto e acentuado). "
            "'Por quê' acentuado só aparece no fim da frase ou antes de pausa forte."
        ),
        armadilha="A quarta forma existe só para confundir: sem artigo antes, nunca é 'porquê'.",
    ),
    Questao(
        id="port-005",
        materia="portugues",
        tema="Concordância nominal",
        nivel="medio",
        enunciado="Assinale a alternativa correta quanto à concordância nominal.",
        alternativas=(
            ("A", "É proibida a entrada de pessoas não autorizadas."),
            ("B", "É proibido a entrada de pessoas não autorizadas."),
            ("C", "É proibidas a entrada de pessoas não autorizadas."),
            ("D", "São proibido a entrada de pessoas não autorizadas."),
            ("E", "É proibido as entradas de pessoas não autorizadas."),
        ),
        correta="A",
        comentario=(
            "Nas expressões 'é proibido', 'é necessário', 'é bom', a concordância varia: sem "
            "determinante, o adjetivo fica no masculino singular ('É proibido entrada'); com "
            "determinante ('a' entrada), há concordância plena: 'É proibida a entrada'."
        ),
        armadilha="A alternativa (B) só estaria certa se o artigo 'a' fosse retirado.",
    ),
    Questao(
        id="port-006",
        materia="portugues",
        tema="Regência verbal",
        nivel="medio",
        enunciado="Assinale a alternativa em que a regência verbal está de acordo com a norma-padrão.",
        alternativas=(
            ("A", "Assistimos o jogo pela televisão."),
            ("B", "Assistimos ao jogo pela televisão."),
            ("C", "Prefiro mais estudar questões do que ler apostila."),
            ("D", "Cheguei na unidade às sete horas."),
            ("E", "Obedeça o regulamento em qualquer situação."),
        ),
        correta="B",
        comentario=(
            "No sentido de 'ver, presenciar', 'assistir' é transitivo indireto e pede a preposição "
            "'a': assistir AO jogo. 'Preferir' rejeita 'mais... do que' (prefiro X a Y); 'chegar' "
            "pede 'a' ('cheguei à unidade'); 'obedecer' é transitivo indireto ('obedeça AO "
            "regulamento')."
        ),
        armadilha="Todas as alternativas erradas repetem construções comuns na fala do dia a dia.",
    ),
    Questao(
        id="port-007",
        materia="portugues",
        tema="Interpretação de texto",
        nivel="medio",
        enunciado=(
            "Leia: «Não faltou esforço nas três primeiras tentativas; faltou direção. O candidato "
            "estudava muitas horas, mas distribuía o tempo entre assuntos que raramente eram "
            "cobrados.»\n\nDe acordo com o texto, o problema do candidato era:"
        ),
        alternativas=(
            ("A", "a falta de dedicação ao estudo diário."),
            ("B", "a impossibilidade de estudar por muitas horas."),
            ("C", "a escolha inadequada do conteúdo estudado."),
            ("D", "a ausência de material didático de qualidade."),
            ("E", "o excesso de questões resolvidas sem teoria."),
        ),
        correta="C",
        comentario=(
            "O texto afirma explicitamente que esforço havia ('não faltou esforço') e localiza a "
            "falha na direção — isto é, no que era estudado. Interpretação cobra o que está "
            "escrito, não o que é plausível."
        ),
        armadilha="(A) e (B) contradizem o texto; (D) e (E) trazem informação que o texto não dá.",
    ),
    Questao(
        id="port-008",
        materia="portugues",
        tema="Pontuação",
        nivel="dificil",
        enunciado="Assinale a alternativa corretamente pontuada.",
        alternativas=(
            ("A", "O sargento responsável pelo setor, comunicou a decisão à equipe."),
            ("B", "O sargento, responsável pelo setor comunicou a decisão à equipe."),
            ("C", "O sargento responsável, pelo setor comunicou a decisão, à equipe."),
            ("D", "O sargento, responsável pelo setor, comunicou a decisão à equipe."),
            ("E", "O sargento responsável pelo setor comunicou, a decisão à equipe."),
        ),
        correta="D",
        comentario=(
            "Em (D) 'responsável pelo setor' está entre vírgulas como explicação intercalada, uso "
            "correto. As demais separam sujeito do verbo (A), abrem sem fechar a intercalação (B) "
            "ou isolam o objeto direto do verbo (D e E) — proibido pela norma-padrão."
        ),
        armadilha="Vírgula 'onde a gente respira' é o erro clássico: entre sujeito e verbo, nunca.",
    ),
    Questao(
        id="port-009",
        materia="portugues",
        tema="Sujeito e oração sem sujeito",
        nivel="medio",
        enunciado="Assinale a alternativa em que a oração NÃO tem sujeito.",
        alternativas=(
            ("A", "Chegaram os reforços."),
            ("B", "Precisa-se de voluntários."),
            ("C", "Alguém deixou o portão aberto."),
            ("D", "Alugam-se salas comerciais."),
            ("E", "Choveu forte durante a madrugada."),
        ),
        correta="E",
        comentario=(
            "Verbos que indicam fenômeno da natureza são impessoais: a oração não tem sujeito. Em "
            "(B) o sujeito é indeterminado (partícula 'se' com verbo transitivo indireto) e em (D) "
            "há sujeito paciente ('salas comerciais' — voz passiva sintética)."
        ),
        armadilha="Sujeito indeterminado ≠ oração sem sujeito. A banca vive nessa fronteira.",
    ),
    Questao(
        id="port-010",
        materia="portugues",
        tema="Onde x aonde",
        nivel="facil",
        enunciado="Assinale a alternativa correta.",
        alternativas=(
            ("A", "Aonde você pretende chegar com esse ritmo de estudo?"),
            ("B", "Onde você vai depois do expediente?"),
            ("C", "Aonde ele trabalha, todos cumprem o horário."),
            ("D", "Aonde você mora atualmente?"),
            ("E", "Onde iremos amanhã?"),
        ),
        correta="A",
        comentario=(
            "'Aonde' é usado com verbos de movimento que pedem a preposição 'a' (chegar a, ir a): "
            "'aonde pretende chegar'. 'Onde' indica lugar fixo, sem movimento: 'onde você mora', "
            "'onde ele trabalha'. Por isso (D), (C), (B) e (E) invertem os dois usos."
        ),
        armadilha="Movimento pede 'aonde'; permanência pede 'onde'.",
    ),
    Questao(
        id="port-011",
        materia="portugues",
        tema="Há x a (tempo)",
        nivel="facil",
        enunciado="Assinale a alternativa correta quanto ao emprego de 'há' e 'a'.",
        alternativas=(
            ("A", "Daqui há dois meses farei a prova."),
            ("B", "Trabalho nesta função há dois anos."),
            ("C", "Há dois meses farei a prova."),
            ("D", "Estudo a três semanas sem parar."),
            ("E", "Ele saiu a pouco da unidade."),
        ),
        correta="B",
        comentario=(
            "'Há' indica tempo decorrido (passado): 'há dois anos'. 'A' indica tempo futuro ou "
            "distância: 'daqui a dois meses', 'a três quilômetros'. Em (E) o certo é 'há pouco', "
            "porque a saída já ocorreu."
        ),
        armadilha="Se o tempo já passou, use 'há'; se ainda vai chegar, use 'a'.",
    ),
    Questao(
        id="port-012",
        materia="portugues",
        tema="Coesão e conectivos",
        nivel="medio",
        enunciado=(
            "«Estudou todos os dias durante dois meses; ____, não obteve o resultado esperado.»\n"
            "O conectivo que preenche corretamente a lacuna, mantendo o sentido de oposição, é:"
        ),
        alternativas=(
            ("A", "portanto"),
            ("B", "porquanto"),
            ("C", "contudo"),
            ("D", "por conseguinte"),
            ("E", "assim"),
        ),
        correta="C",
        comentario=(
            "'Contudo' é conjunção adversativa (oposição), assim como 'mas', 'porém', 'todavia' e "
            "'entretanto'. 'Portanto', 'por conseguinte' e 'assim' são conclusivos; 'porquanto' é "
            "explicativo/causal."
        ),
        armadilha="Trocar oposição por conclusão inverte o sentido do período inteiro.",
    ),

    Questao(
        id="port-013",
        materia="portugues",
        tema="Sinônimos e antônimos",
        nivel="facil",
        enunciado=(
            "Assinale a alternativa em que a palavra destacada pode substituir «ágil», na frase "
            "«o policial foi ágil na abordagem», sem alterar o sentido."
        ),
        alternativas=(
            ("A", "lento"),
            ("B", "rígido"),
            ("C", "distraído"),
            ("D", "veloz"),
            ("E", "hesitante"),
        ),
        correta="D",
        comentario=(
            "Sinônimo é a palavra de sentido igual ou muito próximo: ágil e veloz. As demais são "
            "antônimas ou de campo semântico diferente."
        ),
        armadilha="Sinônimo precisa caber na frase; nem toda palavra 'parecida' serve no contexto.",
    ),
    Questao(
        id="port-014",
        materia="portugues",
        tema="Sentido próprio e figurado",
        nivel="facil",
        enunciado="Assinale a alternativa em que a expressão está empregada em sentido figurado.",
        alternativas=(
            ("A", "O muro da delegacia é de pedra."),
            ("B", "A estrada é de pedra britada."),
            ("C", "A pedra rolou pela ladeira."),
            ("D", "Comprou uma pedra de gelo."),
            ("E", "Ele tem um coração de pedra."),
        ),
        correta="E",
        comentario=(
            "Sentido figurado (conotativo) é o uso simbólico: 'coração de pedra' significa "
            "insensibilidade, não o material. Nas demais, 'pedra' está no sentido próprio "
            "(denotativo), literal."
        ),
        armadilha="A mesma palavra pode ser literal numa frase e metafórica em outra.",
    ),
    Questao(
        id="port-015",
        materia="portugues",
        tema="Classes de palavras",
        nivel="medio",
        enunciado=(
            "Na frase «o soldado atento respondeu rapidamente ao chamado», as palavras destacadas "
            "«atento» e «rapidamente» são, respectivamente:"
        ),
        alternativas=(
            ("A", "adjetivo e advérbio."),
            ("B", "advérbio e adjetivo."),
            ("C", "substantivo e adjetivo."),
            ("D", "adjetivo e preposição."),
            ("E", "pronome e conjunção."),
        ),
        correta="A",
        comentario=(
            "'Atento' qualifica o substantivo 'soldado' — adjetivo. 'Rapidamente' modifica o verbo "
            "'respondeu' — advérbio de modo. Quem qualifica nome é adjetivo; quem modifica verbo é "
            "advérbio."
        ),
        armadilha="Ler 'respectivamente' por cima e inverter a ordem da resposta.",
    ),
    Questao(
        id="port-016",
        materia="portugues",
        tema="Colocação pronominal",
        nivel="medio",
        enunciado="Assinale a alternativa que exemplifica corretamente a próclise.",
        alternativas=(
            ("A", "Diga-me a verdade."),
            ("B", "Não me diga isso."),
            ("C", "Dir-me-á a verdade amanhã."),
            ("D", "Falarei com ele depois."),
            ("E", "Entregou-lhe o documento."),
        ),
        correta="B",
        comentario=(
            "Próclise é o pronome antes do verbo, atraído por palavra negativa ('não me diga'). "
            "Ênclise é depois ('diga-me', 'entregou-lhe') e mesóclise é no meio do verbo no futuro "
            "('dir-me-á')."
        ),
        armadilha="Palavras atrativas — negação, advérbio, pronome relativo — puxam o pronome para antes.",
    ),

    Questao(
        id="port-017",
        materia="portugues",
        tema="Interpretação: ideia central",
        nivel="medio",
        enunciado=(
            "Leia: «A leitura atenta do edital economiza meses de estudo. Muita gente decora "
            "conteúdo que não será cobrado simplesmente porque nunca abriu o documento que define "
            "a prova.»\n\nA ideia central do texto é:"
        ),
        alternativas=(
            ("A", "que decorar conteúdo é a melhor forma de estudar."),
            ("B", "que o edital é um documento difícil de compreender."),
            ("C", "que conhecer o edital evita estudo desperdiçado."),
            ("D", "que estudar por meses é sempre necessário."),
            ("E", "que a prova cobra todo o conteúdo existente."),
        ),
        correta="C",
        comentario=(
            "A ideia central é o que sustenta o texto inteiro: ler o edital evita estudar o que "
            "não cai. As demais alternativas contrariam o texto ou trazem detalhe que ele não "
            "afirma."
        ),
        armadilha="Ideia central não é o detalhe mais chamativo — é o que organiza todo o resto.",
    ),
    Questao(
        id="port-018",
        materia="portugues",
        tema="Pontuação: aposto",
        nivel="medio",
        enunciado="Assinale a alternativa em que a vírgula isola corretamente um aposto explicativo.",
        alternativas=(
            ("A", "O comandante convocou, a tropa para a formatura."),
            ("B", "A prova será, aplicada em setembro."),
            ("C", "Os candidatos aprovados, receberão a convocação."),
            ("D", "São Paulo, capital do estado, concentra o maior efetivo."),
            ("E", "O edital, foi publicado no Diário Oficial."),
        ),
        correta="D",
        comentario=(
            "Em (D), 'capital do estado' explica 'São Paulo' e vem entre vírgulas — aposto "
            "explicativo. As demais separam indevidamente sujeito e verbo ou verbo e complemento."
        ),
        armadilha="Vírgula entre sujeito e verbo é erro, por mais natural que pareça na fala.",
    ),
    Questao(
        id="port-019",
        materia="portugues",
        tema="Concordância verbal",
        nivel="medio",
        enunciado="Assinale a alternativa em que a concordância verbal está correta.",
        alternativas=(
            ("A", "Fazem dois anos que ele presta concurso."),
            ("B", "Tratam-se de questões difíceis."),
            ("C", "Fizeram muito calor durante a prova."),
            ("D", "Havemos de ter muitas vagas neste ano."),
            ("E", "Faz dois anos que ele presta concurso."),
        ),
        correta="E",
        comentario=(
            "O verbo 'fazer' indicando tempo decorrido é impessoal e fica no singular: 'faz dois "
            "anos'. O mesmo vale para fenômenos ('fez calor'). Em (B), o correto é 'trata-se de', "
            "também impessoal."
        ),
        armadilha="'Fazem dois anos' é erro comuníssimo na fala — e cobrança certa na prova.",
    ),
    Questao(
        id="port-020",
        materia="portugues",
        tema="Crase em locuções",
        nivel="medio",
        enunciado="Assinale a alternativa em que o uso da crase está correto.",
        alternativas=(
            ("A", "A prova terá início às 8 horas."),
            ("B", "A prova terá início as 8 horas."),
            ("C", "Compareceu à local indicado."),
            ("D", "Voltou à sair depois do intervalo."),
            ("E", "Entregou o material à todos os candidatos."),
        ),
        correta="A",
        comentario=(
            "Antes de horas determinadas há crase: 'às 8 horas'. Não há crase antes de palavra "
            "masculina ('local'), de verbo ('sair') nem de pronome indefinido masculino ('todos')."
        ),
        armadilha="Locuções adverbiais femininas — às vezes, às pressas, à noite — sempre levam crase.",
    ),
    Questao(
        id="port-021",
        materia="portugues",
        tema="Classes de palavras: pronomes",
        nivel="facil",
        enunciado="Na frase «este documento é meu, aquele é seu», as palavras «meu» e «seu» são:",
        alternativas=(
            ("A", "pronomes demonstrativos."),
            ("B", "pronomes possessivos."),
            ("C", "artigos definidos."),
            ("D", "advérbios de lugar."),
            ("E", "conjunções coordenativas."),
        ),
        correta="B",
        comentario=(
            "'Meu' e 'seu' indicam posse — pronomes possessivos. 'Este' e 'aquele', na mesma "
            "frase, são demonstrativos, porque situam os elementos no espaço ou no discurso."
        ),
        armadilha="A frase contém os dois tipos de pronome; leia qual deles a questão pede.",
    ),
    Questao(
        id="port-022",
        materia="portugues",
        tema="Regência nominal",
        nivel="dificil",
        enunciado="Assinale a alternativa em que a regência nominal está correta.",
        alternativas=(
            ("A", "Ele tem preferência por concursos do que por empregos privados."),
            ("B", "O candidato está apto no serviço militar."),
            ("C", "O candidato está apto para o serviço militar."),
            ("D", "Estamos ansiosos de saber o resultado."),
            ("E", "É necessário de muita disciplina."),
        ),
        correta="C",
        comentario=(
            "'Apto' pede a preposição 'a' ou 'para': apto para o serviço. 'Preferência' pede 'por' "
            "seguido de 'a' na comparação; 'ansioso' pede 'por'; e 'é necessário' não pede "
            "preposição alguma."
        ),
        armadilha="Regência nominal segue a mesma lógica da verbal: cada palavra pede sua preposição.",
    ),
]
