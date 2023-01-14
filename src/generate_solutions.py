import json
from multiprocessing import Process
from pathlib import Path
from time import sleep

from client.client import Client
from datamodels.models import ServiceInput, ServiceOutput
from service.service import run_service
from solution.current_solution import get_current_solution


def generate_solutions():
    server = Process(target=run_server)
    client = Process(target=run_client)
    server.start()
    sleep(1)
    client.start()
    client.join()
    server.terminate()


def run_server():
    run_service(8888)


def run_client():
    client = Client("localhost", 8888)
    current_solution = get_current_solution()
    Path("data/solution_current.json").write_text(json.dumps(current_solution))
    input = get_input(current_solution)
    solution_simple = client.get_solution("simple", input)
    Path("data/solution_simple.json").write_text(json.dumps(solution_simple))
    solution_main = client.get_solution("main", input)
    Path("data/solution_main.json").write_text(json.dumps(solution_main))
    solution_ab = client.get_solution_ab(input)
    Path("data/solution_ab_main.json").write_text(json.dumps(solution_ab["main"]))
    Path("data/solution_ab_simple.json").write_text(json.dumps(solution_ab["simple"]))


def get_input(current_solution: ServiceOutput) -> ServiceInput:
    tracks = [
        json.loads(x)
        for x in Path("IUM22Z_Zad_02_01_v2/tracks.jsonl").read_text().splitlines()
    ]
    avg_delay_constraint = current_solution["avg_delay"]
    return {"tracks": tracks, "avg_delay_constraint": avg_delay_constraint}


if __name__ == "__main__":
    generate_solutions()
