#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configuration as config
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache, users
from google.appengine.ext.webapp.util import run_wsgi_app
from utils import render_template, dec
import logging
from models import Person, News, Job, JOB_TYPE_DISPLAY_LIST
from django.utils import simplejson as json
from datetime import datetime

MAX_FETCH_LIMIT = 400

logging.basicConfig(level=logging.INFO)

# Generic

class ApproveHandler(webapp.RequestHandler):
    def get(self, key):
        o = db.get(db.Key(key))
        o.is_active = True
        o.put()
        self.response.out.write(o.is_active)

class UnapproveHandler(webapp.RequestHandler):
    def get(self, key):
        o = db.get(db.Key(key))
        o.is_active = False
        o.put()
        self.response.out.write(o.is_active)

class DeleteHandler(webapp.RequestHandler):
    def get(self, key):
        o = db.get(db.Key(key))
        o.is_deleted = True
        o.put()
        self.response.out.write(o.is_deleted)

class UndeleteHandler(webapp.RequestHandler):
    def get(self, key):
        o = db.get(db.Key(key))
        o.is_deleted = False
        o.put()
        self.response.out.write(o.is_deleted)

class ToggleStarHandler(webapp.RequestHandler):
    def get(self, key):
        o = db.get(db.Key(key))
        o.is_starred = not o.is_starred
        o.put()
        self.response.out.write(o.is_starred)

# Specific

class PersonEditHandler(webapp.RequestHandler):
    def get(self, key):
        person = db.get(db.Key(key))
        person_email = person.user.email()
        response = render_template('admin/edit_person.html', person=person, person_email=person_email)
        self.response.out.write(response)

    def post(self, key):
        person = db.get(db.Key(key))
        person.first_name = self.request.get('first_name')
        person.last_name = self.request.get('last_name')
        person.put()
        self.response.out.write(person.to_json('first_name', 'last_name', 'is_deleted', 'is_active', 'is_starred', 'when_created'))

class PersonListHandler(webapp.RequestHandler):
    def get(self):
        people = Person.all().order('first_name').order('last_name').fetch(MAX_FETCH_LIMIT)
        people_list = []
        for person in people:
            people_list.append(person.to_json_dict('first_name', 'last_name', 'is_starred', 'is_active', 'is_deleted', 'when_created'))
        self.response.out.write(json.dumps(people_list))

class NewsApproveHandler(webapp.RequestHandler):
    def get(self, key):
        o = db.get(db.Key(key))
        o.is_active = True
        o.when_published = datetime.utcnow()
        o.put()
        self.response.out.write(o.is_active)

class NewsEditHandler(webapp.RequestHandler):
    def get(self, key):
        news = db.get(db.Key(key))
        response = render_template('admin/edit_news.html', news=news)
        self.response.out.write(response)

    def post(self, key):
        news = db.get(db.Key(key))

        content = self.request.get('content')

        news.title = self.request.get('title')
        news.slug_title = self.request.get('slug_title')
        news.content = self.request.get('content')
        news.when_published = datetime.utcnow()
        news.put()
        self.response.out.write(news.to_json('title', 'is_deleted', 'is_active', 'is_starred'))

class NewsNewHandler(webapp.RequestHandler):
    def get(self):
        today = datetime.utcnow()
        response = render_template('admin/new_news.html', today=today)
        self.response.out.write(response)

    def post(self):
        news = News()
        news.title = self.request.get('title')
        news.slug_title = self.request.get('slug_title')
        news.content = self.request.get('content')
        news.when_published = datetime.utcnow()
        news.put()
        self.response.out.write(news.to_json('title', 'is_deleted', 'is_active', 'is_starred'))


class NewsListHandler(webapp.RequestHandler):
    def get(self):
        news = News.all().order('title').fetch(MAX_FETCH_LIMIT)
        news_list = []
        for item in news:
            news_list.append(item.to_json_dict('title', 'is_starred', 'is_active', 'is_deleted', 'when_created'))
        self.response.out.write(json.dumps(news_list))

class JobEditHandler(webapp.RequestHandler):
    def get(self, key):
        job = db.get(db.Key(key))
        response = render_template('admin/edit_job.html', job=job, job_type_display_list=JOB_TYPE_DISPLAY_LIST)
        self.response.out.write(response)

    def post(self, key):
        job = db.get(db.Key(key))
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
        job.put()
        self.response.out.write(job.to_json('title', 'is_deleted', 'is_active', 'is_starred', 'when_created'))

class JobNewHandler(webapp.RequestHandler):
    def get(self):
        response = render_template('admin/new_job.html', job_type_display_list=JOB_TYPE_DISPLAY_LIST)
        self.response.out.write(response)

    def post(self):
        job = Job()
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
        job.put()
        self.response.out.write(job.to_json('title', 'is_deleted', 'is_active', 'is_starred', 'when_created'))

class JobListHandler(webapp.RequestHandler):
    def get(self):
        jobs = Job.all().order('title').fetch(MAX_FETCH_LIMIT)
        job_list = []
        for item in jobs:
            job_list.append(item.to_json_dict('title', 'is_starred', 'is_active', 'is_deleted', 'when_created'))
        self.response.out.write(json.dumps(job_list))

#class PersonEditHandler(webapp.RequestHandler):
#    def get(self, key):
#        user = db.get(db.Key(key))
#        response = render_template('admin/edit_user.html', user_key=key, user=user)
#        self.response.out.write(response)
#
#    def post(self, key):
#        user = db.get(db.Key(key))
#        user.full_name = self.request.get('full_name')
#        user.email = self.request.get('email')
#        user.phone_number = self.request.get('phone_number')
#        wants_book = self.request.get('wants_book')
#        if wants_book == 'yes':
#            user.wants_book = True
#        user.put()
#
#        self.response.out.write(user.to_json('full_name', 'wants_book', 'phone_number', 'email', 'is_starred', 'is_deleted', 'is_active'))
#
#class PersonListHandler(webapp.RequestHandler):
#    def get(self):
#        users = User.all().order('full_name').fetch(MAX_FETCH_LIMIT)
#        user_list = []
#        for user in users:
#            user_list.append(user.to_json_dict('full_name',
#                'is_starred', 'is_active', 'is_deleted', 'when_created'))
#        self.response.out.write(json.dumps(user_list))

urls = [
    (r'/api/people/(.*)/delete/?', DeleteHandler),
    (r'/api/people/(.*)/undelete/?', UndeleteHandler),
    (r'/api/people/(.*)/approve/?', ApproveHandler),
    (r'/api/people/(.*)/unapprove/?', UnapproveHandler),
    (r'/api/people/(.*)/toggle_star/?', ToggleStarHandler),
    (r'/api/people/list/?', PersonListHandler),
    (r'/api/people/(.*)/edit/?', PersonEditHandler),

    (r'/api/news/(.*)/delete/?', DeleteHandler),
    (r'/api/news/(.*)/undelete/?', UndeleteHandler),
    (r'/api/news/(.*)/approve/?', NewsApproveHandler),
    (r'/api/news/(.*)/unapprove/?', UnapproveHandler),
    (r'/api/news/(.*)/toggle_star/?', ToggleStarHandler),
    (r'/api/news/list/?', NewsListHandler),
    (r'/api/news/(.*)/edit/?', NewsEditHandler),
    (r'/api/news/new/?', NewsNewHandler),

    (r'/api/jobs/(.*)/delete/?', DeleteHandler),
    (r'/api/jobs/(.*)/undelete/?', UndeleteHandler),
    (r'/api/jobs/(.*)/approve/?', ApproveHandler),
    (r'/api/jobs/(.*)/unapprove/?', UnapproveHandler),
    (r'/api/jobs/(.*)/toggle_star/?', ToggleStarHandler),
    (r'/api/jobs/list/?', JobListHandler),
    (r'/api/jobs/(.*)/edit/?', JobEditHandler),
    (r'/api/jobs/new/?', JobNewHandler),
]
application = webapp.WSGIApplication(urls, debug=config.DEBUG)

def main():
    from gaefy.db.datastore_cache import DatastoreCachingShim
    DatastoreCachingShim.Install()
    run_wsgi_app(application)
    DatastoreCachingShim.Uninstall()

if __name__ == '__main__':
    main()

