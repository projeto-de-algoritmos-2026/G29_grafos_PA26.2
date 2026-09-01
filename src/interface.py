"""
interface.py

Interface do usuario: seletores de origem/destino e criterio de rota,
lista de bloqueios ativos, botao de calculo e exibicao do resultado
(rota, tempo, distancia, dificuldade) ou da mensagem de rota indisponivel.

Responsabilidade: Pessoa 2 (interface e experiencia).
"""


def iniciar_interface(grafo):
    """
    Inicializa a janela/tela principal e conecta as acoes da interface
    aos modulos de grafo e dijkstra.

    Previsto:
    - seletor de local atual e de saida (ou "saida mais rapida");
    - seletor de criterio de rota (tempo, distancia, dificuldade);
    - lista de bloqueios ativos (ativar/desativar);
    - botao "CALCULAR ROTA";
    - exibicao da rota, tempo estimado, distancia total e dificuldade;
    - mensagem clara quando nao houver passagem segura.
    """
    # TODO: implementar interface (ex.: tkinter).
    raise NotImplementedError
