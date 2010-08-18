#!/usr/bin/python

from Cheetah.Template import Template

print Template("start $test end", searchList={"test": "testinger"})
