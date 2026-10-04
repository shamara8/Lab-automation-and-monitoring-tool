import argparse
import json
import random
import time


class LoggerSim():
    '''A simple logger simulator that generates random readings at a specified interval.'''
    def __init__(self, interval, duration, output_path):
        '''
        Initializes the logger simulator
        Parameters:
            interval (float) : time in seconds between readings
            duration (float) : total time in seconds to run the simulation
            output_path (str): path to the output log file
        '''
        self.interval        = interval
        self.duration        = duration
        self.output_path     = output_path
        self.running         = True
        self.entries         = []

    def logger_process(self):
        t_end = time.time() + self.duration
        
        while time.time() < t_end and self.running:
            entry = {"timestamp": time.time(), "entries_written": len(self.entries)}
            self.entries.append(entry)                              #create logger output

            print(json.dumps(entry), flush=True)                    #simulate logger output by printing to stdout

            time.sleep(self.interval)

        self._write_log()

    def _write_log(self):   #internal method to write the log entries to a file
        with open(self.output_path, 'w') as f:
            json.dump(self.entries, f, indent=4)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=0.5                        , help="Seconds between readings")
    parser.add_argument("--duration", type=float, default=30                         , help="Total runtime in seconds")
    parser.add_argument("--output"  , type=str  , default="outputs/output/logger_output.json", help="Path to output log file")
    return parser.parse_args()

def main():
    args = parse_args()
    sim = LoggerSim(interval=args.interval, duration=args.duration, output_path=args.output)
    sim.logger_process()


if __name__ == "__main__":
    main()
