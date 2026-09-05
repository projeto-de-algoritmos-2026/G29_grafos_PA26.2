"""
test_dijkstra.py

Testa o algoritmo em si: o menor caminho encontrado, o custo acumulado,
a troca de criterio, a busca da saida mais proxima e as metricas da rota.

Os valores esperados vem do mapa em dados/mapa.json e foram conferidos
somando os pesos trecho a trecho.
"""

import unittest

# O contexto precisa vir primeiro: e ele quem coloca src no sys.path.
from contexto import criar_grafo

import dijkstra  # noqa: E402

# Sala 203 ate a Saida Principal, sem bloqueios: a rota mais rapida
# desce pelo elevador (86 s), a mais curta usa a Escada Norte (69 m) e a
# menos cansativa usa a Escada Sul (dificuldade 8).
ROTA_MAIS_RAPIDA = ["S203", "CA", "CC", "EL", "H1", "P1", "SP"]
ROTA_MAIS_CURTA = ["S203", "CA", "EN", "H1", "P1", "SP"]
ROTA_MAIS_FACIL = ["S203", "CA", "CB", "ES", "H1", "P1", "SP"]


class TestCalcularRota(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_rota_mais_rapida_desce_pelo_elevador(self):
        caminho, custo = dijkstra.calcular_rota(
            self.grafo, "S203", "SP", "tempo"
        )

        self.assertEqual(caminho, ROTA_MAIS_RAPIDA)
        self.assertEqual(custo, 86)

    def test_custo_e_a_soma_dos_pesos_do_criterio(self):
        _, custo = dijkstra.calcular_rota(
            self.grafo, "S203", "SP", "distancia"
        )

        self.assertEqual(custo, 12 + 15 + 25 + 12 + 5)

    def test_criterio_distancia_prefere_a_escada_norte(self):
        caminho, custo = dijkstra.calcular_rota(
            self.grafo, "S203", "SP", "distancia"
        )

        self.assertEqual(caminho, ROTA_MAIS_CURTA)
        self.assertEqual(custo, 69)

    def test_criterio_dificuldade_prefere_a_escada_sul(self):
        caminho, custo = dijkstra.calcular_rota(
            self.grafo, "S203", "SP", "dificuldade"
        )

        self.assertEqual(caminho, ROTA_MAIS_FACIL)
        self.assertEqual(custo, 8)

    def test_modo_seguro_evita_o_elevador(self):
        caminho, _ = dijkstra.calcular_rota(
            self.grafo, "S203", "SP", "seguro"
        )

        self.assertEqual(caminho, ROTA_MAIS_FACIL)
        self.assertNotIn("EL", caminho)

    def test_rota_para_o_proprio_local_nao_tem_custo(self):
        caminho, custo = dijkstra.calcular_rota(self.grafo, "SP", "SP")

        self.assertEqual(caminho, ["SP"])
        self.assertEqual(custo, 0)

    def test_bloqueio_forca_rota_alternativa(self):
        self.grafo.bloquear_local("EL")
        caminho, custo = dijkstra.calcular_rota(
            self.grafo, "S203", "SP", "tempo"
        )

        self.assertEqual(caminho, ROTA_MAIS_CURTA)
        self.assertEqual(custo, 91)
        self.assertNotIn("EL", caminho)

    def test_sem_caminho_livre_devolve_none(self):
        for local in ("EN", "ES", "EL"):
            self.grafo.bloquear_local(local)

        caminho, custo = dijkstra.calcular_rota(self.grafo, "S203", "SP")

        self.assertIsNone(caminho)
        self.assertIsNone(custo)

    def test_origem_interditada_nao_tem_rota(self):
        self.grafo.bloquear_local("CA")

        caminho, _ = dijkstra.calcular_rota(self.grafo, "CA", "SP")

        self.assertIsNone(caminho)

    def test_recusa_local_desconhecido(self):
        with self.assertRaises(ValueError):
            dijkstra.calcular_rota(self.grafo, "S203", "Heliponto")

    def test_recusa_criterio_desconhecido(self):
        with self.assertRaises(ValueError):
            dijkstra.calcular_rota(self.grafo, "S203", "SP", "menor tempo")


class TestMelhorSaida(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_escolhe_a_saida_de_menor_custo(self):
        caminho, custo, saida = dijkstra.calcular_melhor_saida(
            self.grafo, "S203", "tempo"
        )

        self.assertEqual(saida, "SP")
        self.assertEqual(caminho, ROTA_MAIS_RAPIDA)
        self.assertEqual(custo, 86)

    def test_troca_de_saida_quando_a_principal_esta_bloqueada(self):
        self.grafo.bloquear_local("SP")
        caminho, custo, saida = dijkstra.calcular_melhor_saida(
            self.grafo, "S203", "tempo"
        )

        self.assertEqual(saida, "SE")
        self.assertEqual(caminho[-1], "SE")
        self.assertEqual(custo, 91)

    def test_sem_saida_liberada_devolve_none(self):
        self.grafo.bloquear_local("SP")
        self.grafo.bloquear_local("SE")

        self.assertEqual(
            dijkstra.calcular_melhor_saida(self.grafo, "S203"),
            (None, None, None),
        )

    def test_saidas_inalcancaveis_devolvem_none(self):
        for local in ("EN", "ES", "EL"):
            self.grafo.bloquear_local(local)

        self.assertEqual(
            dijkstra.calcular_melhor_saida(self.grafo, "S203"),
            (None, None, None),
        )

    def test_uma_busca_responde_por_todas_as_saidas(self):
        # A saida escolhida tem de ser a mesma que sairia de uma busca
        # direta ate cada saida, comparando os custos no final.
        _, custo_sp = dijkstra.calcular_rota(self.grafo, "S203", "SP")
        _, custo_se = dijkstra.calcular_rota(self.grafo, "S203", "SE")
        _, custo, saida = dijkstra.calcular_melhor_saida(self.grafo, "S203")

        self.assertEqual(custo, min(custo_sp, custo_se))
        self.assertEqual(saida, "SP" if custo_sp <= custo_se else "SE")


class TestMetricas(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_soma_os_pesos_de_cada_trecho(self):
        metricas = dijkstra.calcular_metricas(self.grafo, ROTA_MAIS_RAPIDA)

        self.assertEqual(metricas["tempo"], 86)
        self.assertEqual(metricas["distancia"], 84)
        self.assertEqual(metricas["dificuldade_total"], 10)
        self.assertEqual(metricas["dificuldade_maxima"], 5)
        self.assertEqual(metricas["trechos"], 6)

    def test_dificuldade_maxima_e_o_pior_trecho(self):
        metricas = dijkstra.calcular_metricas(self.grafo, ROTA_MAIS_FACIL)

        self.assertEqual(metricas["dificuldade_maxima"], 2)

    def test_caminho_de_um_local_nao_tem_trechos(self):
        metricas = dijkstra.calcular_metricas(self.grafo, ["SP"])

        self.assertEqual(metricas["tempo"], 0)
        self.assertEqual(metricas["trechos"], 0)

    def test_recusa_caminho_com_trecho_inexistente(self):
        with self.assertRaises(ValueError):
            dijkstra.calcular_metricas(self.grafo, ["S203", "H1"])


if __name__ == "__main__":
    unittest.main()
