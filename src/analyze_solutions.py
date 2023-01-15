import json
from pathlib import Path

from datamodels.models import ServiceOutput


def analyze_solutions():
    current_solution: ServiceOutput = json.loads(
        Path("data/solution_current.json").read_text()
    )
    print("current")
    print(f"avg_delay: {current_solution['avg_delay']}")
    print(f"daily_cost: {current_solution['daily_cost']}")
    print()

    avg_solution: ServiceOutput = json.loads(
        Path("data/solution_avg.json").read_text()
    )
    print("avg")
    print(f"avg_delay: {avg_solution['avg_delay']}")
    print(f"daily_cost: {avg_solution['daily_cost']}")
    print()

    linear_solution: ServiceOutput = json.loads(
        Path("data/solution_linear.json").read_text()
    )
    print("linear")
    print(f"avg_delay: {linear_solution['avg_delay']}")
    print(f"daily_cost: {linear_solution['daily_cost']}")
    print()


if __name__ == "__main__":
    analyze_solutions()
