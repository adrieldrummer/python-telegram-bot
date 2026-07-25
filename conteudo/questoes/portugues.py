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
            ("C", "O relatório foi mau redigido."),
            ("D", "Mau chegou à unidade, iniciou o serviço."),
            ("E", "Foi um mau começo, mas o dia terminou mal."),
        ),
        correta="E",
        comentario=(
            "'Mau' é adjetivo e se opõe a 'bom' ('mau começo' / 'bom começo'). 'Mal' é advérbio "
            "(ou substantivo) e se opõe a 'bem' ('terminou mal' / 'terminou bem'). Em (E) as duas "
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
            ("C", "Houve muitas ocorrências no fim de semana."),
            ("D", "Existiu, no bairro, diversos casos semelhantes."),
            ("E", "Devem haver soluções melhores para o problema."),
        ),
        correta="C",
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
            ("A", "Por que — porque — porquê"),
            ("B", "Porque — por que — por quê"),
            ("C", "Por quê — porque — por que"),
            ("D", "Por que — por quê — porquê"),
            ("E", "Porquê — porque — por que"),
        ),
        correta="A",
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
            ("A", "É proibido a entrada de pessoas não autorizadas."),
            ("B", "É proibida a entrada de pessoas não autorizadas."),
            ("C", "É proibidas a entrada de pessoas não autorizadas."),
            ("D", "São proibido a entrada de pessoas não autorizadas."),
            ("E", "É proibido as entradas de pessoas não autorizadas."),
        ),
        correta="B",
        comentario=(
            "Nas expressões 'é proibido', 'é necessário', 'é bom', a concordância varia: sem "
            "determinante, o adjetivo fica no masculino singular ('É proibido entrada'); com "
            "determinante ('a' entrada), há concordância plena: 'É proibida a entrada'."
        ),
        armadilha="A alternativa (A) só estaria certa se o artigo 'a' fosse retirado.",
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
            ("B", "a escolha inadequada do conteúdo estudado."),
            ("C", "a impossibilidade de estudar por muitas horas."),
            ("D", "a ausência de material didático de qualidade."),
            ("E", "o excesso de questões resolvidas sem teoria."),
        ),
        correta="B",
        comentario=(
            "O texto afirma explicitamente que esforço havia ('não faltou esforço') e localiza a "
            "falha na direção — isto é, no que era estudado. Interpretação cobra o que está "
            "escrito, não o que é plausível."
        ),
        armadilha="(A) e (C) contradizem o texto; (D) e (E) trazem informação que o texto não dá.",
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
            ("C", "O sargento, responsável pelo setor, comunicou a decisão à equipe."),
            ("D", "O sargento responsável, pelo setor comunicou a decisão, à equipe."),
            ("E", "O sargento responsável pelo setor comunicou, a decisão à equipe."),
        ),
        correta="C",
        comentario=(
            "Em (C) 'responsável pelo setor' está entre vírgulas como explicação intercalada, uso "
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
            ("C", "Choveu forte durante a madrugada."),
            ("D", "Alugam-se salas comerciais."),
            ("E", "Alguém deixou o portão aberto."),
        ),
        correta="C",
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
            ("A", "Aonde você mora atualmente?"),
            ("B", "Onde você vai depois do expediente?"),
            ("C", "Aonde ele trabalha, todos cumprem o horário."),
            ("D", "Aonde você pretende chegar com esse ritmo de estudo?"),
            ("E", "Onde iremos amanhã?"),
        ),
        correta="D",
        comentario=(
            "'Aonde' é usado com verbos de movimento que pedem a preposição 'a' (chegar a, ir a): "
            "'aonde pretende chegar'. 'Onde' indica lugar fixo, sem movimento: 'onde você mora', "
            "'onde ele trabalha'. Por isso (A), (C), (B) e (E) invertem os dois usos."
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
            ("A", "Trabalho nesta função há dois anos."),
            ("B", "Daqui há dois meses farei a prova."),
            ("C", "Há dois meses farei a prova."),
            ("D", "Estudo a três semanas sem parar."),
            ("E", "Ele saiu a pouco da unidade."),
        ),
        correta="A",
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
            ("B", "contudo"),
            ("C", "porquanto"),
            ("D", "por conseguinte"),
            ("E", "assim"),
        ),
        correta="B",
        comentario=(
            "'Contudo' é conjunção adversativa (oposição), assim como 'mas', 'porém', 'todavia' e "
            "'entretanto'. 'Portanto', 'por conseguinte' e 'assim' são conclusivos; 'porquanto' é "
            "explicativo/causal."
        ),
        armadilha="Trocar oposição por conclusão inverte o sentido do período inteiro.",
    ),
]
