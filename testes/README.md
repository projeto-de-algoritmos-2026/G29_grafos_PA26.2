# Testes

Cobrem o grafo, o algoritmo e os cenários de emergência. Na raiz do
projeto:

```bash
python -m unittest discover testes
```

| Arquivo | O que verifica |
| -- | -- |
| [contexto.py](./contexto.py) | Deixa `src/` visível para os testes e carrega uma cópia limpa do mapa |
| [test_grafo.py](./test_grafo.py) | Lista de adjacência, bloqueios de passagens e de locais, conversão entre nomes e códigos |
| [test_dijkstra.py](./test_dijkstra.py) | Menor caminho, custo acumulado, critérios de peso, saída mais próxima e métricas |
| [test_cenarios.py](./test_cenarios.py) | Os cenários de emergência pela mesma porta usada pela interface |

## Cenários cobertos

- **Rota normal** — origem e destino sem nenhum bloqueio ativo.
- **Incêndio** — bloquear o elevador e confirmar que a rota recalculada
  usa a Escada Norte.
- **Escada indisponível** — bloquear as duas primeiras opções de descida
  e confirmar o uso da Escada Sul.
- **Saída bloqueada** — bloquear a Saída Principal e confirmar a seleção
  automática da Saída de Emergência.
- **Sem rota segura** — bloquear todas as descidas e confirmar que o
  sistema informa claramente a impossibilidade de evacuar.
- **Critérios de rota** — mesma origem e destino, comparando o caminho
  escolhido por tempo, distância, dificuldade e evacuação segura.
- **Erros do usuário** — origem não escolhida, local inexistente e
  critério inválido voltam como mensagem, sem quebrar a interface.

Os valores esperados (86 s, 84 m, 6 trechos, entre outros) foram
conferidos somando os pesos de `dados/mapa.json` trecho a trecho.
