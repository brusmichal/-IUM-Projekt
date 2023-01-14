import json
from pathlib import Path

from data.generate_delays import load_tracks
from data.generate_tracks_for_delay import load_track_storage
from models import Track, TrackForStorage, TrackStorage


def generate_tracks_for_storage():
    tracks = load_tracks(Path("IUM22Z_Zad_02_01_v2/tracks.jsonl"))
    track_storage = load_track_storage(Path("IUM22Z_Zad_02_01_v2/track_storage.jsonl"))
    tracks_for_storage = make_tracks_for_storage(tracks, track_storage)
    save_tracks_for_storage(tracks_for_storage, Path("data/tracks_for_storage.jsonl"))


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


def save_tracks_for_storage(tracks_for_storage: list[TrackForStorage], data_path: Path):
    with open(data_path, "w") as out:
        for track in tracks_for_storage:
            out.write(json.dumps(track))
            out.write("\n")
