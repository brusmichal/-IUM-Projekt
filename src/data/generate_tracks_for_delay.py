import json
import random
from pathlib import Path
from typing import Literal

from data.generate_delays import load_tracks
from datamodels.models import Track, TrackDelay, TrackForDelay, TrackStorage


def generate_tracks_for_delay():
    delays = load_track_delays()
    tracks = load_tracks()
    track_storage = load_track_storage()
    tracks_for_delay = make_tracks_for_delay(tracks, track_storage, delays)
    divided_tracks_for_delay = divide_tracks_for_delay(tracks_for_delay)
    save_tracks_for_delay(divided_tracks_for_delay)


def load_track_delays() -> list[TrackDelay]:
    return [
        json.loads(x) for x in Path("data/track_delays.jsonl").read_text().splitlines()
    ]


def load_track_storage() -> list[TrackStorage]:
    return [
        json.loads(x)
        for x in Path("IUM22Z_Zad_02_01_v2/track_storage.jsonl")
        .read_text()
        .splitlines()
    ]


def make_tracks_for_delay(
    tracks: list[Track], track_storage: list[TrackStorage], delays: list[TrackDelay]
) -> list[TrackForDelay]:
    storage_by_id = {x["track_id"]: x for x in track_storage}
    delays_by_id = {x["track_id"]: x for x in delays}
    return [
        make_track_for_delay(
            track, storage_by_id[track["id"]], delays_by_id[track["id"]]
        )
        for track in tracks
        if track["id"] in storage_by_id.keys() and track["id"] in delays_by_id.keys()
    ]


def make_track_for_delay(
    track: Track, storage: TrackStorage, delay: TrackDelay
) -> TrackForDelay:
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
        "avg_delay": delay["avg_delay"],
    }


def divide_tracks_for_delay(
    tracks_for_storage: list[TrackForDelay],
) -> dict[Literal["train", "validate"], list[TrackForDelay]]:
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


def save_tracks_for_delay(
    tracks_for_delay: dict[Literal["train", "validate"], list[TrackForDelay]]
):
    with open(Path("data/tracks_for_delay_train.jsonl"), "w") as out:
        for track in sorted(tracks_for_delay["train"], key=lambda x: x["id"]):
            out.write(json.dumps(track))
            out.write("\n")
    with open(Path("data/tracks_for_delay_validate.jsonl"), "w") as out:
        for track in sorted(tracks_for_delay["validate"], key=lambda x: x["id"]):
            out.write(json.dumps(track))
            out.write("\n")
