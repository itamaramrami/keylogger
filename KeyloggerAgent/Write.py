from abc import ABC, abstractmethod
import json
import requests

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
        for mac in data:
            if mac not in origin_data:
                origin_data[mac] = dict()
            for window in data[mac]:
                if window not in origin_data[mac]:
                    origin_data[mac][window] = dict()
                for timestamp in data[mac][window]:
                    if timestamp not in origin_data[mac][window]:
                        origin_data[mac][window][timestamp] = list()
                    origin_data[mac][window][timestamp] += data[mac][window][timestamp]

        with open(name, "w",encoding="utf-8") as file:
            json.dump(origin_data, file, indent='\t' , ensure_ascii=False )
    @staticmethod
    def load(file_name : str):
        with open(file_name , encoding="utf-8") as file:
            temp = json.load(file)
        return temp


class NetworkWriter(IWriter):
    def write(self, data, name:str):
        url = f"http://{name}/api/storage"
        headers = {
            "Content-Type": "application/json"
        }
        requests.post(url , json = data , headers = headers)


