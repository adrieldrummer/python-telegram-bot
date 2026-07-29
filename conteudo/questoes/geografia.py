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
            ("C", "Cerrado"),
            ("D", "Pampa"),
            ("E", "Pantanal"),
        ),
        correta="C",
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
            ("B", "ocupa o litoral brasileiro e é um dos biomas mais desmatados do país."),
            ("C", "situa-se exclusivamente na região Norte."),
            ("D", "corresponde à maior planície alagável do mundo."),
            ("E", "é formada por vegetação adaptada à seca prolongada."),
        ),
        correta="B",
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
            ("A", "Predominam cadeias montanhosas de grande altitude, como os Andes."),
            ("B", "Predominam planaltos e depressões, com poucas áreas de grande altitude, e o país "
                  "possui uma das maiores redes hidrográficas do mundo."),
            ("C", "O território é majoritariamente desértico, com rios temporários."),
            ("D", "A Bacia do Prata é a maior bacia hidrográfica brasileira."),
            ("E", "O relevo brasileiro é formado principalmente por vulcões ativos."),
        ),
        correta="B",
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
            ("B", "tem crescimento desacelerado e processo de envelhecimento, com concentração no "
                  "litoral e nas regiões Sudeste e Nordeste."),
            ("C", "está distribuída de forma homogênea pelo território."),
            ("D", "é majoritariamente rural."),
            ("E", "não registra movimentos migratórios internos."),
        ),
        correta="B",
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
            ("B", "A hidrelétrica tem papel central, com participação crescente de fontes renováveis "
                  "como eólica e solar."),
            ("C", "O carvão mineral responde por mais da metade da geração elétrica."),
            ("D", "A industrialização brasileira concentrou-se historicamente na região Norte."),
            ("E", "A agropecuária tem participação irrelevante nas exportações."),
        ),
        correta="B",
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
            ("A", "ao aumento da emissão de gases de efeito estufa."),
            ("B", "à redução da atividade industrial no mundo."),
            ("C", "ao aumento da camada de ozônio."),
            ("D", "ao resfriamento das correntes marítimas equatoriais."),
            ("E", "à diminuição do desmatamento nas florestas tropicais."),
        ),
        correta="A",
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
        tema="Atualidades: como estudar",
        nivel="facil",
        enunciado=(
            "O tópico Atualidades do edital costuma cobrar fatos ocorridos, principalmente:"
        ),
        alternativas=(
            ("A", "nos últimos seis meses anteriores à prova, com atenção também ao noticiário local."),
            ("B", "na década anterior à publicação do edital."),
            ("C", "exclusivamente no exterior."),
            ("D", "apenas em anos eleitorais."),
            ("E", "somente fatos históricos anteriores a 1988."),
        ),
        correta="A",
        comentario=(
            "O recorte usual é o semestre anterior à prova, incluindo fatos nacionais e do estado de "
            "São Paulo. Por isso o estudo de atualidades deve se concentrar nas semanas próximas à "
            "data da prova, em resumos e telejornais confiáveis."
        ),
        armadilha="Estudar atualidades meses antes é esforço perdido: o recorte é móvel.",
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
            ("A", "é a maior floresta tropical do mundo e concentra os maiores índices de "
                  "desmatamento monitorados no país."),
            ("B", "é o menor bioma brasileiro em extensão."),
            ("C", "está integralmente fora do território brasileiro."),
            ("D", "não possui população residente."),
            ("E", "é uma área desértica em processo de recuperação."),
        ),
        correta="A",
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
            ("B", "êxodo rural intenso, crescimento acelerado das cidades e concentração industrial "
                  "no Sudeste."),
            ("C", "distribuição equilibrada da indústria por todas as regiões."),
            ("D", "urbanização planejada, sem formação de periferias."),
            ("E", "estagnação demográfica nas capitais."),
        ),
        correta="B",
        comentario=(
            "A industrialização concentrada no Sudeste puxou o êxodo rural e produziu crescimento "
            "urbano acelerado — muitas vezes sem infraestrutura, o que explica a formação de "
            "periferias e os problemas urbanos atuais."
        ),
        armadilha="Urbanização rápida não é sinônimo de urbanização planejada.",
    ),
]
