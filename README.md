# 📌 Automação em Python — Organizador de Arquivos

> Organiza automaticamente os arquivos de uma pasta (ex: Downloads) em subpastas por categoria: Imagens, Documentos, Planilhas, Vídeos, Áudios, Compactados e mais.

![status](https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen)
![license](https://img.shields.io/badge/license-MIT-blue)

## 🖼️ Capa

<!-- Coloque aqui um print/banner principal do projeto -->
![capa do projeto](./docs/cover.png)

## 🧠 Sobre o projeto

Script de automação para resolver um problema bem comum: pastas como Downloads que acumulam arquivos de todo tipo misturados. A ferramenta varre uma pasta informada e move cada arquivo para uma subpasta de acordo com sua extensão (imagem, documento, planilha, vídeo, áudio, compactado, executável ou "Outros"), evitando sobrescrever arquivos com nomes repetidos.

## ✨ Funcionalidades

- Classificação automática por extensão em 8 categorias + "Outros"
- Modo simulação (`--simular`) que mostra o que seria movido sem alterar nada
- Prevenção de conflito de nomes (`foto.jpg` → `foto (1).jpg` se já existir)
- Log configurável (`--verbose`) de cada ação realizada
- Não mexe em subpastas já existentes, só em arquivos soltos na raiz informada

## 🖥️ Prints

| Antes | Depois |
|---|---|
| ![tela1](./docs/screenshot1.png) | ![tela2](./docs/screenshot2.png) |

## 🛠️ Tecnologias

- Python 3
- `pathlib` e `shutil` (manipulação de arquivos)
- `argparse` (interface de linha de comando)
- `logging` (registro de ações)
- `pytest` (testes automatizados)

## 📂 Estrutura do projeto

```
02-automacao-python/
├── organizador.py
├── requirements.txt
├── docs/
├── tests/
│   └── test_organizador.py
└── README.md
```

## ▶️ Como rodar localmente

```bash
# clonar o repositório
git clone https://github.com/Kashalicov/automacao-organizador.git
cd automacao-organizador

# instalar dependências
pip install -r requirements.txt

# ver o que seria feito, sem mover nada
python organizador.py "C:/Users/voce/Downloads" --simular

# organizar de verdade
python organizador.py "C:/Users/voce/Downloads"
```

## ✅ Testes

```bash
pytest tests/ -v
```

## 📚 O que eu aprendi

Nesse projeto o foco foi automatizar uma tarefa repetitiva do dia a dia com o mínimo de código necessário. O maior cuidado foi com segurança da operação: como o script move arquivos reais do usuário, implementei um modo de simulação e uma função dedicada para nunca sobrescrever um arquivo existente por engano. Também pratiquei separar a lógica pura (decidir categoria, decidir nome de destino) das operações de I/O (mover arquivo de fato), o que tornou os testes muito mais simples — a maior parte roda sem precisar simular o sistema de arquivos manualmente, usando o fixture `tmp_path` do pytest.

## 🚧 Possíveis melhorias futuras

- Arquivo de configuração para o usuário customizar categorias e extensões
- Opção de organizar por data de modificação, além de por tipo
- Modo "desfazer" a última organização

## 👤 Autor

**Júnior Rodrigues**
Coordenador de T.I. na Fundação Banco de Olhos | Estudante de Ciência da Computação
[LinkedIn](https://www.linkedin.com/feed/) · [GitHub](https://github.com/Kashalicov)
