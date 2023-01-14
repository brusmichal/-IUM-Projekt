import json
from pathlib import Path

from data.generate_delays import load_tracks
from models import Track, TrackDelay, TrackForDelay, TrackStorage


def generate_tracks_for_delay():
    delays = load_track_delays(Path("data/track_delays.jsonl"))
    tracks = load_tracks(Path("IUM22Z_Zad_02_01_v2/tracks.jsonl"))
    track_storage = load_track_storage(Path("IUM22Z_Zad_02_01_v2/track_storage.jsonl"))
    tracks_for_delay = make_tracks_for_delay(tracks, track_storage, delays)
    save_tracks_for_delay(tracks_for_delay, Path("data/tracks_for_delay.jsonl"))


def load_track_delays(data_path: Path) -> list[TrackDelay]:
    return [json.loads(x) for x in data_path.read_text().splitlines()]


def load_track_storage(data_path: Path) -> list[TrackStorage]:
    return [json.loads(x) for x in data_path.read_text().splitlines()]


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


def save_tracks_for_delay(tracks_for_delay: list[TrackForDelay], data_path: Path):
    with open(data_path, "w") as out:
        for track in tracks_for_delay:
            out.write(json.dumps(track))
            out.write("\n")
