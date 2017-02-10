from google.appengine.ext import ndb

class Movie(ndb.Model):
    title = ndb.StringProperty()
    year = ndb.IntegerProperty()
    comment = ndb.TextProperty()
    rating = ndb.IntegerProperty()
    img = ndb.TextProperty()
    author = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)