"""
grafo.py

Representa o predio como um grafo nao direcionado usando lista de
adjacencia: para cada local, guarda apenas as conexoes existentes.

Cada conexao mantem: destino, distancia, tempo, dificuldade e estado de
bloqueio. Um bloqueio nao remove a conexao do grafo, apenas a marca como
indisponivel -- o Dijkstra deve ignora-la ao calcular rotas.

Responsabilidade: Pessoa 1 (algoritmos e dados).
"""

import json


class Grafo:
    """Grafo nao direcionado do predio, representado por lista de adjacencia."""

    def __init__(self):
        # TODO: estrutura de adjacencia, por exemplo:
        # {"S101": [{"destino": "CA", "distancia": 12, "tempo": 0.3,
        #            "dificuldade": 1, "bloqueado": False}, ...], ...}
        self.adjacencia = {}

    def carregar_de_json(self, caminho_arquivo):
        """Carrega locais e conexoes a partir de um arquivo mapa.json."""
        # TODO: ler o JSON, criar os locais com adicionar_local() e as
        # conexoes com adicionar_conexao().
        raise NotImplementedError

    def adicionar_local(self, codigo, nome, tipo):
        """Adiciona um novo local (vertice) ao grafo."""
        # TODO
        raise NotImplementedError

    def adicionar_conexao(self, origem, destino, distancia, tempo, dificuldade):
        """Cria uma conexao (aresta) nos dois sentidos entre dois locais."""
        # TODO: ao adicionar, criar as duas direcoes automaticamente.
        raise NotImplementedError

    def bloquear_conexao(self, origem, destino):
        """Marca uma conexao como indisponivel, sem remove-la do grafo."""
        # TODO
        raise NotImplementedError

    def desbloquear_conexao(self, origem, destino):
        """Remove o bloqueio de uma conexao."""
        # TODO
        raise NotImplementedError

    def vizinhos(self, local):
        """Retorna as conexoes disponiveis (nao bloqueadas) de um local."""
        # TODO
        raise NotImplementedError
