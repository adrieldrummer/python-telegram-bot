"""Gera os banners do checkout da Cakto.

O banner do checkout não é decoração: é a última tela antes do pagamento, o
lugar onde a pessoa desiste. Por isso ele não repete a chamada da página de
vendas — ela já foi convencida. Ele responde às três dúvidas de quem está com o
cartão na mão: o que eu recebo, quando eu recebo, e o que acontece se eu me
arrepender.

Uso:  python scripts/gerar_banners_checkout.py

Saída em app/static/img/checkout/ — arquivos prontos para subir no construtor
de checkout, em versão desktop e celular.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

IMG = RAIZ / "app" / "static" / "img"
SAIDA = IMG / "checkout"

# paleta da marca
PRETO = (5, 5, 5)
BRANCO = (255, 255, 255)
CLARO = (230, 232, 236)
SUAVE = (167, 172, 182)
AZUL = (10, 92, 255)
ACO = (200, 204, 212)

FONTES = Path("/usr/share/fonts/truetype/dejavu")


def fonte(tamanho: int, negrito: bool = False) -> ImageFont.FreeTypeFont:
    nome = "DejaVuSans-Bold.ttf" if negrito else "DejaVuSans.ttf"
    return ImageFont.truetype(str(FONTES / nome), tamanho)


def largura(desenho: ImageDraw.ImageDraw, texto: str, f) -> int:
    return desenho.textbbox((0, 0), texto, font=f)[2]


def fundo(dimensoes: tuple[int, int], origem: Path, escurecer: float = 0.72) -> Image.Image:
    """Recorta a arte de fundo no formato pedido e escurece para o texto ler."""
    largura_alvo, altura_alvo = dimensoes
    base = Image.open(origem).convert("RGB")

    proporcao = max(largura_alvo / base.width, altura_alvo / base.height)
    nova = (int(base.width * proporcao) + 1, int(base.height * proporcao) + 1)
    base = base.resize(nova, Image.LANCZOS)
    esq = (base.width - largura_alvo) // 2
    topo = int((base.height - altura_alvo) * 0.35)   # privilegia o terço superior
    base = base.crop((esq, topo, esq + largura_alvo, topo + altura_alvo))

    # leve desfoque: o fundo não pode competir com o texto na hora do pagamento
    base = base.filter(ImageFilter.GaussianBlur(1.4))
    veu = Image.new("RGB", dimensoes, PRETO)
    return Image.blend(base, veu, escurecer)


def barra_azul(img: Image.Image, altura: int = 6) -> None:
    ImageDraw.Draw(img).rectangle([0, 0, img.width, altura], fill=AZUL)


def emblema(img: Image.Image, caixa: int, posicao: tuple[int, int]) -> None:
    """Cola o emblema recortado em círculo.

    O PNG da marca vem com fundo preto sólido, sem transparência: colado direto
    vira um quadrado sobre a foto. O recorte circular resolve e ainda combina
    com a mira do próprio emblema.
    """
    marca = Image.open(IMG / "emblema.png").convert("RGBA").resize((caixa, caixa), Image.LANCZOS)

    mascara = Image.new("L", (caixa * 4, caixa * 4), 0)
    ImageDraw.Draw(mascara).ellipse([0, 0, caixa * 4 - 1, caixa * 4 - 1], fill=255)
    mascara = mascara.resize((caixa, caixa), Image.LANCZOS)  # suaviza a borda
    marca.putalpha(mascara)

    # anel fino para destacar do fundo escuro
    anel = Image.new("RGBA", (caixa + 6, caixa + 6), (0, 0, 0, 0))
    ImageDraw.Draw(anel).ellipse(
        [0, 0, caixa + 5, caixa + 5], outline=(255, 255, 255, 46), width=2
    )
    img.paste(marca, posicao, marca)
    img.paste(anel, (posicao[0] - 3, posicao[1] - 3), anel)


def selo(desenho, x, y, texto, f, cor_texto=CLARO, cor_borda=None, respiro=(14, 8)):
    """Etiqueta arredondada; devolve a largura ocupada."""
    px, py = respiro
    larg = largura(desenho, texto, f) + px * 2
    alt = desenho.textbbox((0, 0), texto, font=f)[3] + py * 2
    desenho.rounded_rectangle(
        [x, y, x + larg, y + alt], radius=alt // 2,
        fill=(18, 18, 24), outline=cor_borda or (60, 60, 72), width=1,
    )
    desenho.text((x + px, y + py - 1), texto, font=f, fill=cor_texto)
    return larg


def banner_desktop() -> Path:
    L, A = 1200, 300
    img = fundo((L, A), IMG / "hero-farda.webp", escurecer=0.74)
    d = ImageDraw.Draw(img)
    barra_azul(img)

    emblema(img, 96, (56, 96))

    x = 180
    d.text((x, 92), "OPERAÇÃO ", font=fonte(34, True), fill=ACO)
    deslocamento = largura(d, "OPERAÇÃO ", fonte(34, True))
    d.text((x + deslocamento, 92), "APROVAÇÃO", font=fonte(34, True), fill=AZUL)

    d.text(
        (x, 140),
        "Acesso liberado por e-mail assim que o pagamento é aprovado.",
        font=fonte(19), fill=CLARO,
    )
    d.text(
        (x, 170),
        "Você estuda pelo celular, no computador ou instalando como aplicativo.",
        font=fonte(17), fill=SUAVE,
    )

    f = fonte(15, True)
    cx = x
    for texto in ("✓ 7 dias de trilha", "✓ 112 questões comentadas", "✓ Cancele quando quiser"):
        cx += selo(d, cx, 214, texto, f) + 10

    return salvar(img, "banner-checkout-desktop")


def banner_celular() -> Path:
    L, A = 800, 420
    img = fundo((L, A), IMG / "hero-farda.webp", escurecer=0.76)
    d = ImageDraw.Draw(img)
    barra_azul(img, 8)

    emblema(img, 92, ((L - 92) // 2, 44))

    titulo_a, titulo_b = "OPERAÇÃO ", "APROVAÇÃO"
    f_t = fonte(38, True)
    total = largura(d, titulo_a, f_t) + largura(d, titulo_b, f_t)
    x = (L - total) // 2
    d.text((x, 158), titulo_a, font=f_t, fill=ACO)
    d.text((x + largura(d, titulo_a, f_t), 158), titulo_b, font=f_t, fill=AZUL)

    linhas = [
        ("Acesso liberado por e-mail", fonte(23, True), CLARO, 214),
        ("assim que o pagamento é aprovado.", fonte(21), SUAVE, 248),
    ]
    for texto, f, cor, y in linhas:
        d.text(((L - largura(d, texto, f)) // 2, y), texto, font=f, fill=cor)

    f = fonte(16, True)
    itens = ("✓ Trilha de 7 dias", "✓ 112 questões", "✓ Sem fidelidade")
    larguras = [largura(d, t, f) + 28 for t in itens]
    cx = (L - sum(larguras) - 10 * (len(itens) - 1)) // 2
    for texto in itens:
        cx += selo(d, cx, 316, texto, f) + 10

    return salvar(img, "banner-checkout-celular")


def banner_topo_fino() -> Path:
    """Faixa estreita, para quem preferir um banner discreto acima do formulário."""
    L, A = 1200, 120
    img = Image.new("RGB", (L, A), (10, 10, 14))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, L, 4], fill=AZUL)
    emblema(img, 56, (40, 32))

    d.text((116, 34), "OPERAÇÃO ", font=fonte(22, True), fill=ACO)
    d.text((116 + largura(d, "OPERAÇÃO ", fonte(22, True)), 34), "APROVAÇÃO",
           font=fonte(22, True), fill=AZUL)
    d.text((116, 66), "Edital PM-SP 2026 explicado em 7 dias · acesso imediato por e-mail",
           font=fonte(16), fill=SUAVE)

    texto = "PAGAMENTO SEGURO"
    f = fonte(14, True)
    d.text((L - largura(d, texto, f) - 40, 52), texto, font=f, fill=(120, 126, 138))
    return salvar(img, "banner-checkout-faixa")


def salvar(img: Image.Image, nome: str) -> Path:
    SAIDA.mkdir(parents=True, exist_ok=True)
    destino = SAIDA / f"{nome}.png"
    img.save(destino, "PNG", optimize=True)
    # o construtor da Cakto aceita JPG e costuma carregar mais rápido
    img.save(SAIDA / f"{nome}.jpg", "JPEG", quality=88, optimize=True)
    return destino


def main() -> int:
    for gerar in (banner_desktop, banner_celular, banner_topo_fino):
        caminho = gerar()
        tamanho = caminho.stat().st_size // 1024
        with Image.open(caminho) as im:
            print(f"  {caminho.name:32} {im.width}x{im.height}  {tamanho} KB")
    print(f"\nArquivos em {SAIDA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
