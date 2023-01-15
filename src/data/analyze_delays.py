import pandas as pd


def analyze_delays():
    print("-- ANALYZE TRACK DELAYS --")
    print()

    tracks_for_delay_train = pd.read_json(
        "data/tracks_for_delay_train.jsonl", lines=True
    )
    tracks_for_delay_validate = pd.read_json(
        "data/tracks_for_delay_validate.jsonl", lines=True
    )

    count_storage_class(tracks_for_delay_train, "TRAINING SET")
    count_storage_class(tracks_for_delay_validate, "VALIDATION SET")

    describe_avg_delay(tracks_for_delay_train, "TRAINING SET")


def count_storage_class(df: pd.DataFrame, label: str):
    print(f"{label}: count storage_class")
    print(f"slow   {len(df[df['storage_class'] == 'slow'])}")
    print(f"medium {len(df[df['storage_class'] == 'medium'])}")
    print(f"fast   {len(df[df['storage_class'] == 'fast'])}")
    print()


def describe_avg_delay(df: pd.DataFrame, label: str):
    print(f"{label}: describe avg_delay - all classes")
    print(df["avg_delay"].describe())
    print()
    print(f"{label}: describe avg_delay - class slow")
    slow = df[df["storage_class"] == "slow"]
    print(slow["avg_delay"].describe())
    print()
    print(f"{label}: describe avg_delay - class medium")
    medium = df[df["storage_class"] == "medium"]
    print(medium["avg_delay"].describe())
    print()
    print(f"{label}: describe avg_delay - class fast")
    fast = df[df["storage_class"] == "fast"]
    print(fast["avg_delay"].describe())
    print()
