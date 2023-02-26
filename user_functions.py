from models import User, Likes, News, db, Category, connect_db
from api_test import search
from flask import flash, redirect, Flask, render_template, session
from forms import LoginForm



def show_likes(user_id):
    """Show the news articles the user liked"""
    user = User.query.get_or_404(user_id)

    user_likes = Likes.query.filter(Likes.user_id == user.id).all()
    # Isolate the news id and iterate over the ids to retrieve those news item from our database
    news_ids = [l.news_id for l in user_likes]
    news = [News.query.get_or_404(n) for n in news_ids]

    return news

def like(g,news_id):
    """Add a news article to the users likes"""

    liked_news = News.query.get_or_404(news_id)
    user_likes = g.user.likes

    if liked_news in user_likes:
        g.user.likes = [like for like in user_likes if like != liked_news]
    else:
        g.user.likes.append(liked_news)

    db.session.commit()

def custom_search(term):
    """Search for a news item by category"""
    categories = Category.query.all()
    cat_names = [c.name for c in categories]
    # If the term searched for is not already in our Category database, perform the search function for it
    if term not in cat_names:
        search(term)
    cat = Category.query.filter(Category.name == term).all()
    data = News.query.filter(News.category == cat[0].id).all()
    return data

def user_signup(form):
    """Signup user"""
    user = User.signup(
        username=form.username.data,
        password=form.password.data,
        email=form.email.data)
    db.session.commit()

    return user

def verify_user(user):
    if not user:
        flash("Access unauthorized.", "danger")
        return redirect('/login')
    
