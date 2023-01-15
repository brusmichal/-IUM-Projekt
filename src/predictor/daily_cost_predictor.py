import json
from pathlib import Path
from typing import Literal, Protocol

from datamodels.models import Track, TrackForStorage


class DailyCostPredictor(Protocol):
    def predict_daily_cost(
        self, track: Track, storage_class: Literal["slow", "medium", "fast"]
    ) -> float:
        ...


class DailyCostPredictorAvg:
    averages: dict[Literal["slow", "medium", "fast"], float]

    def __init__(self):
        tracks_for_storage: list[TrackForStorage] = [
            json.loads(x)
            for x in Path("data/tracks_for_storage_train.jsonl")
            .read_text()
            .splitlines()
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


class DailyCostPredictorLinearByDuration:
    average_per_duration: dict[Literal["slow", "medium", "fast"], float]

    def __init__(self):
        tracks_for_storage: list[TrackForStorage] = [
            json.loads(x)
            for x in Path("data/tracks_for_storage_train.jsonl")
            .read_text()
            .splitlines()
        ]
        cost_per_duration_slow = [
            x["daily_cost"] / x["duration_ms"]
            for x in tracks_for_storage
            if x["storage_class"] == "slow"
        ]
        cost_per_duration_medium = [
            x["daily_cost"] / x["duration_ms"]
            for x in tracks_for_storage
            if x["storage_class"] == "medium"
        ]
        cost_per_duration_fast = [
            x["daily_cost"] / x["duration_ms"]
            for x in tracks_for_storage
            if x["storage_class"] == "fast"
        ]
        self.average_per_duration = {
            "slow": sum(cost_per_duration_slow) / len(cost_per_duration_slow),
            "medium": sum(cost_per_duration_medium) / len(cost_per_duration_medium),
            "fast": sum(cost_per_duration_fast) / len(cost_per_duration_fast),
        }

    def predict_daily_cost(
        self, track: Track, storage_class: Literal["slow", "medium", "fast"]
    ) -> float:
        return self.average_per_duration[storage_class] * track["duration_ms"]
