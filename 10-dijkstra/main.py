# TODO 0 pipem nainstalovat
# https://github.com/JakubSido/adthelpers

# pip install git+https://github.com/JakubSido/adthelpers
# nebo stáhnout zip a instalovat jako pip install <cesta_k_rozbalenému_zipu>

import json
from queue import PriorityQueue
from tqdm import tqdm
import adthelpers

import plotly.express as px

class Graph:
    def __init__(self, oriented: bool = False) -> None:
        self.edges: dict[int, list[tuple[float, int]]] = {}
        self.oriented = oriented
        self.edge_count = 0

    def add_edge(self, src: int, dst: int, weight: float = 0) -> None:
        if src not in self.edges:
            self.edges[src] = []
        if dst not in self.edges:
            self.edges[dst] = []
    
        self.edges[src].append((weight,dst))
        self.edges[dst].append((weight,src))
            



    def dijkstra(
        self, start_id: int, end_id: int, show_progress: bool = True,
    ) -> tuple[dict[int, float], dict[int, int]]:
        closed: set[int] = set()
        sp_tree: list[tuple[int, int]] = []
        queue: PriorityQueue = PriorityQueue()

        # navíc
        distances: dict[int, float] = dict()
        predecessors: dict[int, int] = dict()

        for i in self.edges:
            if i not in distances:
                predecessors[i] = -1
                if i == start_id:
                    distances[i] = (0)
                else:
                    distances[i] = float("inf")
        
        #každému prvku v distances nastavíme vzdálenost jako inf
        #v predecesors vše nastavíme jako -1

        if show_progress:
            painter = adthelpers.painter.Painter(
                self,
                visible=queue,
                closed=closed,
                color_edges=sp_tree,
                distances=distances,  # navic
            )
            painter.draw_graph()

        queue.put((0,(-1,start_id)))

        while not queue.empty():
            weight, (source, curentNode) = queue.get() #popnu z fronty

            paths = self.edges[curentNode] #najdu všechny cesty z tohodle nodu

            if curentNode not in closed:

                for newWeight,WhereTo in paths:
                    queue.put((newWeight+weight,(curentNode,WhereTo)))
                closed.add(curentNode) #přidám cesty z téhle nody které mají celkovou váhu cesty, ne jen jedné hrany
                
                if source != -1: #kontrola jestli to není fake prvek
                    sp_tree.append((source, curentNode))

                if source != -1:#zase fake prvek
                    #Pokud najdeme lepší cestu tak tu originální přepíšeme
                    if distances[curentNode] > weight:
                        distances[curentNode] = weight
                        predecessors[curentNode] = source

                #vykreslíme graf
                if show_progress:
                    painter.draw_graph()
            
                #pokud jsme na konci tak gg
                if curentNode == end_id:
                    break

        return distances, predecessors
    

def load_graph(filename: str) -> Graph:
    graph = Graph(oriented=False)

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    for edge in data["links"]:
        node1, node2 = edge["source"], edge["target"]
        graph.add_edge(node1, node2, edge["weight"])

    return graph


def load_graph_csv(filename: str) -> Graph:
    graph = Graph(oriented=True)

    #PARSING WOHOO
    with open(filename, encoding="utf-8") as f:
        f.readline()
        for line in f:
            source, target, weight = line.strip().split(",")
            graph.add_edge(int(source),int(target), float(weight))
    return graph

def reconstruct_path(
    predecessors: dict[int, int], start_id: int, end_id: int,
) -> list[int]:
    path:list[int] = []

    #projedu list od zadu dokud není start_id, pak ho otočím ať mám cestu od startu do konce
    current = end_id

    while current != start_id:
        path.append(current)
        current = predecessors[current]

    path.append(current)
    path.reverse()

    
    return path

def load_nodes_metadata(filename: str) -> dict[int, tuple[str, str]]:
    """Načte metadata o uzlech z CSV souboru. V případě GPS dat je možné zobrazit trasu na mapě pomocí plotly express.
    Returns:
        dict[int, tuple[str, str]]: metadata uzlů (id uzlu, [latitude, longitude])
    """
    node_info = dict()

    #prostě parsing hnusných dat
    with open(filename, encoding="utf-8") as f:
        f.readline()
        for line in f:
            nodeNum, text = line.strip().split(",")

            temp = text.strip().split('(')
            temp = temp[1].strip().split(')')

            wk = temp[0].split(" ")
            node_info[int(nodeNum)] = (wk[0],wk[1])
    return node_info


def show_path(
    node_info: dict[int, tuple[str, str]], # metadata uzlů načtená pomocí load_ndodes_metadata
    path: list[int],
):
    """
    Args:
        node_info (dict[int, tuple[str, str]]): metadata uzlů načtená pomocí load_ndodes_metadata
        path (list[int]): cesta získaná pomocí reconstruct_path
    """
    if node_info:
        lats = [float(la) for la, lo in [node_info[p] for p in path]]
        lons = [float(lo) for la, lo in [node_info[p] for p in path]]

        fig = px.line_mapbox(lat=lats, lon=lons, mapbox_style="open-street-map", zoom=12)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, mapbox_center_lat=49.747)
        fig.show()

def demo() -> None:
    graph = load_graph("graph_grid_s3_3.json")

    # painter = adthelpers.painter.Painter(
    #     graph,
    #     # colors=("red", "blue", "yellow", "grey") # pokud by byl problém s barvami je možné je změnit
    # )
    # painter.draw_graph()
    start = 0
    end = 8
    distances, predecessors = graph.dijkstra(start, end)
    path = reconstruct_path(predecessors, start, end)
    print(path)
    print(distances[end])


def pilsen() -> None:
    edge_file = "pilsen/pilsen_edges_nice.csv"
    node_file = "pilsen/pilsen_nodes.csv"
    graph = load_graph_csv(edge_file)
    start = 4651
    end = 4569
    distances, predecessors = graph.dijkstra(start, end, show_progress=False)
    path = reconstruct_path(predecessors, start, end)
    show_path(
        load_nodes_metadata(node_file),
        path,
    )
    print(path)
    print(distances[end])


def main() -> None:
    #demo()
    pilsen()
    input("...")

if __name__ == "__main__":
    main()

