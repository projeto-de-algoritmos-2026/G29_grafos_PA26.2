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
- **Dificuldade:** representada por uma escala de 1 a 5;
- **Evacuação segura:** combina os dois anteriores com o custo
  `tempo + dificuldade × 25`, para que um trecho de risco não seja
  escolhido só por economizar alguns segundos.

### Mapa

O [mapa](./dados/mapa.json) possui 17 locais e 20 conexões bidirecionais. Os locais são os vértices
do grafo, enquanto as passagens são as arestas com os pesos utilizados pelo
algoritmo.

### Complexidade

A busca usa uma **lista de adjacência**: cada local guarda apenas as
passagens que existem. Com `V` locais e `E` passagens, o mapa ocupa
`O(V + E)` — bem menos que uma matriz `V × V`, que seria quase toda
vazia neste prédio.

A **fila de prioridade** é o que dá a complexidade final. Ela devolve
sempre o local de menor custo conhecido ainda não visitado; quando um
local sai da fila, seu custo já é definitivo, porque qualquer outro
caminho até ele passaria por um local mais caro e todos os pesos são
positivos. É por isso que o algoritmo nunca precisa revisitar decisões.

Não usamos *decrease-key*: quando um custo melhora, o local é inserido
de novo na fila e as entradas antigas são descartadas na retirada, pelo
conjunto de visitados. A fila chega a ter `O(E)` entradas, mas cada
inserção e cada retirada continua custando `O(log V)`.

| Operação | Complexidade |
| -- | -- |
| Carregar o mapa | `O(V + E)` |
| Bloquear ou liberar um local | `O(1)` |
| Bloquear ou liberar uma passagem | `O(grau do local)` |
| Listar os vizinhos livres | `O(grau do local)` |
| **Dijkstra com fila de prioridade** | **`O((V + E) log V)`** |
| Reconstruir a rota | `O(V)` |
| Somar as métricas da rota | `O(V + E)` |


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

### Testes

```bash
python -m unittest discover testes
```

### Demonstração no terminal

Roda os cenários de emergência sem abrir a interface:

```bash
python src/demo_terminal.py
```

## Uso
