#!/usr/bin/env python
# -*- coding: utf-8 -*-


import configuration as config
from google.appengine.ext import db
from google.appengine.api import memcache, users
from util.db.models import RegularModel, Phone, PostalAddress, EmailAddress, ADDRESS_TYPES, EMAIL_TYPES, PHONE_TYPES
import logging

logging.basicConfig(level=logging.INFO)

CACHE_TIMEOUT = 60 # seconds

GENDER_CHOICES = (
    'male',
    'female'
)

RECRUITERS = {
    "asian-paints": {"name": "Asian Paints", "url": "http://asianpaints.com/"},
    "astrazeneca": {"name": "Astrazeneca", "url": "http://astrazeneca.com/"},
    "bennett-coleman": {"name": "Bennett Coleman", "url": "http://www.timesofindia.com/"},
    "countrywide-finances": {"name": "Countrywide Finances", "url": "http://my.countrywide.com/"},
    "siemens-india": {"name": "Siemens India", "url": "http://w1.siemens.com/"},
    "accenture": {"name": "Accenture", "url": "http://www.accenture.com/"},
    "bpcl": {"name": "Bharat Petroleum", "url": "http://www.bharatpetroleum.com/"},
    "cadbury": {"name": "Cadbury", "url": "http://www.cadburyindia.com/home/index.asp"},
    "citibank": {"name": "Citibank", "url": "http://www.citibank.com/us/home.htm"},
    "coca-cola": {"name": "Coca-Cola", "url": "http://www.coca-cola.com/index.jsp"},
    "colgate-palmolive": {"name": "Colgate Palmolive", "url": "http://www.colgate.co.in/app/Colgate/IN/HomePage.cvsp"},
    "deutsche-bank": {"name": "Deutsche Bank", "url": "http://www.db.com"},
    "dr-reddy": {"name": "Dr. Reddy", "url": "http://www.drreddys.com/"},
    "ernst-young": {"name": "Ernst Young", "url": "http://www.ey.com"},
    "fidelity": {"name": "Fidelity", "url": "http://www.fidelity.co.in/"},
    "google": {"name": "Google", "url": "http://www.google.com"},
    "ge-shipping": {"name": "GE Shipping", "url": "http://www.greatship.com/"},
    "hpcl": {"name": "Hindustan Petroleum", "url": "http://www.hindustanpetroleum.com/"},
    "honeywell": {"name": "Honeywell", "url": "http://www.honeywell.com/"},
    "hsbc": {"name": "HSBC", "url": "http://www.hsbc.co.in/"},
    "ibm": {"name": "IBM", "url": "http://www.ibm.com/"},
    "icici-prudential": {"name": "ICICI Prudential", "url": "http://www.iciciprulife.com/"},
    "kpmg": {"name": "KPMG", "url": "http://www.in.kpmg.com/"},
    "intel": {"name": "Intel", "url": "http://www.intel.com/"},
    "johnson-and-johnson": {"name": "Johnson and Johnson", "url": "http://www.jnj.com/"},
    "jp-morgan-chase": {"name": "JP Morgan Chase", "url": "http://www.jpmorganmf.com/"},
    "mahindra": {"name": "Mahindra", "url": "http://www.mahindra.com/"},
    "marico": {"name": "Marico", "url": "http://www.marico.com/"},
    "mercer": {"name": "Mercer", "url": "http://www.mercer.com/"},
    "microsoft": {"name": "Microsoft", "url": "http://www.microsoft.com/"},
    "motorola": {"name": "Motorola", "url": "http://www.motorola.com/in"},
    "nestle": {"name": "Nestle", "url": "http://www.nestle.com/"},
    "nokia": {"name": "Nokia", "url": "http://www.nokia.com"},
    "novartis": {"name": "Novartis", "url": "http://www.novartis.com/"},
    "oracle": {"name": "Oracle", "url": "http://www.oracle.com/"},
    "patni": {"name": "Patni", "url": "http://www.patni.com/"},
    "pepsi": {"name": "Pepsi", "url": "http://www.pepsi.com/"},
    "pfizer": {"name": "Pfizer", "url": "http://www.pfizer.com/"},
    "procter-and-gamble": {"name": "Procter and Gamble", "url": "http://www.pg.com/"},
    "pwc": {"name": "Price Waterhouse Coopers", "url": "http://www.pwc.com/"},
    "ranbaxy": {"name": "Ranbaxy", "url": "http://www.ranbaxy.com/"},
    "rpg": {"name": "RPG Group", "url": "http://www.rpggroup.com/"},
    "sap": {"name": "SAP", "url": "http://www.sap.com/"},
    "standard-chartered": {"name": "Standard Chartered", "url": "http://www.standardchartered.com/"},
    "sterlite": {"name": "Sterlite", "url": "http://www.sterlite-industries.com/"},
    "taj": {"name": "Taj Hotels", "url": "http://www.tajhotels.com/"},
    "tata": {"name": "TATA", "url": "http://www.tata.com/"},
    "wipro": {"name": "Wipro", "url": "http://www.wipro.com/"},
    "hindustan-unilever": {"name": "Hindustan Unilever", "url": "http://www.www.hul.co.in/"},
    "yahoo": {"name": "Yahoo! Inc.", "url": "http://www.yahoo.com/"},
}
RECRUITERS_ID_URLS = [(identifier, val["url"]) for identifier, val in RECRUITERS.iteritems()]


JOB_TYPE_DISPLAY_MAP = {
    'part_time': 'Part-Time',
    'permanent': 'Permanent',
    'contract': 'Contract',
}
JOB_TYPE_CHOICES = JOB_TYPE_DISPLAY_MAP.keys()
JOB_TYPE_CHOICES.sort()
JOB_TYPE_DISPLAY_LIST = [(k, v) for (k, v) in JOB_TYPE_DISPLAY_MAP.iteritems()]
JOB_TYPE_DISPLAY_LIST.sort()

logging.info(JOB_TYPE_DISPLAY_LIST)

# Specific
class Job(RegularModel):
    """
    Basic job model.
    """
    title = db.StringProperty()
    location = db.StringProperty()
    description = db.TextProperty()
    salary = db.StringProperty()
    job_type = db.StringProperty(choices=JOB_TYPE_CHOICES)
    contact_name = db.StringProperty()
    contact_email = db.EmailProperty()
    company = db.StringProperty()
    contact_phone = db.PhoneNumberProperty()
    industry = db.StringProperty()

class News(RegularModel):
    """
    News articles that will be displayed in the news section.
    """
    title = db.StringProperty()
    slug_title = db.StringProperty()
    content = db.TextProperty()
    content_html = db.TextProperty()
    when_published = db.DateTimeProperty()

    @classmethod
    def get_latest(cls, count=10):
        cache_key = 'News.get_latest(' + str(count) + ')'
        latest_news = memcache.get(cache_key)
        if not latest_news:
            latest_news = db.Query(News) \
                .order('-when_published') \
                .filter('is_active =', True) \
                .filter('is_deleted = ', False) \
                .fetch(count)
            memcache.set(cache_key, latest_news, CACHE_TIMEOUT)
        return latest_news

class Person(RegularModel):
    user = db.UserProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    gender = db.StringProperty(choices=GENDER_CHOICES)
    birthdate = db.DateTimeProperty()

class PersonAddress(PostalAddress):
    person = db.ReferenceProperty(Person, collection_name='addresses')

class PersonPhone(Phone):
    person = db.ReferenceProperty(Person, collection_name='phones')

class PersonEmailAddress(EmailAddress):
    person = db.ReferenceProperty(Person, collection_name='email_addresses')

class WorkExperience(RegularModel):
    company_name = db.StringProperty()
    start_year = db.IntegerProperty()
    end_year = db.IntegerProperty()
    designation = db.StringProperty()
    description = db.TextProperty()
    person = db.ReferenceProperty(Person, collection_name='work_experiences')

class Qualification(RegularModel):
    school = db.StringProperty()
    degree = db.StringProperty()
    graduation_year = db.IntegerProperty()
    decription = db.StringProperty()
    person = db.ReferenceProperty(Person, collection_name='qualifications')

