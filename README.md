# Sistema de Evacuação de Emergência com Dijkstra

## Alunos

| Matrícula | Aluno |
| -- | -- |
| 211041105 | Bruna de Lima Santos |
| 212005453 | Pedro Luciano de Azevedo |

## Sobre

Trabalho 1 para a disciplina de Projeto de Algoritmos do 2º semestre de 2026. O sistema
calcula rotas de evacuação de emergência em um prédio representado como um grafo
ponderado.

### Problema

Em uma emergência, o caminho mais próximo pode estar bloqueado ou não ser o
mais adequado. O sistema deve encontrar uma rota disponível entre a localização
de origem e uma saída do prédio.

### Solução

O usuário informa a origem, a saída, o critério de busca e os locais
indisponíveis (bloqueios no caminho). O sistema apresenta a rota encontrada ou
informa quando não existe um caminho possível.

### Algoritmo

O menor caminho é calculado com o **algoritmo de Dijkstra** e uma fila de
prioridade **heap**. A busca ignora conexões bloqueadas e pode priorizar:

- **Tempo:** medido em segundos;
- **Distância:** medida em metros;
- **Dificuldade:** representada por uma escala de 1 a 5.

### Mapa

O [mapa](./dados/mapa.json) possui 17 locais e 20 conexões bidirecionais. Os locais são os vértices
do grafo, enquanto as passagens são as arestas com os pesos utilizados pelo
algoritmo.

### Complexidade

## Screenshots

## Apresentação do trabalho: [assistir ao vídeo]()

## Instalação

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

## Uso
