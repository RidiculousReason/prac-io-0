import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from networkx.generators.community import stochastic_block_model


#Начальные фиксированные параметры:

#SEED = 191191
P_ACTIVATE = 0.05
START_COUNT = 7
ICM_RUNS_COUNT = 20


#SBM-параметры
SBM_SIZES = [500, 300, 200]
P_IN = 0.06
P_OUT = 0.0001

#random.seed(SEED)
#np.random.seed(SEED)


def generate_sbm_graph():
    prob_matrix = [
        [P_IN, P_OUT, P_OUT],
        [P_OUT, P_IN, P_OUT],
        [P_OUT, P_OUT, P_IN]
    ]
    G = stochastic_block_model(SBM_SIZES, prob_matrix) #seed=SEED
    return G


def ICM(G, start_nodes, p=P_ACTIVATE):
    activated = set(start_nodes)
    new_activated = set(start_nodes)
    while new_activated:
        next_activated = set()
        for node in new_activated:
            for neighbor in G.neighbors(node):
                if neighbor not in activated:
                    if random.random() < p:
                        next_activated.add(neighbor)
                        activated.add(neighbor)
        new_activated = next_activated
    return activated

def Running(G, start_nodes, p=P_ACTIVATE, runs=ICM_RUNS_COUNT):
    total_activated = 0
    for _ in range(runs):
        activated = ICM(G, start_nodes, p)
        total_activated += len(activated)
    return total_activated / runs


def visualization_of_diffusion(G, start_nodes, p=P_ACTIVATE):
    activated = ICM(G, start_nodes, p)
    pos = nx.spring_layout(G)  #seed=SEED
    plt.figure(figsize=(10, 7))
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='#898981')
    nx.draw_networkx_nodes(G, pos,
                           node_color='#646DC5', node_size=50, label="Не активированы")

    final_activated = activated - set(start_nodes)
    nx.draw_networkx_nodes(G, pos, nodelist=list(final_activated),
                           node_color='#BA202D', node_size=50,label="Активированы")
    nx.draw_networkx_nodes(G, pos, nodelist=list(start_nodes),
                           node_color='#C5C31A', node_size=100,label="Начальные")

    plt.title("Визуализация одного прогона")
    plt.legend()
    plt.axis('off')
    plt.show()


G = generate_sbm_graph()
start_nodes = random.sample(list(G.nodes()), START_COUNT)
ICM_result = Running(G, start_nodes)
print("Средний охват (количество активированных вершин) при фиксированных случайных", ICM_result,
      "\nпри", ICM_RUNS_COUNT, "прогонах")
visualization_of_diffusion(G, start_nodes, P_ACTIVATE)
