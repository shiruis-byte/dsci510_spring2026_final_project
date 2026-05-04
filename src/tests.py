import os
from load import get_unemployment_data, get_top10_states, plot_unemployment_trends, get_functional_trends, get_recreational_trends


def get_api_key():
    api_key = os.getenv("BLS_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "BLS_API_KEY environment variable not set.\n"
            "  Mac/Linux: export BLS_API_KEY=your_key_here\n"
            "  Windows:   set BLS_API_KEY=your_key_here"
        )
    return api_key

# Test that BLS API
def test_get_unemployment_data():
    print("\nTest 1: Fetching BLS unemployment data...")
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2023", end_year="2023")

    print(f"Total records fetched: {len(records)}")
    print(f"Sample record: {records[0]}")

    assert len(records) > 0, "No records returned"
    assert "state" in records[0]
    assert "year" in records[0]
    assert "month" in records[0]
    assert "unemployment_rate" in records[0]
    assert isinstance(records[0]["unemployment_rate"], float)

    print("PASS: Test 1 finished.")

# Test 10 states
def test_get_top10_states():
    print("\nTest 2: Finding top 10 states...")
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2023", end_year="2023")
    top10 = get_top10_states(records)

    print(f"Top 10 states: {top10}")
    print(f"Number of states: {len(top10)}")

    assert len(top10) == 10
    assert all(isinstance(s, str) for s in top10)

    print("PASS: Test 2 finished.")

 # Test the unemployment plot
def test_plot_unemployment_trends():
    print("\nTest 3: Generating unemployment trend plots...")
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2019", end_year="2024")
    top10 = get_top10_states(records)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")

    plot_unemployment_trends(records, top10, result_dir=RESULTS_DIR)

    assert os.path.exists(os.path.join(RESULTS_DIR, "unemployment_trends.png"))
    print(f"Plot saved to: {RESULTS_DIR}/unemployment_trends.png")
    print("PASS: Test 3 finished.")

# Test that we can fetch functional Google Trends data
def test_get_functional_trends():
    print("\nTest 4: Fetching functional Google Trends data...")
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2023", end_year="2023")
    top10 = get_top10_states(records)

    functional_records = get_functional_trends(top10[:1])

    print(f"Total functional records: {len(functional_records)}")
    if len(functional_records) > 0:
        print(f"Sample record: {functional_records[0]}")
        assert "state" in functional_records[0]
        assert "keyword" in functional_records[0]
        assert "search_index" in functional_records[0]
        assert "category" in functional_records[0]

    print("PASS: Test 4 finished.")

# Test that we can fetch recreational Google Trends data
def test_get_recreational_trends():
    print("\nTest 5: Fetching recreational Google Trends data...")
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2023", end_year="2023")
    top10 = get_top10_states(records)

    recreational_records = get_recreational_trends(top10[:1])

    print(f"Total recreational records: {len(recreational_records)}")
    if len(recreational_records) > 0:
        print(f"Sample record: {recreational_records[0]}")
        assert "state" in recreational_records[0]
        assert "keyword" in recreational_records[0]
        assert "search_index" in recreational_records[0]
        assert "category" in recreational_records[0]

    print("PASS: Test 5 finished.")


if __name__ == "__main__":
    test_get_unemployment_data()
    test_get_top10_states()
    test_plot_unemployment_trends()
    test_get_functional_trends()
    test_get_recreational_trends()