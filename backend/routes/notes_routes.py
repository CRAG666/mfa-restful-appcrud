from . import notes
from models.note import NotesModel, NotesSchema
from routes.create_routesStandars import create_routes

create_routes(
    table=NotesModel,
    table_schema=NotesSchema,
    blueprint=notes,
    noun="notes")
