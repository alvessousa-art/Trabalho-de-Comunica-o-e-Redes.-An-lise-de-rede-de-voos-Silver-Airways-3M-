import networkx as nx
import matplotlib.pyplot as plt
from gerarGrafoDeAeroportosERotas import gerarGrafoDeAeroportosERotas
import sys

dadosDoGrafo = gerarGrafoDeAeroportosERotas()
grafo_silver = dadosDoGrafo["GrafoDeAeroportosERotas"]

#métricas básicas
graus = dict(grafo_silver.degree()).values()
grau_medio = sum(graus) / len(grafo_silver.nodes())
conec_vert = nx.node_connectivity(grafo_silver)
conec_arest = nx.edge_connectivity(grafo_silver)

#Diâmetro e Excentricidade, conectividade
if nx.is_connected(grafo_silver):
    status_conexao = "Conexo"
    diametro = nx.diameter(grafo_silver)
    excentricidades = list(nx.eccentricity(grafo_silver).items())
else:
    status_conexao = "Desconexo"
    maior_componente = max(nx.connected_components(grafo_silver), key=len)
    subgrafo = grafo_silver.subgraph(maior_componente)
    diametro = f"{nx.diameter(subgrafo)} (Maior Comp.)"
    excentricidade_max = f"{max(nx.eccentricity(subgrafo).values())} (Maior Comp.)"

#tabela (matriz)
dados_tabela = [
    ["Métrica", "Resultado"],
    ["Status da Rede", status_conexao],
    ["Grau Médio dos Vértices", f"{grau_medio:.2f}"],
    ["Conectividade de Vértices", str(conec_vert)],
    ["Conectividade de Arestas", str(conec_arest)],
    ["Diâmetro do Grafo", str(diametro)]
    #["Excentricidade Máxima", str(excentricidade_max)]
]

dados_tabela_excentricidade = [["vértice", "execentricidade"]] + excentricidades

#Pontos de articulação
pontos_articulacao = list(nx.articulation_points(grafo_silver))

dados_tabela_pontos_articulacao =  [["vértice"]] + [[x] for x in pontos_articulacao]

#Centralide de intermediação
def byCentralidade (e):
    return e[1]

centralidade_intermediacao = list(nx.betweenness_centrality(grafo_silver).items())
centralidade_intermediacao.sort(key=byCentralidade, reverse=True)
dados_tabela_centralidade_intermediacao = [["Vértice", "Centralidade"]] + centralidade_intermediacao

#Centralidade de proximidade
centralidade_proximidade = list(nx.closeness_centrality(grafo_silver).items())
centralidade_proximidade.sort(key=byCentralidade, reverse=True)
dados_tabela_centralidade_proximidade = [["Vértice", "Centralidade"]] + centralidade_proximidade

#Pontes
pontes = list(list(nx.bridges(grafo_silver)))
dados_tabela_pontes = [["Vértice 1", "vértice 2"]] + pontes

#Comunidades
comunidades = list(nx.community.greedy_modularity_communities(grafo_silver))
dados_tabela_comunidades = [["Comunidade", "Vértices"]]
for i, comunidade in enumerate(comunidades, start=1):
    dados_tabela_comunidades.append([
        i,
        ", ".join(sorted(comunidade))
    ])

def getTabela (dados_tabela, titulo, figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    tabela = ax.table(cellText=dados_tabela, loc='upper center', cellLoc='center', colWidths=[0.4, 0.4])
    tabela.auto_set_font_size(False)
    ax.set_title(titulo, fontweight="bold", fontsize=12, loc='center', y=1.0)
    ncols = len(dados_tabela[0])

    for j in range(ncols):
        tabela[(0, j)].set_facecolor('#e0e0e0')
        tabela[(0, j)].set_text_props(weight='bold')
    return tabela

#Matplotlib, tabela

#Métricas gerais
tabela_metricas = getTabela(dados_tabela, "Métricas da Rede", figsize=(6,4))
tabela_metricas.set_fontsize(8)
tabela_metricas.scale(1, 3)

plt.savefig("images/metricasGerais.jpg", dpi=600)
plt.show()

#Excentricidade
tabela_execentricidades= getTabela(dados_tabela_excentricidade, "Execentricidade dos vértices da Rede - Silver Airways (3M)", figsize=(8, 8))
tabela_execentricidades.set_fontsize(8)
tabela_execentricidades.scale(1.5, 1.5)

plt.savefig("images/execentricidadesDaRede.jpg", dpi=600)
plt.show()

#Pontos de Ariculação
tabela_pontos_articulacao = getTabela(dados_tabela_pontos_articulacao, "Pontos de articulação", figsize=(6,4))

tabela_pontos_articulacao.set_fontsize(8)
tabela_pontos_articulacao.scale(1.5, 1.5)

plt.savefig("images/pontosDeArticulacao.jpg", dpi=600)
plt.show()

#Centralidade de intermdiação
tabela_centralidade_intermediacao = getTabela(dados_tabela_centralidade_intermediacao, "Centralidade de intermediação", figsize=(8,8))

tabela_centralidade_intermediacao.set_fontsize(8)
tabela_centralidade_intermediacao.scale(1.5, 1.5)

plt.savefig("images/centralidadeDeintermediacao.jpg", dpi=600)
plt.show()

#Centralidade de proximidade
tabela_centralidade_proximidade = getTabela(dados_tabela_centralidade_proximidade, "Centralidade de proximidade", figsize=(8,8))

tabela_centralidade_proximidade.set_fontsize(8)
tabela_centralidade_proximidade.scale(1.5, 1.5)

plt.savefig("images/centralidadeDeproximidade.jpg", dpi=600)
plt.show()

#Pontes
tabela_pontes = getTabela(dados_tabela_pontes, "Pontes", figsize=(6,4))

tabela_pontes.set_fontsize(8)
tabela_pontes.scale(1.5, 1.5)

plt.savefig("images/pontes.jpg", dpi=600)
plt.show()

#Comunidades
tabela_comunidades = getTabela(dados_tabela_comunidades, "Comunidades", figsize=(6,4))

tabela_comunidades.set_fontsize(8)
tabela_comunidades.scale(1.5, 1.5)

plt.savefig("images/comunidades.jpg", dpi=600)
plt.show()