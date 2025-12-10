import random
from collections import deque

class NamedQueue:
    def __init__(self,name:str):
        self.name = name
        self.q:deque[int] = deque()

    def append(self,item:int):
        self.q.append(item)

class ProcessingNode:
    def __init__(
        self, name: str, period: int, source: NamedQueue, destination: NamedQueue, sigma: float = 0.1):
        self.name = name
        self.period = period
        self.source = source
        self.destination = destination
        self.sigma = sigma

        self.remaining_time = self.next_occur_in()

    def perform(self) -> None:
        if len(self.source.q) > 0:
            temp = self.source.q.popleft()
            self.destination.q.append(temp)

    def next_occur_in(self) -> int:
        return int(abs(random.gauss(self.period, self.sigma)))
    
    def tick(self) -> None:
        self.remaining_time -= 1

        if self.remaining_time <= 0:
            self.perform()
            self.remaining_time = self.next_occur_in()

class Observer:
    def __init__(self,listToObserve:list[NamedQueue]):
        self.listQ = listToObserve
        
    def showQueue(self):
        for queue in self.listQ:
            print(f"{queue.name}({len(queue.q)})->",end="")
        print()

    
def main():
    listObserve = []
    street_q = NamedQueue("street")
    street_q.q = deque(list(range(10000)))

    gate = NamedQueue("start")
    vege_q = NamedQueue("vege")
    final_q = NamedQueue("register queue")
    final_final_q = NamedQueue("end")

    street = ProcessingNode("carts",50,street_q,gate,0.6)
    entrance = ProcessingNode("entry",10,gate,vege_q,0.2)
    vege = ProcessingNode("weighting", 300, vege_q, final_q,0.3)
    void = ProcessingNode("end", 10, final_q, final_final_q,0.5)

    listObserve.append(gate)
    listObserve.append(vege_q)
    listObserve.append(final_q)
    listObserve.append(final_final_q)
    observe = Observer(listObserve)

    for sec in range(60 * 60 * 50):
        street.tick()
        entrance.tick()
        vege.tick()
        void.tick()
        observe.showQueue()
    
        
if __name__ == '__main__':
    main()

