import json

from pathlib import Path
from random import randint

def main():
    analyze_sessions()
    analyze_tracks()
    analyze_track_storage()
    analyze_track_costs()


def analyze_sessions():
    input = Path("sessions.jsonl").read_text().splitlines()
    sessions = []
    for line in input:
        session = json.loads(line)
        sessions.append(session)

    print("-- sessions.jsonl")
    
    # null userid
    userid_nones = 0
    for session in sessions:
        if session.get("user_id") is None:
            userid_nones += 1
    print(f"Ilość nulli w userid: {userid_nones}")
    
    # types
    types = set()
    for session in sessions:
        types.add(session.get("event_type"))
    print(f"Typy eventów w sesjach: {types}")

    # null type
    timestamps_nones = 0
    for session in sessions:
        if session.get("timestamp") is None:
            timestamps_nones += 1
    print(f"Ilość nulli w timestampach: {timestamps_nones}")

    # null timestamp
    timestamps_nones = 0
    for session in sessions:
        if session.get("timestamp") is None:
            timestamps_nones += 1
    print(f"Ilość nulli w timestampach: {timestamps_nones}")

    print()


def analyze_tracks():
    input = Path("tracks.jsonl").read_text().splitlines()
    tracks = []
    for line in input:
        track = json.loads(line)
        tracks.append(track)

    print("-- tracks.jsonl")
    
    # null id
    id_nones = 0
    for track in tracks:
        if track.get("id") is None:
            id_nones += 1
    print(f"Ilość nulli w id: {id_nones}")

    # popularity
    popularity_min = None
    popularity_max = None
    for track in tracks:
        popularity = track.get("popularity")
        if popularity is not None:
            if popularity_min is None or popularity < popularity_min:
                popularity_min = popularity
            if popularity_max is None or popularity > popularity_max:
                popularity_max = popularity
    print(f"Zakres popularity: {popularity_min} - {popularity_max}")

    # explicit
    explicits = set()
    for track in tracks:
        explicits.add(track.get("explicit"))
    print(f"Wartości explicit: {explicits}")

    # release_dates
    release_date_sample_size = 30
    release_dates = set()
    for _ in range(release_date_sample_size):
        index = randint(0, len(tracks) - 1)
        track = tracks[index]
        release_dates.add(track.get("release_date"))
    print(f"Próbka wartości release_date: {release_dates}")

    # danceability
    danceability_min = None
    danceability_max = None
    for track in tracks:
        danceability = track.get("danceability")
        if danceability is not None:
            if danceability_min is None or danceability < danceability_min:
                danceability_min = danceability
            if danceability_max is None or danceability > danceability_max:
                danceability_max = danceability
    print(f"Zakres danceability: {danceability_min} - {danceability_max}")

    # energy
    energy_min = None
    energy_max = None
    for track in tracks:
        energy = track.get("energy")
        if energy is not None:
            if energy_min is None or energy < energy_min:
                energy_min = energy
            if energy_max is None or energy > energy_max:
                energy_max = energy
    print(f"Zakres energy: {energy_min} - {energy_max}")

    # key
    keys = set()
    for track in tracks:
        keys.add(track.get("key"))
    print(f"Wartości key: {keys}")

    # loudness
    loudness_min = None
    loudness_max = None
    for track in tracks:
        loudness = track.get("loudness")
        if loudness is not None:
            if loudness_min is None or loudness < loudness_min:
                loudness_min = loudness
            if loudness_max is None or loudness > loudness_max:
                loudness_max = loudness
    print(f"Zakres loudness: {loudness_min} - {loudness_max}")

    # speechiness
    speechiness_min = None
    speechiness_max = None
    for track in tracks:
        speechiness = track.get("speechiness")
        if speechiness is not None:
            if speechiness_min is None or speechiness < speechiness_min:
                speechiness_min = speechiness
            if speechiness_max is None or speechiness > speechiness_max:
                speechiness_max = speechiness
    print(f"Zakres speechiness: {speechiness_min} - {speechiness_max}")

    # acousticness
    acousticness_min = None
    acousticness_max = None
    for track in tracks:
        acousticness = track.get("acousticness")
        if acousticness is not None:
            if acousticness_min is None or acousticness < acousticness_min:
                acousticness_min = acousticness
            if acousticness_max is None or acousticness > acousticness_max:
                acousticness_max = acousticness
    print(f"Zakres acousticness: {acousticness_min} - {acousticness_max}")

    # instrumentalness
    instrumentalness_min = None
    instrumentalness_max = None
    for track in tracks:
        instrumentalness = track.get("instrumentalness")
        if instrumentalness is not None:
            if instrumentalness_min is None or instrumentalness < instrumentalness_min:
                instrumentalness_min = instrumentalness
            if instrumentalness_max is None or instrumentalness > instrumentalness_max:
                instrumentalness_max = instrumentalness
    print(f"Zakres instrumentalness: {instrumentalness_min} - {instrumentalness_max}")

    # liveness
    liveness_min = None
    liveness_max = None
    for track in tracks:
        liveness = track.get("liveness")
        if liveness is not None:
            if liveness_min is None or liveness < liveness_min:
                liveness_min = liveness
            if liveness_max is None or liveness > liveness_max:
                liveness_max = liveness
    print(f"Zakres liveness: {liveness_min} - {liveness_max}")

    # valence
    valence_min = None
    valence_max = None
    for track in tracks:
        valence = track.get("valence")
        if valence is not None:
            if valence_min is None or valence < valence_min:
                valence_min = valence
            if valence_max is None or valence > valence_max:
                valence_max = valence
    print(f"Zakres valence: {valence_min} - {valence_max}")

    # tempo
    tempo_min = None
    tempo_max = None
    for track in tracks:
        tempo = track.get("tempo")
        if tempo is not None:
            if tempo_min is None or tempo < tempo_min:
                tempo_min = tempo
            if tempo_max is None or tempo > tempo_max:
                tempo_max = tempo
    print(f"Zakres tempo: {tempo_min} - {tempo_max}")

    print()


def analyze_track_storage():
    input = Path("track_storage.jsonl").read_text().splitlines()
    track_storages = []
    for line in input:
        storage = json.loads(line)
        track_storages.append(storage)

    print("-- track_storage.jsonl")

    sums = {"fast": 0, "medium": 0, "slow": 0}
    for storage in track_storages:
        sums[storage["storage_class"]] += 1

    print(sums)


def analyze_track_costs():

    input = Path("tracks.jsonl").read_text().splitlines()
    tracks = []
    for line in input:
        track = json.loads(line)
        tracks.append(track)

    input = Path("track_storage.jsonl").read_text().splitlines()
    track_storages = []
    for line in input:
        storage = json.loads(line)
        track_storages.append(storage)
    track_storage_by_id = { x["track_id"]: x for x in track_storages }

    print("-- track costs")

    cost_instances = {
        "slow": [],
        "medium": [],
        "fast": [],
    }
    for track in tracks:
        id = track.get("id")
        dur = track.get("duration_ms")
        if id is None: continue
        if dur is None: continue
        storage = track_storage_by_id.get(id)
        if storage is None: continue
        sclass = storage.get("storage_class")
        cost = storage.get("daily_cost")
        if sclass != "slow" and sclass != "medium" and sclass != "fast": continue
        if cost is None: continue
        cost_instances[sclass].append({
            "cost": cost,
            "dur": dur,
        })
    
    for sclass in cost_instances.keys():
        print(f"{sclass} raw")
        avg = sum([x["cost"]for x in cost_instances[sclass]]) / len(cost_instances[sclass])
        print(f"avg: {avg}")
        sd = sum([((x["cost"] - avg) ** 2) for x in cost_instances[sclass]]) / len(cost_instances[sclass])
        print(f"sd: {sd}")


if __name__ == "__main__":
    main()
