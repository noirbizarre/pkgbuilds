'''
System, shell & invoke related helpers
'''
import os
import sys

from pathlib import Path
from invoke import task


#: Project absolute root path
ROOT = Path(__file__).parent
CWD = Path(os.getcwd())
PKG = CWD.stem


def color(code):
    '''A simple ANSI color wrapper factory'''
    return lambda t: '\033[{0}{1}\033[0;m'.format(code, t)


green = color('1;32m')
red = color('1;31m')
cyan = color('1;36m')
white = color('1;39m')
yellow = color('1;33m')


def header(text, *args, **kwargs):
    '''Display an header'''
    text = text.format(*args, **kwargs)
    print(' '.join((yellow('★'), white(text), yellow('★'))))
    sys.stdout.flush()


def info(text, *args, **kwargs):
    '''Display informations'''
    text = text.format(*args, **kwargs)
    print(' '.join((cyan('➤'), text)))
    sys.stdout.flush()


def success(text, *args, **kwargs):
    '''Display a success message'''
    text = text.format(*args, **kwargs)
    print(' '.join((green('✔'), white(text))))
    sys.stdout.flush()


def warn(text, *args, **kwargs):
    '''Display a warning message'''
    text = text.format(*args, **kwargs)
    print(' '.join((yellow('⚠'), white(text))))
    sys.stdout.flush()


def error(text, *args, **kwargs):
    '''Display an error message'''
    text = text.format(*args, **kwargs)
    print(' '.join((red('✘'), yellow(text))))
    sys.stdout.flush()


def exit(text=None, code=-1):
    if text:
        error(text)
    sys.exit(-1)


def ensure_pkg():
    if not CWD.parent == ROOT:
        exit('This command needs to be executed from a package dir')


@task
def debug(ctx):
    header('header')
    info('info')
    success('success')
    warn('warning')
    error('error')
    info(f'ROOT: {ROOT}')
    info(f'CWD: {CWD}')
    info(f'PKG: {PKG}')


@task
def update(ctx):
    ensure_pkg()
    header('Updating signatures')
    ctx.run('updpkgsums', pty=True)


@task
def build(ctx, force=False):
    '''Build the package'''
    ensure_pkg()
    header(f'Building {PKG}')
    cmd = 'makepkg'
    if force:
        cmd += ' -f'
    ctx.run(cmd, pty=True)


@task
def install(ctx):
    '''Install the package after a build if required'''
    ensure_pkg()
    header(f'Installing {PKG}')
    ctx.run('makepkg -si', pty=True)
