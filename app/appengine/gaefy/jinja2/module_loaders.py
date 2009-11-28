# -*- coding: utf-8 -*-
"""
    gaefy.jinja2.module_loaders
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Loads a pre-compiled template, stored as Python code in a template module.

    This loader requires a modification in Jinja2 code (see jinja2.diff). The
    change doesn't affect other loaders, only allows templates to be loaded
    as modules, as described in http://dev.pocoo.org/projects/jinja/ticket/349

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from os import path
from jinja2.exceptions import TemplateNotFound


class ModuleLoader(object):
    def __init__(self, templatemodule):
        """Loads a template from a module.

        `templatemodule`: a single module where compiled templates are stored.
        """
        self.modules = {}
        self.templatemodule = templatemodule

    def load(self, environment, filename, globals=None):
        """Loads a pre-compiled template, stored as Python code in a template
        module.
        """
        if globals is None:
            globals = {}

        # Strip '/' and remove extension.
        filename, ext = path.splitext(filename.strip('/'))

        if filename not in self.modules:
            # Store module to avoid unnecessary repeated imports.
            self.modules[filename] = self.get_module(environment, filename)

        tpl_vars = self.modules[filename].run(environment)

        t = object.__new__(environment.template_class)
        t.environment = environment
        t.globals = globals
        t.name = tpl_vars['name']
        t.filename = filename
        t.blocks = tpl_vars['blocks']

        # render function and module
        t.root_render_func = tpl_vars['root']
        t._module = None

        # debug and loader helpers
        t._debug_info = tpl_vars['debug_info']
        t._uptodate = lambda: True

        return t

    def get_module(self, environment, template):
        # Convert the path to a module name.
        module_name = self.templatemodule + '.' + template.replace('/', '.')
        prefix, obj = module_name.rsplit('.', 1)

        try:
            return getattr(__import__(prefix, None, None, [obj]), obj)
        except (ImportError, AttributeError):
            raise TemplateNotFound(template)
