#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configuration as config
#import logging
from google.appengine.api import users, memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from utils import dec
from haggoo.template.jinja2 import render_generator
from gaefy.jinja2.code_loaders import FileSystemCodeLoader

render_template = render_generator(loader=FileSystemCodeLoader, builtins=config.TEMPLATE_BUILTINS)

#logging.basicConfig(level=logging.DEBUG)

class PeopleHandler(webapp.RequestHandler):
    def get(self):
        response = render_template('admin/generic_list.html', page_name='people', page_description='Approving and editing personal information is easy.')
        self.response.out.write(response)

class JobsHandler(webapp.RequestHandler):
    def get(self):
        response = render_template('admin/generic_list.html', page_name='jobs', page_description='Add, remove or update jobs.')
        self.response.out.write(response)

class NewsHandler(webapp.RequestHandler):
    def get(self):
        response = render_template('admin/generic_list.html', page_name='news', page_description='Add and update news.')
        self.response.out.write(response)

urls = [
    ('/admin/?', PeopleHandler),
    ('/admin/people/?', PeopleHandler),
    ('/admin/jobs/?', JobsHandler),
    ('/admin/news/?', NewsHandler),
]
application = webapp.WSGIApplication(urls, debug=config.DEBUG)

def main():
    from gaefy.db.datastore_cache import DatastoreCachingShim
    DatastoreCachingShim.Install()
    run_wsgi_app(application)
    DatastoreCachingShim.Uninstall()

if __name__ == '__main__':
	main()

