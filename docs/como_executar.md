# Como executar o projeto

## Pré-requisitos

Antes de começar, certifique-se de ter:

- Python 3.10 ou superior
- Git

Após isso, clone o repositório, acesse a pasta do projeto e siga as instruções
abaixo.

### 1) Instale as dependências do sistema

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
```

### 2) Crie e ative o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Instale as dependências do projeto

```bash
python -m pip install -r requirements.txt
```

## Execução

Na raiz do projeto, ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Em seguida, execute:

```bash
python src/main.py
```

## Testes

Para executar os testes automatizados:

```bash
python -m unittest discover testes
```
