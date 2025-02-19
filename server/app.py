from flask import Flask, jsonify, request
from routes import app_routes
from flask_cors import CORS




app = Flask(__name__)
app.register_blueprint(app_routes)

CORS(app)  # מאפשר גישה ל-Frontend


pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
