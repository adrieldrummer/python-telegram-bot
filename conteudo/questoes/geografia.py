"""Geografia e Atualidades — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="geo-001",
        materia="geografia",
        tema="Biomas brasileiros",
        nivel="facil",
        enunciado=(
            "Bioma do Centro-Oeste brasileiro, considerado a savana brasileira, com árvores de "
            "troncos retorcidos e casca grossa:"
        ),
        alternativas=(
            ("A", "Amazônia"),
            ("B", "Caatinga"),
            ("C", "Pampa"),
            ("D", "Cerrado"),
            ("E", "Pantanal"),
        ),
        correta="D",
        comentario=(
            "O Cerrado é a savana brasileira, típica do Centro-Oeste. A Caatinga é do semiárido "
            "nordestino; o Pampa são os campos do Sul; o Pantanal é a maior planície alagável do "
            "mundo."
        ),
        armadilha="Cerrado e Caatinga são confundidos por serem os dois de clima seco.",
    ),
    Questao(
        id="geo-002",
        materia="geografia",
        tema="Biomas brasileiros",
        nivel="medio",
        enunciado="Sobre a Mata Atlântica, é correto afirmar que:",
        alternativas=(
            ("A", "é o bioma mais preservado do país, com mais de 90% da área original."),
            ("B", "é formada por vegetação adaptada à seca prolongada."),
            ("C", "situa-se exclusivamente na região Norte."),
            ("D", "corresponde à maior planície alagável do mundo."),
            ("E", "ocupa o litoral brasileiro e é um dos biomas mais desmatados do país."),
        ),
        correta="E",
        comentario=(
            "A Mata Atlântica acompanha o litoral brasileiro — justamente a área de ocupação mais "
            "antiga e densa do país —, o que a tornou um dos biomas mais desmatados."
        ),
        armadilha="A maior floresta preservada é a Amazônia; a mais devastada, a Mata Atlântica.",
    ),
    Questao(
        id="geo-003",
        materia="geografia",
        tema="Relevo e hidrografia",
        nivel="medio",
        enunciado="Sobre o relevo e a hidrografia do Brasil, é correto afirmar:",
        alternativas=(
            ("A", "Predominam planaltos e depressões, com poucas áreas de grande altitude, e o país "
                  "possui uma das maiores redes hidrográficas do mundo."),
            ("B", "Predominam cadeias montanhosas de grande altitude, como os Andes."),
            ("C", "O território é majoritariamente desértico, com rios temporários."),
            ("D", "A Bacia do Prata é a maior bacia hidrográfica brasileira."),
            ("E", "O relevo brasileiro é formado principalmente por vulcões ativos."),
        ),
        correta="A",
        comentario=(
            "O relevo brasileiro é de altitudes modestas, com predomínio de planaltos e depressões. "
            "Na hidrografia, destaca-se a Bacia Amazônica, a maior do país e do mundo em volume."
        ),
        armadilha="Associar o Brasil a grandes cadeias montanhosas — isso é a América andina.",
    ),
    Questao(
        id="geo-004",
        materia="geografia",
        tema="Clima",
        nivel="facil",
        enunciado="Predominam no território brasileiro os climas:",
        alternativas=(
            ("A", "polar e temperado frio."),
            ("B", "tropical e equatorial, com variações como o semiárido no Nordeste e o subtropical no Sul."),
            ("C", "desértico em quase toda a extensão."),
            ("D", "mediterrâneo, em razão da latitude."),
            ("E", "frio de montanha, pela altitude do relevo."),
        ),
        correta="B",
        comentario=(
            "A posição em latitudes tropicais explica o predomínio dos climas tropical e "
            "equatorial. O semiárido nordestino e o subtropical do Sul são as variações mais "
            "cobradas."
        ),
        armadilha="O Sul é subtropical, não temperado frio — a diferença aparece em prova.",
    ),
    Questao(
        id="geo-005",
        materia="geografia",
        tema="População brasileira",
        nivel="medio",
        enunciado="Sobre a população brasileira atual, é correto afirmar que:",
        alternativas=(
            ("A", "cresce em ritmo acelerado, com população cada vez mais jovem."),
            ("B", "está distribuída de forma homogênea pelo território."),
            ("C", "tem crescimento desacelerado e processo de envelhecimento, com concentração no "
                  "litoral e nas regiões Sudeste e Nordeste."),
            ("D", "é majoritariamente rural."),
            ("E", "não registra movimentos migratórios internos."),
        ),
        correta="C",
        comentario=(
            "A taxa de crescimento vem caindo e a pirâmide etária envelhece. A ocupação continua "
            "concentrada no litoral e nas regiões Sudeste e Nordeste, e o país é majoritariamente "
            "urbano desde os anos 1970."
        ),
        armadilha="O êxodo rural do século 20 inverteu a relação campo-cidade: hoje o Brasil é urbano.",
    ),
    Questao(
        id="geo-006",
        materia="geografia",
        tema="Atividades econômicas",
        nivel="medio",
        enunciado="Sobre a matriz energética e a economia brasileira, é correto afirmar:",
        alternativas=(
            ("A", "A energia nuclear é a principal fonte de eletricidade do país."),
            ("B", "A industrialização brasileira concentrou-se historicamente na região Norte."),
            ("C", "O carvão mineral responde por mais da metade da geração elétrica."),
            ("D", "A hidrelétrica tem papel central, com participação crescente de fontes renováveis "
                  "como eólica e solar."),
            ("E", "A agropecuária tem participação irrelevante nas exportações."),
        ),
        correta="D",
        comentario=(
            "A hidreletricidade é a base da matriz elétrica brasileira, com avanço expressivo de "
            "eólica e solar nos últimos anos. A industrialização concentrou-se no Sudeste, e a "
            "agropecuária — soja, cana e pecuária — é peso pesado das exportações."
        ),
        armadilha="Confundir matriz elétrica (geração) com matriz energética (todo o consumo).",
    ),
    Questao(
        id="geo-007",
        materia="geografia",
        tema="Problemas ambientais",
        nivel="facil",
        enunciado="O aquecimento global está diretamente associado:",
        alternativas=(
            ("A", "à diminuição do desmatamento nas florestas tropicais."),
            ("B", "à redução da atividade industrial no mundo."),
            ("C", "ao aumento da camada de ozônio."),
            ("D", "ao resfriamento das correntes marítimas equatoriais."),
            ("E", "ao aumento da emissão de gases de efeito estufa."),
        ),
        correta="E",
        comentario=(
            "O aumento da temperatura média do planeta está ligado à emissão de gases de efeito "
            "estufa, sobretudo pela queima de combustíveis fósseis e pelo desmatamento."
        ),
        armadilha="Buraco na camada de ozônio e efeito estufa são fenômenos distintos.",
    ),
    Questao(
        id="geo-008",
        materia="geografia",
        tema="Impactos ambientais",
        nivel="medio",
        enunciado="São impactos ambientais decorrentes de atividades humanas no Brasil:",
        alternativas=(
            ("A", "desmatamento para expansão agrícola, poluição urbana, uso intensivo de "
                  "agrotóxicos e pressão sobre recursos hídricos."),
            ("B", "movimentos tectônicos e formação de vulcões."),
            ("C", "alternância natural entre estações do ano."),
            ("D", "deriva continental e formação de cadeias montanhosas."),
            ("E", "eclipses e marés."),
        ),
        correta="A",
        comentario=(
            "A questão pede impactos de origem humana (antrópicos). As demais alternativas trazem "
            "fenômenos naturais, que não dependem da ação humana."
        ),
        armadilha="Ler 'impacto ambiental' como qualquer fenômeno da natureza.",
    ),
    Questao(
        id="geo-009",
        materia="geografia",
        tema="Nova ordem mundial",
        nivel="medio",
        enunciado="Após o fim da Guerra Fria, a configuração geopolítica mundial passou a ser marcada por:",
        alternativas=(
            ("A", "manutenção da divisão do mundo em dois blocos militares equivalentes."),
            ("B", "predomínio dos Estados Unidos, ascensão de novas potências como a China e "
                  "fortalecimento de blocos econômicos regionais."),
            ("C", "desaparecimento das organizações internacionais."),
            ("D", "isolamento econômico generalizado entre os países."),
            ("E", "retorno do sistema colonial europeu."),
        ),
        correta="B",
        comentario=(
            "Com o colapso soviético, o mundo bipolar deu lugar a uma ordem mais complexa: "
            "hegemonia americana, ascensão chinesa e blocos regionais como a União Europeia e o "
            "Mercosul ganhando peso."
        ),
        armadilha="Bipolar (Guerra Fria) x multipolar (hoje): a banca cobra esse contraste.",
    ),
    Questao(
        id="geo-010",
        materia="geografia",
        tema="Amazônia e circulação atmosférica",
        nivel="medio",
        enunciado=(
            "A Floresta Amazônica libera para a atmosfera, por evapotranspiração, enormes volumes "
            "de vapor d'água. Barrado pela cordilheira dos Andes, esse vapor é desviado e alimenta "
            "as chuvas de outras regiões do continente. Esse fenômeno é conhecido como:"
        ),
        alternativas=(
            ("A", "rios voadores."),
            ("B", "efeito orográfico."),
            ("C", "inversão térmica."),
            ("D", "El Niño."),
            ("E", "zona de convergência intertropical."),
        ),
        correta="A",
        comentario=(
            "Os <strong>rios voadores</strong> são massas de ar carregadas de umidade que saem da "
            "Amazônia, encontram a barreira dos Andes e são desviadas para o Centro-Oeste, o Sudeste "
            "e o Sul do Brasil — daí a ligação direta entre desmatamento amazônico e regime de "
            "chuvas em São Paulo. Efeito orográfico é a chuva provocada pelo relevo; inversão "
            "térmica concentra poluentes; El Niño é o aquecimento anômalo do Pacífico."
        ),
        armadilha=(
            "O nome sugere um rio de verdade. O fenômeno é atmosférico: vapor transportado pelo ar."
        ),
    ),
    Questao(
        id="geo-011",
        materia="geografia",
        tema="Meio ambiente e políticas públicas",
        nivel="medio",
        enunciado=(
            "A Amazônia é frequentemente citada em atualidades ambientais porque:"
        ),
        alternativas=(
            ("A", "não possui população residente."),
            ("B", "é o menor bioma brasileiro em extensão."),
            ("C", "está integralmente fora do território brasileiro."),
            ("D", "é a maior floresta tropical do mundo e concentra os maiores índices de "
                  "desmatamento monitorados no país."),
            ("E", "é uma área desértica em processo de recuperação."),
        ),
        correta="D",
        comentario=(
            "A Amazônia é a maior floresta tropical do planeta, ocupa a região Norte e concentra o "
            "debate sobre desmatamento, queimadas e políticas de fiscalização — temas recorrentes "
            "em atualidades."
        ),
        armadilha="A floresta é internacional, mas a maior parte está em território brasileiro.",
    ),
    Questao(
        id="geo-012",
        materia="geografia",
        tema="Urbanização",
        nivel="medio",
        enunciado="A urbanização brasileira do século 20 caracterizou-se por:",
        alternativas=(
            ("A", "esvaziamento das cidades e retorno da população ao campo."),
            ("B", "estagnação demográfica nas capitais."),
            ("C", "distribuição equilibrada da indústria por todas as regiões."),
            ("D", "urbanização planejada, sem formação de periferias."),
            ("E", "êxodo rural intenso, crescimento acelerado das cidades e concentração industrial "
                  "no Sudeste."),
        ),
        correta="E",
        comentario=(
            "A industrialização concentrada no Sudeste puxou o êxodo rural e produziu crescimento "
            "urbano acelerado — muitas vezes sem infraestrutura, o que explica a formação de "
            "periferias e os problemas urbanos atuais."
        ),
        armadilha="Urbanização rápida não é sinônimo de urbanização planejada.",
    ),
    Questao(
        id="geo-013",
        materia="geografia",
        tema="Domínios morfoclimáticos",
        nivel="medio",
        enunciado=(
            "Domínio morfoclimático brasileiro caracterizado por chapadões recobertos por vegetação "
            "de árvores baixas e retorcidas, solos ácidos e duas estações bem marcadas — uma chuvosa "
            "e outra seca. Trata-se do domínio:"
        ),
        alternativas=(
            ("A", "das araucárias."),
            ("B", "dos mares de morros."),
            ("C", "do cerrado."),
            ("D", "das caatingas."),
            ("E", "das pradarias."),
        ),
        correta="C",
        comentario=(
            "Na classificação de Aziz Ab'Sáber, o <strong>domínio do cerrado</strong> reúne "
            "chapadões, solos ácidos e vegetação de troncos retorcidos, com sazonalidade marcada. "
            "Mares de morros é o relevo mamelonar do Sudeste; caatingas é o semiárido nordestino; "
            "araucárias é o planalto meridional; pradarias é o pampa gaúcho."
        ),
        armadilha=(
            "Bioma e domínio morfoclimático não são a mesma coisa: o domínio combina relevo, clima, "
            "solo, vegetação e hidrografia — a banca costuma cobrar o conjunto, não só a vegetação."
        ),
    ),
    Questao(
        id="geo-014",
        materia="geografia",
        tema="Monitoramento ambiental",
        nivel="facil",
        enunciado=(
            "O órgão brasileiro responsável por monitorar, por imagens de satélite, o desmatamento e "
            "os focos de queimada no território nacional é o:"
        ),
        alternativas=(
            ("A", "IBGE."),
            ("B", "IBAMA."),
            ("C", "INMET."),
            ("D", "INPE."),
            ("E", "ICMBio."),
        ),
        correta="D",
        comentario=(
            "O <strong>INPE</strong> (Instituto Nacional de Pesquisas Espaciais) opera os sistemas "
            "PRODES e DETER, que medem desmatamento, e o programa de queimadas. O IBGE faz censos e "
            "cartografia; o IBAMA fiscaliza e autua; o INMET é meteorologia; o ICMBio administra as "
            "unidades de conservação federais."
        ),
        armadilha=(
            "Monitorar é diferente de fiscalizar: o INPE mede e divulga o dado, o IBAMA é quem aplica "
            "a multa."
        ),
    ),
    Questao(
        id="geo-015",
        materia="geografia",
        tema="Geopolítica e Guerra Fria",
        nivel="medio",
        enunciado=(
            "Criada em 1949, no contexto da Guerra Fria, reuniu países ocidentais em uma aliança "
            "militar de defesa mútua e permanece ativa até hoje. A organização é a:"
        ),
        alternativas=(
            ("A", "ONU."),
            ("B", "OTAN."),
            ("C", "Pacto de Varsóvia."),
            ("D", "OEA."),
            ("E", "Mercosul."),
        ),
        correta="B",
        comentario=(
            "A <strong>OTAN</strong> (Organização do Tratado do Atlântico Norte) nasceu em 1949 "
            "liderada pelos Estados Unidos. A resposta soviética veio em 1955, com o "
            "<strong>Pacto de Varsóvia</strong>, dissolvido em 1991. A ONU é de 1945 e não é aliança "
            "militar; a OEA reúne países americanos; o Mercosul é bloco econômico sul-americano."
        ),
        armadilha=(
            "OTAN e Pacto de Varsóvia são os dois lados do mesmo tabuleiro — a banca troca as datas "
            "(1949 e 1955) e os blocos."
        ),
    ),
    Questao(
        id="geo-016",
        materia="geografia",
        tema="Atualidades: clima e saúde",
        nivel="medio",
        enunciado=(
            "Eventos climáticos extremos mais frequentes — enchentes, secas prolongadas e ondas de "
            "calor — vêm sendo associados por organismos internacionais a impactos diretos na saúde "
            "pública. Sobre essa relação, é correto afirmar que:"
        ),
        alternativas=(
            ("A", "não há relação estabelecida entre clima e doenças transmissíveis."),
            ("B", "enchentes reduzem a incidência de doenças de veiculação hídrica."),
            ("C", "ondas de calor afetam apenas países de clima temperado."),
            ("D", "a expansão de áreas quentes e úmidas favorece a proliferação de vetores como o "
                  "mosquito Aedes aegypti, ampliando a área de risco de arboviroses."),
            ("E", "secas prolongadas melhoram a qualidade do ar nas regiões afetadas."),
        ),
        correta="D",
        comentario=(
            "O aquecimento amplia a área com temperatura e umidade favoráveis a vetores, empurrando "
            "doenças como dengue, zika e chikungunya para regiões e altitudes onde antes não "
            "ocorriam. Enchentes <em>aumentam</em> doenças de veiculação hídrica (leptospirose, "
            "hepatite A); secas pioram a qualidade do ar, por poeira e fumaça de queimadas."
        ),
        armadilha=(
            "As alternativas erradas invertem o sentido do impacto. Em questão de atualidades "
            "ambientais, desconfie de qualquer opção que descreva um evento extremo como benéfico."
        ),
    ),
]
