"""Legislação Especial e Institucional — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="leg-001",
        materia="legislacao",
        tema="Lei de Drogas (Lei 11.343/2006)",
        nivel="medio",
        enunciado=(
            "Quanto ao agente que adquire, guarda ou traz consigo drogas para consumo pessoal "
            "(art. 28 da Lei 11.343/2006), é correto afirmar que:"
        ),
        alternativas=(
            ("A", "está sujeito à pena de reclusão de 5 a 15 anos."),
            ("B", "está sujeito a advertência sobre os efeitos das drogas, prestação de serviços à "
                  "comunidade e medida educativa de comparecimento a programa ou curso educativo."),
            ("C", "não sofre qualquer consequência jurídica."),
            ("D", "responde obrigatoriamente por tráfico privilegiado."),
            ("E", "está sujeito apenas a multa em valor fixado pelo delegado."),
        ),
        correta="B",
        comentario=(
            "O art. 28 prevê essas três medidas para quem porta droga para consumo próprio. Para "
            "distinguir do tráfico, o § 2º manda considerar natureza e quantidade da substância, "
            "local e condições da ação, circunstâncias sociais e pessoais, conduta e antecedentes."
        ),
        armadilha="Presumir tráfico só pela quantidade, ignorando os demais critérios legais.",
    ),
    Questao(
        id="leg-002",
        materia="legislacao",
        tema="Lei de Drogas: tráfico",
        nivel="medio",
        enunciado=(
            "Assinale a alternativa que NÃO corresponde a uma conduta típica do art. 33 da Lei de "
            "Drogas (tráfico)."
        ),
        alternativas=(
            ("A", "Importar ou exportar droga sem autorização legal."),
            ("B", "Vender ou expor à venda."),
            ("C", "Ter em depósito para entrega a consumo de terceiro."),
            ("D", "Adquirir para consumo pessoal."),
            ("E", "Transportar ou trazer consigo para fornecer a terceiros."),
        ),
        correta="D",
        comentario=(
            "Adquirir para consumo pessoal é conduta do art. 28, com consequências próprias. O "
            "art. 33 descreve dezoito verbos ligados ao comércio e à difusão da droga."
        ),
        armadilha="Enunciado com 'NÃO': quatro alternativas verdadeiras e uma falsa é o gabarito.",
    ),
    Questao(
        id="leg-003",
        materia="legislacao",
        tema="Lei Maria da Penha (Lei 11.340/2006)",
        nivel="medio",
        enunciado="Sobre a Lei Maria da Penha, é correto afirmar:",
        alternativas=(
            ("A", "Aplica-se somente a agressões físicas."),
            ("B", "Configura violência doméstica e familiar contra a mulher qualquer ação ou omissão "
                  "baseada no gênero que cause morte, lesão, sofrimento físico, sexual ou psicológico "
                  "e dano moral ou patrimonial."),
            ("C", "Exige coabitação entre agressor e vítima em todos os casos."),
            ("D", "Não admite medidas protetivas de urgência antes do inquérito."),
            ("E", "Aplica-se exclusivamente a relações conjugais formalizadas pelo casamento."),
        ),
        correta="B",
        comentario=(
            "O art. 5º define violência doméstica e familiar de forma ampla, no âmbito da unidade "
            "doméstica, da família ou em qualquer relação íntima de afeto — independentemente de "
            "coabitação. As formas de violência incluem física, psicológica, sexual, patrimonial e "
            "moral (art. 7º)."
        ),
        armadilha="Reduzir a lei à agressão física é o erro mais comum — e o mais cobrado.",
    ),
    Questao(
        id="leg-004",
        materia="legislacao",
        tema="Estatuto da Criança e do Adolescente",
        nivel="facil",
        enunciado="Nos termos do ECA (Lei 8.069/1990), considera-se:",
        alternativas=(
            ("A", "criança a pessoa até 14 anos e adolescente entre 14 e 21 anos."),
            ("B", "criança a pessoa até 12 anos incompletos e adolescente entre 12 e 18 anos de idade."),
            ("C", "criança a pessoa até 10 anos e adolescente até 16 anos."),
            ("D", "adolescente somente quem já completou 16 anos."),
            ("E", "criança e adolescente indistintamente qualquer menor de 18 anos."),
        ),
        correta="B",
        comentario=(
            "Art. 2º do ECA: criança é a pessoa até 12 anos incompletos; adolescente, entre 12 e 18 "
            "anos. Em casos expressos em lei, o Estatuto aplica-se a pessoas entre 18 e 21 anos."
        ),
        armadilha="Trocar '12 anos incompletos' por '12 anos completos' muda o resultado da questão.",
    ),
    Questao(
        id="leg-005",
        materia="legislacao",
        tema="ECA: ato infracional",
        nivel="medio",
        enunciado="Ao adolescente a quem se atribua a prática de ato infracional aplicam-se:",
        alternativas=(
            ("A", "penas privativas de liberdade previstas no Código Penal."),
            ("B", "medidas socioeducativas, como advertência, obrigação de reparar o dano, prestação "
                  "de serviços à comunidade, liberdade assistida, semiliberdade e internação."),
            ("C", "somente medidas de proteção."),
            ("D", "multa convertida em prisão."),
            ("E", "prisão preventiva pelo prazo de até 90 dias."),
        ),
        correta="B",
        comentario=(
            "Art. 112 do ECA. Ato infracional é a conduta descrita como crime ou contravenção "
            "praticada por criança ou adolescente; a resposta estatal é socioeducativa, não penal. "
            "À criança aplicam-se apenas medidas de proteção (art. 105)."
        ),
        armadilha="Criança recebe medida de proteção; adolescente, medida socioeducativa.",
    ),
    Questao(
        id="leg-006",
        materia="legislacao",
        tema="Estatuto do Idoso",
        nivel="facil",
        enunciado="Segundo o Estatuto da Pessoa Idosa (Lei 10.741/2003), considera-se idosa a pessoa com:",
        alternativas=(
            ("A", "55 anos ou mais."),
            ("B", "60 anos ou mais."),
            ("C", "65 anos ou mais."),
            ("D", "70 anos ou mais."),
            ("E", "idade variável conforme o Estado da Federação."),
        ),
        correta="B",
        comentario=(
            "Art. 1º: a lei destina-se a regular os direitos das pessoas com idade igual ou "
            "superior a 60 anos. Atenção: alguns direitos específicos, como a gratuidade no "
            "transporte coletivo urbano, têm previsão a partir dos 65 anos."
        ),
        armadilha="Misturar o marco geral (60) com o marco de benefícios específicos (65).",
    ),
    Questao(
        id="leg-007",
        materia="legislacao",
        tema="Lei de Abuso de Autoridade (Lei 13.869/2019)",
        nivel="dificil",
        enunciado="Sobre os crimes de abuso de autoridade, assinale a alternativa correta.",
        alternativas=(
            ("A", "Configuram-se por qualquer erro na atuação do agente público."),
            ("B", "Exigem que o agente atue com a finalidade específica de prejudicar outrem, "
                  "beneficiar a si mesmo ou a terceiro, ou por mero capricho ou satisfação pessoal."),
            ("C", "Só podem ser praticados por policiais militares."),
            ("D", "Dispensam qualquer elemento subjetivo."),
            ("E", "A divergência na interpretação da lei configura, por si só, abuso."),
        ),
        correta="B",
        comentario=(
            "Art. 1º, § 1º, da Lei 13.869/2019 exige a finalidade específica (dolo especial). O § 2º "
            "afirma expressamente que a divergência na interpretação de lei ou na avaliação de "
            "fatos e provas não configura abuso de autoridade."
        ),
        armadilha="Sem a finalidade específica não há crime — a lei protege a atuação regular do agente.",
    ),
    Questao(
        id="leg-008",
        materia="legislacao",
        tema="Estatuto do Desarmamento (Lei 10.826/2003)",
        nivel="medio",
        enunciado="Sobre porte e posse de arma de fogo, é correto afirmar:",
        alternativas=(
            ("A", "Posse é manter a arma dentro de casa ou no local de trabalho, quando o agente é "
                  "titular ou responsável; porte é trazê-la consigo fora desses limites."),
            ("B", "Posse e porte são expressões sinônimas na lei."),
            ("C", "O porte é livre para maiores de 21 anos."),
            ("D", "A posse de arma com numeração suprimida é conduta atípica."),
            ("E", "O porte ilegal de arma de uso restrito é infração administrativa."),
        ),
        correta="A",
        comentario=(
            "Os arts. 12 e 14 distinguem posse (dentro da residência ou dependência desta, ou local "
            "de trabalho, sendo o agente titular ou responsável legal) de porte (trazer consigo). "
            "Arma com numeração suprimida e arma de uso restrito têm tipos penais próprios e mais "
            "graves."
        ),
        armadilha="Confundir posse com porte muda completamente o enquadramento da conduta.",
    ),
    Questao(
        id="leg-009",
        materia="legislacao",
        tema="Crimes hediondos",
        nivel="medio",
        enunciado="Nos termos da Lei 8.072/1990, os crimes hediondos são insuscetíveis de:",
        alternativas=(
            ("A", "progressão de regime, em qualquer hipótese."),
            ("B", "anistia, graça e indulto, e de fiança."),
            ("C", "prisão preventiva."),
            ("D", "livramento condicional, mesmo para réu primário."),
            ("E", "denúncia pelo Ministério Público."),
        ),
        correta="B",
        comentario=(
            "Art. 2º, I e II: os crimes hediondos e equiparados (tortura, tráfico e terrorismo) são "
            "insuscetíveis de anistia, graça, indulto e fiança. A progressão de regime é admitida, "
            "com frações mais severas previstas na Lei de Execução Penal."
        ),
        armadilha="A vedação absoluta de progressão foi superada — cuidado com material desatualizado.",
    ),
    Questao(
        id="leg-010",
        materia="legislacao",
        tema="Código de Trânsito Brasileiro",
        nivel="medio",
        enunciado=(
            "Conduzir veículo automotor com capacidade psicomotora alterada em razão da influência "
            "de álcool ou outra substância psicoativa que determine dependência é, segundo o CTB:"
        ),
        alternativas=(
            ("A", "mera infração administrativa, sem repercussão penal."),
            ("B", "crime de trânsito, com pena de detenção, multa e suspensão do direito de dirigir."),
            ("C", "conduta atípica se não houver acidente."),
            ("D", "contravenção penal punida apenas com multa."),
            ("E", "crime apenas quando o condutor for profissional."),
        ),
        correta="B",
        comentario=(
            "Art. 306 do CTB: é crime, punido com detenção de seis meses a três anos, multa e "
            "suspensão ou proibição de obter a permissão ou habilitação. Independe de acidente ou "
            "de dano concreto — é crime de perigo."
        ),
        armadilha="Achar que sem acidente não há crime: o perigo abstrato basta para a tipificação.",
    ),
    Questao(
        id="leg-011",
        materia="legislacao",
        tema="Prisão em flagrante",
        nivel="medio",
        enunciado="Considera-se em flagrante delito quem:",
        alternativas=(
            ("A", "é encontrado, até 72 horas após o fato, em qualquer lugar."),
            ("B", "está cometendo a infração penal ou acaba de cometê-la."),
            ("C", "é apontado por denúncia anônima como autor de crime antigo."),
            ("D", "confessa crime cometido há um mês."),
            ("E", "possui antecedentes criminais pelo mesmo delito."),
        ),
        correta="B",
        comentario=(
            "Art. 302 do CPP: está em flagrante quem está cometendo a infração, acaba de cometê-la, "
            "é perseguido logo após em situação que faça presumir ser o autor, ou é encontrado logo "
            "depois com instrumentos, armas, objetos ou papéis que o presumam autor."
        ),
        armadilha="Prazos fixos como '72 horas' não existem no conceito legal de flagrante.",
    ),
    Questao(
        id="leg-012",
        materia="legislacao",
        tema="Uso diferenciado da força",
        nivel="dificil",
        enunciado=(
            "Sobre o uso da força por agentes de segurança pública, à luz da legalidade e dos "
            "direitos humanos, é correto afirmar:"
        ),
        alternativas=(
            ("A", "A força pode ser empregada livremente, desde que haja resistência."),
            ("B", "O uso da força deve observar legalidade, necessidade, proporcionalidade, "
                  "moderação e conveniência, sendo a arma de fogo o último recurso."),
            ("C", "O disparo de arma de fogo é o primeiro recurso diante de desobediência verbal."),
            ("D", "A força letal é admitida para proteção exclusiva do patrimônio."),
            ("E", "A prestação de socorro ao ferido é facultativa."),
        ),
        correta="B",
        comentario=(
            "Os princípios internacionais e a normatização interna impõem gradação no uso da força, "
            "reservando a arma de fogo para situações de risco à vida. Após a intervenção, há dever "
            "de prestar socorro e de comunicar o fato."
        ),
        armadilha="Alternativas que autorizam força letal para proteger patrimônio invertem a lógica da lei.",
    ),
]
