import pandas as pd 
#Biblioteca básica para formar o grafo
import networkx as nx
#Biblioteca para calcular a distância usando longitue e latitude.
from haversine import haversine
#Biblioteca padrão do python para fins de teste para gerar grafos diferentes de acordo com o argumento passado pela linha de comando no momento da chamada do script

def gerarGrafoDeAeroportosERotas():
    GrafoDeAeroportosERotas = nx.Graph()
    #Dados na forma de um csv 
    #Dados das companhias aéreas
    companhiasAereas = pd.read_csv("airlines.csv")
    #Dados das rotas aéreas
    rotas = pd.read_csv("routes.csv")
    #Dados dos aeroportos
    aeroportos = pd.read_csv("airports.csv")
    
    #Pego as iinformações da silver airways
    silverAirways = companhiasAereas[companhiasAereas[companhiasAereas.columns[1]] == "Silver Airways (3M)"]
    #pego o código IATA dela
    silverAirwaysIATA = silverAirways.iloc[0, 3] 
    
    #Linhas aéreas da silver airways
    rotasDaSilverAirways = rotas[rotas[rotas.columns[0]] == silverAirwaysIATA]
    
    #Vertices e arestas são conjuntos na forma do python, ou seja, um objeto do stipo Set
    verticesDeAeroportos = set()
    arestasDeRotas = set()
    
    #Passo por todas as rotas e pego os aeroportos de origem e e destino, tornando-os em vértices.
    for indice, rota in rotasDaSilverAirways.iterrows():
        #Código IATA do aeroporto de origem
        aeroportoDeOrigem = rota[rotasDaSilverAirways.columns[2]]
        #Código IATA do aeroporto de destino
        aeroportoDeDestino = rota[rotasDaSilverAirways.columns[4]]
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
        
    return {
        "GrafoDeAeroportosERotas": GrafoDeAeroportosERotas,
        "verticesDeAeroportos": verticesDeAeroportos,
        "arestasDeRotas": arestasDeRotas,
        "etiquetas": etiquetas
    }
