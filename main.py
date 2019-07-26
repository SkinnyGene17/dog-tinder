<<<<<<< HEAD
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, CSSI World!') #the response

# the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage), #this maps the root url to the Main Page Handler
], debug=True)
=======
import os
import socialdata
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template


def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))


def get_user_email():
    user = users.get_current_user()
    if user:
        return user.email()
    else:
        return None


def get_template_parameters():
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
    else:
        values['login_url'] = users.create_login_url('/')
    return values

class Image(webapp2.RequestHandler):
    def get(self):
        dog_key = ndb.Key(urlsafe=self.request.get('img_id'))
        dog = dog_key.get()
        if dog.image:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(dog.image)
        else:
            self.response.out.write('No image')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        if get_user_email():
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
                values['name'] = profile.name
        render_template(self, 'mainpage.html', values)

class ProfileViewHandler(webapp2.RequestHandler):
    def get(self, ids):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = socialdata.get_profile_by_name(ids)
            if profile:
                values['name'] = profile.name
                values['description'] = profile.description
                values['dogName'] = profile.dogName
                values['dogBreed'] = profile.dogBreed
            render_template(self, 'profile-view.html', values)

class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = socialdata.get_user_profile(get_user_email())
            if profile:
                values['name'] = profile.name
                values['description'] = profile.description
                values['dogName'] = profile.dogName
                values['dogBreed'] = profile.dogBreed
            render_template(self, 'profile-edit.html', values)


class ProfileSaveHandler(webapp2.RequestHandler):
    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get('name')
            description = self.request.get('description')
            dogName = self.request.get('dogName')
            dogBreed = self.request.get('dogBreed')

            if len(name) < 2:
                error_text += 'Your name must be at least 2 characters.\n'
            if len(name) > 30:
                error_text += 'Your name cannot be more than 30 characters.\n'
            if len(dogName) < 2:
                error_text += "Your dog's name must be at least 2 characters.\n"
            if len(description) > 4000:
                error_text += "Your dog's description is too long; 4000 characters or less.\n"
            for word in description.split():
                if len(word) > 50:
                    error_text += 'Make each word in your description no longer than 50 characters.\n'
                    break

            values = get_template_parameters()
            values['name'] = name
            values['description'] = description
            values['dogName'] = dogName
            values['dogBreed'] = dogBreed

            if error_text:
                values['errormsg'] = error_text
            else:
                socialdata.save_profile(email, name, description)
                values['successmsg'] = 'Successfully saved!'

            render_template(self, 'profile-edit.html', values)


app = webapp2.WSGIApplication([
    ('/profile-view/(.*)', ProfileViewHandler),
    ('/profile-edit', ProfileEditHandler),
    ('/profile-save', ProfileSaveHandler),
    ('/img', Image)
    ('.*', MainHandler),
])
>>>>>>> 07eb9675cf632b106bb26fdf8378bf0a82f74067
