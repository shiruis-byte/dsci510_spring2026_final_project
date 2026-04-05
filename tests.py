import os
from bls_unemployment import get_unemployment_data, get_top10_states, plot_unemployment_trends


def get_api_key() -> str:
    """
    Read BLS API key from environment variable BLS_API_KEY.
    Set it before running:
        Mac/Linux:  export BLS_API_KEY=your_key_here
        Windows:    set BLS_API_KEY=your_key_here
    """
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
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2023", end_year="2023")

    assert len(records) > 0, "No records returned"
    assert "state" in records[0], "Missing 'state' field"
    assert "year" in records[0], "Missing 'year' field"
    assert "month" in records[0], "Missing 'month' field"
    assert "unemployment_rate" in records[0], "Missing 'unemployment_rate' field"
    assert isinstance(records[0]["unemployment_rate"], float), "unemployment_rate should be a float"

    print(f"PASS: fetched {len(records)} records")
    print(f"Sample record: {records[0]}")


def test_get_top10_states():
    """Test that top 10 returns exactly 10 states."""
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2023", end_year="2023")
    top10 = get_top10_states(records)

    assert len(top10) == 10, f"Expected 10 states, got {len(top10)}"
    assert all(isinstance(s, str) for s in top10), "All state names should be strings"

    print(f"PASS: top 10 states = {top10}")


def test_plot_unemployment_trends():
    """Test that plot runs without error and saves the output file."""
    import os
    api_key = get_api_key()

    records = get_unemployment_data(api_key, start_year="2019", end_year="2024")
    top10 = get_top10_states(records)
    plot_unemployment_trends(records, top10)

    assert os.path.exists("unemployment_trends.png"), "Plot file was not saved"
    print("PASS: unemployment_trends.png saved successfully")


if __name__ == "__main__":
    test_get_unemployment_data()
    test_get_top10_states()
    test_plot_unemployment_trends()