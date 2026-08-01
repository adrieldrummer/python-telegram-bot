"""Carimba o emblema da marca sobre um criativo já pronto.

Por que não pedir o logotipo direto ao gerador de imagem: modelo de imagem
não reproduz marca. Ele desenha *algo parecido* — proporção errada, letra
trocada, cor fora da paleta — e uma marca aproximada passa exatamente o
oposto de autoridade. O emblema real vai por cima, no arquivo, em pixel
certo.

Uso:
    python3 scripts/assinar_criativo.py entrada.jpg saida.jpg
    python3 scripts/assinar_criativo.py entrada.jpg saida.jpg --canto direita
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
EMBLEMA = RAIZ / "app" / "static" / "img" / "emblema.png"

# proporção da largura da arte ocupada pelo emblema — pequeno de propósito:
# selo de autoridade, não anunciante. Grande demais vira concorrente da manchete.
PROPORCAO = 0.11
MARGEM = 0.045


def _emblema_recortado(lado: int) -> Image.Image:
    """Tira o fundo preto do emblema para ele não virar um adesivo quadrado.

    O arquivo da marca é 100% opaco, com fundo quase preto. Colado direto
    sobre a foto ele aparece como um selo colado por cima — o olho lê como
    remendo, não como assinatura. Aqui o brilho de cada pixel vira a
    transparência: o preto some, o traço prateado fica.
    """
    emblema = Image.open(EMBLEMA).convert("RGBA").resize((lado, lado), Image.LANCZOS)
    luminancia = emblema.convert("L")
    # abaixo de 12 some por completo; acima de 60 fica cheio; no meio, degradê
    alfa = luminancia.point(lambda v: 0 if v < 12 else (255 if v > 60 else int((v - 12) * 255 / 48)))
    emblema.putalpha(alfa)
    return emblema


def assinar(entrada: Path, saida: Path, canto: str = "esquerda") -> Path:
    arte = Image.open(entrada).convert("RGB")
    lado = max(64, int(arte.width * PROPORCAO))
    emblema = _emblema_recortado(lado)

    margem = int(arte.width * MARGEM)
    x = margem if canto == "esquerda" else arte.width - lado - margem
    y = margem

    # sombra suave por baixo: sobre céu claro ou farda cinza o emblema escuro
    # simplesmente some, e aí não assina nada
    sombra = Image.new("RGBA", (lado + 24, lado + 24), (0, 0, 0, 0))
    sombra.paste((0, 0, 0, 90), (12, 12, lado + 12, lado + 12), emblema.split()[3])
    sombra = sombra.filter(__import__("PIL.ImageFilter", fromlist=["ImageFilter"]).GaussianBlur(9))

    base = arte.convert("RGBA")
    base.alpha_composite(sombra, (x - 12, y - 12))
    base.alpha_composite(emblema, (x, y))

    saida.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(saida, "JPEG", quality=92, optimize=True)
    return saida


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("entrada", type=Path)
    ap.add_argument("saida", type=Path)
    ap.add_argument("--canto", choices=("esquerda", "direita"), default="esquerda")
    args = ap.parse_args()
    caminho = assinar(args.entrada, args.saida, args.canto)
    print(f"{caminho}  ({caminho.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
