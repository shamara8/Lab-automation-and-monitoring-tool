import subprocess
import json
import yaml


class Dispatcher():
    '''Dispatcher class to manage the execution of component scripts and collect their outputs.'''
    def __init__(self):
        self.data = []

    def dispatch(self, config, duration):
        '''
        Dispatches the component scripts based on the provided configuration and duration.
        Parameters:
            config (dict)   : configuration dictionary containing component details
            duration (float): total time in seconds to run the simulation
        Returns:
            (list): a list of subprocess.Popen objects for each dispatched component
        '''
        queue = []
        for component in config["components"]:
            cmd = [
                "python3", component["script"], 
                "--interval", str(component["interval_expected"]),
                "--duration", str(duration)
            ]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            queue.append(process)
        return queue

def get_config():
    '''Loads config.yaml from the current working directory. Must be on project root, or config.yaml will not be found.'''
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config

def main(dispatcher, config):
    '''
    Runs a full dispatch cycle for all components, waits for them and returns their outputs.
    Parameters:
        dispatcher (Dispatcher): the dispatcher instance
        config (dict)          : the configuration dictionary
    Returns:
        (dict): a dictionary containing the outputs of each component
    '''
    duration = config["run"]["duration"]

    queue = dispatcher.dispatch(config, duration)
    
    reading = {}
    for process, component in zip(queue, config["components"]):
        process.wait()
        lines = [json.loads(line.strip()) for line in process.stdout] #parses the output of each of the components
        reading[component["name"]] = lines

    return reading


if __name__ == "__main__":
    dispatcher = Dispatcher()
    config = get_config()

    main(dispatcher, config)
