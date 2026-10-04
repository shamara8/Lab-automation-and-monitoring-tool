import argparse
import json
import random
import time


class DisplaySim():
    '''A simple display simulator that generates random readings at a specified interval.'''
    def __init__(self, interval, duration):
        '''
        Initializes the display simulator
        Parameters:
            interval (float): time in seconds between readings
            duration (float): total time in seconds to run the simulation
        '''
        self.interval = interval
        self.duration = duration
        self.running = True
    
    def display_process(self):
        t_end = time.time() + self.duration
        while time.time() < t_end and self.running:
            reading = {"timestamp": time.time(), "value": random.random()}
            print(json.dumps(reading), flush=True)          #simulate display output by printing to stdout

            if random.random() < 0.04:                      #simulate display lag with 4% chance
                time.sleep(self.interval * 6)
            else:
                time.sleep(self.interval)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=0.5, help="Seconds between readings")
    parser.add_argument("--duration", type=float, default=30, help="Total runtime in seconds")
    return parser.parse_args()

def main():
    args = parse_args()
    sim = DisplaySim(interval=args.interval, duration=args.duration)
    sim.display_process()


if __name__ == "__main__":
    main()