import customtkinter as ctk

ctk.set_appearance_mode("light")

COR_FUNDO = "#EDF7FC"
COR_CARTAO = "#FFFFFF"
COR_CABECALHO = "#DCEEF7"
COR_TITULO = "#245B78"
COR_TEXTO = "#526D7A"
COR_BORDA = "#C5DDE9"
COR_SELETOR = "#E7F2F8"

LOCAIS = [
    "Selecione um local",
    "Sala 101",
    "Sala 102",
    "Sala 103",
    "Sala 201",
    "Sala 202",
    "Sala 203",
    "Corredor A",
    "Corredor B",
    "Corredor Central",
    "Escada Norte",
    "Escada Sul",
    "Elevador",
    "Hall do Térreo",
    "Porta Principal",
    "Porta Lateral",
]
SAIDAS = ["Saída mais próxima", "Saída Principal", "Saída de Emergência"]
CRITERIOS = ["Menor tempo", "Menor distância", "Menor dificuldade"]
TIPOS_BLOQUEAVEIS = {"corredor", "escada", "elevador", "saida"}
BLOQUEIOS = [
    "Corredor A",
    "Corredor B",
    "Corredor Central",
    "Escada Norte",
    "Escada Sul",
    "Elevador",
    "Saída Principal",
    "Saída de Emergência",
]

class JanelaPrincipal:
    def __init__(self, raiz, grafo):
        self.raiz = raiz
        self.grafo = grafo
        self.bloqueios = {}
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

        self.painel_controles = self.criar_painel(
            conteudo,
            0,
            "Controles",
        )
        self.painel_mapa = self.criar_painel(
            conteudo,
            1,
            "Mapa do prédio",
        )
        self.painel_resultado = self.criar_painel(
            conteudo,
            2,
            "Resultado da rota",
        )

        self.criar_seletores()

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
        self.seletor_criterio = self.criar_seletor(area, "Critério", CRITERIOS)

        self.criar_bloqueios(area)

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
        locais_do_grafo = getattr(self.grafo, "locais", {})

        if not locais_do_grafo:
            return LOCAIS, SAIDAS, BLOQUEIOS

        locais = ["Selecione um local"]
        saidas = ["Saída mais próxima"]
        bloqueios = []

        for dados in locais_do_grafo.values():
            nome = dados["nome"]
            tipo = dados["tipo"]

            if tipo == "saida":
                saidas.append(nome)
            else:
                locais.append(nome)

            if tipo in TIPOS_BLOQUEAVEIS:
                bloqueios.append(nome)

        return locais, saidas, bloqueios

    def obter_bloqueios_selecionados(self):
        return [
            local
            for local, selecionado in self.bloqueios.items()
            if selecionado.get()
        ]


def iniciar_interface(grafo):
    raiz = ctk.CTk()
    JanelaPrincipal(raiz, grafo)
    raiz.mainloop()
