from google.appengine.ext import ndb


class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    dogName = ndb.StringProperty()
    dogBreed = ndb.StringProperty()
    description = ndb.TextProperty()
