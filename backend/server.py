from flask import Flask


def create_app(config_class, *blueprints):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_errorhandlers(app)
    register_blueprints(app, *blueprints)
    register_extensions(app)
    return app


def register_blueprints(app: Flask, *args):
    for blueprint in args:
        app.register_blueprint(blueprint)


def register_extensions(app: Flask):
    from models import ma
    from models import db, create_database
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        create_database()
        db.create_all()


def register_errorhandlers(app: Flask):
    from flask import jsonify
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
    def method_not_unauthorized(err):
        return jsonify({'Authenticate': 'Could not verify'}), 401
