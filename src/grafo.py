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
