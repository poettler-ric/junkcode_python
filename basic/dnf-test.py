#!/usr/bin/python

"""Prints upgradeable packages. Similar to ``dnf list upgrades -q``."""

import dnf

with dnf.Base() as base:
    base.read_all_repos()
    base.fill_sack()
    q = base.sack.query()
    u = q.upgrades()

    for p in u:
        print(p)
    print("count: %d" % len(u))
