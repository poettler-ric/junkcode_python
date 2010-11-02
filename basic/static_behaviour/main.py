#!/usr/bin/env python
import to_import

print "got:", to_import.get_var()
to_import.set_var("asdf")
print "got:", to_import.get_var()
