#!/usr/local/python-3.6.5/bin/python3.6
# coding: utf-8
'''
Usage:
    install.py --name=<name> --email=<email>
'''

import os
import subprocess

COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_DEFAULT = '\033[0m'

HOME = os.path.expanduser('~')
WORKING_DIR = os.path.dirname(os.path.dirname(__file__))


def run(cmd, cwd=None):
    print('%srun:%s %s' % (COLOR_GREEN, COLOR_DEFAULT, cmd))
    process = subprocess.Popen(cmd.split(), env=os.environ, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, cwd=cwd)
    while process.returncode is None:
        line = process.stdout.readline()
        if len(line) == 0:
            break
        print(line.rstrip().decode('utf-8'))
    process.communicate()
    assert process.returncode == 0


def copy(src, path, is_dir=False):
    if is_dir:
        run('cp -rf %s %s' % (src, path))
    else:
        run('cp %s %s' % (src, path))


def check_oh_my_zsh():
    if not os.path.isdir(os.path.expanduser('~/.oh-my-zsh')):
        run('./oh_my_zsh.sh')
    else:
        run('cd %s/.oh-my-zsh && git checkout .' % HOME)
        run('sh %s/.oh-my-zsh/tools/upgrade.sh' % HOME)

    copy(os.path.join(WORKING_DIR, 'mytheme.zsh-theme'),
         os.path.join(HOME, '.oh-my-zsh/themes/mytheme.zsh-theme'))
    copy(os.path.join(WORKING_DIR, 'zshrc'), os.path.join(HOME, '.zshrc'))

    # zsh-autosuggestions
    url = 'https://github.com/zsh-users/zsh-autosuggestions'
    path = os.path.expanduser('~/.oh-my-zsh/custom/plugins/zsh-autosuggestions')
    if not os.path.isdir(path):
        run('git clone %s %s' % (url, path), cwd=HOME)


def check_vim():
    if not (os.path.isdir(os.path.expanduser('~/.vim')) and
            os.path.isdir(os.path.expanduser('~/.vim/bundle/Vundle.vim'))):
        run('git clone https://github.com/VundleVim/Vundle.vim.git '
            '%s/.vim/bundle/Vundle.vim' % HOME)

    if not os.path.isdir(os.path.expanduser('~/.vim/colors')):
        run('mkdir %s/.vim/colors' % HOME)
    copy(os.path.join(WORKING_DIR, 'solarized.vim'),
         os.path.join(HOME, '.vim/colors/solarized.vim'))
    copy(os.path.join(WORKING_DIR, 'molokai.vim'), os.path.join(HOME, '.vim/colors/molokai.vim'))

    if not os.path.isdir(os.path.expanduser('~/.vim/bundle/YouCompleteMe')):
        run('git clone https://github.com/Valloric/YouCompleteMe.git '
            '%s/.vim/bundle/YouCompleteMe' % HOME)

    ycm_core = '~/.vim/bundle/YouCompleteMe/third_party/ycmd/ycm_core.so'
    if not os.path.isfile(os.path.expanduser(ycm_core)):
        ycm_dir = '%s/.vim/bundle/YouCompleteMe' % HOME
        run(cmd='git submodule update --init --recursive', cwd=ycm_dir)
        run(cmd='./install.py --clang-completer', cwd=ycm_dir)


def check_configs():
    configs = [('gitconfig', '.gitconfig'), ('tmux.conf', '.tmux.conf'), ('vimrc', '.vimrc'),
               ('clang-format', '.clang-format'), ('dircolors.256dark', '.dir_colors'),
               ('zshrc', '.zshrc')]
    if not os.path.isdir(os.path.expanduser('~/.config')):
        os.makedirs(os.path.expanduser('~/.config'))
    copy(os.path.join(WORKING_DIR, 'flake8'), os.path.join(HOME, '.config/flake8'))
    for src, path in configs:
        copy(os.path.join(WORKING_DIR, src), os.path.join(HOME, path))
    run(cmd='git config --global user.name %s' % cmd_args['--name'], cwd=HOME)
    run(cmd='git config --global user.email %s' % cmd_args['--email'], cwd=HOME)


def check_dependency():
    print('====== check dependency ======')
    fmt_yes = '%-*s' + '[%syes%s]' % (COLOR_GREEN, COLOR_DEFAULT)
    fmt_no = '%-*s' + '[%sno%s]' % (COLOR_RED, COLOR_DEFAULT)
    try:
        import supervisor
        print(fmt_yes % (25, 'supervisor(%s)' % supervisor.__version__))
    except ImportError:
        print(fmt_no % (25, 'supervisor'))

    try:
        import flake8
        print(fmt_yes % (25, 'flake8(%s)' % flake8.__version__))
    except ImportError:
        print(fmt_no % (25, 'flake8'))

    try:
        import autopep8
        print(fmt_yes % (25, 'autopep8(%s)' % autopep8.__version__))
    except ImportError:
        print(fmt_no % (25, 'autopep8'))


if __name__ == '__main__':
    from docopt import docopt
    cmd_args = docopt(__doc__, version="zshenv v1.0")
    check_oh_my_zsh()
    check_vim()
    check_configs()
    check_dependency()
    print('%s[Finished]%s' % (COLOR_GREEN, COLOR_DEFAULT))
