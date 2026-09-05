"""
contexto.py

Deixa os modulos de 'src' visiveis para os testes e carrega o mapa real
do projeto. Todos os arquivos de teste comecam importando daqui.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_MAPA = RAIZ / "dados" / "mapa.json"

if str(RAIZ / "src") not in sys.path:
    sys.path.insert(0, str(RAIZ / "src"))

from grafo import Grafo  # noqa: E402


def criar_grafo():
    """Carrega uma copia limpa do mapa do predio para cada teste."""
    grafo = Grafo()
    grafo.carregar_de_json(CAMINHO_MAPA)

    return grafo
