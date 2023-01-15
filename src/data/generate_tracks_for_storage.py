import json
import random
from pathlib import Path
from typing import Literal

from data.generate_delays import load_tracks
from data.generate_tracks_for_delay import load_track_storage
from datamodels.models import Track, TrackForStorage, TrackStorage


def generate_tracks_for_storage():
    tracks = load_tracks()
    track_storage = load_track_storage()
    tracks_for_storage = make_tracks_for_storage(tracks, track_storage)
    divided_tracks_for_storage = divide_tracks_for_storage(tracks_for_storage)
    save_tracks_for_storage(divided_tracks_for_storage)


def make_tracks_for_storage(
    tracks: list[Track], track_storage: list[TrackStorage]
) -> list[TrackForStorage]:
    storage_by_id = {x["track_id"]: x for x in track_storage}
    return [
        make_track_for_storage(track, storage_by_id[track["id"]])
        for track in tracks
        if track["id"] in storage_by_id.keys() and track["id"]
    ]


def make_track_for_storage(track: Track, storage: TrackStorage) -> TrackForStorage:
    return {
        "id": track["id"],
        "name": track["name"],
        "popularity": track["popularity"],
        "duration_ms": track["duration_ms"],
        "explicit": track["explicit"],
        "id_artist": track["id_artist"],
        "release_date": track["release_date"],
        "danceability": track["danceability"],
        "energy": track["energy"],
        "key": track["key"],
        "loudness": track["loudness"],
        "speechiness": track["speechiness"],
        "acousticness": track["acousticness"],
        "instrumentalness": track["instrumentalness"],
        "liveness": track["liveness"],
        "valence": track["valence"],
        "tempo": track["tempo"],
        "storage_class": storage["storage_class"],
        "daily_cost": storage["daily_cost"],
    }


def divide_tracks_for_storage(
    tracks_for_storage: list[TrackForStorage],
) -> dict[Literal["train", "validate"], list[TrackForStorage]]:
    tracks_slow = {x["id"] for x in tracks_for_storage if x["storage_class"] == "slow"}
    tracks_medium = {
        x["id"] for x in tracks_for_storage if x["storage_class"] == "medium"
    }
    tracks_fast = {x["id"] for x in tracks_for_storage if x["storage_class"] == "fast"}
    frac_validate = 0.2
    num_validate_slow = int(len(tracks_slow) * frac_validate)
    num_validate_medium = int(len(tracks_medium) * frac_validate)
    num_validate_fast = int(len(tracks_fast) * frac_validate)
    tracks_validate_slow = random.sample(tracks_slow, num_validate_slow)
    tracks_validate_medium = random.sample(tracks_medium, num_validate_medium)
    tracks_validate_fast = random.sample(tracks_fast, num_validate_fast)
    tracks_train_slow = tracks_slow.difference(tracks_validate_slow)
    tracks_train_medium = tracks_medium.difference(tracks_validate_medium)
    tracks_train_fast = tracks_fast.difference(tracks_validate_fast)
    tracks_train = tracks_train_fast.union(tracks_train_medium).union(tracks_train_slow)
    tracks_validate = set(
        tracks_validate_fast + tracks_validate_medium + tracks_validate_slow
    )
    return {
        "train": [x for x in tracks_for_storage if x["id"] in tracks_train],
        "validate": [x for x in tracks_for_storage if x["id"] in tracks_validate],
    }


def save_tracks_for_storage(
    tracks_for_storage: dict[Literal["train", "validate"], list[TrackForStorage]]
):
    with open(Path("data/tracks_for_storage_train.jsonl"), "w") as out:
        for track in sorted(tracks_for_storage["train"], key=lambda x: x["id"]):
            out.write(json.dumps(track))
            out.write("\n")
    with open(Path("data/tracks_for_storage_validate.jsonl"), "w") as out:
        for track in sorted(tracks_for_storage["validate"], key=lambda x: x["id"]):
            out.write(json.dumps(track))
            out.write("\n")
