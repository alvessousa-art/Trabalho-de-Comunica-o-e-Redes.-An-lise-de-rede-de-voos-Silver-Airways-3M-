
Trabalho para a disciplina de comunicação e rdes da UFABC.
O script tarefa1.py salva o visualizazao.jpg numa pasta images/, junto o script tarefa2.py também gera uma imagem da tabela e outra imagem adicional caso seja passado um parâmetro extra

Na tarefa1.py é possível usar um parâmetro para renderizar o grafo os nomes dos aeroporto na forma:
> python tarefa1.py airportName 

No tarefa2.py é possível passar um parâemtro para gerar um tabela dum grafo para que seja confirmado e válidado uma anpalise do artigo ao comparar o grafo original com este modelo. Para salvar e mostar esta tabela use:
> python tarefa2.py validar 

Como usar a função gerarGrafoDeAeroportosERotas():
importe ela:
> from gerarGrafoDeAeroportosERotas import gerarGrafoDeAeroportosERotas 

Depois chame ela é atribua a uma variável:

> dadosDoGrafoDeAeroportosERotas = gerarGrafoDeAeroportosERotas()

Ela iria retornar um dicionário com as seguintes propriedades:
- GrafoDeAeroportosERotas: o próprio grafo feito com networkx
- verticesDeAeroportos: um conjunto com vertices que representam cada um aeroporto. Eles são representados pelo código IATA
- arestasDeRotas: um conjunto com arestas que representam as rotas entre aeroportos. Eles são uma tupla com (código IATA do aeroporto de origem, código IATA do aeroporto de desino)