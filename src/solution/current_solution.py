from data.generate_delays import load_tracks
from data.generate_tracks_for_storage import load_track_storage
from datamodels.models import ServiceOutput, TrackAssignment
from predictor.avg_delay_predictor import AvgDelayPredictor


def get_current_solution() -> ServiceOutput:
    tracks = load_tracks()
    track_storage = load_track_storage()
    track_storage_by_id = {x["track_id"]: x for x in track_storage}
    avg_delay_predictor = AvgDelayPredictor()
    sum_popularity = sum((x["popularity"] for x in tracks))
    track_assignments: list[TrackAssignment] = [
        {
            "track_id": track["id"],
            "storage_class": track_storage_by_id[track["id"]]["storage_class"],
            "daily_cost": track_storage_by_id[track["id"]]["daily_cost"],
            "avg_delay": avg_delay_predictor.predict_avg_delay(
                track_storage_by_id[track["id"]]["storage_class"]
            ),
            "fraction_of_all_plays": track["popularity"] / sum_popularity,
        }
        for track in tracks
    ]
    return {
        "track_assignments": track_assignments,
        "avg_delay": sum(
            (x["avg_delay"] * x["fraction_of_all_plays"] for x in track_assignments)
        ),
        "daily_cost": sum((x["daily_cost"] for x in track_assignments)),
    }
