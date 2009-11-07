#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configuration as config
from google.appengine.api import users, memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app, login_required

from models import Person, Job, News, RECRUITERS_ID_URLS, JOB_TYPE_DISPLAY_LIST
from utils import render_template, dec, login_required_signup

class IndexHandler(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        news = News.get_latest(10)
        response = render_template('index.html', logout_url=logout_url, news=news)
        self.response.out.write(response)

class RecruitersPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('recruiters.html', logout_url=logout_url, recruiters_list=RECRUITERS_ID_URLS)
        self.response.out.write(response)

class Differential_LearningPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('differential_learning.html', logout_url=logout_url)
        self.response.out.write(response)
        
class ReportsPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('reports.html', logout_url=logout_url)
        self.response.out.write(response)


class ContactUsPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('contact_us.html', logout_url=logout_url)
        self.response.out.write(response)

class AchievementPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('achievements.html', logout_url=logout_url)
        self.response.out.write(response)

class EventsPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('event.html', logout_url=logout_url)
        self.response.out.write(response)

class GalleryPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('gallery.html', logout_url=logout_url)
        self.response.out.write(response)

class JobsNewPage(webapp.RequestHandler):
    @login_required_signup
    def get(self):
        logout_url = users.create_logout_url('/')
        response = render_template('post_job.html', logout_url=logout_url, job_type_display_list=JOB_TYPE_DISPLAY_LIST)
        self.response.out.write(response)

    def post(self):
        job = Job()
        #job.poster = users.get_current_user()
        job.title = self.request.get('title')
        job.description = self.request.get('description')
        job.salary = self.request.get('salary')
        job.location = self.request.get('location')
        job.industry = self.request.get('industry')
        job.contact_phone = self.request.get('contact_phone')
        job.job_type = self.request.get('job_type')
        job.company = self.request.get('company')
        job.contact_name = self.request.get('contact_name')
        job.contact_email = self.request.get('contact_email')
        job.is_active = True
        job.put()
        #self.response.out.write(job.to_json('title', 'is_deleted', 'is_active', 'is_starred', 'when_created'))
        self.redirect('/alumni/jobs/')

class JobsPage(webapp.RequestHandler):
    @login_required_signup
    def get(self):
        jobs = Job.get_latest(10)
        logout_url = users.create_logout_url('/')
        response = render_template('jobs.html', logout_url=logout_url, jobs=jobs)
        self.response.out.write(response)

class IndrelPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('forum/indrel.html', logout_url=logout_url)
        self.response.out.write(response)

class TrndevPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('forum/trndev.html', logout_url=logout_url)
        self.response.out.write(response)

class CombenPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None

        response = render_template('forum/comben.html', logout_url=logout_url)
        self.response.out.write(response)

class HipmsPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None

        response = render_template('forum/hipms.html', logout_url=logout_url)
        self.response.out.write(response)

class OddevPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logout_url = users.create_logout_url('/')
        else:
            logout_url = None
        response = render_template('forum/oddev.html', logout_url=logout_url)
        self.response.out.write(response)

class AccountHandler(webapp.RequestHandler):
    @login_required_signup
    def get(self):
        continue_uri = self.request.get('continue')
        person = Person.is_user_already_registered(users.get_current_user())
        if person:
            self.redirect(continue_uri)
        else:
            logout_url = users.create_logout_url('/')
            response = render_template('signup.html', logout_url=logout_url, continue_uri=continue_uri)
            self.response.out.write(response)

    def post(self):
        continue_uri = self.request.get('continue')
        person = Person()
        person.first_name = self.request.get('first_name')
        person.last_name = self.request.get('last_name')
        person.put()
        self.redirect(continue_uri)

urls = (
    ('/', IndexHandler),
    ('/placements/recruiters/?', RecruitersPage),
    ('/placements/differential_learning/?', Differential_LearningPage),
    ('/placements/reports/?', ReportsPage),
    ('/contactus/?', ContactUsPage),
    ('/alumni/achievements/?', AchievementPage),
    ('/alumni/events/?', EventsPage),
    ('/alumni/gallery/?', GalleryPage),
    ('/alumni/jobs/new/?', JobsNewPage),
    ('/alumni/jobs/?', JobsPage),
    ('/forum/indrel/?', IndrelPage),
    ('/forum/trndev/?', TrndevPage),
    ('/forum/comben/?', CombenPage),
    ('/forum/hipms/?', HipmsPage),
    ('/forum/oddev/?', OddevPage),

    ('/account/signup/?', AccountHandler),
)

application = webapp.WSGIApplication(urls, debug=config.DEBUG)


def main():
    from gaefy.db.datastore_cache import DatastoreCachingShim
    DatastoreCachingShim.Install()
    run_wsgi_app(application)
    DatastoreCachingShim.Uninstall()

if __name__ == '__main__':
    main()

