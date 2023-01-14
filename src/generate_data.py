from data.analyze_delays import analyze_delays
from data.analyze_storage_cost import analyze_storage_cost
from data.generate_delays import generate_delays
from data.generate_tracks_for_delay import generate_tracks_for_delay
from data.generate_tracks_for_storage import generate_tracks_for_storage


def generate_data():
    generate_delays()
    generate_tracks_for_delay()
    generate_tracks_for_storage()
    analyze_delays()
    analyze_storage_cost()


if __name__ == "__main__":
    generate_data()
