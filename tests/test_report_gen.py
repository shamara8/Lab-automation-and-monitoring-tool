import json
import os

import pytest

import core.report_gen as report


# ---- Fixtures: reusable sample data for multiple tests ----

@pytest.fixture
def passing_result():
    return {
        "name": "sensor_sim",
        "status": "PASS",
        "readings": 20,
        "sample_readings": [],
        "errors": {"range_errors": [], "interval_errors": []},
    }


@pytest.fixture
def failing_result():
    return {
        "name": "display_sim",
        "status": "FAIL",
        "readings": 15,
        "sample_readings": [],
        "errors": {
            "range_errors": [],
            "interval_errors": [{"gap": 4.2, "index": 3, "timestamp": 1735500612.41}],
        },
    }


# ---- determine_overall_status ----

def test_overall_status_all_pass(passing_result):
    result = report.determine_overall_status([passing_result, passing_result])
    assert result == "PASS"


def test_overall_status_all_fail(failing_result):
    result = report.determine_overall_status([failing_result, failing_result])
    assert result == "FAIL"


def test_overall_status_mixed(passing_result, failing_result):
    result = report.determine_overall_status([passing_result, failing_result])
    assert result == "PARTIAL_FAILURE"


def test_overall_status_empty_list():
    # edge case: no components at all
    result = report.determine_overall_status([])
    assert result == "PASS"  # all() on an empty list is True — worth knowing this Python quirk


# ---- format_errors ----

def test_format_errors_with_interval_error(failing_result):
    lines = report.format_errors(failing_result)
    assert len(lines) == 1
    assert "display_sim" in lines[0]
    assert "4.20" in lines[0]


def test_format_errors_no_errors(passing_result):
    lines = report.format_errors(passing_result)
    assert lines == []


def test_format_errors_with_range_error():
    component = {
        "name": "sensor_sim",
        "errors": {
            "range_errors": [{"value": 150, "timestamp": 1735500612.41}],
            "interval_errors": [],
        },
    }
    lines = report.format_errors(component)
    assert len(lines) == 1
    assert "150" in lines[0]
    assert "sensor_sim" in lines[0]


# ---- write_json_report / write_markdown_report (real file I/O, using tmp_path) ----

def test_write_json_report_creates_valid_file(tmp_path, passing_result):
    output_dir = str(tmp_path)
    path = report.write_json_report(
        [passing_result], "20260930_120000", output_dir, "2026-09-30 12:00:00", "2026-09-30 12:00:10"
    )

    assert os.path.exists(path)
    with open(path) as f:
        data = json.load(f)

    assert data["run_id"] == "20260930_120000"
    assert data["status"] == "PASS"
    assert data["components"] == [passing_result]


def test_write_markdown_report_includes_errors_section(tmp_path, failing_result):
    output_dir = str(tmp_path)
    path = report.write_markdown_report(
        [failing_result], "20260930_120000", output_dir, "2026-09-30 12:00:00", "2026-09-30 12:00:10"
    )

    with open(path) as f:
        content = f.read()

    assert "display_sim" in content
    assert "FAIL" in content
    assert "## Errors" in content


def test_write_markdown_report_no_errors_says_none(tmp_path, passing_result):
    output_dir = str(tmp_path)
    path = report.write_markdown_report(
        [passing_result], "20260930_120000", output_dir, "2026-09-30 12:00:00", "2026-09-30 12:00:10"
    )

    with open(path) as f:
        content = f.read()

    assert "None." in content