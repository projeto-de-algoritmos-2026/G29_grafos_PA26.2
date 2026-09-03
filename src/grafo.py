class Grafo:
    def __init__(self):
        self.locais = {}
        self.adjacencia = {}

    def carregar_de_json(self, caminho_arquivo):
        """Carrega locais e conexoes a partir de um arquivo mapa.json."""
        # TODO: ler o JSON, criar os locais com adicionar_local() e as
        # conexoes com adicionar_conexao().
        raise NotImplementedError

    def adicionar_local(self, codigo, nome, tipo):
        self.locais[codigo] = {
            "nome": nome,
            "tipo": tipo,
        }
        self.adjacencia.setdefault(codigo, [])

    def adicionar_conexao(self, origem, destino, distancia, tempo, dificuldade):
        if origem not in self.locais or destino not in self.locais:
            raise ValueError("Os dois locais devem existir no grafo.")

        self.adjacencia[origem].append(
            {
                "destino": destino,
                "distancia": distancia,
                "tempo": tempo,
                "dificuldade": dificuldade,
                "bloqueado": False,
            }
        )

        self.adjacencia[destino].append(
            {
                "destino": origem,
                "distancia": distancia,
                "tempo": tempo,
                "dificuldade": dificuldade,
                "bloqueado": False,
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
