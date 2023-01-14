import json
from multiprocessing import Process
from pathlib import Path
from time import sleep

from service.service import run as run_service
from client import Client
from data_models import ServiceInput


def main():
    service = Process(target=run_service)
    client = Process(target=run_client)
    service.start()
    sleep(1)
    client.start()
    client.join()


def run_client():
    client = Client("127.0.0.1", 8888)
    input = get_input()
    solution_simple = client.get_solution("simple", input)
    Path("data/solution_simple.json").write_text(json.dumps(solution_simple))
    solution_main = client.get_solution("main", input)
    Path("data/solution_main.json").write_text(json.dumps(solution_main))


def get_input() -> ServiceInput:
    tracks = [
        json.loads(x)
        for x in Path("IUM22Z_Zad_02_01_v2/tracks.jsonl").read_text().splitlines()
    ]
    avg_delay_constraint = get_avg_delay_constraint()
    return {"tracks": tracks, "avg_delay_constraint": avg_delay_constraint}


def get_avg_delay_constraint() -> float:
    return 0.0


if __name__ == "__main__":
    main()
