# !/usr/bin/env python
import os

import jinja2
import webapp2

from models import Guestbook
from models import Message

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
        return self.render_template("home.html")


class ResultHandler(BaseHandler):
    def post(self):
        params = {}
        params["publish"] = self.request.get("some_text")
        message = Message(message_text=params["publish"])
        message.put()
        return self.render_template("result.html", params)


class UnterseitenHandler(BaseHandler):
    def get(self):
        return self.render_template("unterseite.html")


class ListenHandler(BaseHandler):
    def get(self):
        message = Message.query().fetch()
        params = {}
        params["messages"] = message
        return self.render_template("liste.html", params)


class GaesteHandler(BaseHandler):
    def get(self):
        entry = Guestbook.query().order(-Guestbook.created).fetch()
        params = {}
        params["entries"] = entry
        return self.render_template("gaestebuch.html",params)

    def post(self):
        params = {}
        name = self.request.get("name")
        email = self.request.get("email")
        comment = self.request.get("comment")
        if not name:
            name = "Anonymous"
        params.update({"name": name, "email": email, "comment": comment})
        entry = Guestbook(name=params["name"], email=params["email"], text=params["comment"])
        entry.put()
        return self.redirect_to("gaeste")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/unterseite', UnterseitenHandler),
    webapp2.Route('/result', ResultHandler),
    webapp2.Route('/liste', ListenHandler),
    webapp2.Route('/gaestebuch', GaesteHandler, name="gaeste"),
], debug=True)
