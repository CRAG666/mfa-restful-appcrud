from . import users
from models.user import UsersModel, UsersSchema
from routes.create_routesStandars import create_routes

create_routes(
    table=UsersModel,
    table_schema=UsersSchema,
    blueprint=users,
    noun="users",
    login_endpoint=True)
