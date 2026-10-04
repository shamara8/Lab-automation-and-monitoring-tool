import core.health_check as health


# ---- check_range ----

def test_check_range_all_within_bounds():
    readings = [{"value": 10, "timestamp": 1}, {"value": 50, "timestamp": 2}, {"value": 99, "timestamp": 3}]
    valid, errors = health.check_range(readings, [0, 100])
    assert valid is True
    assert errors == []


def test_check_range_detects_out_of_bounds():
    readings = [{"value": 10, "timestamp": 1}, {"value": 150, "timestamp": 2}, {"value": -5, "timestamp": 3}]
    valid, errors = health.check_range(readings, [0, 100])
    assert valid is False
    assert len(errors) == 2


def test_check_range_boundary_values_are_valid():
    # exactly on the boundary should count as valid (inclusive range)
    readings = [{"value": 0, "timestamp": 1}, {"value": 100, "timestamp": 2}]
    valid, errors = health.check_range(readings, [0, 100])
    assert valid is True
    assert errors == []


def test_check_range_none_skips_check():
    readings = [{"value": 99999, "timestamp": 1}]  # would fail any real range
    valid, errors = health.check_range(readings, None)
    assert valid is True
    assert errors == []


def test_check_range_empty_readings():
    valid, errors = health.check_range([], [0, 100])
    assert valid is True
    assert errors == []


# ---- check_interval ----

def test_check_interval_no_gaps():
    readings = [{"timestamp": 0.0}, {"timestamp": 0.5}, {"timestamp": 1.0}, {"timestamp": 1.5}]
    valid, errors = health.check_interval(readings, interval=0.5, max_missed=3)
    assert valid is True
    assert errors == []


def test_check_interval_detects_large_gap():
    # expected interval 0.5, max_missed 3 → threshold = 0.5 * 4 = 2.0
    readings = [{"timestamp": 0.0}, {"timestamp": 0.5}, {"timestamp": 5.0}]  # 4.5s gap, way over threshold
    valid, errors = health.check_interval(readings, interval=0.5, max_missed=3)
    assert valid is False
    assert len(errors) == 1
    assert errors[0]["gap"] == 4.5


def test_check_interval_gap_exactly_at_threshold_passes():
    # gap == threshold should NOT count as a failure (uses > not >=)
    readings = [{"timestamp": 0.0}, {"timestamp": 2.0}]  # exactly threshold (0.5 * 4)
    valid, errors = health.check_interval(readings, interval=0.5, max_missed=3)
    assert valid is True
    assert errors == []


def test_check_interval_single_reading_no_gaps_possible():
    readings = [{"timestamp": 0.0}]
    valid, errors = health.check_interval(readings, interval=0.5, max_missed=3)
    assert valid is True
    assert errors == []


def test_check_interval_empty_readings():
    valid, errors = health.check_interval([], interval=0.5, max_missed=3)
    assert valid is True
    assert errors == []


# ---- check_components (integration of both checks) ----

def test_check_components_all_pass():
    readings = [{"value": 50, "timestamp": 0.0}, {"value": 51, "timestamp": 0.5}, {"value": 49, "timestamp": 1.0}]
    config = {"name": "sensor_sim", "value_range": [0, 100], "interval_expected": 0.5, "intervals_max_missed": 3}
    result = health.check_components(readings, config)

    assert result["status"] == "PASS"
    assert result["name"] == "sensor_sim"
    assert result["readings"] == 3
    assert result["errors"]["range_errors"] == []
    assert result["errors"]["interval_errors"] == []


def test_check_components_range_failure_sets_status_fail():
    readings = [{"value": 150, "timestamp": 0.0}, {"value": 50, "timestamp": 0.5}]
    config = {"name": "sensor_sim", "value_range": [0, 100], "interval_expected": 0.5, "intervals_max_missed": 3}
    result = health.check_components(readings, config)

    assert result["status"] == "FAIL"
    assert len(result["errors"]["range_errors"]) == 1


def test_check_components_interval_failure_sets_status_fail():
    readings = [{"value": 50, "timestamp": 0.0}, {"value": 50, "timestamp": 10.0}]
    config = {"name": "display_sim", "value_range": None, "interval_expected": 0.5, "intervals_max_missed": 3}
    result = health.check_components(readings, config)

    assert result["status"] == "FAIL"
    assert len(result["errors"]["interval_errors"]) == 1


def test_check_components_sample_readings_capped_at_five():
    readings = [{"value": i, "timestamp": i * 0.5} for i in range(10)]
    config = {"name": "sensor_sim", "value_range": [0, 100], "interval_expected": 0.5, "intervals_max_missed": 3}
    result = health.check_components(readings, config)

    assert len(result["sample_readings"]) == 5