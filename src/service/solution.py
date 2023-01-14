from data_models import ServiceInput, ServiceOutput, Track, TrackForSolution


def solve(input: ServiceInput) -> ServiceOutput:
    tracks_for_solution = calculate_tracks_for_solution(input["tracks"])


def calculate_tracks_for_solution(tracks: list[Track]) -> list[TrackForSolution]:
    sum_popularity = sum((x["popularity"] for x in tracks))
    return [
        {
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
            "avg_delay_contribution": track["popularity"] / sum_popularity,
        }
        for track in tracks
    ]
