from typing import Literal

from data_models import ServiceInput, ServiceOutput, Track, TrackAssignment
from predictor.avg_delay_predictor import AvgDelayPredictor
from predictor.daily_cost_predictor import DailyCostPredictor
from service.solver import Solver


def find_solution(
    input: ServiceInput,
    avg_delay_predictor: AvgDelayPredictor,
    daily_cost_predictor: DailyCostPredictor,
) -> ServiceOutput:
    delay_contributions = calculate_fractions_of_all_plays(input["tracks"])
    options = build_options(
        input["tracks"], delay_contributions, avg_delay_predictor, daily_cost_predictor
    )
    solver = Solver(options, input["avg_delay_constraint"])
    return build_output(solver.solve())


def calculate_fractions_of_all_plays(tracks: list[Track]) -> dict[str, float]:
    sum_popularity = sum((x["popularity"] for x in tracks))
    return {x["id"]: x["popularity"] / sum_popularity for x in tracks}


def build_options(
    tracks: list[Track],
    fractions_of_all_plays: dict[str, float],
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
                "fraction_of_all_plays": fractions_of_all_plays[track["id"]],
            },
            "medium": {
                "track_id": track["id"],
                "storage_class": "medium",
                "daily_cost": daily_cost_predictor.predict_daily_cost(track, "medium"),
                "avg_delay": avg_delay_predictor.predict_avg_delay("medium"),
                "fraction_of_all_plays": fractions_of_all_plays[track["id"]],
            },
            "fast": {
                "track_id": track["id"],
                "storage_class": "fast",
                "daily_cost": daily_cost_predictor.predict_daily_cost(track, "fast"),
                "avg_delay": avg_delay_predictor.predict_avg_delay("fast"),
                "fraction_of_all_plays": fractions_of_all_plays[track["id"]],
            },
        }
        for track in tracks
    }


def build_output(solution: list[TrackAssignment]) -> ServiceOutput:
    return {
        "track_assignments": solution,
        "daily_cost": sum((x["daily_cost"] for x in solution)),
        "avg_delay": sum(
            (x["avg_delay"] * x["fraction_of_all_plays"] for x in solution)
        ),
    }
