from utils import measure_time
import functools


#Rekurzivni fibonaci
def fib(n: int) -> int:
    if n <= 1:
        return n
    
    return fib(n-1) + fib(n-2)


#Rekurzivni fibonaci který ukládá prvky do dictionary a bere je z toho
def fib_mem(n:int, lookup:dict[int,int]) -> int:
    if n <= 1:
        return n
    
    if n in lookup:
        return lookup[n]
    else:
        return fib_mem(n-1, lookup) + fib_mem(n-2, lookup)


#rekurzivní fibonaci co pouziva cache
@functools.cache
def fib_cache(n: int) -> int:
    if n <= 1:
        return n
    
    return fib_cache(n-1) + fib_cache(n-2)

def main():
    n = 30
    
    #utils potrebuje neco callable bez argumentu-> pouzijeme wraper classu nebo lambdu
    def noArgument() -> int:
        return fib(n)

    print(measure_time(noArgument,3))
    print(measure_time(lambda: fib_mem(n, {}),3))
    print(measure_time(lambda: fib_cache(n),3))
    


if __name__ == "__main__":
    main()