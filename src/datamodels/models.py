from __future__ import annotations

from typing import Literal, TypedDict

from typing_extensions import NotRequired


class SessionEvent(TypedDict):
    session_id: int
    timestamp: str
    user_id: str
    track_id: NotRequired[str]
    event_type: Literal["play", "like", "skip", "advertisment"]


class Track(TypedDict):
    id: str
    name: str
    popularity: int
    duration_ms: int
    explicit: int
    id_artist: str
    release_date: str
    danceability: float
    energy: float
    key: int
    loudness: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float


class TrackStorage(TypedDict):
    track_id: str
    storage_class: Literal["slow", "medium", "fast"]
    daily_cost: float


class TrackForStorage(Track):
    storage_class: Literal["slow", "medium", "fast"]
    daily_cost: float


class TrackForDelay(Track):
    storage_class: Literal["slow", "medium", "fast"]
    avg_delay: float


class TrackDelay(TypedDict):
    track_id: str
    avg_delay: float
    delays: list[float]


class ServiceInput(TypedDict):
    tracks: list[Track]
    avg_delay_constraint: float


class ServiceOutput(TypedDict):
    track_assignments: list[TrackAssignment]
    daily_cost: float
    avg_delay: float


class TrackAssignment(TypedDict):
    track_id: str
    storage_class: Literal["slow", "medium", "fast"]
    daily_cost: float
    avg_delay: float
    fraction_of_all_plays: float


class ServiceOutputAB(TypedDict):
    a: ServiceOutput
    b: ServiceOutput
