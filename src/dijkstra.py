"""
dijkstra.py

Implementa o algoritmo de Dijkstra com fila de prioridade (heapq) para
encontrar o menor custo acumulado entre a origem e o destino. Como todos
os custos sao positivos, o algoritmo e adequado para o problema.

Responsabilidade: Pessoa 1 (algoritmos e dados).
"""

import heapq

INFINITO = float("inf")

# O algoritmo e o mesmo nos quatro casos: muda apenas a funcao que
# devolve o peso da aresta.
CRITERIOS = ("tempo", "distancia", "dificuldade", "seguro")

# Modo "evacuacao segura": cada ponto de dificuldade custa o equivalente
# a 12 segundos de caminhada. O planejamento sugeria 0,2 minuto por
# ponto; como o mapa registra o tempo em segundos, 0,2 min = 12 s. Assim
# um trecho cansativo deixa de ser escolhido so por ser alguns segundos
# mais rapido.
FATOR_SEGURANCA = 12


def peso_da_conexao(conexao, criterio):
    """
    Devolve o custo de atravessar uma conexao segundo o criterio.

    "tempo" usa segundos, "distancia" usa metros e "dificuldade" usa a
    escala de esforco de 1 a 5. "seguro" combina tempo e dificuldade.
    """
    if criterio == "seguro":
        return conexao["tempo"] + conexao["dificuldade"] * FATOR_SEGURANCA

    return conexao[criterio]


def calcular_rota(grafo, origem, destino, criterio="tempo"):
    """
    Calcula a rota de menor custo entre origem e destino segundo o
    criterio informado ("tempo", "distancia", "dificuldade" ou "seguro").

    Retorna uma tupla (caminho, custo_total), onde caminho e a lista de
    locais do trajeto, ou (None, None) caso nao exista rota disponivel
    (por exemplo, todos os caminhos bloqueados).
    """
    _validar_local(grafo, origem)
    _validar_local(grafo, destino)
    _validar_criterio(criterio)

    if grafo.local_bloqueado(origem) or grafo.local_bloqueado(destino):
        return None, None

    distancias, anteriores = _executar_dijkstra(
        grafo, origem, criterio, destino
    )

    if distancias[destino] == INFINITO:
        return None, None

    caminho = _reconstruir_caminho(anteriores, destino)

    return caminho, distancias[destino]


def _executar_dijkstra(grafo, origem, criterio, destino=None):
    """
    Percorre o grafo a partir da origem acumulando o menor custo conhecido.

    A fila de prioridade guarda pares (custo_total, local) e devolve
    sempre o local mais barato ainda nao visitado. Quando esse local sai
    da fila, seu custo ja e definitivo: qualquer outro caminho ate ele
    passaria por um local mais caro e, como todos os pesos sao positivos,
    so ficaria pior.

    Retorna (distancias, anteriores). 'distancias' guarda o menor custo
    conhecido ate cada local; 'anteriores' guarda o local que precede
    cada um deles, o que permite reconstruir a rota no final.
    """
    distancias = {codigo: INFINITO for codigo in grafo.locais}
    anteriores = {codigo: None for codigo in grafo.locais}
    visitados = set()

    distancias[origem] = 0
    fila = [(0, origem)]

    while fila:
        custo_atual, atual = heapq.heappop(fila)

        # O mesmo local pode ter entrado na fila mais de uma vez, com
        # custos diferentes. So a primeira retirada interessa.
        if atual in visitados:
            continue

        visitados.add(atual)

        if atual == destino:
            break

        for conexao in grafo.vizinhos(atual):
            vizinho = conexao["destino"]
            novo_custo = custo_atual + peso_da_conexao(conexao, criterio)

            if novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                anteriores[vizinho] = atual
                heapq.heappush(fila, (novo_custo, vizinho))

    return distancias, anteriores


def _reconstruir_caminho(anteriores, destino):
    """Refaz a rota do destino ate a origem e devolve na ordem correta."""
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse()

    return caminho


def _validar_local(grafo, codigo):
    """Garante que o local existe no mapa antes de iniciar a busca."""
    if codigo not in grafo.locais:
        raise ValueError(f"Local desconhecido: {codigo}.")


def _validar_criterio(criterio):
    """Garante que o criterio de busca e um dos previstos."""
    if criterio not in CRITERIOS:
        validos = ", ".join(CRITERIOS)
        raise ValueError(
            f"Criterio desconhecido: {criterio}. Use um destes: {validos}."
        )
