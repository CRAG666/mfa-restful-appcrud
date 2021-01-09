from server import create_app
from config import ProductionConfig
from routes.notes_routes import notes
from routes.users_routes import users

app = create_app(ProductionConfig, users, notes)

if __name__ == "__main__":
    app.run()
