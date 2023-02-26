from models import User_Category, Category, News, Likes

def homepage(id):
    """Displaying News items based off a users favorite categories"""
    user_category = User_Category.query.filter(User_Category.user_id == id).all()
    cat_id = [c.category_id for c in user_category]
    categories = Category.query.filter(Category.id.in_(cat_id)).all()

    data1 = [News.query.filter(News.category == c.id) for c in categories]
    data = []

    for category in data1:
        for news in category:
            data.append(news)

    data.sort(key=lambda data: data.date, reverse=True)

    return data

def get_likes(id):
    like = Likes.query.filter(Likes.user_id == id)
    likes = [l.news_id for l in like]

    return likes
    



    

