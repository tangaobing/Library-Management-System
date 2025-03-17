from flask import Flask
from flask_migrate import Migrate
from models import db
from config import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    from models.book_model import Book
    from models.category_model import Category
    from models.user_model import User
    from models.borrow_model import Borrow 