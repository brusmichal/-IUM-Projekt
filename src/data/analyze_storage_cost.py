import pandas as pd


def analyze_storage_cost():
    tracks_for_delay = pd.read_json("data/tracks_for_storage.jsonl", lines=True)

    print("class slow")
    class_slow = tracks_for_delay[tracks_for_delay["storage_class"] == "slow"]
    print(class_slow["daily_cost"].describe())
    print()

    print("class medium")
    class_medium = tracks_for_delay[tracks_for_delay["storage_class"] == "medium"]
    print(class_medium["daily_cost"].describe())
    print()

    print("class fast")
    class_fast = tracks_for_delay[tracks_for_delay["storage_class"] == "fast"]
    print(class_fast["daily_cost"].describe())
    print()
