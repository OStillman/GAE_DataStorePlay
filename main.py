import jinja2
import os
import webapp2
from google.appengine.ext import ndb

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())  # Get the templates in current directory
)

class Person(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    age = ndb.IntegerProperty()


class MainPage(webapp2.RequestHandler):
    def get(self): #Quite literally responding to GET HTTP calls

        template = template_env.get_template('home.html')
        context = {
            'text': 'Hello',
        }
        self.response.out.write(template.render(context))

    def post(self):
        person_fname = self.request.get('firstname')
        person_sname = self.request.get('surname')
        person_age = int(self.request.get('age'))

        person_details = Person(first_name=person_fname, last_name=person_sname, age=person_age)
        person_details.put()

        self.redirect("/read")


class ReadPage(webapp2.RequestHandler):
    def get(self):
        q = Person.query()
        data = []
        for person in q:
            data.append([person.first_name, person.last_name, person.age])

        template = template_env.get_template('entries.html')
        context = {
            'data': data,
        }
        self.response.out.write(template.render(context))

application = webapp2.WSGIApplication([('/', MainPage), ('/read', ReadPage)], debug=True)  # Debug will be false when in production
