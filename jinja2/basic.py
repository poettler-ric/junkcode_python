#!/usr/bin/env python

""" Basic template test for jinja2. """

from jinja2 import Template

template = Template("hello {{ name }}")
print template.render(name="world")
