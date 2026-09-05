import customtkinter as ctk

from dijkstra import calcular_melhor_saida, calcular_metricas
from dijkstra import calcular_rota as encontrar_rota

from .mapa import criar_mapa

ctk.set_appearance_mode("light")

COR_FUNDO = "#EDF7FC"
COR_CARTAO = "#FFFFFF"
COR_CABECALHO = "#DCEEF7"
COR_TITULO = "#245B78"
COR_TEXTO = "#526D7A"
COR_BORDA = "#C5DDE9"
COR_SELETOR = "#E7F2F8"
COR_ERRO = "#B42318"

CRITERIOS = {
    "Menor tempo": "tempo",
    "Menor distância": "distancia",
    "Menor dificuldade": "dificuldade",
    "Rota mais segura": "seguro",
}
TIPOS_BLOQUEAVEIS = {"corredor", "escada", "elevador", "saida"}


class JanelaPrincipal:
    def __init__(self, raiz, grafo):
        self.raiz = raiz
        self.grafo = grafo
        self.bloqueios = {}
        self.codigos_por_nome = {}
        self.locais, self.saidas, self.locais_bloqueaveis = self.obter_opcoes()

        self.raiz.title("Sistema de Evacuação de Emergência")
        self.raiz.geometry("1000x650")
        self.raiz.minsize(800, 520)
        self.raiz.configure(fg_color=COR_FUNDO)

        self.criar_cabecalho()
        self.criar_paineis()

    def criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(
            self.raiz,
            fg_color=COR_CARTAO,
            corner_radius=0,
        )
        cabecalho.pack(fill="x")

        ctk.CTkLabel(
            cabecalho,
            text="Sistema de Evacuação de Emergência",
            text_color=COR_TITULO,
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(anchor="w", padx=25, pady=(20, 0))

        ctk.CTkLabel(
            cabecalho,
            text="Encontre uma rota segura até a saída do prédio.",
            text_color=COR_TEXTO,
        ).pack(anchor="w", padx=25, pady=(4, 20))

    def criar_paineis(self):
        conteudo = ctk.CTkFrame(self.raiz, fg_color="transparent")
        conteudo.pack(fill="both", expand=True, padx=18, pady=22)

        conteudo.columnconfigure(0, weight=3)
        conteudo.columnconfigure(1, weight=5)
        conteudo.columnconfigure(2, weight=3)
        conteudo.rowconfigure(0, weight=1)

        self.painel_controles = self.criar_painel(conteudo, 0, "Controles")
        self.painel_mapa = self.criar_painel(conteudo, 1, "Mapa do prédio")
        self.painel_resultado = self.criar_painel(
            conteudo, 2, "Resultado da rota"
        )

        self.criar_seletores()
        criar_mapa(self.painel_mapa, self.grafo, COR_TEXTO)
        self.criar_resultado()

    def criar_painel(self, pai, coluna, titulo):
        painel = ctk.CTkFrame(
            pai,
            fg_color=COR_CARTAO,
            border_color=COR_BORDA,
            border_width=1,
            corner_radius=0,
        )
        painel.grid(row=0, column=coluna, sticky="nsew", padx=7)

        faixa_titulo = ctk.CTkFrame(
            painel,
            fg_color=COR_CABECALHO,
            height=48,
            corner_radius=0,
        )
        faixa_titulo.pack(fill="x", padx=1, pady=(1, 0))
        faixa_titulo.pack_propagate(False)

        ctk.CTkLabel(
            faixa_titulo,
            text=titulo,
            text_color=COR_TITULO,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).pack(fill="both", expand=True, padx=16)

        return painel

    def criar_seletores(self):
        area = ctk.CTkScrollableFrame(
            self.painel_controles,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=COR_BORDA,
            scrollbar_button_hover_color="#A9CBDC",
        )
        area.pack(fill="both", expand=True, padx=8, pady=12)

        self.seletor_origem = self.criar_seletor(
            area, "Local de origem", self.locais
        )
        self.seletor_saida = self.criar_seletor(area, "Saída", self.saidas)
        self.seletor_criterio = self.criar_seletor(
            area, "Critério", list(CRITERIOS)
        )

        self.criar_bloqueios(area)
        self.criar_botoes(area)

    def criar_seletor(self, pai, titulo, opcoes):
        ctk.CTkLabel(
            pai,
            text=titulo,
            text_color=COR_TEXTO,
            anchor="w",
        ).pack(fill="x")

        seletor = ctk.CTkOptionMenu(
            pai,
            values=opcoes,
            fg_color=COR_SELETOR,
            button_color=COR_BORDA,
            button_hover_color="#A9CBDC",
            text_color=COR_TITULO,
            dropdown_fg_color=COR_SELETOR,
            dropdown_hover_color=COR_CABECALHO,
            dropdown_text_color=COR_TEXTO,
            corner_radius=0,
        )
        seletor.pack(fill="x", pady=(4, 16))
        seletor.set(opcoes[0])

        return seletor

    def criar_bloqueios(self, pai):
        ctk.CTkLabel(
            pai,
            text="Bloqueios",
            text_color=COR_TITULO,
            font=ctk.CTkFont(weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        ctk.CTkLabel(
            pai,
            text="Selecione os indisponíveis",
            text_color=COR_TEXTO,
            anchor="w",
            wraplength=210,
        ).pack(fill="x", pady=(0, 10))

        for local in self.locais_bloqueaveis:
            selecionado = ctk.BooleanVar(value=False)
            self.bloqueios[local] = selecionado

            ctk.CTkCheckBox(
                pai,
                text=local,
                variable=selecionado,
                fg_color=COR_TITULO,
                hover_color="#447F9A",
                border_color=COR_BORDA,
                text_color=COR_TEXTO,
                corner_radius=0,
            ).pack(anchor="w", pady=5)

    def obter_opcoes(self):
        locais = ["Selecione um local"]
        saidas = ["Saída mais próxima"]
        bloqueios = []

        for codigo, dados in self.grafo.locais.items():
            nome = dados["nome"]
            tipo = dados["tipo"]
            self.codigos_por_nome[nome] = codigo

            if tipo == "saida":
                saidas.append(nome)
            else:
                locais.append(nome)

            if tipo in TIPOS_BLOQUEAVEIS:
                bloqueios.append(nome)

        return locais, saidas, bloqueios

    def obter_bloqueios_selecionados(self):
        return [
            self.codigos_por_nome[local]
            for local, selecionado in self.bloqueios.items()
            if selecionado.get()
        ]

    def criar_botoes(self, pai):
        self.botao_calcular = ctk.CTkButton(
            pai,
            text="Calcular rota",
            command=self.calcular,
            fg_color=COR_TITULO,
            hover_color="#1D4A61",
            corner_radius=0,
        )
        self.botao_calcular.pack(fill="x", pady=(18, 8))

        ctk.CTkButton(
            pai,
            text="Limpar seleção",
            command=self.limpar_selecao,
            fg_color="transparent",
            hover_color=COR_SELETOR,
            border_color=COR_BORDA,
            border_width=1,
            text_color=COR_TITULO,
            corner_radius=0,
        ).pack(fill="x")

    def criar_resultado(self):
        area = ctk.CTkFrame(self.painel_resultado, fg_color="transparent")
        area.pack(fill="both", expand=True, padx=16, pady=18)

        self.mensagem_resultado = ctk.CTkLabel(
            area,
            text="Nenhuma rota calculada.",
            text_color=COR_TEXTO,
            wraplength=200,
        )
        self.mensagem_resultado.pack(pady=(8, 24))

        self.metricas = {}
        for nome in ["Tempo", "Distância", "Dificuldade"]:
            quadro = ctk.CTkFrame(area, fg_color=COR_SELETOR, corner_radius=0)
            quadro.pack(fill="x", pady=5)

            ctk.CTkLabel(
                quadro,
                text=nome,
                text_color=COR_TEXTO,
            ).pack(anchor="w", padx=12, pady=(8, 0))

            valor = ctk.CTkLabel(
                quadro,
                text="—",
                text_color=COR_TITULO,
                font=ctk.CTkFont(size=16, weight="bold"),
            )
            valor.pack(anchor="w", padx=12, pady=(0, 8))
            self.metricas[nome] = valor

    def calcular(self):
        nome_origem = self.seletor_origem.get()

        if nome_origem == self.locais[0]:
            self.exibir_erro("Selecione um local de origem.")
            return

        origem = self.codigos_por_nome[nome_origem]
        criterio = CRITERIOS[self.seletor_criterio.get()]

        self.grafo.limpar_bloqueios()
        for codigo in self.obter_bloqueios_selecionados():
            self.grafo.bloquear_local(codigo)

        try:
            if self.seletor_saida.get() == self.saidas[0]:
                caminho, _, _ = calcular_melhor_saida(
                    self.grafo, origem, criterio
                )
            else:
                destino = self.codigos_por_nome[self.seletor_saida.get()]
                caminho, _ = encontrar_rota(
                    self.grafo, origem, destino, criterio
                )
        except ValueError as erro:
            self.exibir_erro(str(erro))
            return

        if caminho is None:
            self.exibir_erro("Não existe uma rota disponível com os bloqueios selecionados.")
            return

        metricas = calcular_metricas(self.grafo, caminho)
        nomes = [self.grafo.nome_do_local(codigo) for codigo in caminho]

        self.mensagem_resultado.configure(
            text=" → ".join(nomes),
            text_color=COR_TITULO,
        )
        self.metricas["Tempo"].configure(
            text=self.formatar_tempo(metricas["tempo"])
        )
        self.metricas["Distância"].configure(
            text=f'{metricas["distancia"]} m'
        )
        self.metricas["Dificuldade"].configure(
            text=f'{metricas["dificuldade_maxima"]}/5'
        )

    def exibir_erro(self, mensagem):
        self.mensagem_resultado.configure(text=mensagem, text_color=COR_ERRO)
        for valor in self.metricas.values():
            valor.configure(text="—")

    @staticmethod
    def formatar_tempo(segundos):
        minutos, segundos = divmod(segundos, 60)

        if minutos:
            return f"{minutos} min {segundos} s"

        return f"{segundos} s"

    def limpar_selecao(self):
        self.seletor_origem.set(self.locais[0])
        self.seletor_saida.set(self.saidas[0])
        self.seletor_criterio.set(next(iter(CRITERIOS)))

        for selecionado in self.bloqueios.values():
            selecionado.set(False)

        self.grafo.limpar_bloqueios()
        self.mensagem_resultado.configure(
            text="Nenhuma rota calculada.",
            text_color=COR_TEXTO,
        )
        for valor in self.metricas.values():
            valor.configure(text="—")


def iniciar_interface(grafo):
    raiz = ctk.CTk()
    JanelaPrincipal(raiz, grafo)
    raiz.mainloop()
