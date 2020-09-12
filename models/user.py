from . import db, ma, Standard
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import validate
from flask import abort


class UsersModel(db.Model, Standard):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    all_perm = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, fields: dict, curren_user: object = None):
        self.changes(fields, curren_user)

    def changes(self, fields: dict, curren_user: object):
        self.name = fields.get('name')
        self.password = self.__generate_password(fields.get('password'))
        self.email = fields.get('email')
        self.all_perm = fields.get('all_perm', False)
        print(curren_user.name)

    @staticmethod
    def get_by_id(table, id, current_user):
        if current_user.all_perm:
            return db.session.query(table).get_or_404(id)
        return abort(404)

    @staticmethod
    def all(table, current_user):
        if current_user.all_perm:
            return db.session.query(table).all()

    @staticmethod
    def __generate_password(password: str) -> str:
        return generate_password_hash(password)

    def compare_passwords(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class UsersSchema(ma.Schema):
    name = ma.Str(validate=validate.Length(min=1), required=True)
    email = ma.Email(required=True)
    password = ma.Str(validate=validate.Length(min=4), load_only=True, required=True)

    class Meta:
        fields = ('id', 'name', 'email', 'password')
