from models import User_Category, Category, db

# Initialize a few categories
categories_test = [
    'Sports',
    'Finance',
    'Healthcare',
    'Cars',
    'Movies',
    'Education'
]

def add_user_category(user,category):
    """Add a Category to the Users favorite"""
    user_category = User_Category(user_id = user.user.id, category_id = category)
    db.session.add(user_category)



def show_cats(g,form):
    """Show available categories for user to choose from"""
    all_categories = Category.query.all()
    curr_categories = User_Category.query.filter(User_Category.user_id == g.user.id).all()
    curr_categories_id = [c.category_id for c in curr_categories]
    available_categories = []
    # If a user has a category in their favorites, it should not appear on the list
    for category in all_categories:
        if category.id not in curr_categories_id:
            available_categories.append(category)

    form.category.choices = [(c.id, c.name) for c in  available_categories]
    
    return all_categories


def submit(g,form):
    """Submit multiple categories as favorites"""
    categories = form.category.data
    for category in categories:
        add_user_category(g,category)
        db.session.commit()



def show_user_choices(user_id):
    """Show users favorite categories"""
    user_cat = User_Category.query.filter(User_Category.user_id==user_id).all()
    user_cats = [c.category_id for c in user_cat]
    categories = [Category.query.get(c) for c in user_cats]

    return categories

def delete_category(user_id,cat_id):
    """Delete a category from Users favorite list"""
    cat = User_Category.query.filter(User_Category.user_id == user_id, User_Category.category_id == cat_id).all()
    db.session.delete(cat[0])
    db.session.commit()







