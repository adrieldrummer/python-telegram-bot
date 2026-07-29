"""Matemática e Raciocínio Lógico — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="mat-001",
        materia="matematica",
        tema="Porcentagem",
        nivel="facil",
        enunciado=(
            "Em um simulado com 60 questões, um candidato acertou 42. O percentual de acerto foi de:"
        ),
        alternativas=(
            ("A", "58%"),
            ("B", "65%"),
            ("C", "68%"),
            ("D", "70%"),
            ("E", "75%"),
        ),
        correta="D",
        comentario="42 ÷ 60 = 0,7 = 70%. Percentual de acerto é sempre acertos ÷ total × 100.",
        armadilha="Calcular 60 ÷ 42 por pressa e marcar um valor acima de 100% arredondado.",
    ),
    Questao(
        id="mat-002",
        materia="matematica",
        tema="Variações percentuais sucessivas",
        nivel="medio",
        enunciado=(
            "Um produto custava R$ 200,00. Sofreu um aumento de 10% e, no mês seguinte, um desconto "
            "de 10% sobre o novo valor. O preço final é:"
        ),
        alternativas=(
            ("A", "R$ 196,00"),
            ("B", "R$ 198,00"),
            ("C", "R$ 200,00"),
            ("D", "R$ 202,00"),
            ("E", "R$ 220,00"),
        ),
        correta="B",
        comentario=(
            "200 × 1,10 = 220; 220 × 0,90 = 198. Aumento e desconto de mesmo percentual NÃO se "
            "anulam, porque incidem sobre bases diferentes — sobra uma queda de 1%."
        ),
        armadilha="A resposta 'intuitiva' R$ 200,00 é exatamente a que a banca coloca como isca.",
    ),
    Questao(
        id="mat-003",
        materia="matematica",
        tema="Regra de três composta",
        nivel="medio",
        enunciado=(
            "Três agentes conferem 90 documentos em 6 horas. Mantido o mesmo ritmo, cinco agentes "
            "conferirão 200 documentos em:"
        ),
        alternativas=(
            ("A", "6 horas"),
            ("B", "7 horas"),
            ("C", "8 horas"),
            ("D", "9 horas"),
            ("E", "10 horas"),
        ),
        correta="C",
        comentario=(
            "3 agentes × 6 h = 18 agentes-hora para 90 documentos → 0,2 agente-hora por documento. "
            "200 documentos exigem 40 agentes-hora; divididos por 5 agentes, dão 8 horas."
        ),
        armadilha="Montar a proporção invertendo o número de agentes (grandeza inversamente proporcional).",
    ),
    Questao(
        id="mat-004",
        materia="matematica",
        tema="Razão e proporção",
        nivel="facil",
        enunciado=(
            "Um candidato dividirá 120 questões entre Português e Matemática, na razão de 3 para 5, "
            "respectivamente. O número de questões de Matemática será:"
        ),
        alternativas=(
            ("A", "45"),
            ("B", "60"),
            ("C", "72"),
            ("D", "75"),
            ("E", "80"),
        ),
        correta="D",
        comentario="3 + 5 = 8 partes; 120 ÷ 8 = 15 por parte. Matemática fica com 5 × 15 = 75 questões.",
        armadilha="Responder 45 (a parte de Português) por não conferir a qual matéria a razão se refere.",
    ),
    Questao(
        id="mat-005",
        materia="matematica",
        tema="Juros simples",
        nivel="medio",
        enunciado=(
            "Um capital de R$ 1.200,00 foi aplicado a juros simples de 2% ao mês durante 5 meses. "
            "O montante ao final do período é:"
        ),
        alternativas=(
            ("A", "R$ 1.224,00"),
            ("B", "R$ 1.260,00"),
            ("C", "R$ 1.320,00"),
            ("D", "R$ 1.332,00"),
            ("E", "R$ 1.440,00"),
        ),
        correta="C",
        comentario=(
            "J = C × i × t = 1200 × 0,02 × 5 = 120. Montante = capital + juros = 1200 + 120 = "
            "R$ 1.320,00. Em juros simples o percentual incide sempre sobre o capital inicial."
        ),
        armadilha="Aplicar juros compostos (R$ 1.324,90 aprox.) quando o enunciado disse 'simples'.",
    ),
    Questao(
        id="mat-006",
        materia="matematica",
        tema="MMC",
        nivel="facil",
        enunciado=(
            "Um candidato revisa Português a cada 4 dias e Informática a cada 6 dias. Se hoje revisou "
            "as duas matérias, voltará a revisá-las no mesmo dia daqui a:"
        ),
        alternativas=(
            ("A", "8 dias"),
            ("B", "10 dias"),
            ("C", "12 dias"),
            ("D", "18 dias"),
            ("E", "24 dias"),
        ),
        correta="C",
        comentario="O encontro ocorre no mínimo múltiplo comum: MMC(4, 6) = 12 dias.",
        armadilha="Multiplicar 4 × 6 = 24 em vez de calcular o MMC.",
    ),
    Questao(
        id="mat-007",
        materia="matematica",
        tema="Equação do 1º grau",
        nivel="facil",
        enunciado="O triplo de um número, diminuído de 8, é igual a 40. Esse número é:",
        alternativas=(
            ("A", "12"),
            ("B", "14"),
            ("C", "16"),
            ("D", "18"),
            ("E", "24"),
        ),
        correta="C",
        comentario="3x − 8 = 40 → 3x = 48 → x = 16. Traduza a frase em equação antes de calcular.",
        armadilha="Ler 'o triplo de um número diminuído de 8' como 3(x − 8), que daria outro resultado.",
    ),
    Questao(
        id="mat-008",
        materia="matematica",
        tema="Média aritmética",
        nivel="medio",
        enunciado=(
            "Um candidato tirou 6,0; 7,0 e 8,0 nos três primeiros simulados. Para fechar média 7,5 "
            "nos quatro simulados, precisa tirar no quarto:"
        ),
        alternativas=(
            ("A", "8,0"),
            ("B", "8,5"),
            ("C", "9,0"),
            ("D", "9,5"),
            ("E", "10,0"),
        ),
        correta="C",
        comentario=(
            "A soma necessária é 7,5 × 4 = 30. Ele já tem 6 + 7 + 8 = 21. Falta 30 − 21 = 9,0."
        ),
        armadilha="Calcular a média dos três (7,0) e 'completar a diferença' sem multiplicar pelo total.",
    ),
    Questao(
        id="mat-009",
        materia="matematica",
        tema="Sequências lógicas",
        nivel="medio",
        enunciado="Na sequência 2, 5, 11, 23, 47, ..., o próximo termo é:",
        alternativas=(
            ("A", "71"),
            ("B", "83"),
            ("C", "94"),
            ("D", "95"),
            ("E", "96"),
        ),
        correta="D",
        comentario="Cada termo é o anterior multiplicado por 2 e somado 1: 47 × 2 + 1 = 95.",
        armadilha="Repetir a última diferença (24) em vez de dobrá-la, somando 47 + 24 e marcando 71.",
    ),
    Questao(
        id="mat-010",
        materia="matematica",
        tema="Lógica: negação de quantificador",
        nivel="medio",
        enunciado="A negação da proposição «Todo policial é pontual» é:",
        alternativas=(
            ("A", "Existe pelo menos um policial que não é pontual."),
            ("B", "Todo policial é impontual."),
            ("C", "Nenhum policial é pontual."),
            ("D", "Nem todo policial é impontual."),
            ("E", "Alguns policiais são pontuais."),
        ),
        correta="A",
        comentario=(
            "A negação de 'todo A é B' é 'existe pelo menos um A que não é B'. Negar um universal "
            "afirmativo produz um particular negativo — não o oposto extremo."
        ),
        armadilha="Marcar 'nenhum policial é pontual', que é o contrário, não a negação.",
    ),
    Questao(
        id="mat-011",
        materia="matematica",
        tema="Lógica: negação da condicional",
        nivel="dificil",
        enunciado="A negação de «Se estudo todos os dias, então serei aprovado» é:",
        alternativas=(
            ("A", "Se não estudo todos os dias, então não serei aprovado."),
            ("B", "Estudo todos os dias e não serei aprovado."),
            ("C", "Não estudo todos os dias ou serei aprovado."),
            ("D", "Se serei aprovado, então estudo todos os dias."),
            ("E", "Não estudo todos os dias e não serei aprovado."),
        ),
        correta="B",
        comentario=(
            "A negação de 'se p então q' é 'p e não q'. Só há negação quando a condição se cumpre "
            "e a consequência falha. (A) é a inversa e (D) é a recíproca — nenhuma das duas nega."
        ),
        armadilha="Trocar negação por contrapositiva, o erro mais comum em lógica proposicional.",
    ),
    Questao(
        id="mat-012",
        materia="matematica",
        tema="Probabilidade",
        nivel="facil",
        enunciado=(
            "Uma caixa contém 5 questões de Português e 7 de Matemática. Sorteando-se uma questão "
            "ao acaso, a probabilidade de ser de Português é:"
        ),
        alternativas=(
            ("A", "5/7"),
            ("B", "7/12"),
            ("C", "5/12"),
            ("D", "1/5"),
            ("E", "1/2"),
        ),
        correta="C",
        comentario="Casos favoráveis ÷ casos possíveis = 5 ÷ (5 + 7) = 5/12.",
        armadilha="Usar 5/7 (razão entre os grupos) em vez da razão sobre o total.",
    ),
    Questao(
        id="mat-013",
        materia="matematica",
        tema="Geometria: área e perímetro",
        nivel="facil",
        enunciado=(
            "Um pátio retangular mede 25 m de comprimento por 12 m de largura. A área e o "
            "perímetro do pátio são, respectivamente:"
        ),
        alternativas=(
            ("A", "37 m² e 300 m"),
            ("B", "300 m² e 37 m"),
            ("C", "150 m² e 74 m"),
            ("D", "300 m² e 74 m"),
            ("E", "300 m² e 100 m"),
        ),
        correta="D",
        comentario="Área = 25 × 12 = 300 m². Perímetro = 2 × (25 + 12) = 74 m.",
        armadilha="Esquecer de dobrar a soma dos lados e marcar 37 m de perímetro.",
    ),

    Questao(
        id="mat-014",
        materia="matematica",
        tema="Sistema métrico",
        nivel="facil",
        enunciado="Um trajeto de 2,5 km percorrido por uma viatura corresponde, em metros, a:",
        alternativas=(
            ("A", "25 m"),
            ("B", "250 m"),
            ("C", "2.500 m"),
            ("D", "25.000 m"),
            ("E", "250.000 m"),
        ),
        correta="C",
        comentario="1 km = 1.000 m, logo 2,5 × 1.000 = 2.500 m.",
        armadilha="Errar a casa decimal na conversão — fonte clássica de ponto perdido por desatenção.",
    ),
    Questao(
        id="mat-015",
        materia="matematica",
        tema="Teorema de Pitágoras",
        nivel="medio",
        enunciado=(
            "Em um triângulo retângulo, os catetos medem 6 cm e 8 cm. A hipotenusa mede:"
        ),
        alternativas=(
            ("A", "10 cm"),
            ("B", "12 cm"),
            ("C", "14 cm"),
            ("D", "48 cm"),
            ("E", "100 cm"),
        ),
        correta="A",
        comentario="a² = b² + c² = 6² + 8² = 36 + 64 = 100 → a = 10 cm.",
        armadilha="Parar em 100 e marcar sem extrair a raiz quadrada.",
    ),
    Questao(
        id="mat-016",
        materia="matematica",
        tema="Sistema de equações do 1º grau",
        nivel="medio",
        enunciado=(
            "A soma de dois números é 30 e a diferença entre eles é 8. Esses números são:"
        ),
        alternativas=(
            ("A", "10 e 20"),
            ("B", "11 e 19"),
            ("C", "12 e 18"),
            ("D", "13 e 17"),
            ("E", "14 e 16"),
        ),
        correta="B",
        comentario=(
            "x + y = 30 e x − y = 8. Somando as equações: 2x = 38 → x = 19; logo y = 11. O método "
            "da adição elimina uma variável de imediato."
        ),
        armadilha="Conferir sempre as duas condições: várias alternativas somam 30, mas só uma tem diferença 8.",
    ),
    Questao(
        id="mat-017",
        materia="matematica",
        tema="Tabelas e gráficos",
        nivel="facil",
        enunciado=(
            "Um gráfico de barras mostra as ocorrências registradas em quatro meses: janeiro 40, "
            "fevereiro 55, março 35 e abril 50. A média mensal de ocorrências no período é:"
        ),
        alternativas=(
            ("A", "40"),
            ("B", "45"),
            ("C", "46"),
            ("D", "50"),
            ("E", "55"),
        ),
        correta="B",
        comentario="(40 + 55 + 35 + 50) ÷ 4 = 180 ÷ 4 = 45 ocorrências por mês.",
        armadilha="Somar e esquecer de dividir pelo número de meses.",
    ),
    Questao(
        id="mat-018",
        materia="matematica",
        tema="Divisão em partes proporcionais",
        nivel="medio",
        enunciado=(
            "Um chefe de setor distribuiu 378 processos entre três agentes, em partes proporcionais "
            "a 2, 3 e 4. O agente que recebeu a maior quantidade ficou com:"
        ),
        alternativas=(
            ("A", "84 processos."),
            ("B", "126 processos."),
            ("C", "140 processos."),
            ("D", "168 processos."),
            ("E", "189 processos."),
        ),
        correta="D",
        comentario=(
            "Some as partes: 2 + 3 + 4 = 9. Divida o total pelo número de partes: "
            "378 ÷ 9 = 42 processos por parte. A maior fração é 4 partes: 4 × 42 = "
            "<strong>168 processos</strong>. Conferindo: 84 + 126 + 168 = 378."
        ),
        armadilha=(
            "O enunciado pede a maior quantidade, não a menor nem o valor de uma parte. Marcar 42 "
            "(uma parte) ou 84 (a menor) é o deslize mais frequente."
        ),
    ),
    Questao(
        id="mat-019",
        materia="matematica",
        tema="Contagem e senhas",
        nivel="dificil",
        enunciado=(
            "Um cofre abre com uma senha de 3 dígitos, escolhidos entre os algarismos de 0 a 9, "
            "permitida a repetição. Quantas senhas diferentes são possíveis?"
        ),
        alternativas=(
            ("A", "30"),
            ("B", "270"),
            ("C", "720"),
            ("D", "900"),
            ("E", "1.000"),
        ),
        correta="E",
        comentario=(
            "São 10 opções para cada uma das 3 posições, e a repetição é permitida: "
            "10 × 10 × 10 = <strong>1.000</strong> senhas (de 000 a 999). Se a repetição fosse "
            "proibida, seriam 10 × 9 × 8 = 720."
        ),
        armadilha=(
            "A frase 'permitida a repetição' decide a conta inteira. Sem ela, a resposta seria 720 — "
            "que está entre as alternativas justamente para pegar quem leu rápido."
        ),
    ),
    Questao(
        id="mat-020",
        materia="matematica",
        tema="Regra de três: tempo e trabalho",
        nivel="medio",
        enunciado=(
            "Três funcionários levam 3 horas e 20 minutos para organizar um arquivo. Mantido o mesmo "
            "ritmo de trabalho, quatro funcionários levarão:"
        ),
        alternativas=(
            ("A", "2 horas e 30 minutos."),
            ("B", "2 horas e 45 minutos."),
            ("C", "3 horas."),
            ("D", "4 horas."),
            ("E", "4 horas e 30 minutos."),
        ),
        correta="A",
        comentario=(
            "Converta tudo para minutos: 3 h 20 min = 200 minutos. O trabalho total é "
            "3 × 200 = 600 funcionário-minutos. Com 4 funcionários: 600 ÷ 4 = 150 minutos = "
            "<strong>2 h 30 min</strong>. Mais gente, menos tempo — grandezas inversamente "
            "proporcionais."
        ),
        armadilha=(
            "Aqui a proporção é inversa. Montar a regra de três direta dá 4 h 27 min, um valor que "
            "não aparece nas alternativas justamente porque o erro esperado é outro."
        ),
    ),
]
