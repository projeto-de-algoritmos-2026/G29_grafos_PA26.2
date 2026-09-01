# Testes planejados

Ainda sem testes automatizados. Casos previstos, a implementar junto com
`grafo.py` e `dijkstra.py` (ver [../docs/CONTEXTO.md](../docs/CONTEXTO.md)):

- **Rota normal** — origem e destino sem nenhum bloqueio ativo.
- **Bloqueio simples** — bloquear um corredor e confirmar que a rota
  recalculada usa um caminho alternativo.
- **Escada indisponível** — bloquear uma escada e confirmar o uso de outra
  escada ou do elevador.
- **Saída bloqueada** — bloquear a saída padrão e confirmar a seleção
  automática da outra saída.
- **Sem rota segura** — bloquear todos os caminhos possíveis e confirmar
  que o sistema informa claramente a impossibilidade de evacuar.
- **Critérios de rota** — mesma origem/destino, comparando o caminho
  escolhido para tempo, distância e dificuldade.

Quando os primeiros testes existirem, devem rodar com:

```bash
python -m unittest discover testes
```
