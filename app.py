import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, SelectForm, SourceForm
from models import db, connect_db, User, News, Author, Source, User_Author, User_Source




from homepage_functions import homepage, get_likes
from category import show_cats, submit, show_user_choices, delete_category
from author_functions import add_user_author, user_fave_author, delete_author
from sources_functions import show_sources, submit_source, user_sources, add_source, delete_source
from user_functions import show_likes, like, custom_search, user_signup
from news_functions import news_search

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/homepageing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///news'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def first_page():
    return redirect('/signup')

@app.route('/getnews')
def home():
    """Get news items from API based on users saved categories"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    news_search(g.user.id)
    
    return redirect('/homepage')


@app.route('/homepage')
def news_homepage():
    """Display news for user"""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    data = homepage(g.user.id)
    likes = get_likes(g.user.id)

    return render_template('homepage.html',data = data, likes = likes)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Sign up User"""
    form = UserAddForm()
    if form.validate_on_submit():
        try:
            user = user_signup(form)
        except IntegrityError:
            flash("Username or email already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)
        return redirect("/choices")
    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/getnews")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('Successfully Logged Out')
    return redirect('/login')




@app.route('/choices', methods = ['GET','POST'])
def choices():
    """User Select Favorite Categories"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    form = SelectForm()
    # Show available categories to choose from
    all_categories = show_cats(g,form)
    if form.validate_on_submit():
        # Submit multiple catefories as users favorite
        submit(g,form)
        return redirect('/getnews')
    return render_template('choices.html',form=form, all_categories = all_categories)


@app.route('/users/<int:user_id>/choices', methods = ['GET'])
def view_choices(user_id):
    """Show Users favorite categories"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    user = User.query.get_or_404(user_id)
    categories = show_user_choices(user_id)

    return render_template('user_choices.html',user=user, categories = categories)



@app.route('/users/<int:user_id>/choices/<int:cat_id>', methods = ['POST'])
def delete_cat(user_id,cat_id):
    """Delete a category from users favorite"""
    delete_category(user_id, cat_id)

    return redirect ('/homepage')


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    return render_template('user.html',user=user)




@app.route('/author/<int:auth_id>')
def show_author(auth_id):
    """Show Author."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    author = Author.query.get_or_404(auth_id)
    # user_author is used to determine whether the button will say Add to Favorite to Remove
    user_author = User_Author.query.filter(User_Author.user_id == g.user.id, User_Author.author_id == auth_id).all()

    return render_template('author.html', author=author, user_author = user_author)


@app.route('/authors/<int:author_id>', methods = ['POST'])
def user_author(author_id):
    """Submit Author as favorite."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    add_user_author(g.user.id,author_id)
    db.session.commit()

    return redirect('/homepage')


@app.route('/user/<int:user_id>/authors')
def show_user_author(user_id):
    """Find Users favortore authors"""

    authors = user_fave_author(user_id)

    return render_template('user_authors.html', authors = authors)


@app.route('/authors/<int:auth_id>/delete', methods = ['POST'])
def delete_auth(auth_id):
    """Delete an author from a users favorite list"""
    delete_author(g,auth_id)

    return redirect('/homepage')


@app.route('/authors/<int:auth_id>/articles')
def show_articles_by_auth(auth_id):
    """Show news articles by a specific author"""

    news = News.query.filter(News.author == auth_id).all()
    author = Author.query.get_or_404(auth_id)

    likes = get_likes(g.user.id)
    
    return render_template('auther_articles.html', news = news, author = author, likes = likes)


@app.route('/sources', methods = ['GET','POST'])
def disp_sources():
    """Display available sources for User to choose from"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    form = SourceForm()
    show_sources(g,form)

    if form.validate_on_submit():
        submit_source(g.user.id,form)
        return redirect('/homepage')

    return render_template('sources.html',form=form)

@app.route('/source/<int:src_id>/add', methods = ['POST'])
def add_single_source(src_id):
    """Add a singular source to user favorites"""
    add_source(g.user.id, src_id)
    
    return redirect(f'/user/{g.user.id}/sources')
    


@app.route('/source/<int:src_id>')
def show_source(src_id):
    """Show Source."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    source = Source.query.get_or_404(src_id)
    # user_source is used to determine whether the button will say Add to Favorite to Remove
    user_source = User_Source.query.filter(User_Source.user_id == g.user.id, User_Source.source_id == src_id).all()

    return render_template('source.html', source=source, user_source = user_source)



@app.route('/user/<int:user_id>/sources')
def show_user_source(user_id):
    """Show users favorite sources"""

    sources = user_sources(user_id)
    return render_template('user_sources.html', sources = sources)
    

@app.route('/users/<int:user_id>/likes')
def show_user_likes(user_id):
    """Show users liked news articles"""

    news = show_likes(user_id)
    return render_template('user_likes.html', news = news)


@app.route('/sources/<int:source_id>/articles')
def show_articles_by_source(source_id):
    """Display news articles from a specific source"""
    news = News.query.filter(News.source == source_id).all()
    source = Source.query.get_or_404(source_id)
    likes = get_likes(g.user.id)
    return render_template('source_articles.html', news = news, source = source,likes=likes)


@app.route('/sources/<int:source_id>/delete', methods = ['POST'])
def del_source(source_id):
    """Delete a source from users favorite list"""
    delete_source(g,source_id)
    return redirect('/homepage')



@app.route('/news/add_like/<int:news_id>', methods=['POST'])
def add_like(news_id):
    """Toggle a liked news for the currently-logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    like(g,news_id)

    return ("",204)

@app.route('/articles')
def search_term():
    """Search for custom articles and display results"""
    term = request.args['q']
    try:
        data = custom_search(term)
        #  If search term yields no results, handle the error
    except IndexError:
        flash(f'No results for {term}','danger')
        return redirect ('/homepage')
 
    likes = get_likes(g.user.id)

    return render_template('custom_search.html', data = data, term=term, likes = likes)



