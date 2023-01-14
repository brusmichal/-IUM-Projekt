import json
from pathlib import Path
from typing import Literal, Protocol

from data_models import Track, TrackForStorage


class DailyCostPredictor(Protocol):
    def predict_daily_cost(
        self, track: Track, storage_class: Literal["slow", "medium", "fast"]
    ) -> float:
        ...


class DailyCostPredictorSimple:
    averages: dict[Literal["slow", "medium", "fast"], float]

    def __init__(self):
        tracks_for_storage: list[TrackForStorage] = [
            json.loads(x)
            for x in Path("data/tracks_for_storage.jsonl").read_text().splitlines()
        ]
        cost_slow = [
            x["daily_cost"] for x in tracks_for_storage if x["storage_class"] == "slow"
        ]
        cost_medium = [
            x["daily_cost"]
            for x in tracks_for_storage
            if x["storage_class"] == "medium"
        ]
        cost_fast = [
            x["daily_cost"] for x in tracks_for_storage if x["storage_class"] == "fast"
        ]
        self.averages = {
            "slow": sum(cost_slow) / len(cost_slow),
            "medium": sum(cost_medium) / len(cost_medium),
            "fast": sum(cost_fast) / len(cost_fast),
        }

    def predict_daily_cost(
        self, track: Track, storage_class: Literal["slow", "medium", "fast"]
    ) -> float:
        return self.averages[storage_class]


class DailyCostPredictorML:
    def predict_daily_cost(
        self, track: Track, storage_class: Literal["slow", "medium", "fast"]
    ) -> float:
        # TODO
        return 0
