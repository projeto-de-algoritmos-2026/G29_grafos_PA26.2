# Como executar

> Projeto em fase inicial. Este arquivo será atualizado conforme cada módulo
> for implementado.

## Pré-requisitos

- Python 3.10 ou superior.
- Nenhuma dependência externa por enquanto — o projeto usa apenas
  bibliotecas padrão (`heapq`, `json`). Caso a interface gráfica passe a
  usar uma biblioteca externa (ex.: alguma alternativa ao `tkinter`), ela
  será listada aqui e em um `requirements.txt`.

## Obtendo o projeto

```bash
git clone <url-do-repositorio>
cd G29_grafos_PA26.2
```

## Executando

A partir da raiz do repositório:

```bash
python src/main.py
```

No estado atual, isso apenas confirma que o ponto de entrada está
funcionando (o carregamento do mapa, o cálculo de rota e a interface ainda
são placeholders — `TODO`s nos respectivos módulos).

## Estrutura de pastas

```
dados/    -> mapa.json: locais, conexões e pesos do prédio fictício
src/      -> código-fonte (grafo, dijkstra, interface, main)
testes/   -> casos de teste (normais, bloqueios, critérios, sem rota)
docs/     -> documentação do projeto (este arquivo e CONTEXTO.md)
```

## Executando os testes

Ainda não há testes automatizados — os casos planejados estão descritos em
[testes/README.md](../testes/README.md). Quando implementados, deverão
rodar com:

```bash
python -m unittest discover testes
```
