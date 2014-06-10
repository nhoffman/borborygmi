#!/usr/bin/env python

"""
Colorize source-code blocks using pygments.
"""

import os
import sys
import argparse
import re

from lxml import html

from pygments import highlight
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters import get_formatter_by_name

from pygments_pprint_sql import SqlFilter

def get_lexer(css_class):
    """Associate css-classes in code blocks with pygemnts lexer names

    """

    lexers = {'src-python': 'python',
              'src-sh': 'bash',
              'src-sqlite': 'sql',
              'emacs-lisp': 'cl'}

    try:
        lexer = get_lexer_by_name(lexers[css_class])
    except KeyError:
        lexer = None
    else:
        if 'sql' in css_class:
            lexer.add_filter(SqlFilter())

    return lexer

def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help = "Input file name")
    parser.add_argument('-o', '--outfile',
                        help = "Output file name (replaces infile by default)")
    parser.add_argument('-L', '--list-lexers', action='store_true', default=False)

    args = parser.parse_args(arguments)

    if args.list_lexers:
        for x in get_all_lexers():
            print x
        sys.exit()

    formatter = get_formatter_by_name('html')

    with open(args.infile) as f:
        tree = html.fromstring(f.read())

    code_blocks = tree.xpath('//pre')
    for block in code_blocks:
        css_class = block.get('class').split()[-1]

        lexer = get_lexer(css_class)

        if lexer:
            colorized = html.fragment_fromstring(
                highlight(block.text, lexer, formatter),
                create_parent=False)

            parent = block.getparent()
            parent.replace(block, colorized)

    with open(args.outfile or args.infile, 'w') as f:
        f.write(html.tostring(tree))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
