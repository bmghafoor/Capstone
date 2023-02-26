import requests
from key import api_key
from models import News, Category, Author, Source, db

def search(term):
    res = requests.get('https://newsapi.org/v2/everything', params = {
        'q':term,
        'apiKey':api_key
    })

    data = res.json()

    for news in data['articles']:

        news_items = News.query.all()
        news_titles = [n.title for n in news_items]
        # Check to see if news titles returned from the API already exist in our database. This is to prevent duplicate news items.
        if news['title'] not in news_titles: 
        
            categories = Category.query.all()
            category_names = [c.name for c in categories]

            authors = Author.query.all()
            author_names = [a.name for a in authors]

            sources = Source.query.all()
            source_names = [s.name for s in sources]
            # If the term searched for is not in our database, add it to the database
            if term not in category_names:
                cat = Category(name = term)
                db.session.add(cat)
                db.session.commit()
            # If an author for a news item exists and its not currently in our database, add author to the database
            if news['author'] and news['author'] not in author_names:
                auth = Author(name = news['author'])
                db.session.add(auth)
                db.session.commit()
                author = Author.query.filter(Author.name == news['author']).all()
            
            if news['author']:
                author = Author.query.filter(Author.name == news['author']).all()

                
            # If a source for a news items exists and its not currently in our database, add source to database
            if news['source']['name'] and news['source']['name'] not in source_names:
                src = Source(name = news['source']['name'])
                db.session.add(src)
                db.session.commit()
            
            source = Source.query.filter(Source.name == news['source']['name']).all()

            category = Category.query.filter(Category.name == term).all()
            

            if news['author']:
                news_item = News(
                        title = news['title'],
                        author = author[0].id,
                        category = category[0].id,
                        source = source[0].id,
                        description = news['description'],
                        content = news['content'],
                        date = news['publishedAt'],
                        url = news['url'],
                        image = news['urlToImage']
                    )

                db.session.add(news_item)

            else:
                news_item = News(
                        title = news['title'],
                        category = category[0].id,
                        source = source[0].id,
                        description = news['description'],
                        content = news['content'],
                        date = news['publishedAt'],
                        url = news['url'],
                        image = news['urlToImage']
                    )

                db.session.add(news_item)




    return data

