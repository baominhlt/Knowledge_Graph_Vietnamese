import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def print_kg(kg):
    source = [word[0] for word in kg]
    target = [word[2] for word in kg]
    edge = [word[1] for word in kg]
    kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':edge})
    G=nx.from_pandas_edgelist(kg_df, "source", "target",
                          edge_attr=True, create_using=nx.MultiDiGraph())
    plt.figure(figsize=(12,12))

    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
    plt.show()

kg = []
with open('knowledge_graph_saving_file', 'r', encoding='utf-8') as f:
    f.readline()
    while f.readable():
        kg.append(f.readline().replace('[','').replace("'","").replace(']','').replace('\n','').split(', '))

print_kg(kg)