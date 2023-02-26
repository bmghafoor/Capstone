from models import User, Author, User_Author, db


def add_user_author(userid,author):
    """Add an author to the users favorites"""
    user_author = User_Author(user_id = userid, author_id = author)
    db.session.add(user_author)


def user_fave_author(user_id):
    """Return all authors the user has as favorites"""
    user = User.query.get_or_404(user_id)

    user_authors = User_Author.query.filter(User_Author.user_id == user.id).all()
    authors_id = [a.author_id for a in user_authors]
    authors = [Author.query.get(a) for a in authors_id]

    return authors

def delete_author(g,auth_id):
    """Delete an Author from database"""
    author = User_Author.query.filter(User_Author.user_id == g.user.id, User_Author.author_id == auth_id).all()
    db.session.delete(author[0])
    db.session.commit()