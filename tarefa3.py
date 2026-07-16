import networkx as nx
import pandas as pd
import math

#calcular a distancia entre as 2 coordenadas (lat e long) (caminho mínimo):
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0 #Raio da terra em KM

    #convertendo graus para radianos
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    #calculo das distancias em relacao a long e lat
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    #usando a formula de haversine que calcula distancias em curva
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distancia = R * c
    return distancia

def main():
    #criar o grafo usando Graph já que o grafo é simples e nao direcionado
    grafo = nx.Graph()

    print("Carregando os dados da Silver Airways (3M)")

    try:
        #ler o arquivo de aerportos, o arquivo nao tem cabecalho
        df_airports = pd.read_csv('airports.csv', header=None)
    except FileNotFoundError:
        print("Erro: Os arquivos CSV não foram encontrados na pasta.")
        return

    #criar dicionario para procurar as coordenadas
    coordenadas = {}
    linhas_ignoradas_airports = 0
    for index, row in df_airports.iterrows():
        try:
            #usando o numero da coluna: 4 p/ sigla, 6 p/ lat e 7 p/lon
            sigla = str(row[4]).strip()

            #pular os aeroportos sem codigo IATA (\N)
            if sigla != '\\N':
                lat = float(row[6])
                lon = float(row[7])
                coordenadas[sigla] = (lat, lon)
        except (ValueError, IndexError, KeyError):
            #se a linha tiver dado inválido (lat/lon quebrado, coluna faltando etc),
            #pula só essa linha e continua processando o restante do arquivo
            linhas_ignoradas_airports += 1
            continue

    if linhas_ignoradas_airports > 0:
        print(f"Aviso: {linhas_ignoradas_airports} linha(s) de airports.csv ignorada(s) por dados inválidos.")

    try:
        #carregar rotas e filtrar pela Silver Airways (3M), arquivo sem cabecalho
        df_routes = pd.read_csv('routes.csv', header=None)
    except FileNotFoundError:
        print("Erro: Os arquivos CSV não foram encontrados na pasta.")
        return

    rotas_adicionadas = 0
    linhas_ignoradas_routes = 0
    for index, row in df_routes.iterrows():
        try:
            comp_aerea = str(row[0]).strip()

            #considerando apenas os voos da Silver Airways (3M)
            if comp_aerea == '3M':
                origem = str(row[2]).strip()
                destino = str(row[4]).strip()

                #ignora rotas onde origem e destino sao o mesmo aeroporto,
                #para o grafo nao ter laco A(exigencia do enunciado: grafo simples)
                if origem == destino:
                    continue

                #para calcular a distancia, ambos os aeroportos tem que possuir coordenadas conhecidas
                if origem in coordenadas and destino in coordenadas:
                    lat_origem, lon_origem = coordenadas[origem]
                    lat_destino, lon_destino = coordenadas[destino]

                    distancia = calcular_distancia(lat_origem, lon_origem, lat_destino, lon_destino)

                    #adiciona a aresta no grafo
                    #como o grafo é simples, a aresta nao sera duplicada se o voo de volta ja for inserido
                    grafo.add_edge(origem, destino, weight=distancia)
                    rotas_adicionadas += 1
        except (ValueError, IndexError, KeyError):
            #pula so a linha de rota problematica, sem abortar o processamento inteiro
            linhas_ignoradas_routes += 1
            continue

    if linhas_ignoradas_routes > 0:
        print(f"Aviso: {linhas_ignoradas_routes} linha(s) de routes.csv ignorada(s) por dados inválidos.")

    print("Grafo construído com sucesso!")
    print(f"Total de aeroportos ativos (vértices): {grafo.number_of_nodes()}")
    print(f"Total de rotas únicas (arestas ponderadas): {grafo.number_of_edges()}")

    #interacao com usuario
    print("BUSCA DE CAMINHO MÍNIMO - SILVER AIRWAYS")

    origem_usuario = input("Digite o código IATA do aeroporto de origem: ").strip().upper()
    destino_usuario = input("Digite o código IATA do aeroporto de destino: ").strip().upper()

    #calculando o caminho minimo
    try:
        #encontrar o menor caminho dos aeroportos com o peso (distancia)
        caminho = nx.shortest_path(grafo, source=origem_usuario, target=destino_usuario, weight='weight')

        #calcula a distancia total percorrida somando os pesos das arestas
        distancia_total = nx.shortest_path_length(grafo, source=origem_usuario, target=destino_usuario, weight='weight')

        print("\n Rota ótima encontrada!")
        print(f"Caminho sugerido: {' -> '.join(caminho)}")
        print(f"Distância total do trajeto: {distancia_total:.2f} km")
        print(f"Número de conexões/escalas: {len(caminho) - 2 if len(caminho) > 2 else 0}")

    except nx.NetworkXNoPath:
        print(f"\n Não existe nenhuma rota viável entre {origem_usuario} e {destino_usuario} na rede da Silver Airways.")
    except nx.NodeNotFound as e:
        print(f"\n Erro: O aeroporto {e} não foi encontrado na base de dados ativa da companhia.")

if __name__ == "__main__":
    main()