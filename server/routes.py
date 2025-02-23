from flask import Blueprint, request
from controllers import *

# Creating a Blueprint for the management of the routers
app_routes = Blueprint("app_routes", __name__)


@app_routes.route("/storage", methods=["POST"])
def stores_data():
       pass


@app_routes.route("/")
def index():
    pass



@app_routes.route("/signup", methods=["POST"])
def index_signup():
   pass



@app_routes.route("/users", methods=["GET", "POST"])
def users():
   pass



@app_routes.route("/get_data", methods=["GET"])
def get():
     pass

@app_routes.route("/handle_url_params")
def handle_url():
    pass
