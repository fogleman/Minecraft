# -*- coding: UTF-8 -*-


"""Manager module just to organize some tasks. It helps to compile and run the
game. Also cleans the directory, deleting .pyc and temporary files.

There is functionalities to commit and push/pull.

"""

# Imports, sorted alphabetically.

# Python packages
import subprocess
import sys

# Third-party packages
# Nothing for now...

# Modules from this project
# Nothing for now...


src = 'src'
images = 'resources/images'
sounds = 'resources/sounds'


def bash(command):
    """Run the command on bash"""

    print(command)
    subprocess.call(command, shell=True)

def clean():
    """Clean the repository."""

    command = 'rm %s/*.pyc' % src
    bash(command)
    bash('clear')

def run():
    """Compile all files .py and run main.py."""

    command = 'python %s/main.py' % src
    bash(command)

def commit(msg):
    """
    Commit on git.
    """

    clean()
    bash('git add README.md TODO.md LICENSE manager.py')
    bash('git add %s/*.py %s/*' % (src, images)) #TODO put 'sounds' dir
    bash('git commit -m "%s"' % msg)

def update(mode):
    """"""

    bash('git %s origin master' % mode)


args = sys.argv[1:]
if '--clean' in args:
    clean()
if '--run' in args:
    run()
if '--commit' in args:
    index = sys.argv.index('--commit')
    msg = sys.argv[index + 1]
    commit(msg)
if '--update' in args:
    index = sys.argv.index('--update')
    mode = sys.argv[index + 1]
    update(mode)
