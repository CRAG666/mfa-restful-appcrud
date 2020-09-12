from flask import Flask, jsonify
from config import DevelopmentConfig
from routes.users_routes import users
from routes.notes_routes import notes
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


# * Error 404
@app.errorhandler(404)
def page_not_found(err):
    return jsonify({"Message": "This page could not be found"}), 404


# * Error 405
@app.errorhandler(405)
def method_not_allowed(err):
    return jsonify({"Message": "The method is not allowed for the requested URL"}), 405


# * Error 401
@app.errorhandler(401)
def method_not_allowed(err):
    return jsonify({'Authenticate': 'Could not verify'}), 401


# * Routes
app.register_blueprint(users)
app.register_blueprint(notes)
