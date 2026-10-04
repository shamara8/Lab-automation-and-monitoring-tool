import argparse
import json
import random
import time


class SensorSim():
    '''A simple sensor simulator that generates random readings at a specified interval.'''
    def __init__(self, interval, duration):
        '''
        Initializes the sensor simulator
        Parameters:
            interval (float): time in seconds between readings
            duration (float): total time in seconds to run the simulation
        '''
        self.interval = interval
        self.duration = duration
        self.running  = True
        self.val      = random.randint(0, 100)
    
    def sensor_process(self):
        t_end = time.time() + self.duration
        
        while time.time() < t_end and self.running:
            reading = {"timestamp": time.time(), "value": self.val}
            print(json.dumps(reading), flush=True)                  #simulate sensor output by printing to stdout
            
            self.val += random.randint(-5, 5)                       #simulate sensor value change
            self.val = max(0, min(100, self.val))                   #keep the value between 0 and 100
            
            if random.random() < 0.04:                              #simulate sensor failure with 4% chance
                self.val += random.randint(-20, 150)
            
            time.sleep(self.interval)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=0.5, help="Seconds between readings")
    parser.add_argument("--duration", type=float, default=30 , help="Total runtime in seconds")
    return parser.parse_args()

def main():
    args = parse_args()
    sim = SensorSim(interval=args.interval, duration=args.duration)
    sim.sensor_process()


if __name__ == "__main__":
    main()