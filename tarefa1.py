#Biblioteca para ler os arquivos .csv
import pandas as pd 
#Biblioteca básica para formar o grafo
import networkx as nx
#Biblioteca para a visualização do grafo
import matplotlib.pyplot as plt
#Biblioteca para calcular a distância usando longitue e latitude.
from haversine import haversine
#Biblioteca padrão do python para fins de teste para gerar grafos diferentes de acordo com o argumento passado pela linha de comando no momento da chamada do script
import sys

#Define o tamanho que o matplotlib irá usar para montar e mostrar o grafo
plt.figure(figsize=(10, 10))
plt.axis("off")

GrafoDeAeroportosERotas = nx.Graph()

#Dados na forma de um csv 
#Dados das companhias aéreas
companhiasAereas = pd.read_csv("airlines.csv")
#Dados das rotas aéreas
rotas = pd.read_csv("routes.csv")
#Dados dos aeroportos
aeroportos = pd.read_csv("airports.csv")

#Pego as iinformações da silver airlines
silverAirlines = companhiasAereas[companhiasAereas[companhiasAereas.columns[1]] == "Silver Airways (3M)"]
#pego o código IATA dela
silverAirlinesIATA = silverAirlines.iloc[0, 3] 

#Linhas aéreas da silver airlines
rotasDaSilverAirlines = rotas[rotas[rotas.columns[0]] == silverAirlinesIATA]

#Vertices e arestas são conjuntos na forma do python, ou seja, um objeto do stipo Set
verticesDeAeroportos = set()
arestasDeRotas = set()

#Passo por todas as rotas e pego os aeroportos de origem e e destino, tornando-os em vértices.
for indice, rota in rotasDaSilverAirlines.iterrows():
    #Código IATA do aeroporto de origem
    aeroportoDeOrigem = rota[rotasDaSilverAirlines.columns[2]]
    #Código IATA do aeroporto de destino
    aeroportoDeDestino = rota[rotasDaSilverAirlines.columns[4]]
    
    #Adiciona os aeroportos de origem e destino no conjunto de vertides de aeroportos, como é um conjunto duplicatas são ignoradas
    verticesDeAeroportos.add(aeroportoDeOrigem)
    verticesDeAeroportos.add(aeroportoDeDestino)

    #Adiciona os aeroportos de origem e destino no conjunto de vértices de rotas como uma aresta
    arestasDeRotas.add((aeroportoDeOrigem, aeroportoDeDestino))

GrafoDeAeroportosERotas.add_nodes_from(verticesDeAeroportos)
GrafoDeAeroportosERotas.add_edges_from(arestasDeRotas)

#Passo por todas as arestas já catalogadas pego as informações de longitude a latitude entre os aeroportos e calculo a distânci entre eles e transformando em pesos
for aresta in arestasDeRotas:
    aeroportoDeOrigem = aresta[0]
    aeroportoDeDestino = aresta[1]
    aeroportoDeOrigemDados = aeroportos[aeroportos[aeroportos.columns[4]] == aeroportoDeOrigem].iloc[0]
    aeroportoDeDestinoDados = aeroportos[aeroportos[aeroportos.columns[4]] == aeroportoDeDestino].iloc[0]
    
    #Latitude do aeroporto de origem
    latitudaDaOrigem = aeroportoDeOrigemDados[aeroportos.columns[6]]
    #Longitude do aeroporto de origem
    longitudeDaOrigem = aeroportoDeOrigemDados[aeroportos.columns[7]]

    #Latitude do aeroporto de origem
    latitudaDoDestino = aeroportoDeDestinoDados[aeroportos.columns[6]]
    #Longitude do aeroporto de origem
    longitudeDoDestino = aeroportoDeDestinoDados[aeroportos.columns[7]]

    #Distância entre os dois aeroportos calculados com apoio da biblioteca haversine usando a longitude e latiude.
    distância = haversine((latitudaDaOrigem, longitudeDaOrigem), (latitudaDoDestino, longitudeDoDestino))
    #Adiciona a distância como peso no grafo
    GrafoDeAeroportosERotas.edges[aeroportoDeOrigem, aeroportoDeDestino]["weight"] = float('{0:.2f}'.format(distância))

#É um dicionário em que eu vou correlacionar um vértice que é o aeroporto e seu código IATA com o nome do aeroporto real na forma: {"Nome do aeroporto": }
etiquetas = {}

for indice, aeroporto in aeroportos.iterrows():
    nomeDoAeroporto = aeroporto[aeroportos.columns[1]]
    codigoIATADoAeroporto = aeroporto[aeroportos.columns[4]]

    if codigoIATADoAeroporto in verticesDeAeroportos:
        etiquetas[codigoIATADoAeroporto] = nomeDoAeroporto

#Layout é uma variável que diz que como será desenhado o gráfico, existem várias formas de organizar um grafo, o networkx contém algumas delas já feitas, e uma delas é o spring_layout
layout = nx.kamada_kawai_layout(GrafoDeAeroportosERotas, weight=10)

#Etiquetas dos pesos do grafo
edge_labels = nx.get_edge_attributes(GrafoDeAeroportosERotas, "weight")

#Configurações de visualização
if "airportName" in sys.argv:
    nx.draw_networkx_nodes(GrafoDeAeroportosERotas, pos=layout, node_size=400)
    nx.draw_networkx_edges(GrafoDeAeroportosERotas, pos=layout)
    nx.draw_networkx_labels(GrafoDeAeroportosERotas, pos=layout, labels=etiquetas, font_size=6.5)
    nx.draw_networkx_edge_labels(GrafoDeAeroportosERotas, layout, edge_labels, font_size=5)
else:
    nx.draw_networkx_nodes(GrafoDeAeroportosERotas, pos=layout, node_size=400)
    nx.draw_networkx_edges(GrafoDeAeroportosERotas, pos=layout)
    nx.draw_networkx_labels(GrafoDeAeroportosERotas, pos=layout, font_size=6.5)
    nx.draw_networkx_edge_labels(GrafoDeAeroportosERotas, layout, edge_labels, font_size=5)

#Escolhe se vai salvar como jpg, visualizar ou ambos
if "save" in sys.argv: 
    plt.savefig("visualizacao.jpg", dpi=500)
elif "both" in sys.argv:
    plt.savefig("visualizacao.jpg", dpi=500)
    plt.show()
else:
    plt.show()