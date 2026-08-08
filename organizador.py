"""Organiza arquivos de uma pasta em subpastas por categoria/extensão."""
import argparse
import json
import logging
import shutil
import sys
from pathlib import Path

CATEGORIAS_PADRAO = {
    "Imagens": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"},
    "Planilhas": {".xls", ".xlsx", ".csv", ".ods"},
    "Apresentacoes": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Audios": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Executaveis": {".exe", ".msi", ".apk"},
}

logger = logging.getLogger("organizador")


def carregar_categorias(caminho_config: Path | None) -> dict[str, set[str]]:
    if caminho_config is None:
        return CATEGORIAS_PADRAO

    with caminho_config.open(encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return {categoria: set(extensoes) for categoria, extensoes in dados.items()}


def categoria_da_extensao(extensao: str, categorias: dict[str, set[str]] = CATEGORIAS_PADRAO) -> str:
    extensao = extensao.lower()
    for categoria, extensoes in categorias.items():
        if extensao in extensoes:
            return categoria
    return "Outros"


def destino_sem_conflito(destino: Path) -> Path:
    if not destino.exists():
        return destino

    pasta, nome, sufixo = destino.parent, destino.stem, destino.suffix
    contador = 1
    while True:
        candidato = pasta / f"{nome} ({contador}){sufixo}"
        if not candidato.exists():
            return candidato
        contador += 1


def organizar_pasta(
    origem: Path, simular: bool = False, categorias: dict[str, set[str]] = CATEGORIAS_PADRAO
) -> dict:
    resultado = {"movidos": 0, "ignorados": 0}

    for item in sorted(origem.iterdir()):
        if item.is_dir():
            continue

        categoria = categoria_da_extensao(item.suffix, categorias)
        pasta_destino = origem / categoria
        destino = destino_sem_conflito(pasta_destino / item.name)

        if simular:
            logger.info("[SIMULAÇÃO] %s -> %s/", item.name, categoria)
        else:
            pasta_destino.mkdir(exist_ok=True)
            shutil.move(str(item), str(destino))
            logger.info("Movido: %s -> %s/", item.name, categoria)

        resultado["movidos"] += 1

    return resultado


def configurar_logging(verbose: bool) -> None:
    nivel = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=nivel, format="%(message)s")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Organiza os arquivos de uma pasta em subpastas por categoria (Imagens, Documentos, etc.)."
    )
    parser.add_argument("pasta", type=Path, help="Pasta a ser organizada")
    parser.add_argument(
        "--simular", "-s", action="store_true",
        help="Mostra o que seria feito sem mover nenhum arquivo"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Log detalhado")
    parser.add_argument(
        "--config", type=Path,
        help="Arquivo JSON com categorias e extensões customizadas (substitui as categorias padrão)"
    )
    args = parser.parse_args()

    configurar_logging(args.verbose)

    if not args.pasta.is_dir():
        logger.error("Pasta não encontrada: %s", args.pasta)
        return 1

    try:
        categorias = carregar_categorias(args.config)
    except (OSError, json.JSONDecodeError) as exc:
        logger.error("Não foi possível ler o arquivo de configuração: %s", exc)
        return 1

    resultado = organizar_pasta(args.pasta, simular=args.simular, categorias=categorias)
    logger.info("Concluído. Arquivos processados: %d", resultado["movidos"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
