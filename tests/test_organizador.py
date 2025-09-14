from pathlib import Path

from organizador import categoria_da_extensao, destino_sem_conflito, organizar_pasta


def test_categoria_da_extensao_imagem():
    assert categoria_da_extensao(".jpg") == "Imagens"


def test_categoria_da_extensao_case_insensitive():
    assert categoria_da_extensao(".PDF") == "Documentos"


def test_categoria_da_extensao_desconhecida():
    assert categoria_da_extensao(".xyz") == "Outros"


def test_destino_sem_conflito_sem_arquivo_existente(tmp_path: Path):
    destino = tmp_path / "foto.jpg"
    assert destino_sem_conflito(destino) == destino


def test_destino_sem_conflito_com_arquivo_existente(tmp_path: Path):
    (tmp_path / "foto.jpg").write_text("x")
    destino = destino_sem_conflito(tmp_path / "foto.jpg")
    assert destino.name == "foto (1).jpg"


def test_organizar_pasta_move_arquivos_por_categoria(tmp_path: Path):
    (tmp_path / "foto.jpg").write_text("img")
    (tmp_path / "relatorio.pdf").write_text("doc")
    (tmp_path / "musica.mp3").write_text("audio")

    resultado = organizar_pasta(tmp_path)

    assert resultado["movidos"] == 3
    assert (tmp_path / "Imagens" / "foto.jpg").exists()
    assert (tmp_path / "Documentos" / "relatorio.pdf").exists()
    assert (tmp_path / "Audios" / "musica.mp3").exists()


def test_organizar_pasta_modo_simulacao_nao_move(tmp_path: Path):
    (tmp_path / "foto.jpg").write_text("img")

    organizar_pasta(tmp_path, simular=True)

    assert (tmp_path / "foto.jpg").exists()
    assert not (tmp_path / "Imagens").exists()
