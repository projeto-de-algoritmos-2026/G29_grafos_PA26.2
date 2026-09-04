import customtkinter as ctk

def criar_mapa(painel, cor_texto):
    ctk.CTkLabel(
        painel,
        text="mapa aqui.",
        text_color=cor_texto,
    ).pack(expand=True)
