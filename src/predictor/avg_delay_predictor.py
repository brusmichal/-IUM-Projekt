import json
from pathlib import Path
from typing import Literal

from datamodels.models import TrackForDelay


class AvgDelayPredictor:
    averages: dict[Literal["slow", "medium", "fast"], float]

    def __init__(self):
        tracks_for_delay: list[TrackForDelay] = [
            json.loads(x)
            for x in Path("data/tracks_for_delay.jsonl").read_text().splitlines()
        ]
        delays_slow = [
            x["avg_delay"] for x in tracks_for_delay if x["storage_class"] == "slow"
        ]
        delays_medium = [
            x["avg_delay"] for x in tracks_for_delay if x["storage_class"] == "medium"
        ]
        delays_fast = [
            x["avg_delay"] for x in tracks_for_delay if x["storage_class"] == "fast"
        ]
        self.averages = {
            "slow": sum(delays_slow) / len(delays_slow),
            "medium": sum(delays_medium) / len(delays_medium),
            "fast": sum(delays_fast) / len(delays_fast),
        }

    def predict_avg_delay(
        self, storage_class: Literal["slow", "medium", "fast"]
    ) -> float:
        return self.averages[storage_class]
