import matplotlib.pyplot as plt
import networkx as nx

# 输入数据
data = {
    "r": [1, 2, 3, 4],
    "p": {
        "1": [1001, 1002,1003,1004,1005],
        "2": [1201, 1202,1203,1204,1205],
        "3": [1301, 1302,1303,1304,1305],
        "4": [1401, 1402,1403,1404,1405]
    }
}

# 创建无向图
G = nx.Graph()

# 添加r中的节点并两两相连
for node in data["r"]:
    G.add_node(f"r{node}")
for i in range(len(data["r"])):
    for j in range(i + 1, len(data["r"])):
        G.add_edge(f"r{data['r'][i]}", f"r{data['r'][j]}")

# 添加p中的节点并根据对应关系相连
for r_node, p_nodes in data["p"].items():
    for p_node in p_nodes:
        G.add_node(f"p{p_node}")
        G.add_edge(f"r{r_node}", f"p{p_node}")

# 使用shell_layout大致放置节点
r_nodes = [f"r{node}" for node in data["r"]]
p_nodes = [f"p{p_node}" for p_nodes in data["p"].values() for p_node in p_nodes]
initial_pos = nx.shell_layout(G, nlist=[r_nodes, p_nodes])

# 使用spring_layout进一步优化边长
pos = nx.spring_layout(G, pos=initial_pos, fixed=r_nodes, k=1.5, iterations=500)

# 绘制图形
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=3000, font_size=12, font_weight='bold')
plt.title("Topology Graph with Shortest Edges")
plt.show()
