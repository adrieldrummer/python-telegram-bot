"""Monta os criativos dos anúncios a partir das artes que já existem no site.

Por que gerar em vez de reaproveitar as capas direto: o Meta pede JPEG ou PNG
(as capas do site são WebP) e o feed corta tudo o que não for 4:5. Uma capa
1200×675 subida como está aparece com tarja preta em cima e embaixo, e o
anúncio perde metade da área útil no celular — que é onde o público inteiro
deste produto está.

Cada criativo é uma arte do site recortada em 1080×1350, escurecida na base
com um degradê e com a manchete do ângulo por cima. O degradê não é enfeite:
sem ele o texto branco some quando a foto tem céu claro ou farda bege.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "app" / "static" / "img"
DESTINO = ORIGEM / "anuncios"

LARGURA, ALTURA = 1080, 1350
AREIA = (232, 226, 214)
DOURADO = (198, 160, 74)

FONTE_TITULO = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONTE_APOIO = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# (arquivo de saída, capa de origem, chapéu, manchete, rodapé)
CRIATIVOS = (
    ("a1-prazo", "capa-prova.webp", "PROVA: 20 DE SETEMBRO",
     "Ainda dá tempo\nde chegar pronto", "O edital inteiro em 7 dias"),
    ("a2-edital", "capa-manual.webp", "EDITAL PM-SP 2026",
     "Pare de estudar\na matéria errada", "60 questões. Cada uma tem um peso."),
    ("a3-prova2025", "capa-simulados.webp", "BASEADO NA PROVA DE 2025",
     "Treine no formato\nda VUNESP", "Simulados com a proporção real"),
    ("a4-celular", "capa-celular.webp", "FEITO PARA O CELULAR",
     "Não tem computador?\nNão precisa", "Funciona até quando a internet cai"),
    ("a5-diagnostico", "capa-questoes.webp", "DIA 1 — DIAGNÓSTICO",
     "Descubra onde você\nestá perdendo ponto", "20 questões e seu mapa de prioridades"),
    ("a6-erro", "capa-erros.webp", "CADERNO DE ERROS",
     "Pare de errar\na mesma questão", "Revisão espaçada, automática"),
    ("a7-preco", "capa-farda.webp", "A PARTIR DE R$ 47/MÊS",
     "Preparação de verdade\npor R$ 47", "Acesso imediato após o pagamento"),
    ("a8-concorrencia", "capa-formatura.webp", "2.000 VAGAS",
     "A maioria não vai\nestudar direito", "Método vale mais que talento"),
)


def recortar(imagem: Image.Image) -> Image.Image:
    """Preenche 1080×1350 sem distorcer, cortando o excesso pelo centro."""
    proporcao = max(LARGURA / imagem.width, ALTURA / imagem.height)
    novo = imagem.resize(
        (round(imagem.width * proporcao), round(imagem.height * proporcao)), Image.LANCZOS
    )
    esquerda = (novo.width - LARGURA) // 2
    # corta mais de baixo que de cima: em foto de pessoa, o rosto está no terço
    # superior, e centralizar corta a cabeça
    topo = int((novo.height - ALTURA) * 0.35)
    return novo.crop((esquerda, topo, esquerda + LARGURA, topo + ALTURA))


def degrade(altura_util: int) -> Image.Image:
    """Véu escuro que sobe da base — dá contraste ao texto sobre qualquer foto."""
    mascara = Image.new("L", (1, ALTURA), 0)
    pixels = mascara.load()
    inicio = ALTURA - altura_util
    for y in range(inicio, ALTURA):
        avanco = (y - inicio) / altura_util
        pixels[0, y] = int(245 * (avanco ** 0.85))
    return Image.new("RGB", (LARGURA, ALTURA), (8, 12, 18)), mascara.resize((LARGURA, ALTURA))


def quebrar(texto: str, fonte, desenho, largura_max: int) -> list[str]:
    linhas: list[str] = []
    for paragrafo in texto.split("\n"):
        atual = ""
        for palavra in paragrafo.split():
            teste = f"{atual} {palavra}".strip()
            if desenho.textlength(teste, font=fonte) <= largura_max:
                atual = teste
            else:
                if atual:
                    linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def montar(saida: str, capa: str, chapeu: str, manchete: str, rodape: str) -> Path:
    origem = ORIGEM / capa
    base = recortar(Image.open(origem).convert("RGB"))

    veu, mascara = degrade(int(ALTURA * 0.62))
    base = Image.composite(veu, base, mascara)

    desenho = ImageDraw.Draw(base)
    margem = 78
    largura_util = LARGURA - margem * 2

    fonte_manchete = ImageFont.truetype(FONTE_TITULO, 82)
    fonte_chapeu = ImageFont.truetype(FONTE_TITULO, 34)
    fonte_rodape = ImageFont.truetype(FONTE_APOIO, 38)

    linhas = quebrar(manchete, fonte_manchete, desenho, largura_util)
    altura_manchete = len(linhas) * 96

    y = ALTURA - margem - 150 - altura_manchete

    # chapéu com traço dourado à esquerda: dá hierarquia sem pedir mais espaço
    desenho.rectangle([margem, y - 58, margem + 8, y - 18], fill=DOURADO)
    desenho.text((margem + 26, y - 62), chapeu, font=fonte_chapeu, fill=DOURADO)

    for linha in linhas:
        desenho.text((margem, y), linha, font=fonte_manchete, fill=AREIA)
        y += 96

    y += 22
    desenho.text((margem, y), rodape, font=fonte_rodape, fill=(196, 200, 208))

    y += 74
    desenho.text((margem, y), "opaprova.com", font=ImageFont.truetype(FONTE_TITULO, 40),
                 fill=DOURADO)

    DESTINO.mkdir(parents=True, exist_ok=True)
    caminho = DESTINO / f"{saida}.jpg"
    base.save(caminho, "JPEG", quality=88, optimize=True)
    return caminho


def main() -> int:
    for saida, capa, chapeu, manchete, rodape in CRIATIVOS:
        if not (ORIGEM / capa).exists():
            print(f"  !! capa ausente: {capa}")
            continue
        caminho = montar(saida, capa, chapeu, manchete, rodape)
        print(f"  {caminho.relative_to(RAIZ)}  {caminho.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
