import json
import os
import time



def generate_run_id(start_time):
    #if given a valid start_time, use it to generate a run_id, else use the current time
    if start_time:
        return time.strftime("%Y%m%d_%H%M%S", time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
    return time.strftime("%Y%m%d_%H%M%S")


def determine_overall_status(check_results):
    statuses = [c["status"] for c in check_results]
    if all(s == "PASS" for s in statuses):
        return "PASS"
    if all(s == "FAIL" for s in statuses):
        return "FAIL"
    return "PARTIAL_FAILURE"


def write_json_report(check_results, run_id, output_dir, start_time, end_time):
    report = {
        "run_id": run_id,
        "start_time": start_time,
        "end_time": end_time,
        "status": determine_overall_status(check_results),
        "components": check_results,
    }
    path = os.path.join(output_dir, f"run_{run_id}.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    return path


def format_errors(component):
    lines = []
    for e in component["errors"]["range_errors"]:
        lines.append(f"- **{component['name']}**: value {e['value']} out of range at {e['timestamp']}")
    for e in component["errors"]["interval_errors"]:
        lines.append(f"- **{component['name']}**: gap of {e['gap']:.2f}s detected at {e['timestamp']}")
    return lines


def write_markdown_report(check_results, run_id, output_dir, start_time, end_time):
    overall_status = determine_overall_status(check_results)

    lines = [
        f"# Lab Run Report — run_{run_id}",
        "",
        f"**Start:** {start_time}",
        f"**End:** {end_time}",
        f"**Overall status:** {overall_status}",
        "",
        "## Component Summary",
        "",
        "| Component | Status | Readings |",
        "|-----------|--------|----------|",
    ]
    for c in check_results:
        lines.append(f"| {c['name']} | {c['status']} | {c['readings']} |")

    error_lines = []
    for c in check_results:
        error_lines.extend(format_errors(c))

    if error_lines:
        lines += ["", "## Errors", ""] + error_lines
    else:
        lines += ["", "## Errors", "", "None."]

    path = os.path.join(output_dir, f"run_{run_id}.md")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return path



def generate(check_results, output_dir="output/", start_time=time.time(), end_time=time.time()):
    '''
    Generates both JSON and Markdown reports based on the provided check results, output directory, start time, and end time.
    Parameters:
        check_results (list): list of dictionaries containing the results of the health checks for each component
        output_dir (str)    : directory where the reports will be saved (default: "output/")
        start_time (str)    : start time of the run in "YYYY-MM-DD HH:MM:SS" format (default: None, will use current time)
        end_time (str)      : end time of the run in "YYYY-MM-DD HH:MM:SS" format (default: None, will use current time)
    Returns:
        (str, str): paths to the generated JSON and Markdown reports
    '''
    os.makedirs(output_dir, exist_ok=True)
    run_id = generate_run_id(start_time)

    json_path = write_json_report(check_results, run_id, output_dir, start_time, end_time)
    md_path = write_markdown_report(check_results, run_id, output_dir, start_time, end_time)
    return json_path, md_path