from data.analyze_delays import analyze_delays
from data.analyze_storage_cost import analyze_storage_cost


def analyze_generated_data():
    analyze_delays()
    analyze_storage_cost()


if __name__ == "__main__":
    analyze_generated_data()
