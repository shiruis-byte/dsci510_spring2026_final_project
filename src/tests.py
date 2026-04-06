import os
from load import get_unemployment_data, get_top10_states, plot_unemployment_trends


def get_api_key() -> str:
    api_key = os.getenv("BLS_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "BLS_API_KEY environment variable not set.\n"
            "  Mac/Linux: export BLS_API_KEY=your_key_here\n"
            "  Windows:   set BLS_API_KEY=your_key_here"
        )
    return api_key


def test_get_unemployment_data():
    """Test that BLS API returns correctly structured records."""
    print("\n--- Test 1: Fetching BLS unemployment data ---")
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2023", end_year="2023")

    print(f"Total records fetched: {len(records)}")
    print(f"Sample record: {records[0]}")
    print(f"Fields present: {list(records[0].keys())}")

    assert len(records) > 0, "No records returned"
    assert "state" in records[0], "Missing 'state' field"
    assert "year" in records[0], "Missing 'year' field"
    assert "month" in records[0], "Missing 'month' field"
    assert "unemployment_rate" in records[0], "Missing 'unemployment_rate' field"
    assert isinstance(records[0]["unemployment_rate"], float), "unemployment_rate should be a float"

    print("PASS: Test 1 finished.")


def test_get_top10_states():
    """Test that top 10 returns exactly 10 states."""
    print("\n--- Test 2: Identifying top 10 highest-unemployment states ---")
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2023", end_year="2023")
    top10 = get_top10_states(records)

    print(f"Top 10 states returned: {top10}")
    print(f"Number of states: {len(top10)}")

    assert len(top10) == 10, f"Expected 10 states, got {len(top10)}"
    assert all(isinstance(s, str) for s in top10), "All state names should be strings"

    print("PASS: Test 2 finished.")


def test_plot_unemployment_trends():
    print("\n--- Test 3: Generating unemployment trend plots ---")
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2019", end_year="2024")
    top10 = get_top10_states(records)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")

    plot_unemployment_trends(records, top10, result_dir=RESULTS_DIR)

    assert os.path.exists(os.path.join(RESULTS_DIR, "unemployment_trends.png")), "Plot file was not saved"
    print(f"Plot saved to: {RESULTS_DIR}/unemployment_trends.png")
    print("PASS: Test 3 finished.")


if __name__ == "__main__":
    test_get_unemployment_data()
    test_get_top10_states()
    test_plot_unemployment_trends()
    print("\n=== All tests finished! ===")