import sys
import re
import glob
from os import path, environ

from SCons.Script import (Variables, Depends, Environment, ARGUMENTS, Copy)


def check_filename(filename):
    fail = filename.startswith('.') or re.search(r'[_<>:"/\\|?*^% ]', filename)
    if fail:
        print ('The name "{}" contains illegal characters '
               '(should be alphanumeric or "-")').format(filename)
        sys.exit(1)


# variables defining destination for output files; can be redefined
# from the command line, eg "scons site=path/to/output"
vars = Variables()
vars.Add('org_content', 'org-mode source files',
         ARGUMENTS.get('org_content', 'org-content'))
vars.Add('content', 'compiled org-mode output', ARGUMENTS.get('content', 'content'))
vars.Add('output', 'site contents', ARGUMENTS.get('output', 'output'))
vars.Add('theme', 'theme name', ARGUMENTS.get('theme', 'tuxlite_tbs'))

paths = ['~/src/org-export'] + environ['PATH'].split(':')
if not 'VIRTUAL_ENV' in environ:
    venv = glob.glob('*-env')[0]
    paths.insert(0, path.join(venv, 'bin'))

env = Environment(ENV=dict(environ, PATH=':'.join(paths)),
                  variables=vars)

# list of org-mode fies containing posts
posts = [path.splitext(path.basename(p))[0]
         for p in glob.glob(env.subst('$org_content/*.org'))]

content = []
for post_name in posts:
    e = env.Clone()
    e['post'] = post_name
    check_filename(post_name)

    html, = e.Command(
        target='$content/${post}.html',
        source='$org_content/${post}.org',
        action=('org-export pelican --infile $SOURCE --outfile $TARGET')
    )

    content.append(html)

    post_dir = e.subst('$org_content/$post')
    if path.isdir(post_dir):
        post_files = glob.glob(path.join(post_dir, '*'))
        for fn in post_files:
            print fn
            copy, = e.Command(
                target='$output/$post/{}'.format(path.basename(fn)),
                source=fn,
                action=Copy('$TARGET', '$SOURCE')
            )

index, = env.Command(
    target='$output/index.html',
    source=content,
    action=('pelican content -t pelican-themes/$theme')
)
Depends(index, ['pelicanconf.py'])






