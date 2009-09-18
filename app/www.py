#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configuration as config
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import RECRUITERS_ID_URLS
from utils import render_template, dec

class IndexHandler(webapp.RequestHandler):
    def get(self):
        response = render_template('index.html')
        self.response.out.write(response)

class RecruitersPage(webapp.RequestHandler):
    def get(self):
        response = render_template('recruiters.html', recruiters_list=RECRUITERS_ID_URLS)
        self.response.out.write(response)

class ContactUsPage(webapp.RequestHandler):
    def get(self):
        response = render_template('contact_us.html')
        self.response.out.write(response)

class AlumniPage(webapp.RequestHandler):
    def get(self):
        response = render_template('achievements.html')
        self.response.out.write(response)

urls = (
    ('/', IndexHandler),
    ('/placements/recruiters/?', RecruitersPage),
    ('/contactus/?', ContactUsPage),

    ('/alumni/achievements/?', AlumniPage)

)

application = webapp.WSGIApplication(urls, debug=config.DEBUG)


def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

