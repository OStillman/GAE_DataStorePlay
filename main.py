import jinja2
import os
import webapp2
from google.appengine.ext import ndb
import json

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

        q = Person.query()
        results = q.fetch(3)
        data = []
        for person in results:
            data.append([person.first_name, person.last_name, person.age])


        template = template_env.get_template('entries.html')
        context = {
            'data': data,
        }
        self.response.out.write(template.render(context))



application = webapp2.WSGIApplication([('/', MainPage)], debug=True)  # Debug will be false when in production
