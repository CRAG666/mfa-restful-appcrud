from server import app
from models import ma
from models import db, create_database, create_user


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        create_database()
        db.create_all()
        create_user()
    app.run()
