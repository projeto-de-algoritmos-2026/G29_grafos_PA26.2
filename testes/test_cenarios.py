"""
test_cenarios.py

Testa os cenarios de emergencia pela mesma porta que a interface usa:
planejar_evacuacao, recebendo nomes de locais, rotulo de criterio e a
lista de bloqueios marcados na tela.

Cobre a secao 11 do planejamento: rota normal, incendio, escada
indisponivel, saida bloqueada e ausencia de rota segura.
"""

import unittest

# O contexto precisa vir primeiro: e ele quem coloca src no sys.path.
from contexto import criar_grafo

import rotas  # noqa: E402


class TestCenariosDeEmergencia(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def planejar(self, **opcoes):
        opcoes.setdefault("origem", "Sala 203")
        opcoes.setdefault("saida", "Saída Principal")

        return rotas.planejar_evacuacao(self.grafo, **opcoes)

    def test_rota_normal_sem_bloqueios(self):
        resultado = self.planejar()

        self.assertTrue(resultado.encontrou)
        self.assertEqual(resultado.rota[0], "Sala 203")
        self.assertEqual(resultado.rota[-1], "Saída Principal")
        self.assertEqual(resultado.saida, "Saída Principal")
        self.assertEqual(resultado.trechos, 6)

    def test_incendio_no_elevador_gera_rota_alternativa(self):
        normal = self.planejar()
        recalculada = self.planejar(bloqueios=["Elevador"])

        self.assertIn("Elevador", normal.rota)
        self.assertNotIn("Elevador", recalculada.rota)
        self.assertIn("Escada Norte", recalculada.rota)
        self.assertTrue(recalculada.encontrou)

    def test_escada_indisponivel_forca_a_outra_escada(self):
        resultado = self.planejar(bloqueios=["Elevador", "Escada Norte"])

        self.assertIn("Escada Sul", resultado.rota)
        self.assertEqual(resultado.trechos, 6)

    def test_saida_bloqueada_seleciona_a_outra_saida(self):
        resultado = self.planejar(
            saida="Saída mais próxima", bloqueios=["Saída Principal"]
        )

        self.assertEqual(resultado.saida, "Saída de Emergência")
        self.assertTrue(resultado.encontrou)

    def test_sala_isolada_avisa_que_nao_ha_caminho(self):
        resultado = self.planejar(origem="Sala 202", bloqueios=["Corredor B"])

        self.assertFalse(resultado.encontrou)
        self.assertIn("Saída Principal", resultado.mensagem)
        self.assertEqual(resultado.rota, [])

    def test_sem_rota_segura_avisa_a_impossibilidade(self):
        resultado = self.planejar(
            saida="Saída mais próxima",
            bloqueios=["Escada Norte", "Escada Sul", "Elevador"],
        )

        self.assertFalse(resultado.encontrou)
        self.assertIn("Não há rota de evacuação segura", resultado.mensagem)

    def test_origem_interditada_avisa_o_usuario(self):
        resultado = self.planejar(
            origem="Corredor A", bloqueios=["Corredor A"]
        )

        self.assertFalse(resultado.encontrou)
        self.assertIn("interditado", resultado.mensagem)

    def test_bloqueios_de_um_calculo_nao_afetam_o_seguinte(self):
        self.planejar(bloqueios=["Elevador"])
        resultado = self.planejar()

        self.assertIn("Elevador", resultado.rota)
        self.assertFalse(self.grafo.local_bloqueado("EL"))


class TestCriteriosNaInterface(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def planejar(self, criterio):
        return rotas.planejar_evacuacao(
            self.grafo,
            origem="Sala 203",
            saida="Saída Principal",
            criterio=criterio,
        )

    def test_cada_criterio_devolve_a_rota_esperada(self):
        self.assertIn("Elevador", self.planejar("Menor tempo").rota)
        self.assertIn("Escada Norte", self.planejar("Menor distância").rota)
        self.assertIn("Escada Sul", self.planejar("Menor dificuldade").rota)
        self.assertIn("Escada Sul", self.planejar("Evacuação segura").rota)

    def test_rotulo_da_tela_e_criterio_interno_dao_o_mesmo_caminho(self):
        self.assertEqual(
            self.planejar("Menor tempo").caminho,
            self.planejar("tempo").caminho,
        )

    def test_criterio_invalido_volta_como_mensagem(self):
        resultado = self.planejar("Menor esforço mental")

        self.assertFalse(resultado.encontrou)
        self.assertIn("Critério desconhecido", resultado.mensagem)


class TestRespostaParaATela(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_metricas_saem_formatadas(self):
        resultado = rotas.planejar_evacuacao(
            self.grafo, origem="Sala 203", saida="Saída Principal"
        )

        self.assertEqual(resultado.tempo_texto, "1 min 26 s")
        self.assertEqual(resultado.distancia_texto, "84 m")
        self.assertEqual(resultado.dificuldade_texto, "5 de 5")

    def test_tempo_curto_aparece_so_em_segundos(self):
        resultado = rotas.planejar_evacuacao(
            self.grafo, origem="Porta Principal", saida="Saída Principal"
        )

        self.assertEqual(resultado.tempo_texto, "6 s")
        self.assertEqual(resultado.distancia_texto, "5 m")

    def test_sem_rota_as_metricas_ficam_vazias(self):
        resultado = rotas.planejar_evacuacao(
            self.grafo,
            origem="Sala 203",
            saida="Saída mais próxima",
            bloqueios=["Escada Norte", "Escada Sul", "Elevador"],
        )

        self.assertEqual(resultado.tempo_texto, "—")
        self.assertEqual(resultado.distancia_texto, "—")
        self.assertEqual(resultado.dificuldade_texto, "—")

    def test_rota_vira_texto_com_setas(self):
        resultado = rotas.planejar_evacuacao(
            self.grafo, origem="Sala 203", saida="Saída Principal"
        )

        self.assertTrue(
            resultado.rota_em_texto().startswith("Sala 203 → Corredor A")
        )

    def test_aceita_codigos_do_grafo(self):
        por_nome = rotas.planejar_evacuacao(
            self.grafo, origem="Sala 203", saida="Saída Principal"
        )
        por_codigo = rotas.planejar_evacuacao(
            self.grafo, origem="S203", saida="SP"
        )

        self.assertEqual(por_nome.caminho, por_codigo.caminho)

    def test_origem_nao_escolhida_pede_selecao(self):
        resultado = rotas.planejar_evacuacao(
            self.grafo, origem="Selecione um local"
        )

        self.assertFalse(resultado.encontrou)
        self.assertIn("Selecione o local de origem", resultado.mensagem)

    def test_local_desconhecido_nao_quebra_a_interface(self):
        resultado = rotas.planejar_evacuacao(
            self.grafo, origem="Heliponto", saida="Saída Principal"
        )

        self.assertFalse(resultado.encontrou)
        self.assertIn("Heliponto", resultado.mensagem)


if __name__ == "__main__":
    unittest.main()
