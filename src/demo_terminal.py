"""
demo_terminal.py

Roda os cenarios de emergencia no terminal, sem depender da interface.
Serve para conferir as rotas durante o desenvolvimento e para mostrar o
algoritmo funcionando caso a demonstracao grafica falhe.

Execucao:

    python src/demo_terminal.py

"""

from pathlib import Path

import rotas
from grafo import Grafo

CAMINHO_MAPA = Path(__file__).resolve().parent.parent / "dados" / "mapa.json"

LARGURA = 68

CENARIOS = [
    {
        "titulo": "1. Rota normal, sem nenhum bloqueio",
        "origem": "Sala 203",
        "saida": "Saída Principal",
        "criterio": "Menor tempo",
        "bloqueios": [],
    },
    {
        "titulo": "2. Incêndio no elevador: a rota é recalculada",
        "origem": "Sala 203",
        "saida": "Saída Principal",
        "criterio": "Menor tempo",
        "bloqueios": ["Elevador"],
    },
    {
        "titulo": "3. Escada Norte também indisponível: sobra a Escada Sul",
        "origem": "Sala 203",
        "saida": "Saída Principal",
        "criterio": "Menor tempo",
        "bloqueios": ["Elevador", "Escada Norte"],
    },
    {
        "titulo": "4. Saída Principal bloqueada: a outra saída é escolhida",
        "origem": "Sala 203",
        "saida": "Saída mais próxima",
        "criterio": "Menor tempo",
        "bloqueios": ["Saída Principal"],
    },
    {
        "titulo": "5. Corredor B interditado: a Sala 202 fica isolada",
        "origem": "Sala 202",
        "saida": "Saída Principal",
        "criterio": "Menor tempo",
        "bloqueios": ["Corredor B"],
    },
    {
        "titulo": "6. Sem rota segura: nenhuma descida disponível",
        "origem": "Sala 203",
        "saida": "Saída mais próxima",
        "criterio": "Menor tempo",
        "bloqueios": ["Escada Norte", "Escada Sul", "Elevador"],
    },
]

COMPARACAO = [
    "Menor tempo",
    "Menor distância",
    "Menor dificuldade",
    "Evacuação segura",
]


def mostrar_cenario(grafo, titulo, origem, saida, criterio, bloqueios):
    """Executa um cenario e imprime a rota com as tres metricas."""
    resultado = rotas.planejar_evacuacao(
        grafo,
        origem=origem,
        saida=saida,
        criterio=criterio,
        bloqueios=bloqueios,
    )

    print("=" * LARGURA)
    print(titulo)
    print("=" * LARGURA)
    print(f"Origem: {origem} | Saída: {saida} | Critério: {criterio}")
    print(f"Bloqueios: {', '.join(bloqueios) if bloqueios else 'nenhum'}")
    print("-" * LARGURA)

    if not resultado.encontrou:
        print(f"SEM ROTA: {resultado.mensagem}")
        print()
        return

    print(f"Rota: {resultado.rota_em_texto(' -> ')}")
    print(
        f"Tempo: {resultado.tempo_texto}"
        f" | Distância: {resultado.distancia_texto}"
        f" | Dificuldade: {resultado.dificuldade_texto}"
        f" | Trechos: {resultado.trechos}"
    )
    print()


def comparar_criterios(grafo, origem):
    """Mostra como cada criterio muda a rota para a mesma origem."""
    print("=" * LARGURA)
    print(f"7. Mesma origem ({origem}), critérios diferentes")
    print("=" * LARGURA)

    for criterio in COMPARACAO:
        resultado = rotas.planejar_evacuacao(
            grafo,
            origem=origem,
            saida="Saída mais próxima",
            criterio=criterio,
        )

        print(f"{criterio}:")
        print(f"  {resultado.rota_em_texto(' -> ')}")
        print(
            f"  Tempo: {resultado.tempo_texto}"
            f" | Distância: {resultado.distancia_texto}"
            f" | Dificuldade: {resultado.dificuldade_texto}"
        )

    print()


def main():
    grafo = Grafo()
    grafo.carregar_de_json(CAMINHO_MAPA)

    print()
    print(f"Mapa: {len(grafo.locais)} locais carregados de {CAMINHO_MAPA.name}")
    print()

    for cenario in CENARIOS:
        mostrar_cenario(grafo, **cenario)

    grafo.limpar_bloqueios()
    comparar_criterios(grafo, "Sala 203")


if __name__ == "__main__":
    main()
