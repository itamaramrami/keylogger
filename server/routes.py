from flask import Blueprint, request
from controllers import *

# Creating a Blueprint for the management of the routers
app_routes = Blueprint("app_routes", __name__)


@app_routes.route("/api/storage", methods=["POST"])
def stores_data():
       return store_data()


@app_routes.route("/")
def index():
    return index_page()


@app_routes.route("/api/get_users", methods=["GET"])
def users():
   return get_users()


@app_routes.route("/api/get_data/<mac_address>", methods=["GET"])
def fetch_data_by_mac(mac_address):
    return get_data_by_mac(mac_address)


@app_routes.route("/api/handle_url_params")
def handle_url():
    return handle_url_params()
