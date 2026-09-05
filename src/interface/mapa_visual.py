import tkinter as tk

from dijkstra import peso_da_conexao

COR_FUNDO = "#FFFFFF"
COR_CONEXAO = "#B8CAD4"
COR_VERTICE = "#DCEEF7"
COR_TEXTO = "#245B78"
COR_ROTA = "#2E8B72"
COR_BLOQUEIO = "#C84B4B"
COR_SAIDA = "#BFE3D5"

POSICOES = {
    "S101": (0.08, 0.08),
    "S102": (0.08, 0.22),
    "S203": (0.08, 0.36),
    "CA": (0.28, 0.22),
    "S103": (0.92, 0.08),
    "S201": (0.92, 0.22),
    "S202": (0.92, 0.36),
    "CB": (0.72, 0.22),
    "CC": (0.50, 0.40),
    "EN": (0.25, 0.56),
    "EL": (0.50, 0.56),
    "ES": (0.75, 0.56),
    "H1": (0.50, 0.70),
    "P1": (0.35, 0.82),
    "P2": (0.65, 0.82),
    "SP": (0.25, 0.94),
    "SE": (0.75, 0.94),
}

class MapaVisual:
    def __init__(self, painel, grafo):
        self.grafo = grafo
        self.rota = []
        self.bloqueios = set()
        self.criterio = None

        legenda = tk.Frame(painel, background=COR_FUNDO)
        legenda.pack(fill="x", padx=12, pady=(10, 0))

        for texto, cor in [
            ("━ Conexão", COR_CONEXAO),
            ("━ Rota", COR_ROTA),
            ("┄ Bloqueio", COR_BLOQUEIO),
            ("● Saída", COR_ROTA),
        ]:
            tk.Label(
                legenda,
                text=texto,
                background=COR_FUNDO,
                foreground=cor,
                font=("TkDefaultFont", 8),
            ).pack(side="left", padx=(0, 10))

        self.canvas = tk.Canvas(
            painel,
            background=COR_FUNDO,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)
        self.canvas.bind("<Configure>", self.desenhar)

    def atualizar(self, rota=None, bloqueios=None, criterio=None):
        self.rota = rota or []
        self.bloqueios = set(bloqueios or [])
        self.criterio = criterio
        self.desenhar()

    def desenhar(self, _evento=None):
        self.canvas.delete("all")

        largura = self.canvas.winfo_width()
        altura = self.canvas.winfo_height()

        if largura <= 1 or altura <= 1:
            return

        pontos = {
            codigo: self.converter_posicao(posicao, largura, altura)
            for codigo, posicao in POSICOES.items()
        }
        arestas_da_rota = {
            frozenset((origem, destino))
            for origem, destino in zip(self.rota, self.rota[1:])
        }

        for origem, conexoes in self.grafo.adjacencia.items():
            for conexao in conexoes:
                destino = conexao["destino"]

                if origem >= destino:
                    continue

                bloqueada = (
                    conexao["bloqueado"]
                    or origem in self.bloqueios
                    or destino in self.bloqueios
                )
                na_rota = frozenset((origem, destino)) in arestas_da_rota

                cor = COR_CONEXAO
                largura_linha = 3
                tracejado = None

                if na_rota:
                    cor = COR_ROTA
                    largura_linha = 5
                if bloqueada:
                    cor = COR_BLOQUEIO
                    tracejado = (5, 4)

                self.canvas.create_line(
                    *pontos[origem],
                    *pontos[destino],
                    fill=cor,
                    width=largura_linha,
                    dash=tracejado,
                )

                if na_rota and self.criterio:
                    x_origem, y_origem = pontos[origem]
                    x_destino, y_destino = pontos[destino]

                    self.canvas.create_text(
                        (x_origem + x_destino) / 2,
                        (y_origem + y_destino) / 2 - 10,
                        text=self.formatar_peso(conexao),
                        fill=COR_ROTA,
                        font=("TkDefaultFont", 8, "bold"),
                    )

        for codigo, dados in self.grafo.locais.items():
            x, y = pontos[codigo]
            bloqueado = codigo in self.bloqueios

            cor = COR_VERTICE
            contorno = COR_TEXTO

            if dados["tipo"] == "saida":
                cor = COR_SAIDA
                contorno = COR_ROTA
            if codigo in self.rota:
                cor = COR_SAIDA
                contorno = COR_ROTA
            if bloqueado:
                cor = "#F6D1D1"
                contorno = COR_BLOQUEIO

            self.canvas.create_oval(
                x - 18,
                y - 18,
                x + 18,
                y + 18,
                fill=cor,
                outline=contorno,
                width=2,
            )
            self.canvas.create_text(
                x,
                y,
                text=codigo,
                fill=COR_TEXTO,
                font=("TkDefaultFont", 8, "bold"),
            )
            self.canvas.create_text(
                x,
                y + 26,
                text=dados["nome"],
                fill=COR_TEXTO,
                font=("TkDefaultFont", 8),
            )

    @staticmethod
    def converter_posicao(posicao, largura, altura):
        margem_x = 45
        margem_y = 35
        x, y = posicao

        return (
            margem_x + x * (largura - 2 * margem_x),
            margem_y + y * (altura - 2 * margem_y),
        )

def criar_mapa(painel, grafo):
    return MapaVisual(painel, grafo)