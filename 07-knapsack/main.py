from dataclasses import dataclass
from utils import measure_time
import functools

@dataclass
class Song:
    rating: float
    length: int

def load_songs(file_path:str) -> list[Song]:
    songs: list[Song] = []

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            attributes = line.strip().split(" ")

            minutes, seconds = attributes[1].split(":")
            time = int(seconds) + int(minutes) * 60

            rating = float(attributes[0])

            songs.append(Song(rating,time))
            
    return songs


#funkce k uvnitř je kvůli tomu že nemusíme posílat pokaždý list songu
def knapsack(songs: list[Song], remaining_time: int) -> float:
    @functools.cache
    def k(n:int, remaining_time: int) -> float:
        if remaining_time <= 0 or n >= len(songs):
            return 0
        
        if songs[n].length > remaining_time:
            return k(n+1, remaining_time)

        return max(
            k(n+1, remaining_time),#neberu
            songs[n].rating + k(n+1, remaining_time - songs[n].length))#beru
    
    return k(0, remaining_time)


def main():
    songs = load_songs("data/songs copy.txt")
    total_rating = measure_time(lambda: knapsack(songs, 4 * 60),5)
    print(total_rating)

if __name__ == "__main__":
    main()