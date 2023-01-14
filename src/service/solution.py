from typing import Literal

from data_models import ServiceInput, ServiceOutput, Track, TrackAssignment
from predictor.avg_delay_predictor import AvgDelayPredictor
from predictor.daily_cost_predictor import DailyCostPredictor
from service.solver import Solver


def solve(
    input: ServiceInput,
    avg_delay_predictor: AvgDelayPredictor,
    daily_cost_predictor: DailyCostPredictor,
) -> ServiceOutput:
    delay_contributions = calculate_delay_contributions(input["tracks"])
    options = build_options(
        input["tracks"], delay_contributions, avg_delay_predictor, daily_cost_predictor
    )
    solution = Solver().solve(options)
    return build_output(solution)


def calculate_delay_contributions(tracks: list[Track]) -> dict[str, float]:
    sum_popularity = sum((x["popularity"] for x in tracks))
    return {x["id"]: sum_popularity / len(tracks) for x in tracks}


def build_options(
    tracks: list[Track],
    delay_contributions: dict[str, float],
    avg_delay_predictor: AvgDelayPredictor,
    daily_cost_predictor: DailyCostPredictor,
) -> dict[str, dict[Literal["slow", "medium", "fast"], TrackAssignment]]:
    return {
        track["id"]: {
            "slow": {
                "track_id": track["id"],
                "storage_class": "slow",
                "daily_cost": daily_cost_predictor.predict_daily_cost(track, "slow"),
                "avg_delay": avg_delay_predictor.predict_avg_delay("slow"),
                "avg_delay_contribution": delay_contributions[track["id"]],
            },
            "medium": {
                "track_id": track["id"],
                "storage_class": "medium",
                "daily_cost": daily_cost_predictor.predict_daily_cost(track, "medium"),
                "avg_delay": avg_delay_predictor.predict_avg_delay("medium"),
                "avg_delay_contribution": delay_contributions[track["id"]],
            },
            "fast": {
                "track_id": track["id"],
                "storage_class": "fast",
                "daily_cost": daily_cost_predictor.predict_daily_cost(track, "fast"),
                "avg_delay": avg_delay_predictor.predict_avg_delay("fast"),
                "avg_delay_contribution": delay_contributions[track["id"]],
            },
        }
        for track in tracks
    }


def build_output(solution: list[TrackAssignment]) -> ServiceOutput:
    return {
        "track_assignments": solution,
        "daily_cost": sum((x["daily_cost"] for x in solution)),
        "avg_delay": sum(
            (x["avg_delay"] / x["avg_delay_contribution"] for x in solution)
        ),
    }
