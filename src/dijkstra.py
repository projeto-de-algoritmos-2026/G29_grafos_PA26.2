"""
dijkstra.py

Implementa o algoritmo de Dijkstra com fila de prioridade (heapq) para
encontrar o menor custo acumulado entre a origem e o destino. Como todos
os custos sao positivos, o algoritmo e adequado para o problema.

Responsabilidade: Pessoa 1 (algoritmos e dados).
"""

import heapq


def calcular_rota(grafo, origem, destino, criterio="tempo"):
    """
    Calcula a rota de menor custo entre origem e destino segundo o
    criterio informado ("tempo", "distancia" ou "dificuldade").

    Retorna uma tupla (caminho, custo_total), onde caminho e a lista de
    locais do trajeto, ou (None, None) caso nao exista rota disponivel
    (por exemplo, todos os caminhos bloqueados).

    Passos previstos:
    1. Definir custo da origem como 0 e de todos os demais como infinito.
    2. Inserir a origem na fila de prioridade (custo_total, local).
    3. Remover o local de menor custo conhecido e examinar suas conexoes.
    4. Ignorar conexoes bloqueadas; para as demais, calcular o novo custo.
    5. Se o novo custo for menor, atualizar distancia, anterior e fila.
    6. Ao chegar ao destino, reconstruir o caminho usando 'anteriores'.
    """
    # TODO: implementar o algoritmo acima usando heapq.
    raise NotImplementedError
