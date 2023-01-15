from data.generate_delays import generate_delays
from data.generate_tracks_for_delay import generate_tracks_for_delay
from data.generate_tracks_for_storage import generate_tracks_for_storage


def generate_data():
    generate_delays()
    generate_tracks_for_delay()
    generate_tracks_for_storage()


if __name__ == "__main__":
    generate_data()
