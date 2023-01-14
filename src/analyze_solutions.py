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
    simple_solution: ServiceOutput = json.loads(
        Path("data/solution_simple.json").read_text()
    )
    print("simple")
    print(f"avg_delay: {simple_solution['avg_delay']}")
    print(f"daily_cost: {simple_solution['daily_cost']}")
    print()
    main_solution: ServiceOutput = json.loads(
        Path("data/solution_main.json").read_text()
    )
    print("main")
    print(f"avg_delay: {main_solution['avg_delay']}")
    print(f"daily_cost: {main_solution['daily_cost']}")


if __name__ == "__main__":
    analyze_solutions()
