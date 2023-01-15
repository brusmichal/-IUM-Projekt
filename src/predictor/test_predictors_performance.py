import json
from pathlib import Path

from datamodels.models import TrackForDelay, TrackForStorage
from predictor.avg_delay_predictor import AvgDelayPredictor
from predictor.daily_cost_predictor import (
    DailyCostPredictor,
    DailyCostPredictorLinearByDuration,
    DailyCostPredictorML,
    DailyCostPredictorSimple,
)


def test_predictors():
    delay_validation_data = [
        json.loads(x)
        for x in Path("data/tracks_for_delay_validate.jsonl").read_text().splitlines()
    ]
    test_avg_delay_predictor(AvgDelayPredictor(), delay_validation_data)

    storage_validation_data = [
        json.loads(x)
        for x in Path("data/tracks_for_storage_validate.jsonl").read_text().splitlines()
    ]
    test_daily_cost_predictor(DailyCostPredictorSimple(), storage_validation_data)
    test_daily_cost_predictor(
        DailyCostPredictorLinearByDuration(), storage_validation_data
    )
    test_daily_cost_predictor(DailyCostPredictorML(), storage_validation_data)


def test_avg_delay_predictor(
    predictor: AvgDelayPredictor, validation_data: list[TrackForDelay]
):
    print(f"{predictor.__class__.__name__} test")
    rel_diffs = []
    for track in validation_data:
        guess = predictor.predict_avg_delay(track["storage_class"])
        actual = track["avg_delay"]
        rel_diff = (guess - actual) / actual
        rel_diffs.append(rel_diff)
    avg_rel_diff = sum(rel_diffs) / len(rel_diffs)
    print(f"average relative difference: {avg_rel_diff}")
    print()


def test_daily_cost_predictor(
    predictor: DailyCostPredictor, validation_data: list[TrackForStorage]
):
    print(f"{predictor.__class__.__name__} test")
    rel_diffs = []
    for track in validation_data:
        guess = predictor.predict_daily_cost(track, track["storage_class"])
        actual = track["daily_cost"]
        rel_diff = (guess - actual) / actual
        rel_diffs.append(rel_diff)
    avg_rel_diff = sum(rel_diffs) / len(rel_diffs)
    print(f"average relative difference: {avg_rel_diff}")
    print()
