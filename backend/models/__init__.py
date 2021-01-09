from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc
from flask import current_app as app
db = SQLAlchemy()
ma = Marshmallow()


class Standard:
    """ Utils for database"""
    def save(self) -> bool:
        db.session.add(self)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True

    @staticmethod
    def get_by_id(table, id, *args):
        return db.session.query(table).get_or_404(id)

    @staticmethod
    def all(table, *args):
        return db.session.query(table).all()

    def delete(self, *args) -> bool:
        db.session.delete(self)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        return True


def create_database():
    """Crate database"""
    engine = db.create_engine(app.config['EGINE_URI'], {})
    engine.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['DB_NAME']}")


from .note import NotesModel
from .user import UsersModel

def create_user():
    search_default_user = UsersModel.query.filter_by(id=1).first()
    if not search_default_user:
        new_user = UsersModel(
            {
                "name": "Peter",
                "email": "prueba@crag.com",
                "password": "12345678",
                "all_perm": True
            }
        )
        new_user.save()
    print("Default user in Data base")
