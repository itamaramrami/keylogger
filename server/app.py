from flask import Flask
from routes import app_routes



app = Flask(__name__, static_folder="../front", static_url_path="")
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(app_routes)



if __name__ == "__main__":
    app.run( port=5555, debug=True)
