from abc import ABC, abstractmethod
import json

class IWriter(ABC):
    @abstractmethod
    def write(self, data , name):
        pass

class FileWriter(IWriter):
    def write(self, data: dict, name:str ):
        """
        Reads the current file and updates
        it again with the new data
        """
        try:
            with open(name, "r",encoding="utf-8") as file:
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
                    origin_data[window][timestamp] = list()
                origin_data[window][timestamp] += data[window][timestamp]

        with open(name, "w",encoding="utf-8") as file:
            json.dump(origin_data, file, indent='\t' , ensure_ascii=False )
    @staticmethod
    def load(file_name : str):
        with open(file_name) as file:
            temp = json.load(file)
        return temp

