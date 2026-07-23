#Biblioteca básica para formar o grafo
import networkx as nx
#Biblioteca para a visualização do grafo
import matplotlib.pyplot as plt
#Biblioteca padrão do python para fins de teste para gerar grafos diferentes de acordo com o argumento passado pela linha de comando no momento da chamada do script
import sys

from gerarGrafoDeAeroportosERotas import gerarGrafoDeAeroportosERotas 

#Define o tamanho que o matplotlib irá usar para montar e mostrar o grafo
plt.figure(figsize=(10, 10))
plt.axis("off")

dadosDoGrafoDeAeroportosERotas = gerarGrafoDeAeroportosERotas()
GrafoDeAeroportosERotas = dadosDoGrafoDeAeroportosERotas["GrafoDeAeroportosERotas"]

#Layout é uma variável que diz que como será desenhado o gráfico, existem várias formas de organizar um grafo, o networkx contém algumas delas já feitas, e uma delas é o spring_layout
layout = nx.kamada_kawai_layout(GrafoDeAeroportosERotas, weight=None)
etiquetas = dadosDoGrafoDeAeroportosERotas["etiquetas"]

#Etiquetas dos pesos do grafo
edge_labels = nx.get_edge_attributes(GrafoDeAeroportosERotas, "weight")
#Configurações de visualização
if "airportName" in sys.argv:
    nx.draw_networkx_nodes(GrafoDeAeroportosERotas, pos=layout, node_size=400)
    nx.draw_networkx_edges(GrafoDeAeroportosERotas, pos=layout)
    nx.draw_networkx_labels(GrafoDeAeroportosERotas, pos=layout, labels=etiquetas, font_size=6.5)
    nx.draw_networkx_edge_labels(GrafoDeAeroportosERotas, layout, edge_labels, font_size=7)
else:
    nx.draw_networkx_nodes(GrafoDeAeroportosERotas, pos=layout, node_size=400)
    nx.draw_networkx_edges(GrafoDeAeroportosERotas, pos=layout)
    nx.draw_networkx_labels(GrafoDeAeroportosERotas, pos=layout, font_size=6.5)
    nx.draw_networkx_edge_labels(GrafoDeAeroportosERotas, layout, edge_labels, font_size=7)

#Escolhe se vai salvar como jpg, visualizar ou ambos
plt.title("Grafo de aeroportos e rotas da Silver Airways (3M)")
plt.savefig("images/visualizacao.jpg", dpi=600)
plt.show()
