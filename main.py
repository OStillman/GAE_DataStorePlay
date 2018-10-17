import jinja2
import os
import webapp2


template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())  # Get the templates in current directory
)

class MainPage(webapp2.RequestHandler):
    def get(self): #Quite literally responding to GET HTTP calls

        template = template_env.get_template('home.html')
        context = {
            'text': 'Hello',
        }
        self.response.out.write(template.render(context))


application = webapp2.WSGIApplication([('/', MainPage)], debug=True)  # Debug will be false when in production
