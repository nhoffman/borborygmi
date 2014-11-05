import sys
import re
import glob
from os import path, environ
from itertools import chain

if not 'VIRTUAL_ENV' in environ:
    sys.exit('No virtualenv is actuve')

from SCons.Script import (Variables, Depends, Environment, ARGUMENTS, Flatten)

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
vars.Add('content', 'compiled org-mode output',
         ARGUMENTS.get('content', 'content'))
vars.Add('output', 'site contents', ARGUMENTS.get('output', 'output'))
vars.Add('theme', 'theme name', ARGUMENTS.get('theme', 'theme'))

paths = ['org-export',
         path.join(environ['VIRTUAL_ENV'], 'bin'),
         '/usr/local/bin', '/usr/local/sbin', '/usr/bin', '/bin',
         '/usr/sbin', '/sbin', '/opt/X11/bin', '/usr/texbin']

env = Environment(ENV=dict(environ, PATH=':'.join(paths)),
                  variables=vars)

# list of org-mode fies containing posts
posts = [path.splitext(path.basename(p))[0]
         for p in glob.glob(env.subst('$org_content/*.org'))]

content = []
for post_name in posts:
    e = env.Clone()
    e['post'] = post_name
    post_dir = e['post_dir'] = e.subst('$org_content/$post')
    this_output = e['output'] = e.subst('$output/$post')

    check_filename(post_name)

    # html, = e.Command(
    #     target='$content/${post}.html',
    #     source='$org_content/${post}.org',
    #     action=('org-export pelican --infile $SOURCE --outfile $TARGET && '
    #             'bin/colorize.py $TARGET')
    # )
    # Depends(html, 'colorize.py')
    # content.append(html)

    html, = e.Command(
        target='$content/${post}.html',
        source='$org_content/${post}.org',
        action=('org-export pelican --infile $SOURCE '
                '--outfile $TARGET --package-dir emacs.d')
    )
    content.append(html)

    # copy any static or derived files associated with the post
    if path.isdir(post_dir):
        inputs = glob.glob(path.join(post_dir, '*'))
        outputs = e.Command(
            target=[fn.replace(post_dir, this_output) for fn in inputs],
            source=inputs,
            action='mkdir -p $output && rsync -a --delete $post_dir/ $output'
        )
        content.extend(outputs)

index, = env.Command(
    target='$output/index.html',
    source=content,
    action=('pelican content -t $theme && '
            'bin/fix_urls.py $output')
)
Depends(index, Flatten([content, 'bin/fix_urls.py', 'pelicanconf.py']))
Default(index)

publish_log, = env.Command(
    target='publish_log.txt',
    source='$output',
    action='ghp-import -p $SOURCE > $TARGET'
)
Depends(publish_log, [content, index])
Alias('publish', publish_log)

reset_log, = env.Command(
    target='reset_log.txt',
    source='$output',
    action='git push origin :gh-pages'
)
Alias('reset', reset_log)
