from abc import ABC, abstractmethod
import json

class Write(ABC):
    @abstractmethod
    def write(self, data , name):
        pass

class FileWriter(Write):
    def write(self, data: dict, name:str ):
        """
        Reads the current file and updates
        it again with the new data
        """
        try:
            with open(name, "r") as file:
                try:
                    origin_data = json.load(file)
                except json.JSONDecodeError:
                    origin_data = dict()
        except FileNotFoundError:
            origin_data = dict()

        for window in data:
            if window not in origin_data:
                origin_data[window] = dict()
            for timestamp in data[window]:
                if timestamp not in origin_data[window]:
                    origin_data[window][timestamp] = str()
                origin_data[window][timestamp] += str(data[window][timestamp])

        with open(name, "w") as file:
            json.dump(origin_data, file, indent='\t')