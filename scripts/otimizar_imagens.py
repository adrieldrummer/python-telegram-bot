"""Otimiza as artes da marca: converte capas para WebP e gera emblema/favicon.

Uso:  python scripts/otimizar_imagens.py

Espera os arquivos originais (PNG) em app/static/img/ com o sufixo `-src`:
    capa-*-src.png, hero-src.png, textura-src.png, emblema-src.png

Para trocar a marca por um arquivo seu, basta salvar o PNG quadrado como
`app/static/img/emblema-src.png` e rodar este script — nada no código muda.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "app" / "static" / "img"

CAPAS = [
    "capa-fase1",
    "capa-fase2",
    "capa-fase3",
    "capa-fase4",
    "capa-erros",
    "capa-questoes",
    "capa-certificado",
    "capa-manual",
    "capa-pontos",
]


def salvar_webp(img: Image.Image, destino: Path, qualidade: int = 80) -> None:
    img.convert("RGB").save(destino, "WEBP", quality=qualidade, method=6)
    print(f"  {destino.name}: {destino.stat().st_size // 1024} KB")


def main() -> int:
    if not IMG.exists():
        print("Pasta de imagens não encontrada", file=sys.stderr)
        return 1

    print("Capas (2:3 → webp):")
    for nome in CAPAS:
        origem = IMG / f"{nome}-src.png"
        if not origem.exists():
            continue
        img = Image.open(origem)
        img.thumbnail((848, 1272), Image.LANCZOS)
        salvar_webp(img, IMG / f"{nome}.webp")

    # simulados reaproveita a arte do cronômetro da fase 3
    if (IMG / "capa-fase3.webp").exists():
        Image.open(IMG / "capa-fase3.webp").save(
            IMG / "capa-simulados.webp", "WEBP", quality=80, method=6
        )
        print("  capa-simulados.webp (a partir da fase 3)")

    print("Hero e textura:")
    for nome, largura, qualidade in (("hero", 1920, 82), ("textura", 1600, 72)):
        origem = IMG / f"{nome}-src.png"
        if not origem.exists():
            continue
        img = Image.open(origem)
        if img.width > largura:
            img = img.resize((largura, round(img.height * largura / img.width)), Image.LANCZOS)
        salvar_webp(img, IMG / f"{nome}.webp", qualidade)

    origem_emblema = IMG / "emblema-src.png"
    if origem_emblema.exists():
        print("Emblema e favicon:")
        base = Image.open(origem_emblema).convert("RGBA")
        lado = min(base.size)
        esquerda = (base.width - lado) // 2
        topo = (base.height - lado) // 2
        quadrado = base.crop((esquerda, topo, esquerda + lado, topo + lado))
        quadrado.resize((512, 512), Image.LANCZOS).save(IMG / "emblema.png", optimize=True)
        quadrado.resize((64, 64), Image.LANCZOS).save(IMG / "favicon.png", optimize=True)
        print("  emblema.png (512) + favicon.png (64)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
