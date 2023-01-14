from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from datamodels.models import TrackAssignment


class Solver:
    options: dict[str, dict[Literal["slow", "medium", "fast"], TrackAssignment]]
    avg_delay_constraint: float

    def __init__(
        self,
        options: dict[str, dict[Literal["slow", "medium", "fast"], TrackAssignment]],
        avg_delay_constraint: float,
    ) -> None:
        self.options = options
        self.avg_delay_constraint = avg_delay_constraint

    def solve(self) -> list[TrackAssignment]:
        assignments = {key: levels["slow"] for key, levels in self.options.items()}

        delay_to_reduce = (
            sum(
                (
                    x["avg_delay"] * x["fraction_of_all_plays"]
                    for x in assignments.values()
                )
            )
            - self.avg_delay_constraint
        )

        actions: list[MoveAction] = []
        for track_id in self.options.keys():
            actions.extend(self._make_actions_for_track(track_id))
        actions.sort(key=lambda x: x.delay_per_cost, reverse=True)

        while len(actions) > 0 and (actions[-1].cost_diff == 0 or delay_to_reduce > 0):
            action = actions.pop()
            if assignments[action.track_id]["storage_class"] == action.move_from:
                assignments[action.track_id] = self.options[action.track_id][
                    action.move_to
                ]
                delay_to_reduce += action.delay_diff

        return [x for x in assignments.values()]

    def _make_actions_for_track(self, track_id: str) -> list[MoveAction]:
        options = self.options[track_id]
        delay_diff = (
            lambda x, y: options[y]["avg_delay"] * options[y]["fraction_of_all_plays"]
            - options[x]["avg_delay"] * options[x]["fraction_of_all_plays"]
        )
        cost_diff = lambda x, y: options[y]["daily_cost"] - options[x]["daily_cost"]
        return [
            MoveAction(
                track_id=track_id,
                move_from=x,
                move_to=y,
                delay_diff=delay_diff(x, y),
                cost_diff=cost_diff(x, y),
                delay_per_cost=delay_diff(x, y) / cost_diff(x, y)
                if cost_diff(x, y) != 0
                else delay_diff(x, y) * float("inf"),
            )
            for x, y in [("slow", "medium"), ("slow", "fast"), ("medium", "fast")]
        ]


@dataclass
class MoveAction:
    track_id: str
    move_from: Literal["slow", "medium", "fast"]
    move_to: Literal["slow", "medium", "fast"]
    delay_diff: float
    cost_diff: float
    delay_per_cost: float
