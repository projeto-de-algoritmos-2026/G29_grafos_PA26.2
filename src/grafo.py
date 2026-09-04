import json

class Grafo:
    def __init__(self):
        self.locais = {}
        self.adjacencia = {}
        self.locais_bloqueados = set()

    def carregar_de_json(self, caminho_arquivo):
        with open(caminho_arquivo, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        self.locais.clear()
        self.adjacencia.clear()
        self.locais_bloqueados.clear()

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

    def bloquear_local(self, codigo):
        """
        Marca um local como interditado.

        E o bloqueio que a interface oferece: um incendio interdita o
        Corredor B inteiro, e nao apenas uma de suas passagens. O local
        continua no mapa, mas nenhuma rota pode atravessa-lo.
        """
        if codigo not in self.locais:
            raise ValueError(f"Local desconhecido: {codigo}.")

        self.locais_bloqueados.add(codigo)

    def desbloquear_local(self, codigo):
        """Libera um local interditado."""
        if codigo not in self.locais:
            raise ValueError(f"Local desconhecido: {codigo}.")

        self.locais_bloqueados.discard(codigo)

    def local_bloqueado(self, codigo):
        """Informa se um local esta interditado."""
        return codigo in self.locais_bloqueados

    def vizinhos(self, local):
        """
        Retorna as conexoes disponiveis a partir de um local.

        Sao descartadas as passagens bloqueadas e as que levam a locais
        interditados. O Dijkstra recebe apenas o que pode percorrer.
        """
        if local not in self.locais:
            raise ValueError(f"Local desconhecido: {local}.")

        return [
            conexao
            for conexao in self.adjacencia[local]
            if not conexao["bloqueado"]
            and not self.local_bloqueado(conexao["destino"])
        ]

    def limpar_bloqueios(self):
        """Libera todas as passagens e todos os locais do mapa."""
        for conexoes in self.adjacencia.values():
            for conexao in conexoes:
                conexao["bloqueado"] = False

        self.locais_bloqueados.clear()

    def codigo_por_nome(self, nome):
        """
        Converte o nome exibido na interface no codigo usado no grafo.

        A interface trabalha com "Escada Norte"; o grafo, com "EN".
        """
        for codigo, local in self.locais.items():
            if local["nome"] == nome:
                return codigo

        for codigo, local in self.locais.items():
            if local["nome"].casefold() == nome.casefold():
                return codigo

        raise ValueError(f"Local desconhecido: {nome}.")

    def nome_do_local(self, codigo):
        """Converte o codigo do grafo no nome exibido na interface."""
        if codigo not in self.locais:
            raise ValueError(f"Local desconhecido: {codigo}.")

        return self.locais[codigo]["nome"]

    def saidas(self):
        """Retorna os codigos de todas as saidas do predio."""
        return [
            codigo
            for codigo, local in self.locais.items()
            if local["tipo"] == "saida"
        ]
