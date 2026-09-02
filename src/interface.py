import customtkinter as ctk

ctk.set_appearance_mode("light")

COR_FUNDO = "#EDF7FC"
COR_CARTAO = "#FFFFFF"
COR_CABECALHO = "#DCEEF7"
COR_TITULO = "#245B78"
COR_TEXTO = "#526D7A"
COR_BORDA = "#C5DDE9"


class JanelaPrincipal:
    def __init__(self, raiz, grafo):
        self.raiz = raiz
        self.grafo = grafo

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


def iniciar_interface(grafo):
    raiz = ctk.CTk()
    JanelaPrincipal(raiz, grafo)
    raiz.mainloop()
