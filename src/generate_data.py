from data.generate_delays import generate_delays
from data.generate_tracks_for_delay import generate_tracks_for_delay
from data.generate_tracks_for_storage import generate_tracks_for_storage
from data.analyze_delays import analyze_delays

def main():
    generate_delays()
    generate_tracks_for_delay()
    generate_tracks_for_storage()
    analyze_delays()


if __name__ == "__main__":
    main()
