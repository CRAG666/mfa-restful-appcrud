from . import ma
from marshmallow import validate


class LoginSchema(ma.Schema):
    email = ma.Email(required=True)
    password = ma.Str(validate=validate.Length(min=8), required=True)
