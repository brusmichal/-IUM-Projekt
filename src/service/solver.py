import random
from typing import Literal

from scipy import optimize

from data_models import TrackAssignment


class Solver:
    options: dict[str, dict[Literal["slow", "medium", "fast"], TrackAssignment]]
    tracks: list[str]
    classes = ["slow", "medium", "fast"]

    def __init__(
        self,
        options: dict[str, dict[Literal["slow", "medium", "fast"], TrackAssignment]],
    ) -> None:
        self.options = options
        self.tracks = [x for x in self.options.keys()]

    def solve(self) -> list[TrackAssignment]:
        pass

    def low_bound_optimistic_solution(self) -> list[TrackAssignment]:
        x0 = [random.randint(0, 2) for _ in self.tracks]
        fun = lambda x: self.objective_function(x)
        optimize.minimize(fun=fun, x0=x0, bounds=[(0, 2) for _ in x0])

    def objective_function(self, x: list[int]) -> float:
        return sum(
            (
                self.options[track_id][choice]["daily_cost"]
                for track_id, choice in zip(self.tracks, x)
            )
        )
