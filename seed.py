from app import app
from models import db, Category
from category import categories_test

def add_to_db(cat):
    cat = Category(name = cat)
    db.session.add(cat)

with app.app_context():
    db.drop_all()
    db.create_all()
    
    for category in categories_test:
        add_to_db(category)

    db.session.commit()
