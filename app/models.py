#!/usr/bin/env python
# -*- coding: utf-8 -*-


import configuration as config
from google.appengine.ext import db
from google.appengine.api import memcache, users
from util.db.models import RegularModel, Phone, PostalAddress, EmailAddress, ADDRESS_TYPES, EMAIL_TYPES, PHONE_TYPES
from pprint import pprint
import logging

TAG_RECRUITMENT = 'recruitment'
TAG_INTERNSHIP = 'internship'
TAG_BFSI = 'bfsi'
TAG_FMCG = 'fmcg'
TAG_PHARMA = 'pharma'
TAG_IT = 'it'
TAG_SERVICES = 'services'
TAG_MEDIA = 'media'
TAG_MANUFACTURING = 'manufacturing'
TAG_CONSULTING = 'consulting'

logging.basicConfig(level=logging.INFO)

CACHE_TIMEOUT = 60 # seconds

GENDER_CHOICES = (
    'male',
    'female',
)


COMPANIES = {'abn-amro': {'name': 'ABN-AMRO',
              'tags': [TAG_INTERNSHIP, TAG_BFSI], 
              'url': 'http://abnamro.com/'},
    'accenture': {'name': 'Accenture',
               'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_IT],
               'url': 'http://www.accenture.com/'},
    'akzonobel': {'name': 'Akzonobel',
               'tags': [TAG_INTERNSHIP, TAG_MANUFACTURING],
               'url': 'http://www.akzonobel.com/'},
    'asian-paints': {'name': 'Asian Paints',
                  'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_MANUFACTURING],
                  'url': 'http://asianpaints.com/'},
    'astrazeneca': {'name': 'Astrazeneca',
                 'tags': [TAG_RECRUITMENT],
                 'url': 'http://astrazeneca.com/'},
    'barista': {'name': 'Barista',
             'tags': [TAG_RECRUITMENT],
             'url': 'http://www.barista.co.in/'},
    'bennett-coleman': {'name': 'Bennett Coleman',
                     'tags': [TAG_RECRUITMENT],
                     'url': 'http://www.timesofindia.com/'},
    'bindasmovies': {'name': 'Bindas Movies',
                  'tags': [TAG_RECRUITMENT],
                  'url': 'http://www.bindassmovies.com/'},
    'bpcl': {'name': 'Bharat Petroleum',
          'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_MANUFACTURING],
          'url': 'http://www.bharatpetroleum.com/'},
    'bru': {'name': 'Bru',
         'tags': [TAG_RECRUITMENT],
         'url': 'http://www.bindassmovies.com/'},
    'cadbury': {'name': 'Cadbury',
             'tags': [TAG_RECRUITMENT],
             'url': 'http://www.cadburyindia.com/home/index.asp'},
    'capgemini': {'name': 'Cap Gemini',
               'tags': [TAG_RECRUITMENT],
               'url': 'http://www.capgemini.com/'},
    'citibank': {'name': 'Citibank',
              'tags': [TAG_RECRUITMENT, TAG_BFSI],
              'url': 'http://www.citibank.com/us/home.htm'},
    'coca-cola': {'name': 'Coca-Cola',
               'tags': [TAG_RECRUITMENT],
               'url': 'http://www.coca-cola.com/index.jsp'},
    'colgate-palmolive': {'name': 'Colgate Palmolive',
                       'tags': [TAG_RECRUITMENT],
                       'url': 'http://www.colgate.co.in/app/Colgate/IN/HomePage.cvsp'},
    'countrywide-finances': {'name': 'Countrywide Finances',
                          'tags': [TAG_RECRUITMENT],
                          'url': 'http://my.countrywide.com/'},
    'crompton-greaves': {'name': 'Crompton-Greaves',
                      'tags': [TAG_INTERNSHIP, TAG_MANUFACTURING],
                      'url': 'http://www.cglonline.com/'},
    'ddi': {'name': 'Diagonstic Devices Inc.',
         'tags': [TAG_INTERNSHIP, TAG_CONSULTING],
         'url': 'http://www.prodigymeter.com/'},
    'deutsche-bank': {'name': 'Deutsche Bank',
                   'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_BFSI],
                   'url': 'http://www.db.com'},
    'dr-reddy': {'name': 'Dr. Reddy',
              'tags': [TAG_RECRUITMENT],
              'url': 'http://www.drreddys.com/'},
    'emkay': {'name': 'Emkay',
           'tags': [TAG_RECRUITMENT],
           'url': 'http://www.emkay.in/'},
    'ernst-young': {'name': 'Ernst Young',
                 'tags': [TAG_RECRUITMENT],
                 'url': 'http://www.ey.com'},
    'fame': {'name': 'Fame',
          'tags': [TAG_RECRUITMENT],
          'url': 'http://www.famecinemas.com/'},
    'fidelity': {'name': 'Fidelity',
              'tags': [TAG_RECRUITMENT],
              'url': 'http://www.fidelity.co.in/'},
    'firstsource': {'name': 'Firstsource',
                 'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_IT],
                 'url': 'http://www.firstsource.com/'},
    'g-mills': {'name': 'G Mills',
             'tags': [TAG_INTERNSHIP, TAG_FMCG],
             'url': 'http://www.generalmills.com/'},
    'ge-shipping': {'name': 'GE Shipping',
                 'tags': [TAG_RECRUITMENT],
                 'url': 'http://www.greatship.com/'},
    'glenmark': {'name': 'Glenmark',
              'tags': [TAG_INTERNSHIP, TAG_PHARMA],
              'url': 'http://www.glenmarkpharma.com/'},
    'godrej': {'name': 'Godrej',
            'tags': [TAG_INTERNSHIP, TAG_FMCG],
            'url': 'http://www.godrej.com/'},
    'google': {'name': 'Google',
            'tags': [TAG_RECRUITMENT],
            'url': 'http://www.google.com'},
    'hindustan-unilever': {'name': 'Hindustan Unilever',
                        'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_FMCG],
                        'url': 'http://www.www.hul.co.in/'},
    'honeywell': {'name': 'Honeywell',
               'tags': [TAG_RECRUITMENT],
               'url': 'http://www.honeywell.com/'},
    'hpcl': {'name': 'Hindustan Petroleum',
          'tags': [TAG_RECRUITMENT],
          'url': 'http://www.hindustanpetroleum.com/'},
    'hsbc': {'name': 'HSBC',
          'tags': [TAG_RECRUITMENT],
          'url': 'http://www.hsbc.co.in/'},
    'humancapital': {'name': 'Humancapital',
                  'tags': [TAG_RECRUITMENT],
                  'url': 'http://www.humancapital.net/'},
    'ibm': {'name': 'IBM',
         'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_IT],
         'url': 'http://www.ibm.com/'},
    'icici-prudential': {'name': 'ICICI Prudential',
                      'tags': [TAG_RECRUITMENT],
                      'url': 'http://www.iciciprulife.com/'},
    'indiadevelopmentgateway': {'name': 'India Development Gateway',
                             'tags': [TAG_RECRUITMENT],
                             'url': 'http://www.indg.in/'},
    'intel': {'name': 'Intel',
           'tags': [TAG_RECRUITMENT],
           'url': 'http://www.intel.com/'},
    'intellcap': {'name': 'Intellcap',
               'tags': [TAG_RECRUITMENT],
               'url': 'http://www.intellcap.com/'},
    'ninex-media': {'name': 'Ninex-media',
               'tags': [TAG_INTERNSHIP, TAG_MEDIA],
               'url': 'http://www.inxgroup.com/'},
    'johnson-and-johnson': {'name': 'Johnson and Johnson',
                         'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_FMCG],
                         'url': 'http://www.jnj.com/'},
    'jp-morgan-chase': {'name': 'JP Morgan Chase',
                     'tags': [TAG_RECRUITMENT],
                     'url': 'http://www.jpmorganmf.com/'},
    'kpmg': {'name': 'KPMG',
          'tags': [TAG_RECRUITMENT],
          'url': 'http://www.in.kpmg.com/'},
    'lbw': {'name': 'lbw',
         'tags': [TAG_RECRUITMENT],
         'url': 'http://www.consultlbw.com/'},
    'loreal': {'name': "L'oreal",
            'tags': [TAG_INTERNSHIP, TAG_FMCG],
            'url': 'http://www.loreal.co.in/'},
    'mafoi': {'name': 'Ma Foi',
           'tags': [TAG_RECRUITMENT],
           'url': 'http://www.mafoi.com/'},
    'mahindra': {'name': 'Mahindra',
              'tags': [TAG_RECRUITMENT],
              'url': 'http://www.mahindra.com/'},
    'marico': {'name': 'Marico',
            'tags': [TAG_RECRUITMENT],
            'url': 'http://www.marico.com/'},
    'mcdonalds': {'name': 'McDonalds',
               'tags': [TAG_INTERNSHIP, TAG_SERVICES],
               'url': 'http://www.mcdonaldsindia.com/'},
    'mercer': {'name': 'Mercer',
            'tags': [TAG_RECRUITMENT],
            'url': 'http://www.mercer.com/'},
    'microsoft': {'name': 'Microsoft',
               'tags': [TAG_RECRUITMENT],
               'url': 'http://www.microsoft.com/'},
    'monsato': {'name': 'Monsato',
             'tags': [TAG_INTERNSHIP, TAG_PHARMA],
             'url': 'http://www.monsatoindia.com/'},
    'motorola': {'name': 'Motorola',
              'tags': [TAG_RECRUITMENT],
              'url': 'http://www.motorola.com/in'},
    'naukri': {'name': 'Naukri',
            'tags': [TAG_RECRUITMENT],
            'url': 'http://www.naukri.com/'},
    'nen': {'name': 'NEN',
         'tags': [TAG_RECRUITMENT],
         'url': 'http://www.nenonline.com/'},
    'nestle': {'name': 'Nestle',
            'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_PHARMA],
            'url': 'http://www.nestle.com/'},
    'nielsen': {'name': 'Nielsen',
             'tags': [TAG_RECRUITMENT],
             'url': 'http://in.nielsen.com/'},
    'nokia': {'name': 'Nokia',
           'tags': [TAG_RECRUITMENT],
           'url': 'http://www.nokia.com'},
    'novartis': {'name': 'Novartis',
              'tags': [TAG_RECRUITMENT],
              'url': 'http://www.novartis.com/'},
    'nse': {'name': 'NSE',
         'tags': [TAG_INTERNSHIP, TAG_BFSI],
         'url': 'http://www.nseindia.com/'},
    'oracle': {'name': 'Oracle',
            'tags': [TAG_RECRUITMENT],
            'url': 'http://www.oracle.com/'},
    'pagalguy': {'name': 'Pagalguy',
              'tags': [TAG_RECRUITMENT],
              'url': 'http://www.pagalguy.com/'},
    'pantaloons-retail': {'name': 'Pantaloons-retail',
                       'tags': [TAG_INTERNSHIP, TAG_SERVICES],
                       'url': 'http://www.pantaloon.com/'},
    'patni': {'name': 'Patni',
           'tags': [TAG_RECRUITMENT],
           'url': 'http://www.patni.com/'},
    'pepsi': {'name': 'Pepsi',
           'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_FMCG],
           'url': 'http://www.pepsi.com/'},
    'pfizer': {'name': 'Pfizer',
            'tags': [TAG_RECRUITMENT],
            'url': 'http://www.pfizer.com/'},
    'powerhorse': {'name': 'Power Horse',
                'tags': [TAG_RECRUITMENT],
                'url': 'http://www.power-horse.com/'},
    'procter-and-gamble': {'name': 'Procter and Gamble',
                        'tags': [TAG_RECRUITMENT],
                        'url': 'http://www.pg.com/'},
    'pwc': {'name': 'Price Waterhouse Coopers',
         'tags': [TAG_RECRUITMENT],
         'url': 'http://www.pwc.com/'},
    'radio-mirchi': {'name': 'Radio Mirchi',
                  'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_MEDIA],
                  'url': 'http://www.radiomirchi.com/'},
    'ranbaxy': {'name': 'Ranbaxy',
             'tags': [TAG_RECRUITMENT],
             'url': 'http://www.ranbaxy.com/'},
    'rcf': {'name': 'rcf',
         'tags': [TAG_RECRUITMENT],
         'url': 'http://www.rcfltd.com/'},
    'rpg': {'name': 'RPG Group',
         'tags': [TAG_RECRUITMENT],
         'url': 'http://www.rpggroup.com/'},
    'sanofi-aventis': {'name': 'Sanofi-aventis',
                    'tags': [TAG_INTERNSHIP, TAG_PHARMA],
                    'url': 'http://www.radiomirchi.com/'},
    'sap': {'name': 'SAP', 'tags': [TAG_RECRUITMENT], 'url': 'http://www.sap.com/'},
    'schering-plough': {'name': 'Schering-plough',
                     'tags': [TAG_INTERNSHIP, TAG_PHARMA],
                     'url': 'http://www.schering-plough.com/'},
    'shell': {'name': 'Shell',
           'tags': [TAG_INTERNSHIP, TAG_MANUFACTURING],
           'url': 'http://www.shell.com/'},
    'shrmindia': {'name': 'SHRM India',
               'tags': [TAG_RECRUITMENT],
               'url': 'http://www.shrm.org/'},
    'siemens-india': {'name': 'Siemens India',
                   'tags': [TAG_RECRUITMENT],
                   'url': 'http://w1.siemens.com/'},
    'standard-chartered': {'name': 'Standard Chartered',
                        'tags': [TAG_RECRUITMENT],
                        'url': 'http://www.standardchartered.com/'},
    'sterlite': {'name': 'Sterlite',
              'tags': [TAG_RECRUITMENT],
              'url': 'http://www.sterlite-industries.com/'},
    'syntel': {'name': 'Syntel',
            'tags': [TAG_RECRUITMENT],
            'url': 'http://www.syntel.com/'},
    'taj': {'name': 'Taj Hotels',
         'tags': [TAG_RECRUITMENT, TAG_INTERNSHIP, TAG_SERVICES],
         'url': 'http://www.tajhotels.com/'},
    'tata': {'name': 'TATA',
          'tags': [TAG_RECRUITMENT],
          'url': 'http://www.tata.com/'},    
    'tata-powers': {'name': 'Tata Powers',
                 'tags': [TAG_INTERNSHIP, TAG_MANUFACTURING],
                 'url': 'http://www.tatapower.com/'},
    'tata-steel': {'name': 'Tata Steel',
                'tags': [TAG_INTERNSHIP, TAG_MANUFACTURING],
                'url': 'http://www.tatasteel.co.in/'},
    'timesascent': {'name': 'Time Ascent',
                 'tags': [TAG_RECRUITMENT],
                 'url': 'http://www.timeascent.in/'},
    'ucb': {'name': 'UCB', 'tags': [TAG_INTERNSHIP, TAG_PHARMA], 'url': 'http://www.ucb.com/'},
    'unitech': {'name': 'Unitech',
             'tags': [TAG_INTERNSHIP, TAG_MANUFACTURING],
             'url': 'http://www.unitech.com/'},
    'utv-i': {'name': 'UTV-i',
           'tags': [TAG_RECRUITMENT],
           'url': 'http://www.utv-i.com/'},
    'wipro': {'name': 'Wipro',
           'tags': [TAG_RECRUITMENT],
           'url': 'http://www.wipro.com/'},
    'wyeth': {'name': 'Wyeth',
           'tags': [TAG_INTERNSHIP, TAG_PHARMA],
           'url': 'http://www.wyethindia.com/'},
    'yahoo': {'name': 'Yahoo! Inc.',
           'tags': [TAG_RECRUITMENT],
           'url': 'http://www.yahoo.com/'},
}

RECRUITERS = {}
INTERNSHIPS = {}
BFSI = {}
FMCG = {}
PHARMA = {}
IT = {}
SERVICES = {}
MEDIA = {}
MANUFACTURING = {}
CONSULTING = {}


for identifier, company in COMPANIES.iteritems():
    tags = company.get('tags', [])
    if TAG_RECRUITMENT in tags:
        RECRUITERS[identifier] = company
    if TAG_INTERNSHIP in tags:
        INTERNSHIPS[identifier] = company
    if TAG_BFSI in tags:
        BFSI[identifier] = company
    if TAG_FMCG in tags:
        FMCG[identifier] = company
    if TAG_PHARMA in tags:
        PHARMA[identifier] = company
    if TAG_IT in tags:
        IT[identifier] = company
    if TAG_SERVICES in tags:
        SERVICES[identifier] = company
    if TAG_MEDIA in tags:
        MEDIA[identifier] = company
    if TAG_MANUFACTURING in tags:
        MANUFACTURING[identifier] = company  
    if TAG_CONSULTING in tags:
        CONSULTING[identifier] = company
        

    
RECRUITERS_ID_URLS = [(identifier, val["url"]) for identifier, val in RECRUITERS.iteritems()]
BFSI_ID_URLS = [(identifier, val["url"]) for identifier, val in BFSI.iteritems()]
FMCG_ID_URLS = [(identifier, val["url"]) for identifier, val in FMCG.iteritems()]
PHARMA_ID_URLS = [(identifier, val["url"]) for identifier, val in PHARMA.iteritems()]
IT_ID_URLS = [(identifier, val["url"]) for identifier, val in IT.iteritems()]
SERVICES_ID_URLS = [(identifier, val["url"]) for identifier, val in SERVICES.iteritems()]
MEDIA_ID_URLS = [(identifier, val["url"]) for identifier, val in MEDIA.iteritems()]
MANUFACTURING_ID_URLS = [(identifier, val["url"]) for identifier, val in MANUFACTURING.iteritems()]
CONSULTING_ID_URLS = [(identifier, val["url"]) for identifier, val in CONSULTING.iteritems()]

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
    poster = db.UserProperty(auto_current_user_add=True)

    @classmethod
    def get_latest(cls, count=10):
        cache_key = 'Job.get_latest(' + str(count) + ')'
        latest_jobs = memcache.get(cache_key)
        if not latest_jobs:
            latest_jobs = db.Query(Job) \
                .order('-when_created') \
                .filter('is_active =', True) \
                .filter('is_deleted = ', False) \
                .fetch(count)
            memcache.set(cache_key, latest_jobs, CACHE_TIMEOUT)
        return latest_jobs

class News(RegularModel):
    """
    News articles that will be displayed in the news section.
    """
    title = db.StringProperty()
    slug_title = db.StringProperty()
    content = db.TextProperty()
    content_html = db.TextProperty()
    when_published = db.DateTimeProperty()
    author = db.UserProperty(auto_current_user_add=True)

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
    user = db.UserProperty(auto_current_user_add=True)
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    gender = db.StringProperty(choices=GENDER_CHOICES)
    birthdate = db.DateTimeProperty()

    @classmethod
    def is_user_already_registered(cls, user):
        person = db.Query(Person).filter('user =', user).get()
        return person

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


