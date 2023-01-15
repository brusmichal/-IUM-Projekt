import pandas as pd
from sklearn.feature_selection import mutual_info_regression


def analyze_storage_cost():
    print("-- ANALYZE STORAGE COST --")
    tracks_for_storage_train = pd.read_json(
        "data/tracks_for_storage_train.jsonl", lines=True
    )
    tracks_for_storage_validate = pd.read_json(
        "data/tracks_for_storage_validate.jsonl", lines=True
    )
    describe_tracks_for_storage(tracks_for_storage_train, "TRAINING SET")
    describe_tracks_for_storage(tracks_for_storage_validate, "VALIDATION SET")
    analyze_storage_cost_pack(tracks_for_storage_train, "TRAIN SET - ALL CLASSES")
    analyze_storage_cost_pack(
        tracks_for_storage_train[tracks_for_storage_train["storage_class"] == "slow"],
        "TRAIN SET - CLASS SLOW",
    )
    analyze_storage_cost_pack(
        tracks_for_storage_train[tracks_for_storage_train["storage_class"] == "medium"],
        "TRAIN SET - CLASS MEDIUM",
    )
    analyze_storage_cost_pack(
        tracks_for_storage_train[tracks_for_storage_train["storage_class"] == "fast"],
        "TRAIN SET - CLASS FAST",
    )


def describe_tracks_for_storage(df: pd.DataFrame, label: str):
    print(f"{label}: describe daily_cost")
    print(df["daily_cost"].describe())
    print()
    print(f"{label}: count storage_class")
    print(f"slow   {len(df[df['storage_class'] == 'slow'])}")
    print(f"medium {len(df[df['storage_class'] == 'medium'])}")
    print(f"fast   {len(df[df['storage_class'] == 'fast'])}")
    print()


def analyze_storage_cost_pack(df: pd.DataFrame, label: str):
    print(f"{label}: describe daily_cost")
    print(df["daily_cost"].describe())
    print()

    print(f"{label}: daily_cost pearson correlation")
    print(df.corrwith(df["daily_cost"], method="pearson", numeric_only=True))
    print()

    print(f"{label}: daily cost mutual information")
    columns = [
        "popularity",
        "duration_ms",
        "explicit",
        "danceability",
        "energy",
        "key",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "daily_cost",
    ]
    for name, value in zip(
        columns, mutual_info_regression(X=df[columns], y=df["daily_cost"])
    ):
        print("{0: <20} {1}".format(name, value))
    print()
