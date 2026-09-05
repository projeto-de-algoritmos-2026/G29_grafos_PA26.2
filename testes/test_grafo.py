"""
test_grafo.py

Testa a lista de adjacencia, os bloqueios e a conversao entre os nomes
exibidos na interface e os codigos usados no grafo.
"""

import unittest

from contexto import CAMINHO_MAPA, criar_grafo


class TestCarregamento(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_carrega_todos_os_locais_do_mapa(self):
        self.assertEqual(len(self.grafo.locais), 17)
        self.assertEqual(self.grafo.locais["S203"]["nome"], "Sala 203")
        self.assertEqual(self.grafo.locais["EN"]["tipo"], "escada")

    def test_toda_conexao_existe_nos_dois_sentidos(self):
        for origem, conexoes in self.grafo.adjacencia.items():
            for conexao in conexoes:
                volta = [
                    vizinho["destino"]
                    for vizinho in self.grafo.adjacencia[conexao["destino"]]
                ]
                self.assertIn(origem, volta)

    def test_conexao_guarda_os_tres_pesos(self):
        conexao = self._conexao("S203", "CA")

        self.assertEqual(conexao["distancia"], 12)
        self.assertEqual(conexao["tempo"], 15)
        self.assertEqual(conexao["dificuldade"], 1)
        self.assertFalse(conexao["bloqueado"])

    def test_recusa_conexao_com_local_inexistente(self):
        with self.assertRaises(ValueError):
            self.grafo.adicionar_conexao("CA", "XX", 1, 1, 1)

    def _conexao(self, origem, destino):
        for conexao in self.grafo.adjacencia[origem]:
            if conexao["destino"] == destino:
                return conexao

        self.fail(f"Conexao {origem}-{destino} nao encontrada.")


class TestBloqueioDeConexao(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_bloqueio_vale_nos_dois_sentidos(self):
        self.grafo.bloquear_conexao("CA", "EN")

        self.assertTrue(self.grafo.conexao_bloqueada("CA", "EN"))
        self.assertTrue(self.grafo.conexao_bloqueada("EN", "CA"))

    def test_desbloqueio_vale_nos_dois_sentidos(self):
        self.grafo.bloquear_conexao("CA", "EN")
        self.grafo.desbloquear_conexao("CA", "EN")

        self.assertFalse(self.grafo.conexao_bloqueada("CA", "EN"))
        self.assertFalse(self.grafo.conexao_bloqueada("EN", "CA"))

    def test_conexao_bloqueada_some_da_lista_de_vizinhos(self):
        self.grafo.bloquear_conexao("CA", "EN")
        destinos = [c["destino"] for c in self.grafo.vizinhos("CA")]

        self.assertNotIn("EN", destinos)
        self.assertIn("CC", destinos)

    def test_bloqueio_nao_remove_a_conexao_do_mapa(self):
        antes = len(self.grafo.adjacencia["CA"])
        self.grafo.bloquear_conexao("CA", "EN")

        self.assertEqual(len(self.grafo.adjacencia["CA"]), antes)

    def test_recusa_bloquear_conexao_inexistente(self):
        with self.assertRaises(ValueError):
            self.grafo.bloquear_conexao("S101", "S102")


class TestBloqueioDeLocal(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_local_interditado_some_dos_vizinhos(self):
        self.grafo.bloquear_local("EN")
        destinos = [c["destino"] for c in self.grafo.vizinhos("CA")]

        self.assertNotIn("EN", destinos)

    def test_desbloquear_local_devolve_a_passagem(self):
        self.grafo.bloquear_local("EN")
        self.grafo.desbloquear_local("EN")
        destinos = [c["destino"] for c in self.grafo.vizinhos("CA")]

        self.assertIn("EN", destinos)

    def test_recusa_bloquear_local_inexistente(self):
        with self.assertRaises(ValueError):
            self.grafo.bloquear_local("XX")

    def test_limpar_bloqueios_libera_locais_e_conexoes(self):
        self.grafo.bloquear_local("EN")
        self.grafo.bloquear_conexao("CA", "CC")
        self.grafo.limpar_bloqueios()

        self.assertFalse(self.grafo.local_bloqueado("EN"))
        self.assertFalse(self.grafo.conexao_bloqueada("CA", "CC"))

    def test_recarregar_o_mapa_desfaz_os_bloqueios(self):
        self.grafo.bloquear_local("EN")
        self.grafo.carregar_de_json(CAMINHO_MAPA)

        self.assertFalse(self.grafo.local_bloqueado("EN"))


class TestNomesECodigos(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_converte_nome_em_codigo(self):
        self.assertEqual(self.grafo.codigo_por_nome("Escada Norte"), "EN")

    def test_converte_nome_ignorando_maiusculas(self):
        self.assertEqual(self.grafo.codigo_por_nome("sala 203"), "S203")

    def test_recusa_nome_desconhecido(self):
        with self.assertRaises(ValueError):
            self.grafo.codigo_por_nome("Heliponto")

    def test_converte_codigo_em_nome(self):
        self.assertEqual(self.grafo.nome_do_local("SE"), "Saída de Emergência")

    def test_lista_as_saidas_do_predio(self):
        self.assertEqual(sorted(self.grafo.saidas()), ["SE", "SP"])


if __name__ == "__main__":
    unittest.main()
