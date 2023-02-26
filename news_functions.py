from models import Category, User_Category, db
from api_test import search

def news_search(userid):
    """Search for news items based on users saved categories"""
    user_category = User_Category.query.filter(User_Category.user_id == userid).all()
    cat_id = [c.category_id for c in user_category]
    categories = Category.query.filter(Category.id.in_(cat_id)).all()
    # For each category the user has saved, run it through the search function to add news items to our database
    for cat in categories:
        search(cat.name)
        
    db.session.commit()