import networkx as nx
# importando a função do arquivo para reaproveitar o grafo pronto
from gerarGrafoDeAeroportosERotas import gerarGrafoDeAeroportosERotas 

def main():
    print("=== Iniciando o Sistema de Rotas ===")
    print("Carregando o grafo de aeroportos e rotas...")

    try:
        # puxo o dicionário completo que a função dele retorna
        dados_projeto = gerarGrafoDeAeroportosERotas()
        
        # extraio o grafo com as rotas e distâncias (pesos) já calculadas por haversine
        grafo = dados_projeto["GrafoDeAeroportosERotas"]
        
        # extraio as etiquetas com o para código e IATA e nome do aeroporto para a visualização
        etiquetas = dados_projeto["etiquetas"]
        
    except Exception as e:
        print(f"Erro ao carregar o grafo: {e}")
        return

    # feedback visual para ver se os dados carregaram corretamente
    print("Grafo carregado com sucesso!")
    print(f"Total de aeroportos (vértices): {grafo.number_of_nodes()}")
    print(f"Total de rotas disponíveis (arestas): {grafo.number_of_edges()}")
    print("Aeroportos disponíveis junto de seu código IATA")
    for IATA in etiquetas:
        print(f"{IATA}: {etiquetas[IATA]}")

    # interação com o usuário para buscar o menor caminho
    print("BUSCA DE CAMINHO MÍNIMO - AEROPORTOS")
    
    # pego as entradas do usuário, limpo os espaços e coloco em maiúsculo (padrão IATA)
    origem_usuario = input("Digite o código IATA de origem: ").strip().upper()
    destino_usuario = input("Digite o código IATA de destino: ").strip().upper()

    # tentativa de cálculo do caminho mínimo usando os pesos do grafo
    try:
        # o networkx vai olhar o atributo 'weight' 
        caminho = nx.shortest_path(grafo, source=origem_usuario, target=destino_usuario, weight='weight')

        # aqui ele soma esses mesmos pesos para nos dar a quilometragem total do trajeto
        distancia_total = nx.shortest_path_length(grafo, source=origem_usuario, target=destino_usuario, weight='weight')

        # mostra o resultado na tela
        print("\n=== Rota Ótima Encontrada! ===")
        print(f"Caminho sugerido: {' -> '.join(caminho)}")
        print(f"Distância total: {distancia_total:.2f} km")
        
        # cálculo de escalas: se o caminho tem 3 aeroportos (A -> B -> C), teve 1 escala (3 - 2 = 1)
        escalas = len(caminho) - 2 if len(caminho) > 2 else 0
        print(f"Número de conexões/escalas: {escalas}")

    except nx.NetworkXNoPath:
        # se os aeroportos existem no grafo, mas não tem nenhuma linha aérea ligando eles
        print(f"\n[Aviso] Não existe nenhuma rota disponível entre {origem_usuario} e {destino_usuario}.")
        
    except nx.NodeNotFound as erro:
        # se o usuário digitou uma sigla de aeroporto que nem sequer existe na base de dados
        print(f"\n[Erro] O aeroporto {erro} não foi encontrado na base de dados ativa.")

if __name__ == "__main__":
    main()