"""Otimiza as artes geradas: recorta o logo, gera o emblema e converte capas para WebP.

Uso:  python scripts/otimizar_imagens.py
As artes originais (PNG 1k) devem estar em app/static/img/ como *-src.png.
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

    origem_logo = IMG / "logo-src.png"
    if origem_logo.exists():
        print("Logo e emblema:")
        base = Image.open(origem_logo).convert("RGBA")
        w, h = base.size
        # recorte do lockup completo (emblema + wordmark), com respiro
        logo = base.crop((int(w * 0.17), int(h * 0.14), int(w * 0.83), int(h * 0.86)))
        logo.thumbnail((720, 720), Image.LANCZOS)
        logo.save(IMG / "logo.png", optimize=True)
        print(f"  logo.png: {(IMG / 'logo.png').stat().st_size // 1024} KB")

        # emblema quadrado (só o escudo)
        emblema = base.crop((int(w * 0.38), int(h * 0.15), int(w * 0.62), int(h * 0.60)))
        lado = max(emblema.size)
        quadro = Image.new("RGBA", (lado, lado), (11, 27, 51, 255))
        quadro.paste(
            emblema, ((lado - emblema.width) // 2, (lado - emblema.height) // 2), emblema
        )
        quadro.resize((256, 256), Image.LANCZOS).save(IMG / "emblema.png", optimize=True)
        quadro.resize((64, 64), Image.LANCZOS).save(IMG / "favicon.png", optimize=True)
        print("  emblema.png + favicon.png")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
