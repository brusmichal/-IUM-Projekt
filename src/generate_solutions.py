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
    solution_avg = client.get_solution("avg", input)
    Path("data/solution_avg.json").write_text(json.dumps(solution_avg))
    solution_linear = client.get_solution("linear", input)
    Path("data/solution_linear.json").write_text(json.dumps(solution_linear))
    solution_ab = client.get_solution_ab("avg", "linear", input)
    Path("data/solution_ab_avg_linear.json").write_text(json.dumps(solution_ab))


def get_input(current_solution: ServiceOutput) -> ServiceInput:
    tracks = [
        json.loads(x)
        for x in Path("IUM22Z_Zad_02_01_v2/tracks.jsonl").read_text().splitlines()
    ]
    avg_delay_constraint = current_solution["avg_delay"]
    return {"tracks": tracks, "avg_delay_constraint": avg_delay_constraint}


if __name__ == "__main__":
    generate_solutions()
