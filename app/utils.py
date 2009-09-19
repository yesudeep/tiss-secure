# -*- coding: utf-8 -*-

import configuration as config
from jinja2 import Environment, FileSystemLoader
from functools import partial
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.api.labs import taskqueue

jinja_env = Environment(loader=FileSystemLoader(['templates']))

#Jinja2 custom filters
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


jinja_env = Environment(loader=FileSystemLoader(['templates']))
jinja_env.filters['datetimeformat'] = datetimeformat


dec = partial(int, base=10)

def render_template(template_name, **context):
	template = jinja_env.get_template(template_name)
	new_context = {}
	new_context.update(config.TEMPLATE_BUILTINS)
	new_context.update(context)
	return template.render(new_context)

from datetime import datetime

def get_iso_datetime_string(date_object):
  return date_object.strftime('%Y-%m-%dT%H:%M:%S')

