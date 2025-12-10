import time
import plotly.graph_objects as go
from typing import Callable

class Rectangle:
    def __init__(self,a:int,b:int):
        self.a = a
        self.b = b

    def __eq__(self, other:object)->bool:
        if isinstance(other,Rectangle):
            return False
        
        return self.a == other.a and self.b == other.b
    
    def __hash__(self) -> int:
        return hash((self.a,self.b))
        
        
                                                           
def time_operation(operation:Callable, n = 1000) -> float:
    start = time.time()
    for i in range(n):
        operation()
    end = time.time()

    return (end - start) / n
    

def createList()-> list[int]:
    a = [5001]
    for i in range(5000):
        a.append(i)

    return a

def time_series(data_sizes:list[int]) -> list[float]:
    times = []

    for size in data_sizes:
        data = list(range(size))
        def operation():
            -1 in data
        time = time_operation(operation)
        times.append(time)
    
    return times

def time_series_set(data_sizes:list[int]) -> list[float]:
    times = []

    for size in data_sizes:
        data = set(range(size))

        time = time_operation(lambda: -1 in data)
        times.append(time)
    
    return times

def main() -> None:
    data_sizes = list(range(1000,10001,1000))

    # Příklad vstupních dat funkce.
    experiments = {
        "in_set": time_series_set(data_sizes),
        "in_list": time_series(data_sizes)
    }

    # Použití funkce
    plot_experiments(experiments, data_sizes)



def plot_experiments(experiments: dict[str, list[float]], x_axis: list[int]) -> None:
    fig = go.Figure()
	
    for method, timings in experiments.items():
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=timings,
            name=method,
        ))
		
    fig.update_layout(
        yaxis={
            "ticksuffix": "s",
            "title": "Time (seconds)",
        }
    )
	
    fig.write_html("complexity_plot.html")
    fig.show()



if __name__ == "__main__":
    main()