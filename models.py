from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Person(polymodel.PolyModel):
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    email = db.EmailProperty()
    abstracts = db.IntegerProperty()
    
    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)
    
    def abstractSubmitted(self):
        if self.abstracts == None: self.abstracts = 1
        else: self.abstracts += 1

class Faculty(Person):
    pass
    
class Student(Person):
    mentor = db.ReferenceProperty(Faculty)

class Abstract(db.Model):
    title = db.StringProperty()
    abstract = db.TextProperty()
    authors = db.StringProperty()
    present_by = db.ReferenceProperty(Person)
    rating = db.IntegerProperty()
    total_ratings = db.IntegerProperty()
    is_starred = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)
