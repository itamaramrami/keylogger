from flask import Blueprint, request
from controllers import *

# יצירת Blueprint לניהול הראוטים
app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/")
def index():
    return index_page()



@app_routes.route("/home", methods=["GET", "POST"])
def index_home():
        return home(request)



@app_routes.route("/signup", methods=["POST"])
def index_singup():
    return signup(request)



@app_routes.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return get_users()



@app_routes.route("/get_data", methods=["GET"])
def get():
     return get_data()

@app_routes.route("/hendle_url_params")
def hendle_url():
    return handle_url_params(request)
