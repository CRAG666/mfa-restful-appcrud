from . import db, ma, Standard
from marshmallow import validate
from flask import abort

class NotesModel(db.Model, Standard):
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(240), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __init__(self, fields: dict, current_user: object):
        self.changes(fields, current_user)

    def changes(self, fields: dict, current_user: object):
        self.name = fields.get('name')
        self.content = fields.get('content')
        self.id_user = current_user.id

    @staticmethod
    def get_by_id(table, id, current_user):
        note = db.session.query(table).filter(table.id == id).filter(table.id_user == current_user.id).first()
        if note:
            return note
        return abort(404)

    @staticmethod
    def all(table, current_user):
        return db.session.query(table).filter_by(id_user=current_user.id).all()


class NotesSchema(ma.Schema):
    name = ma.Str(validate=validate.Length(min=1), required=True)
    content = ma.Str(validate=validate.Length(min=1), required=True)

    class Meta:
        fields = ('id', 'name', 'content')
