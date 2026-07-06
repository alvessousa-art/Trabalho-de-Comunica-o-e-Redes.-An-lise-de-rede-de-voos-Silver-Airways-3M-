Tarefa 1</br>
Para visualizar o grafo rode o arquivo tarefa1.py. Exemplo:
> python tarefa1.py

É possível usar outro parâmetros na forma:
> python tarefa1.py "lista de parâmetros"

Parâmetros:
- save - Salva o grafo ao ínves de abrir uma janela para visualizá-lo
- both - Salva e abre a a janela
- airportName - Gera o grafo com as etiquetas do vertices como o nome dos respectivos aeroportos ao ínves do código IATA.

Como usar a função gerarGrafoDeAeroportosERotas():
importe ela:
> from gerarGrafoDeAeroportosERotas import gerarGrafoDeAeroportosERotas 

Depois chame ela é atribua a uma variável:

> dadosDoGrafoDeAeroportosERotas = gerarGrafoDeAeroportosERotas()

Ela iria retornar um dicionário com as seguintes propriedades:
- GrafoDeAeroportosERotas: o próprio grafo feito com networkx
- verticesDeAeroportos: um conjunto com vertices que representam cada um aeroporto. Eles são representados pelo código IATA
- arestasDeRotas: um conjunto com arestas que representam as rotas entre aeroportos. Eles são uma tupla com (código IATA do aeroporto de origem, código IATA do aeroporto de desino)