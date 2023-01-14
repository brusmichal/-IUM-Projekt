import json
from datetime import datetime
from pathlib import Path

from data_models import SessionEvent, Track, TrackDelay
from utils import unwrap


def generate_delays():
    sessions = load_sessions(Path("IUM22Z_Zad_02_01_v2/sessions.jsonl"))
    tracks = load_tracks(Path("IUM22Z_Zad_02_01_v2/tracks.jsonl"))
    track_delays = calculate_track_delays(sessions, tracks)
    save_track_delays(track_delays, Path("data/track_delays.jsonl"))


def load_sessions(data_path: Path) -> dict[int, list[SessionEvent]]:
    events_json = data_path.read_text().splitlines()
    events: list[SessionEvent] = [json.loads(x) for x in events_json]
    session_ids = {x["session_id"] for x in events}
    sessions = {id: [] for id in session_ids}
    for event in events:
        sessions[event["session_id"]].append(event)
    return sessions


def load_tracks(data_path: Path) -> list[Track]:
    return [json.loads(x) for x in data_path.read_text().splitlines()]


def calculate_track_delays(
    sessions: dict[int, list[SessionEvent]], tracks: list[Track]
) -> list[TrackDelay]:
    tracks_by_id = {x["id"]: x for x in tracks}
    track_ids = (
        set().union(
            *[
                {
                    unwrap(e.get("track_id"))
                    for e in event_list
                    if e.get("track_id") is not None
                }
                for event_list in sessions.values()
            ]
        )
        | tracks_by_id.keys()
    )
    track_delays_lists = {id: [] for id in track_ids}
    for event_list in sessions.values():
        relevant_events = sorted(
            [e for e in event_list if e["event_type"] in {"play", "skip"}],
            key=lambda x: datetime.fromisoformat(x["timestamp"]),
        )
        for i in range(len(relevant_events) - 1):
            event = relevant_events[i]
            event_datetime = datetime.fromisoformat(event["timestamp"])
            next = relevant_events[i + 1]
            next_datetime = datetime.fromisoformat(next["timestamp"])
            if event["event_type"] == "play" and next["event_type"] == "play":
                event_track = tracks_by_id.get(unwrap(event.get("track_id")))
                if event_track is None:
                    continue
                playtime_ms = (next_datetime - event_datetime).total_seconds() * 1000
                delay_ms = playtime_ms - event_track["duration_ms"]
                track_delays_lists[next.get("track_id")].append(delay_ms)
            elif event["event_type"] == "skip" and next["event_type"] == "play":
                delay_ms = (next_datetime - event_datetime).total_seconds() * 1000
                track_delays_lists[next.get("track_id")].append(delay_ms)
    return [
        TrackDelay(track_id=id, avg_delay=sum(delays) / len(delays), delays=delays)
        for id, delays in track_delays_lists.items()
        if len(delays) > 0
    ]


def save_track_delays(track_delays: list[TrackDelay], data_path: Path):
    with open(data_path, "w") as out:
        for delay in sorted(track_delays, key=lambda x: x["track_id"]):
            out.write(json.dumps(delay))
            out.write("\n")
