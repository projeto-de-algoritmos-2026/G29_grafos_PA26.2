import json

class Grafo:
    def __init__(self):
        self.locais = {}
        self.adjacencia = {}

    def carregar_de_json(self, caminho_arquivo):
        with open(caminho_arquivo, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.locais.clear()
        self.adjacencia.clear()

        for codigo, local in dados["locais"].items():
            self.adicionar_local(codigo, local["nome"], local["tipo"])

        for conexao in dados["conexoes"]:
            self.adicionar_conexao(
                conexao["origem"],
                conexao["destino"],
                conexao["distancia"],
                conexao["tempo"],
                conexao["dificuldade"],
                conexao.get("bloqueado", False),
            )

    def adicionar_local(self, codigo, nome, tipo):
        self.locais[codigo] = {
            "nome": nome,
            "tipo": tipo,
        }
        self.adjacencia.setdefault(codigo, [])

    def adicionar_conexao(
        self, origem, destino, distancia, tempo, dificuldade, bloqueado=False
    ):
        if origem not in self.locais or destino not in self.locais:
            raise ValueError("Os dois locais devem existir no grafo.")

        self.adjacencia[origem].append(
            {
                "destino": destino,
                "distancia": distancia,
                "tempo": tempo,
                "dificuldade": dificuldade,
                "bloqueado": bloqueado,
            }
        )

        self.adjacencia[destino].append(
            {
                "destino": origem,
                "distancia": distancia,
                "tempo": tempo,
                "dificuldade": dificuldade,
                "bloqueado": bloqueado,
            }
        )

    def bloquear_conexao(self, origem, destino):
        """Marca uma conexao como indisponivel, sem remove-la do grafo."""
        self._definir_bloqueio(origem, destino, True)

    def desbloquear_conexao(self, origem, destino):
        """Remove o bloqueio de uma conexao."""
        self._definir_bloqueio(origem, destino, False)

    def conexao_bloqueada(self, origem, destino):
        """Informa se a passagem entre dois locais esta indisponivel."""
        for conexao in self.adjacencia.get(origem, []):
            if conexao["destino"] == destino:
                return conexao["bloqueado"]

        raise ValueError(f"Nao existe conexao entre {origem} e {destino}.")

    def _definir_bloqueio(self, origem, destino, bloqueado):
        """
        Aplica o estado de bloqueio nos dois sentidos da conexao.

        O grafo e nao direcionado, entao a mesma passagem aparece na lista
        de adjacencia dos dois locais. Bloquear apenas um dos sentidos
        deixaria o mapa inconsistente.
        """
        if origem not in self.locais or destino not in self.locais:
            raise ValueError("Os dois locais devem existir no grafo.")

        encontrou = False

        for inicio, fim in ((origem, destino), (destino, origem)):
            for conexao in self.adjacencia[inicio]:
                if conexao["destino"] == fim:
                    conexao["bloqueado"] = bloqueado
                    encontrou = True

        if not encontrou:
            raise ValueError(f"Nao existe conexao entre {origem} e {destino}.")

    def vizinhos(self, local):
        """Retorna as conexoes disponiveis (nao bloqueadas) de um local."""
        if local not in self.locais:
            raise ValueError(f"Local desconhecido: {local}.")

        return [
            conexao
            for conexao in self.adjacencia[local]
            if not conexao["bloqueado"]
        ]

    def limpar_bloqueios(self):
        """Libera todas as passagens do mapa."""
        for conexoes in self.adjacencia.values():
            for conexao in conexoes:
                conexao["bloqueado"] = False
