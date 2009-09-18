from google.appengine.ext import db
from django.utils import simplejson as json

class RegularModel(db.Model):
    """
    A model parent that includes properties and functionality
    common to many model classes.

    """
    is_deleted = db.BooleanProperty(default=False)
    is_starred = db.BooleanProperty(default=False)
    is_active = db.BooleanProperty(default=False)
    when_created = db.DateTimeProperty(auto_now_add=True)
    when_modified = db.DateTimeProperty(auto_now=True)

    def to_json_dict(self, *props):
        properties = self.properties()
        if props:
            serializable_properties = props
        else:
            serializable_properties = getattr(self, '__serialize__', [])
            if not serializable_properties:
                serializable_properties = properties.keys()
            else:
                serializable_properties.extend([
                    'is_deleted',
                    'is_starred',
                    'is_active',
                    'when_created',
                    'when_modified',
                    ])
        output = {}
        output['key'] = str(self.key())
        for prop in set(serializable_properties):
            v = properties[prop]
            if isinstance(v, db.DateTimeProperty) or isinstance(v, db.DateProperty):
                convert_function = (lambda d: d.strftime('%Y-%m-%dT%H:%M:%S'))
                output[prop] = convert_function(getattr(self, prop))
            elif isinstance(v, db.ReferenceProperty):
                str_key = str(getattr(self, prop).key())
                output[prop] = str_key
                #output[prop + '_key'] = str_key
            #elif isinstance(v, db.StringProperty):
            #    output[prop] = str(getattr(self, prop))
            #elif isinstance(v, db.BooleanProperty):
            #    output[prop] = bool(getattr(self, prop))
            else:
                output[prop] = getattr(self, prop)
        return output

    def to_json(self, *props):
        json_dict = self.to_json_dict(*props)
        return json.dumps(json_dict)

