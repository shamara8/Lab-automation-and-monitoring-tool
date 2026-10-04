def check_range(readings, value_range):
    '''
    Checks if the readings are within the specified value range. 
    Returns:
        (bool): True if all readings are within range, False otherwise
        (list): List of readings that are out of range
    '''
    if value_range is None:
        return True, []
    
    errors = [
        {"value": r["value"], "timestamp": r["timestamp"]}
        for r in readings 
        if not (value_range[0] <= r["value"] <= value_range[1])
    ]
    
    return len(errors) == 0, errors

def check_interval(readings, interval, max_missed):
    '''
    Checks if the reading intervals are valid based on the expected interval and maximum missed intervals.
    Returns:
        (bool): True if all intervals are valid, False otherwise
        (list): List of intervals that are invalid
    '''
    errors = []
    threshold = interval * (max_missed + 1) #if the gap is more then max_missed intervals, chceck will fail
    
    for r in range(len(readings)-1):
        gap = readings[r+1]["timestamp"] - readings[r]["timestamp"]
        if gap > threshold:
            errors.append({
                "gap": gap, "index": r, "timestamp": readings[r]["timestamp"]
            })
    
    return len(errors) == 0, errors

def check_components(readings, config):
    '''
    Performs an interval and range check based on the provided configuration for a component. 
    Returns a dictionary containing the component name, status, number of readings, sample readings, and any errors found.
    '''
    range_valid, range_errors = check_range(readings, config.get("value_range"))
    interval_valid, interval_errors = check_interval(readings, config.get("interval_expected"), config.get("intervals_max_missed"))
    return{
        "name": config.get("name"),
        "status": "PASS" if range_valid and interval_valid else "FAIL",
        "readings": len(readings),
        "sample_readings": readings[:5],
        "errors": {
            "range_errors": range_errors,
            "interval_errors": interval_errors
        }
    }
