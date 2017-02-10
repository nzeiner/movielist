# !/usr/bin/env python
import os

import jinja2
import webapp2

from google.appengine.api import users

from models import Movie

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')

            params = {"logged_in": logged_in, "logout_url": logout_url, "user": user}
        else:
            logged_in = False
            login_url = users.create_login_url('/')

            params = {"logged_in": logged_in, "login_url": login_url, "user": user}

        return self.render_template("home.html", params)

    def post(self):
        title = self.request.get("title")
        year = int(self.request.get("year"))
        rating = int(self.request.get("rating"))
        img = self.request.get("img")
        comment = self.request.get("comment")
        newmovie = Movie(title=title, year=year,rating=rating, img=img, comment=comment)
        newmovie.put()
        return self.redirect_to("liste")


class ListHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = ""
        logout_url = ""
        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')
        else:
            logged_in = False
            login_url = users.create_login_url('/')

        movies = Movie.query().order(-Movie.rating).fetch()

        params = {"logged_in": logged_in, "login_url": login_url, "logout_url": logout_url, "user": user, "movies":movies}
        return self.render_template("liste.html", params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/thelist', ListHandler, name="liste"),
], debug=True)
