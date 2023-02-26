API: https://newsapi.org/

This website allows a user to view news items based off their favorite categories

Some features I chose to implement were
1. Liking news articles - This allows a user to save news articles they find interesting and have easy access to view them later on.
2. Saving search terms as a favorite category - If a user searches for something once, they have the option of adding that search term to their favorites so when they login, they will see news articles related to that search term
3. Saving Authors - This allows a user to save an Author as a favorite and view articles exclusively by them
4. Saving Sources - Similar to the saving authors feature, a user can save a favorite news source and view news articles by that source

The userflow for this website is
a. Signup using a unique username and email
b. The user is then redirected to a page where they can choose their favorite categories based off a pre-populated list
c. Once they select those categories, they will be redirected to their homepage where they will see news articles of those categories sorted by date
d. They can also search for other categories on the searchbar
f. Each news articles will display the author and the source, and the user can select either of those to add to their favorites. 

Tech Stack: HTML, CSS, Python, Flask, SQLAlchemy, Postgress

