import time

import core.dispatcher as disp
import core.health_check as health
import core.report_gen as report
#@Author: Stefan Hamara

#main execution
dispatcher = disp.Dispatcher()
config     = disp.get_config()

#get time and readings
start_time = time.strftime("%Y-%m-%d %H:%M:%S")
readings   = disp.main(dispatcher, config)
end_time   = time.strftime("%Y-%m-%d %H:%M:%S")

#check the readings for each component
check_results = []
for component in config["components"]:
    name = component["name"]
    check_results.append(health.check_components(readings[name], component))

#generate the report and print the path to the report files
json_path, md_path = report.generate(check_results, config["run"]["output_dir"], start_time, end_time)
print(f"Report written to {json_path} and {md_path}")
