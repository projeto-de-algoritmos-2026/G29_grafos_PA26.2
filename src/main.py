"""
main.py

Ponto de entrada do sistema: inicializa o grafo a partir do mapa.json e
integra os modulos de grafo, dijkstra e interface.
"""

from grafo import Grafo

CAMINHO_MAPA = "dados/mapa.json"


def main():
    grafo = Grafo()
    # TODO: grafo.carregar_de_json(CAMINHO_MAPA) assim que estiver implementado.
    # TODO: iniciar_interface(grafo) assim que a interface estiver pronta.
    print("Sistema de Evacuacao de Emergencia - em desenvolvimento.")


if __name__ == "__main__":
    main()
