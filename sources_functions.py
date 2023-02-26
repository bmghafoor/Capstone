from models import Source, User_Source, db, User


def show_sources(g,form):
    """Show available sources from users to choose from"""
    all_sources = Source.query.all()
    curr_sources = User_Source.query.filter(User_Source.user_id == g.user.id).all()
    curr_sources_id = [c.source_id for c in curr_sources]
    available_sources = []
    # If a user has a source in their favorite list, they should not see it as an option to add again
    for source in all_sources:
        if source.id not in curr_sources_id:
             available_sources.append(source)

    form.source.choices = [(s.id, s.name) for s in available_sources]

def submit_source(userid,form):
    """Function for submitting multiple sources at once"""
    sources = form.source.data
    for source in sources:
        us = User_Source(user_id = userid, source_id = source)
        db.session.add(us)
        db.session.commit()

def user_sources(user_id):
    """Retrieve all sources a user has in their favorite list"""
    user = User.query.get_or_404(user_id)
    user_sources = User_Source.query.filter(User_Source.user_id == user.id).all()
    sources_id = [s.source_id for s in user_sources]
    sources = [Source.query.get(s) for s in sources_id]

    return sources

def add_source(user_id, src_id):
    """Add a single source to favorites"""
    user_source = User_Source(user_id = user_id, source_id = src_id)
    db.session.add(user_source)
    db.session.commit()


def delete_source(g,source_id):
    """Delete a Source"""
    source = User_Source.query.filter(User_Source.user_id == g.user.id, User_Source.source_id == source_id).all()
    db.session.delete(source[0])
    db.session.commit()



