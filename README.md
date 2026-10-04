# Lab process automation & monitoring tool

Built as practice for lab automation, testing/validating and technical documenting work. 

## Project description

A simulated one-click lab test harness: launches **multiple components** (stand-ins for lab hw/sw), **monitors them** for health/validity and produces a **structured report**. 

Each component (sensor_sim, display_sim, logger_sim) is a standalone python process that simulates lab equipment in real time - producing timestamped readings, with occasional injected faults. This models actual coordination problems without physical equipment.

## Architecture

config.yaml -> dispatcher -> components(subprocesses) -> health_check -> report_gen -> JSON + Markdown output

## How to run
    python3 main.py

Reports are written to `output/run_<timestamp>.json` and `.md`

## Configuration

Edit `config.yaml` to change component intervals, duration, failure thresholds, and value ranges — nothing is hardcoded.

## [Example output](output/run_20261004_165713.md)

## Known simplifications
- Components are standalone simulated processes, focusing on validation, not the systems themselves
- logger_sim represents a logging role but doesnt inject live data from the other components
- start_before is declared in config.yaml but not yet implemented in dispatcher

## Testing
    pytest tests/ -v
Unit tests cover health_check logic (range/interval validation) and report_gen (status determination, error formatting, file output)

## Possible extentions
- Real inter-process data flow (logger actually reading sensor output, not just simulating)
- Circular dependency detection for start_before
- A GUI/dashboard visualizing run history