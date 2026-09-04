from grafo import Grafo
from interface import iniciar_interface

PATH_MAPA = "dados/mapa.json"

def main():
    grafo = Grafo()
    grafo.carregar_de_json(PATH_MAPA)
    iniciar_interface(grafo)

if __name__ == "__main__":
    main()
