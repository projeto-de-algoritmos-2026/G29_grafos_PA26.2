"""
rotas.py

Camada entre a interface e o algoritmo. Recebe exatamente o que a tela
tem (nomes de locais, rotulo do criterio e lista de bloqueios marcados)
e devolve um resultado pronto para exibir, com a rota, as metricas e a
mensagem de erro quando nao ha passagem segura.

Uso na interface:

    from rotas import planejar_evacuacao

    resultado = planejar_evacuacao(
        grafo,
        origem="Sala 203",
        saida="Saida mais proxima",
        criterio="Menor tempo",
        bloqueios=["Corredor B"],
    )

Responsabilidade: Pessoa 1 (algoritmos e dados).
"""

from dataclasses import dataclass, field

import dijkstra

SAIDA_MAIS_PROXIMA = "Saída mais próxima"
SEM_ORIGEM = "Selecione um local"

# Traduz o rotulo mostrado no seletor para o criterio usado na busca.
CRITERIOS_INTERFACE = {
    "Menor tempo": "tempo",
    "Menor distância": "distancia",
    "Menor dificuldade": "dificuldade",
    "Evacuação segura": "seguro",
}


@dataclass
class Resultado:
    """Resposta completa de um calculo de rota, pronta para a tela."""

    encontrou: bool = False
    mensagem: str = ""
    caminho: list = field(default_factory=list)
    rota: list = field(default_factory=list)
    saida: str = ""
    tempo: int = 0
    distancia: int = 0
    dificuldade: int = 0
    trechos: int = 0

    @property
    def tempo_texto(self):
        """Tempo estimado em formato legivel."""
        if not self.encontrou:
            return "—"

        if self.tempo < 60:
            return f"{self.tempo} s"

        minutos, segundos = divmod(self.tempo, 60)

        if segundos == 0:
            return f"{minutos} min"

        return f"{minutos} min {segundos} s"

    @property
    def distancia_texto(self):
        """Distancia total percorrida."""
        return f"{self.distancia} m" if self.encontrou else "—"

    @property
    def dificuldade_texto(self):
        """Dificuldade do trecho mais pesado, na escala de 1 a 5."""
        return f"{self.dificuldade} de 5" if self.encontrou else "—"

    def rota_em_texto(self, separador=" → "):
        """Monta a sequencia de locais: Sala 203 → Corredor A → ..."""
        return separador.join(self.rota)


def aplicar_bloqueios(grafo, bloqueios):
    """
    Deixa o mapa com exatamente os bloqueios marcados na tela.

    Os bloqueios anteriores sao desfeitos antes de aplicar os novos: a
    interface envia a selecao atual inteira a cada calculo. Como nenhuma
    conexao e removida do grafo, da para ativar, desfazer e comparar
    simulacoes sem recarregar o mapa.
    """
    grafo.limpar_bloqueios()

    for nome in bloqueios or []:
        grafo.bloquear_local(_codigo(grafo, nome))


def planejar_evacuacao(
    grafo,
    origem,
    saida=SAIDA_MAIS_PROXIMA,
    criterio="Menor tempo",
    bloqueios=None,
):
    """
    Calcula a rota de evacuacao pedida na tela e devolve um Resultado.

    Aceita tanto os nomes exibidos ("Sala 203", "Menor tempo") quanto os
    codigos internos ("S203", "tempo"). Nunca levanta excecao por escolha
    invalida do usuario: o problema volta descrito em 'mensagem'.
    """
    if origem in (None, "", SEM_ORIGEM):
        return Resultado(mensagem="Selecione o local de origem.")

    try:
        codigo_origem = _codigo(grafo, origem)
        codigo_criterio = _criterio(criterio)
        aplicar_bloqueios(grafo, bloqueios)
    except ValueError as erro:
        return Resultado(mensagem=str(erro))

    if grafo.local_bloqueado(codigo_origem):
        nome_origem = grafo.nome_do_local(codigo_origem)
        return Resultado(
            mensagem=(
                f"{nome_origem} está interditado. "
                "Escolha outro ponto de partida."
            )
        )

    if saida in (None, "", SAIDA_MAIS_PROXIMA):
        caminho, _, codigo_saida = dijkstra.calcular_melhor_saida(
            grafo, codigo_origem, codigo_criterio
        )
        indisponivel = (
            "Nenhuma saída pode ser alcançada com os bloqueios atuais. "
            "Não há rota de evacuação segura."
        )
    else:
        try:
            codigo_saida = _codigo(grafo, saida)
        except ValueError as erro:
            return Resultado(mensagem=str(erro))

        caminho, _ = dijkstra.calcular_rota(
            grafo, codigo_origem, codigo_saida, codigo_criterio
        )
        indisponivel = (
            f"Não há caminho livre até {grafo.nome_do_local(codigo_saida)}. "
            "Tente outra saída ou remova um bloqueio."
        )

    if caminho is None:
        return Resultado(mensagem=indisponivel)

    metricas = dijkstra.calcular_metricas(grafo, caminho)

    return Resultado(
        encontrou=True,
        mensagem="Rota encontrada.",
        caminho=caminho,
        rota=[grafo.nome_do_local(codigo) for codigo in caminho],
        saida=grafo.nome_do_local(codigo_saida),
        tempo=metricas["tempo"],
        distancia=metricas["distancia"],
        dificuldade=metricas["dificuldade_maxima"],
        trechos=metricas["trechos"],
    )


def _codigo(grafo, local):
    """Aceita tanto o codigo do grafo quanto o nome exibido na tela."""
    if local in grafo.locais:
        return local

    return grafo.codigo_por_nome(local)


def _criterio(criterio):
    """Aceita tanto o rotulo do seletor quanto o criterio da busca."""
    if criterio in CRITERIOS_INTERFACE:
        return CRITERIOS_INTERFACE[criterio]

    if criterio in dijkstra.CRITERIOS:
        return criterio

    validos = ", ".join(CRITERIOS_INTERFACE)
    raise ValueError(f"Critério desconhecido. Use um destes: {validos}.")
