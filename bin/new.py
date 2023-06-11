#!/usr/bin/env python

"""
Create a new post
"""

import os
import sys
import argparse
import re
import datetime

from os import path

def ask(field):
    return input('{}: '.format(field)).strip()


def main(arguments):

    fields = [('title', ''),
              ('category', 'notes'),
              ('tags', ''),
              ('date', None),]

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--org-content',
                        help = """Path to content dir [%(default)s]""",
                        default='org-content', metavar='PATH')
    parser.add_argument('-o', '--outfile',
                        help="""Name of the output file. Should end
                        with ".org" default: stdout""")
    parser.add_argument('-d', '--create-dir', help='create data dir',
                        default=False, action='store_true')

    for field, default in fields:
        parser.add_argument('--{}'.format(field),
                            default=default, help='default: %(default)s')

    args = parser.parse_args(arguments)

    vals = {}
    for field, default in fields:
        vals[field] = getattr(args, field) # or ask(field)

    vals['date'] = vals['date'] or datetime.date.today().strftime('%Y-%m-%d')

    fstr = """#+TITLE: {title}
#+DATE: {date}
#+CATEGORY: {category}
#+FILETAGS: {tags}
"""

    if args.outfile is None:
        outfile = '/dev/stdout'
    else:
        outfile = path.join(args.org_content, args.outfile)
        assert not path.exists(outfile)
        if args.create_dir:
            os.makedirs(outfile.replace('.org', ''))
        print(outfile)

    with open(outfile, 'w') as f:
        f.write(fstr.format(**vals))



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
