#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configuration as config
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Job, News, RECRUITERS_ID_URLS
from utils import render_template, dec

class IndexHandler(webapp.RequestHandler):
    def get(self):
        news = News.get_latest(10)
        response = render_template('index.html', news=news)
        self.response.out.write(response)

class RecruitersPage(webapp.RequestHandler):
    def get(self):
        response = render_template('recruiters.html', recruiters_list=RECRUITERS_ID_URLS)
        self.response.out.write(response)

class ContactUsPage(webapp.RequestHandler):
    def get(self):
        response = render_template('contact_us.html')
        self.response.out.write(response)

class AchievementPage(webapp.RequestHandler):
    def get(self):
        response = render_template('achievements.html')
        self.response.out.write(response)

class EventPage(webapp.RequestHandler):
    def get(self):
        response = render_template('event.html')
        self.response.out.write(response)

class GalleryPage(webapp.RequestHandler):
    def get(self):
        response = render_template('gallery.html')
        self.response.out.write(response)

class JobBoardPage(webapp.RequestHandler):
    def get(self):
        response = render_template('job_board.html')
        self.response.out.write(response)

class IndrelPage(webapp.RequestHandler):
    def get(self):
        response = render_template('indrel.html')
        self.response.out.write(response)

class TrndevPage(webapp.RequestHandler):
    def get(self):
        response = render_template('trndev.html')
        self.response.out.write(response)

class CombenPage(webapp.RequestHandler):
    def get(self):
        response = render_template('comben.html')
        self.response.out.write(response)

class HipmsPage(webapp.RequestHandler):
    def get(self):
        response = render_template('hipms.html')
        self.response.out.write(response)

class OddevPage(webapp.RequestHandler):
    def get(self):
        response = render_template('oddev.html')
        self.response.out.write(response)

urls = (
    ('/', IndexHandler),
    ('/placements/recruiters/?', RecruitersPage),
    ('/contactus/?', ContactUsPage),
    ('/alumni/achievements/?', AchievementPage),
    ('/alumni/events/?', EventPage),
    ('/alumni/gallery/?', GalleryPage),
    ('/alumni/job_board/?', JobBoardPage),
    ('/forum/indrel/?', IndrelPage),
    ('/forum/trndev/?', TrndevPage),
    ('/forum/comben/?', CombenPage),
    ('/forum/hipms/?', HipmsPage),
    ('/forum/oddev/?', OddevPage)
)

application = webapp.WSGIApplication(urls, debug=config.DEBUG)


def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

