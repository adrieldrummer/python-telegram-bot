"""Noções de Informática — questões autorais no estilo da banca."""

from __future__ import annotations

from . import Questao

QUESTOES: list[Questao] = [
    Questao(
        id="inf-001",
        materia="informatica",
        tema="Planilhas: funções básicas",
        nivel="facil",
        enunciado=(
            "Em uma planilha eletrônica, as células A1, A2 e A3 contêm, respectivamente, 10, 20 e "
            "30. A fórmula =SOMA(A1:A3)/3 retorna:"
        ),
        alternativas=(
            ("A", "20"),
            ("B", "10"),
            ("C", "30"),
            ("D", "60"),
            ("E", "180"),
        ),
        correta="A",
        comentario="SOMA(A1:A3) = 60; dividido por 3 resulta em 20 — o mesmo que =MÉDIA(A1:A3).",
        armadilha="Esquecer a divisão e marcar 60, o valor da soma.",
    ),
    Questao(
        id="inf-002",
        materia="informatica",
        tema="Planilhas: referências",
        nivel="medio",
        enunciado="Em uma planilha, a referência $B$2 é classificada como:",
        alternativas=(
            ("A", "relativa, pois muda ao copiar a fórmula."),
            ("B", "absoluta, pois não se altera ao copiar a fórmula para outras células."),
            ("C", "mista, travando apenas a linha."),
            ("D", "circular."),
            ("E", "externa, por apontar para outro arquivo."),
        ),
        correta="B",
        comentario=(
            "O cifrão trava a referência: $B$2 é absoluta (coluna e linha travadas); B$2 e $B2 são "
            "mistas; B2 é relativa."
        ),
        armadilha="Referência mista trava só um dos dois — leia onde está o cifrão.",
    ),
    Questao(
        id="inf-003",
        materia="informatica",
        tema="Segurança da informação",
        nivel="medio",
        enunciado=(
            "Ataque em que o criminoso se passa por instituição confiável, por e-mail ou mensagem, "
            "para induzir a vítima a fornecer senhas e dados bancários. Trata-se de:"
        ),
        alternativas=(
            ("A", "firewall."),
            ("B", "backup incremental."),
            ("C", "phishing."),
            ("D", "criptografia simétrica."),
            ("E", "compactação de arquivos."),
        ),
        correta="C",
        comentario=(
            "Phishing é engenharia social: explora a confiança do usuário, não uma falha técnica. "
            "Por isso antivírus sozinho não resolve — a defesa principal é a desconfiança treinada."
        ),
        armadilha="Confundir phishing (engano) com ransomware (sequestro de dados por criptografia).",
    ),
    Questao(
        id="inf-004",
        materia="informatica",
        tema="Segurança: malware",
        nivel="medio",
        enunciado=(
            "Programa malicioso que criptografa os arquivos do computador e exige pagamento de "
            "resgate para liberá-los é conhecido como:"
        ),
        alternativas=(
            ("A", "spyware."),
            ("B", "adware."),
            ("C", "worm."),
            ("D", "ransomware."),
            ("E", "cookie."),
        ),
        correta="D",
        comentario=(
            "Ransomware sequestra dados mediante criptografia. Spyware espiona; adware exibe "
            "anúncios; worm se propaga sozinho pela rede; cookie é apenas um arquivo de preferências "
            "do navegador, não um malware."
        ),
        armadilha="Cookie aparece como distrator porque muita gente associa cookie a 'vírus'.",
    ),
    Questao(
        id="inf-005",
        materia="informatica",
        tema="Backup",
        nivel="facil",
        enunciado="A principal finalidade de uma rotina de backup é:",
        alternativas=(
            ("A", "aumentar a velocidade do processador."),
            ("B", "criptografar a comunicação entre navegadores."),
            ("C", "impedir a entrada de vírus na rede."),
            ("D", "compactar arquivos para liberar memória RAM."),
            ("E", "permitir a recuperação de dados em caso de falha, perda ou ataque."),
        ),
        correta="E",
        comentario=(
            "Backup é cópia de segurança para restauração. Boa prática: três cópias, em dois tipos "
            "de mídia, sendo uma fora do local (regra 3-2-1) e com teste periódico de restauração."
        ),
        armadilha="Backup não previne infecção — ele reduz o prejuízo depois dela.",
    ),
    Questao(
        id="inf-006",
        materia="informatica",
        tema="Navegadores",
        nivel="facil",
        enunciado="A presença de 'https://' no endereço de um site indica que:",
        alternativas=(
            ("A", "a comunicação entre navegador e servidor é criptografada."),
            ("B", "o site é oficial do governo."),
            ("C", "o conteúdo do site foi verificado como verdadeiro."),
            ("D", "o site está livre de vírus."),
            ("E", "o acesso é gratuito."),
        ),
        correta="A",
        comentario=(
            "HTTPS garante a criptografia do tráfego, protegendo os dados em trânsito. Não atesta "
            "idoneidade: sites fraudulentos também podem usar HTTPS."
        ),
        armadilha="'Cadeado = site confiável' é justamente o mito que a banca cobra.",
    ),
    Questao(
        id="inf-007",
        materia="informatica",
        tema="Atalhos de teclado",
        nivel="facil",
        enunciado="Em editores de texto no ambiente Windows, o atalho Ctrl + Z corresponde a:",
        alternativas=(
            ("A", "copiar."),
            ("B", "desfazer a última ação."),
            ("C", "colar."),
            ("D", "salvar o documento."),
            ("E", "localizar palavra."),
        ),
        correta="B",
        comentario=(
            "Ctrl+Z desfaz; Ctrl+C copia; Ctrl+V cola; Ctrl+X recorta. Atenção à versão em "
            "português do Office, que é a cobrada: <strong>Ctrl+B salva</strong> e "
            "<strong>Ctrl+S sublinha</strong> — o inverso do que muita gente supõe pelo inglês. "
            "Localizar é Ctrl+L; Negrito é Ctrl+N; Itálico é Ctrl+I."
        ),
        armadilha=(
            "Ctrl+Y ou Ctrl+R refazem — a banca troca desfazer por refazer. E cuidado com "
            "os atalhos do Office em português: Ctrl+S é sublinhar, não salvar."
        ),
    ),
    Questao(
        id="inf-008",
        materia="informatica",
        tema="Hardware e software",
        nivel="facil",
        enunciado="São exemplos, respectivamente, de hardware e software:",
        alternativas=(
            ("A", "navegador e antivírus."),
            ("B", "planilha eletrônica e processador."),
            ("C", "memória RAM e sistema operacional."),
            ("D", "teclado e mouse."),
            ("E", "editor de texto e aplicativo de mensagens."),
        ),
        correta="C",
        comentario=(
            "Hardware é a parte física (memória RAM); software é o conjunto de programas (sistema "
            "operacional). As demais alternativas trazem dois itens da mesma categoria ou invertidos."
        ),
        armadilha="Leia a ordem pedida: 'respectivamente' inverte o gabarito quando ignorado.",
    ),
    Questao(
        id="inf-009",
        materia="informatica",
        tema="Redes",
        nivel="medio",
        enunciado="Em uma rede de computadores, a função do endereço IP é:",
        alternativas=(
            ("A", "impedir o acesso de dispositivos externos."),
            ("B", "armazenar os arquivos do usuário na nuvem."),
            ("C", "criptografar todo o tráfego automaticamente."),
            ("D", "identificar unicamente um dispositivo na rede para permitir o envio e recebimento "
                  "de dados."),
            ("E", "converter texto em imagem."),
        ),
        correta="D",
        comentario=(
            "O IP é o endereço lógico do dispositivo na rede. Quem bloqueia acessos indevidos é o "
            "firewall; quem traduz nomes de sites em IPs é o DNS."
        ),
        armadilha="Atribuir ao IP funções de firewall ou de DNS.",
    ),
    Questao(
        id="inf-010",
        materia="informatica",
        tema="Correio eletrônico",
        nivel="medio",
        enunciado=(
            "Ao enviar um e-mail com vários destinatários, o campo Cco (cópia oculta) serve para:"
        ),
        alternativas=(
            ("A", "converter o e-mail em PDF."),
            ("B", "dar prioridade máxima à mensagem."),
            ("C", "agendar o envio da mensagem."),
            ("D", "assinar digitalmente a mensagem."),
            ("E", "enviar cópia sem que os demais destinatários vejam esse endereço."),
        ),
        correta="E",
        comentario=(
            "Cco preserva a privacidade dos endereços. É a forma correta de enviar comunicados a "
            "muitos destinatários sem expor a lista — inclusive por exigência da LGPD."
        ),
        armadilha="Confundir Cco com Cc: no Cc todos veem todos os endereços.",
    ),
    Questao(
        id="inf-011",
        materia="informatica",
        tema="Extensões de arquivo",
        nivel="facil",
        enunciado="A extensão de arquivo que indica um documento de texto formatado é:",
        alternativas=(
            ("A", ".docx"),
            ("B", ".xlsx"),
            ("C", ".pptx"),
            ("D", ".mp4"),
            ("E", ".exe"),
        ),
        correta="A",
        comentario=(
            ".docx é documento de texto; .xlsx é planilha; .pptx é apresentação; .mp4 é vídeo; "
            ".exe é executável — extensão que exige atenção redobrada quando vem por e-mail."
        ),
        armadilha="Anexos .exe e arquivos com dupla extensão (.pdf.exe) são vetores clássicos de malware.",
    ),
    Questao(
        id="inf-012",
        materia="informatica",
        tema="Boas práticas de senha",
        nivel="medio",
        enunciado="Constitui boa prática de segurança para senhas:",
        alternativas=(
            ("A", "usar a mesma senha em todos os serviços para não esquecer."),
            ("B", "utilizar senhas longas e distintas por serviço, com autenticação em duas etapas "
                  "quando disponível."),
            ("C", "anotar a senha em papel colado ao monitor."),
            ("D", "usar a data de nascimento como senha."),
            ("E", "compartilhar a senha com colegas de setor para agilizar o trabalho."),
        ),
        correta="B",
        comentario=(
            "Comprimento e unicidade são mais eficazes do que trocar caracteres por símbolos. A "
            "autenticação em duas etapas protege mesmo quando a senha vaza."
        ),
        armadilha="Reutilizar senha faz um único vazamento comprometer todas as suas contas.",
    ),

    Questao(
        id="inf-013",
        materia="informatica",
        tema="MS-Windows 10",
        nivel="facil",
        enunciado=(
            "No MS-Windows 10, a área de transferência é utilizada para:"
        ),
        alternativas=(
            ("A", "aumentar a memória RAM do equipamento."),
            ("B", "exibir os programas instalados no computador."),
            ("C", "armazenar temporariamente o conteúdo copiado ou recortado, para posterior colagem."),
            ("D", "organizar automaticamente os arquivos por data."),
            ("E", "proteger o computador contra vírus."),
        ),
        correta="C",
        comentario=(
            "A área de transferência guarda temporariamente o que foi copiado (Ctrl+C) ou "
            "recortado (Ctrl+X) até ser colado (Ctrl+V). Não se confunde com a área de trabalho, "
            "que é a tela inicial com ícones e atalhos."
        ),
        armadilha="Área de transferência x área de trabalho: nomes parecidos, funções diferentes.",
    ),
    Questao(
        id="inf-014",
        materia="informatica",
        tema="MS-Word 2016",
        nivel="medio",
        enunciado=(
            "No MS-Word 2016, o recurso que permite repetir automaticamente um texto no topo de "
            "todas as páginas do documento é:"
        ),
        alternativas=(
            ("A", "o sumário automático."),
            ("B", "a nota de rodapé."),
            ("C", "a quebra de seção."),
            ("D", "o cabeçalho."),
            ("E", "a caixa de texto."),
        ),
        correta="D",
        comentario=(
            "Cabeçalho é a área superior repetida em todas as páginas; rodapé é a inferior. "
            "Quebra de seção divide o documento em partes com formatações diferentes."
        ),
        armadilha="Confundir cabeçalho (topo) com rodapé (base) na hora da pressa.",
    ),
    Questao(
        id="inf-015",
        materia="informatica",
        tema="MS-PowerPoint 2016",
        nivel="medio",
        enunciado="No MS-PowerPoint 2016, a diferença entre animação e transição é que:",
        alternativas=(
            ("A", "animação altera o tema do slide e transição altera a fonte."),
            ("B", "animação só funciona em vídeos e transição só em imagens."),
            ("C", "transição é aplicada a textos e animação, a planilhas."),
            ("D", "as duas são a mesma coisa, com nomes diferentes."),
            ("E", "animação é o efeito aplicado a um objeto dentro do slide; transição é o efeito "
                  "de passagem de um slide para outro."),
        ),
        correta="E",
        comentario=(
            "Animação atua em elementos do slide (texto, imagem, gráfico). Transição atua na "
            "mudança entre slides. É uma das distinções mais cobradas do programa."
        ),
        armadilha="A banca troca os dois conceitos e conta com a leitura apressada.",
    ),
    Questao(
        id="inf-016",
        materia="informatica",
        tema="Google Workspace e Teams",
        nivel="facil",
        enunciado=(
            "No Google Workspace, o aplicativo destinado ao armazenamento de arquivos na nuvem é o:"
        ),
        alternativas=(
            ("A", "Drive"),
            ("B", "Meet"),
            ("C", "Gmail"),
            ("D", "Agenda"),
            ("E", "Formulários"),
        ),
        correta="A",
        comentario=(
            "Drive armazena arquivos; Gmail é e-mail; Meet é videochamada; Agenda é calendário; "
            "Formulários cria questionários. No Microsoft Teams, o equivalente de colaboração "
            "reúne chat, chamadas e edição compartilhada de arquivos do Office."
        ),
        armadilha="Saber o nome de cada aplicativo é meio ponto garantido — é decoreba barata.",
    ),
    Questao(
        id="inf-017",
        materia="informatica",
        tema="MS-Word 2016: legendas e referências",
        nivel="medio",
        enunciado=(
            "Um policial monta um relatório fotográfico no MS-Word 2016, em português, e precisa que "
            "as figuras sejam numeradas automaticamente e que essa numeração se ajuste sozinha "
            "quando uma imagem for inserida no meio do documento. O recurso adequado é:"
        ),
        alternativas=(
            ("A", "digitar o número manualmente abaixo de cada figura."),
            ("B", "Inserir Legenda, na guia Referências."),
            ("C", "Cabeçalho e Rodapé, na guia Inserir."),
            ("D", "Marcador, na guia Página Inicial."),
            ("E", "Hiperlink, na guia Inserir."),
        ),
        correta="B",
        comentario=(
            "Guia <strong>Referências → Inserir Legenda</strong> cria um rótulo numerado "
            "(Figura 1, Figura 2…) que o Word renumera sozinho a cada inclusão ou exclusão. "
            "Depois, <strong>Referência Cruzada</strong> permite citar essas figuras no texto e "
            "manter a citação atualizada."
        ),
        armadilha=(
            "Numerar à mão funciona até a primeira imagem inserida no meio — e aí toda a numeração "
            "seguinte fica errada. A banca gosta de descrever exatamente esse cenário."
        ),
    ),
    Questao(
        id="inf-018",
        materia="informatica",
        tema="MS-Outlook 2016",
        nivel="facil",
        enunciado=(
            "No MS-Outlook 2016, em sua configuração padrão, para incluir uma foto em uma mensagem "
            "nova de modo que o destinatário receba o arquivo original, o usuário deve utilizar, na "
            "guia Mensagem, o comando:"
        ),
        alternativas=(
            ("A", "Assinatura."),
            ("B", "Acompanhamento."),
            ("C", "Anexar Arquivo."),
            ("D", "Catálogo de Endereços."),
            ("E", "Verificar Nomes."),
        ),
        correta="C",
        comentario=(
            "<strong>Anexar Arquivo</strong> envia o arquivo original junto da mensagem. Colar a "
            "imagem no corpo do e-mail a incorpora como conteúdo, e o destinatário nem sempre "
            "consegue salvar o arquivo com a qualidade e os metadados originais — o que importa em "
            "registro de ocorrência."
        ),
        armadilha=(
            "Anexar não é o mesmo que inserir no corpo. A banca descreve a necessidade "
            "('receber o arquivo original') para forçar essa distinção."
        ),
    ),
    Questao(
        id="inf-019",
        materia="informatica",
        tema="Impressão e layout",
        nivel="facil",
        enunciado=(
            "Antes de imprimir um documento, o usuário quer conferir como as páginas ficarão no "
            "papel, sem gastar tinta. Nos aplicativos do MS-Office 2016, em português, isso é feito:"
        ),
        alternativas=(
            ("A", "pela guia Revisão, opção Controlar Alterações."),
            ("B", "pela guia Inserir, opção Quebra de Página."),
            ("C", "pela guia Exibir, opção Régua."),
            ("D", "pelo menu Arquivo, opção Imprimir, que exibe a visualização de impressão "
                  "(atalho Ctrl + P)."),
            ("E", "pela guia Página Inicial, opção Localizar."),
        ),
        correta="D",
        comentario=(
            "No Office 2016 a visualização de impressão foi integrada à tela "
            "<strong>Arquivo → Imprimir</strong>, junto das opções de impressora, intervalo de "
            "páginas e orientação. O atalho é Ctrl + P."
        ),
        armadilha=(
            "Quebra de página e régua alteram o layout, mas não mostram o resultado impresso. "
            "Conferir antes de imprimir é sempre a tela de impressão."
        ),
    ),
    Questao(
        id="inf-020",
        materia="informatica",
        tema="MS-PowerPoint 2016",
        nivel="medio",
        enunciado=(
            "Em uma apresentação no MS-PowerPoint 2016, o usuário quer que os itens de uma lista "
            "apareçam um a um, a cada clique, dentro do mesmo slide. Ele deve usar:"
        ),
        alternativas=(
            ("A", "a guia Transições, escolhendo um efeito de passagem."),
            ("B", "a guia Design, alterando o tema do slide."),
            ("C", "a guia Animações, aplicando um efeito de entrada aos itens."),
            ("D", "a guia Exibir, ativando o modo de classificação de slides."),
            ("E", "a guia Inserir, adicionando um vídeo."),
        ),
        correta="C",
        comentario=(
            "<strong>Animação</strong> atua sobre objetos dentro do slide — texto, imagem, gráfico. "
            "<strong>Transição</strong> atua na passagem de um slide para o outro. Para revelar "
            "itens um a um, o recurso é animação de entrada, com início 'ao clicar'."
        ),
        armadilha=(
            "Animação x transição é uma das distinções mais cobradas de PowerPoint. Dentro do "
            "slide, animação; entre slides, transição."
        ),
    ),
]
