from flask import Flask
from routes import app_routes

from flask_cors import CORS



app = Flask(__name__, static_folder="../front", static_url_path="")
CORS(app)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(app_routes)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)
