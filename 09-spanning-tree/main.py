# TODO 0 pipem nainstalovat
# https://github.com/JakubSido/adthelpers

# pip install git+https://github.com/JakubSido/adthelpers
# nebo stáhnout zip a instalovat jako pip install <cesta_k_rozbalenému_zipu>


import json
from queue import PriorityQueue

import adthelpers


class Graph:
    def __init__(self) -> None:
        self.edges: dict[int, list[tuple[float, int]]] = {}

    def add_edge(self, src: int, dst: int, weight: float = 0) -> None:
        #zkontrolujeme jestli v dictionary máme nějaký bod, pokud ne tak mu uděláme pole, potom přidáme do jeho pole cestu tam i zpátky
        if src not in self.edges:
            self.edges[src] = []
        if dst not in self.edges:
            self.edges[dst] = []
    
        self.edges[src].append((weight,dst))
        self.edges[dst].append((weight,src))


def load_graph(filename: str) -> Graph:
    graph = Graph()

    #načteme json soubor, co vrací dictionary, potom to nějak vyparsujeme a vytvoříme edge, hodíme do magických funkcí a vykreslí to graf

    with open(filename, encoding="utf8") as file:
        json_dat = json.load(file)
        for edge in json_dat["links"]:
            graph.add_edge(edge["source"],edge["target"], edge["weight"])

    return graph


def spanning_tree(graph: Graph) -> None:
    closed: set[int] = set() #kde jsem už byl
    sp_tree: list[tuple[int, int]] = [] # kostra(odkud, kam)
    queue: PriorityQueue = PriorityQueue() 


    painter = adthelpers.painter.Painter(
        graph,
        visible=queue,
        closed=closed,
        color_edges=sp_tree,
    )

    

    queue.put((0,(-1,0))) #přidání fake prvku na start queue


    while not queue.empty() and len(closed) != len(graph.edges):
        weight, (source, curentNode) = queue.get() #popneme z fronty
        

        paths = graph.edges[curentNode] #ziskame všechny cesty co vedou z tohodle nodu

        #Projedeme všechny cesty a přidáme je do fronty, nodu kde jsme teĎ dáme do kostry a do pole kde jsme už byli
        if curentNode not in closed:
            for newWeight,WhereTo in paths:
                queue.put((newWeight,(curentNode,WhereTo)))
            closed.add(curentNode)
            if source != -1:
                sp_tree.append((source,curentNode))

    painter.draw_graph()

    


def main() -> None:
    graph = load_graph("data/graph_grid_s3_3.json")

    painter = adthelpers.painter.Painter(
        graph,
        # colors=("red", "blue", "yellow", "grey") # pokud by byl problém s barvami je možné je změnit
    )
    painter.draw_graph()

    # debug to see progress...
    spanning_tree(graph)

    # don't close before user acknowledges diagrams
    input("Press enter to exit program...")


if __name__ == "__main__":
    main()

