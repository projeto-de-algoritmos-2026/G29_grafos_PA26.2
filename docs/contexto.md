# Contexto do projeto

## O problema

Em prédios como universidades, hospitais, shoppings ou prédios comerciais, uma
pessoa em situação de emergência precisa encontrar rapidamente uma rota até
uma saída segura. Nem sempre o caminho mais óbvio está disponível: trechos
podem estar bloqueados, congestionados, interditados, mais longos que o
necessário ou temporariamente indisponíveis.

A pergunta que o sistema precisa responder é: **qual é a melhor rota entre o
local onde a pessoa está e uma saída segura?**

## Objetivo

Construir uma aplicação que encontre a melhor rota de saída em um prédio
fictício, recalculando o caminho quando houver bloqueios. O sistema recebe:

- o local de origem;
- a saída desejada;
- os bloqueios ativos no momento;
- o critério de rota (menor tempo, menor distância, menor dificuldade).

E devolve: a rota detalhada, o tempo estimado, a distância total, a
dificuldade e uma mensagem clara quando não houver passagem segura.

## Algoritmo central

Dijkstra com fila de prioridade (`heapq`), usando pesos positivos. Como todos
os custos são positivos, o algoritmo é adequado para o problema. A cada
aresta ignorada por estar bloqueada, o Dijkstra simplesmente pula para a
próxima opção — sem precisar recriar o grafo.

## Critérios de rota

O algoritmo é o mesmo nos três casos; muda apenas a função que retorna o peso
da aresta:

- **Menor tempo** — usa tempo (minutos) como peso;
- **Menor distância** — usa distância (metros) como peso;
- **Menor dificuldade** — usa a escala de esforço (1 a 5) como peso.

Modo opcional (evacuação segura): `custo = tempo + (dificuldade * fator_seguranca)`,
para evitar rotas rápidas porém arriscadas.

## O mapa

Um prédio totalmente fictício, modelado como grafo não direcionado: em
condições normais toda conexão pode ser percorrida nos dois sentidos. Cada
local é um vértice (sala, corredor, escada, elevador, hall, porta ou saída) e
cada passagem é uma aresta com três pesos (distância, tempo, dificuldade) e
um estado de bloqueio. Um bloqueio marca a aresta como indisponível sem
apagá-la do grafo, permitindo ativar/desfazer simulações livremente.

Tamanho alvo: por volta de 15 a 25 locais e 25 a 40 conexões — grande o
suficiente para mostrar escolhas reais de rota, sem tornar a implementação
arriscada para o prazo do trabalho.

## Arquitetura prevista

| Arquivo | Responsabilidade |
|---|---|
| `dados/mapa.json` | Locais, conexões e pesos do prédio fictício |
| `src/grafo.py` | Lista de adjacência, carga de dados e bloqueios |
| `src/dijkstra.py` | Fila de prioridade, cálculo de custo e reconstrução da rota |
| `src/interface.py` | Seletores, bloqueios, botão e exibição de resultados |
| `src/main.py` | Inicialização e integração dos módulos |
| `testes/` | Casos normais, bloqueios, critérios e ausência de rota |

## Casos de teste planejados

- Rota normal, sem bloqueios;
- Bloqueio de um corredor, com rota alternativa;
- Escada indisponível, forçando outra escada ou o elevador;
- Saída bloqueada, com seleção automática da outra saída;
- Ausência de rota segura, com mensagem clara de impossibilidade.

## Status atual

Etapa inicial (estrutura do repositório e definição do mapa). A lógica de
`grafo.py`, `dijkstra.py` e `interface.py` ainda será implementada em commits
seguintes — ver [COMO_EXECUTAR.md](COMO_EXECUTAR.md) para o estado do que já
roda.
