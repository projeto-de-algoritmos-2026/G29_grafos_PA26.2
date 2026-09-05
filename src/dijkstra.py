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
# a 25 segundos de caminhada.
#
# O planejamento sugeria 0,2 por ponto, supondo tempos em minutos; como
# o mapa registra segundos, o valor equivalente seria 12. Medindo as
# rotas reais, 12 nao muda decisao nenhuma e o modo seguro vira uma
# copia do "menor tempo". Com 25 o criterio faz o que foi pedido: o
# elevador (dificuldade 5) deixa de ser escolhido so por ser 45 s mais
# rapido que a Escada Sul.
FATOR_SEGURANCA = 25


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
        grafo, origem, criterio, {destino}
    )

    if distancias[destino] == INFINITO:
        return None, None

    caminho = _reconstruir_caminho(anteriores, destino)

    return caminho, distancias[destino]


def calcular_melhor_saida(grafo, origem, criterio="tempo"):
    """
    Encontra a saida mais barata a partir da origem, sem que o usuario
    precise escolher qual delas usar.

    Nao e preciso rodar o Dijkstra uma vez para cada saida: uma unica
    busca calcula o custo ate todos os locais alcancaveis. Como a fila
    de prioridade sempre devolve o local mais barato, a primeira saida
    retirada da fila ja e a melhor, e a busca pode parar ali.

    Retorna (caminho, custo_total, saida) ou (None, None, None) quando
    nenhuma saida esta disponivel.
    """
    _validar_local(grafo, origem)
    _validar_criterio(criterio)

    saidas = [
        codigo
        for codigo in grafo.saidas()
        if not grafo.local_bloqueado(codigo)
    ]

    if not saidas or grafo.local_bloqueado(origem):
        return None, None, None

    distancias, anteriores = _executar_dijkstra(
        grafo, origem, criterio, set(saidas)
    )

    alcancaveis = [
        codigo for codigo in saidas if distancias[codigo] < INFINITO
    ]

    if not alcancaveis:
        return None, None, None

    melhor = min(alcancaveis, key=lambda codigo: distancias[codigo])
    caminho = _reconstruir_caminho(anteriores, melhor)

    return caminho, distancias[melhor], melhor


def calcular_metricas(grafo, caminho):
    """
    Soma os pesos de cada trecho da rota escolhida.

    A busca otimiza um unico criterio, mas a interface mostra os tres
    indicadores. Percorrer o caminho depois da busca garante que os
    numeros exibidos descrevem a rota realmente encontrada.

    'dificuldade_total' e o valor minimizado pelo criterio de esforco;
    'dificuldade_maxima' e o pior trecho do percurso, na escala de 1 a 5
    usada na tela.
    """
    metricas = {
        "distancia": 0,
        "tempo": 0,
        "dificuldade_total": 0,
        "dificuldade_maxima": 0,
        "trechos": 0,
    }

    for atual, proximo in zip(caminho, caminho[1:]):
        conexao = _buscar_conexao(grafo, atual, proximo)

        metricas["distancia"] += conexao["distancia"]
        metricas["tempo"] += conexao["tempo"]
        metricas["dificuldade_total"] += conexao["dificuldade"]
        metricas["dificuldade_maxima"] = max(
            metricas["dificuldade_maxima"], conexao["dificuldade"]
        )
        metricas["trechos"] += 1

    return metricas


def _buscar_conexao(grafo, origem, destino):
    """Recupera os pesos da passagem usada entre dois locais seguidos."""
    for conexao in grafo.adjacencia.get(origem, []):
        if conexao["destino"] == destino:
            return conexao

    raise ValueError(f"Nao existe conexao entre {origem} e {destino}.")


def _executar_dijkstra(grafo, origem, criterio, destinos=None):
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

        if destinos and atual in destinos:
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
