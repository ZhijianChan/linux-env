#! env python
# coding: utf-8
'''
Usage:
    install.py [--name=<name>] [--email=<email>] [--python-path=<python_path>]
'''

import os
import sh
import sys
from jinja2 import Environment, FunctionLoader

SHARG = {'_fg': True}


def hpath(path):
    return os.path.join(os.path.expanduser('~'), path)


def wpath(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


class Setup(object):

    def __init__(self):
        self.user_name = cmd_args['--name'] or input('name: ')
        self.user_email = cmd_args['--email'] or input('email: ')
        self.temp_env = Environment(loader=FunctionLoader(self._load_template))
        self.python_path, self.python_version = cmd_args['--python-path'] or self._get_python_path()

    def _load_template(self, path):
        with open(path) as temp:
            return temp.read()

    def _get_python_version(self, python_path):
        version = sh.Command(python_path)('-V', _err_to_out=True).strip()
        return version.split()[1]

    def _get_python_path(self):
        _python_paths = [sh.which('python'), sh.which('python3'), sh.which('python2')]
        python_paths = [str(path) for path in _python_paths if path]
        if os.path.isfile('/usr/local/python-3.6.5/bin/python'):
            python_paths.append('/usr/local/python-3.6.5/bin/python')

        if os.path.isdir('/usr/local/Cellar/python'):
            out = sh.find('/usr/local/Cellar/python', '-regex', '.*/bin/python3[0-9.]*$',
                          '-type', 'f', _piped=True)
            out = sh.sort(out, _piped=True)
            python_paths.append(sh.head(out, '-n1').strip())

        useable_pythons = []
        python_paths_set = set()
        for python_path in python_paths:
            if python_path in python_paths_set:
                continue
            python_paths_set.add(python_path)
            if os.path.realpath(python_path) in python_paths_set:
                continue
            python_paths_set.add(os.path.realpath(python_path))
            useable_pythons.append((python_path, self._get_python_version(python_path)))

        if len(useable_pythons) == 0:
            print('Not found python!!')
            sys.exit(1)

        error = ''
        while True:
            message = '{}\n{}select python path [{}]: '.format(
                '\n'.join(['{}. {} (v{})'.format(i, *e) for i, e in enumerate(useable_pythons)]),
                error, ','.join([str(i) for i in range(len(useable_pythons))]))
            num = int(input(message))
            if num < 0 or num >= len(useable_pythons):
                error = 'error: invalid input, try again!! '
                continue
            return useable_pythons[num]

    def _get_extra_paths(self):
        extra_paths = []
        for path in [os.path.dirname(self.python_path), '/usr/local/protobuf-3.5.2/bin',
                     '/usr/local/vim-release/bin']:
            if os.path.exists(path):
                extra_paths.append(path)
        print(extra_paths)
        return extra_paths

    def _python_environment(self):
        sh.mkdir('-p', hpath('.config'), **SHARG)
        sh.cp(wpath('python/flake8'), hpath('.config/flake8'), **SHARG)

        sh.pip('install', 'flake8', 'autopep8', 'pyyaml', '--user', **SHARG)

    def _ssh_environment(self):
        sh.mkdir('-p', hpath('.ssh'), **SHARG)
        sh.cp(wpath('ssh/config'), hpath('.ssh/config'), **SHARG)

    def _git_environment(self):
        sh.cp(wpath('git/gitconfig'), hpath('.gitconfig'), **SHARG)
        sh.git('config', '--global', 'user.name', self.user_name, **SHARG)
        sh.git('config', '--global', 'user.email', self.user_email, **SHARG)

    def _tmux_environment(self):
        sh.cp(wpath('tmux/tmux.conf'), hpath('.tmux.conf'), **SHARG)

    def _clang_environment(self):
        sh.cp(wpath('clang/clang-format'), hpath('.clang-format'), **SHARG)

    def _dircolors_environment(self):
        sh.cp(wpath('dircolors/dircolors.256dark'), hpath('.dir_colors'), **SHARG)

    def _zsh_environment(self):
        template = self.temp_env.get_template(wpath('zsh/zshrc.template'))
        with open(hpath('.zshrc'), 'w') as zshrc:
            zshrc.write(template.render(platform=sys.platform, extra_paths=self._get_extra_paths()))
        # sh.cp(wpath('zsh/zshrc'), hpath('.zshrc'), **SHARG)

        if os.path.isdir(hpath('.oh-my-zsh')):
            sh.zsh(hpath('.oh-my-zsh/tools/upgrade.sh'), **SHARG)
        else:
            install_script = 'https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh'
            sh.zsh('-c', '$(wget {} -O -)'.format(install_script), **SHARG)

        sh.cp(wpath('zsh/mytheme.zsh-theme'), hpath('.oh-my-zsh/themes/mytheme.zsh-theme'), **SHARG)

        # zsh-autosuggestions
        zsh_autosuggestions_path = hpath('.oh-my-zsh/custom/plugins/zsh-autosuggestions')
        if os.path.isdir(zsh_autosuggestions_path):
            os.chdir(zsh_autosuggestions_path)
            sh.git('pull', **SHARG)
            os.chdir(working_dir)
        else:
            sh.git('clone', 'https://github.com/zsh-users/zsh-autosuggestions',
                   zsh_autosuggestions_path, **SHARG)

    def _vim_environment(self):
        sh.mkdir('-p', hpath('.vim/colors'), **SHARG)
        sh.cp(wpath('vim/molokai.vim'), hpath('.vim/colors/molokai.vim'), **SHARG)
        sh.cp(wpath('vim/solarized.vim'), hpath('.vim/colors/solarized.vim'), **SHARG)

        sh.rsync('-rzvaP', wpath('vim/UltiSnips'), hpath('.vim'), **SHARG)

        vundle_dir = hpath('.vim/bundle/Vundle.vim')
        if os.path.isdir(vundle_dir):
            os.chdir(vundle_dir)
            sh.git('pull', **SHARG)
            os.chdir(working_dir)
        else:
            sh.git('clone', 'https://github.com/VundleVim/Vundle.vim.git', vundle_dir, **SHARG)

        template = self.temp_env.get_template(wpath('vim/vimrc.template'))
        with open(hpath('.vimrc'), 'w') as vimrc:
            vimrc.write(template.render(python_path=self.python_path))
        # sh.cp(wpath('vim/vimrc'), hpath('.vimrc'), **SHARG)

        sh.vim('+PluginInstall', '+qall', **SHARG)

        ycm_dir = hpath('.vim/bundle/YouCompleteMe')
        if not os.path.isdir(ycm_dir):
            sh.git('clone', 'https://github.com/Valloric/YouCompleteMe.git', ycm_dir, **SHARG)
        if not os.path.isfile(hpath('.vim/bundle/YouCompleteMe/third_party/ycmd/ycm_core.so')):
            os.chdir(ycm_dir)
            sh.git('submodule', 'update', '--init', '--recursive', **SHARG)
            sh.zsh('install.sh', '--clang-completer', **SHARG)
            os.chdir(working_dir)

    def start(self):
        sh.rm('-rf', wpath('bin/tp'), **SHARG)
        sh.ln('-s', wpath('bin/command.py'), wpath('bin/tp'), **SHARG)
        rows, columns = os.popen('stty size', 'r').read().split()
        terminal_width = int(columns)
        for module in ['zsh', 'vim', 'git', 'ssh', 'tmux', 'python', 'clang', 'dircolors']:
            print('{0:-^{1}}'.format(' {} environment '.format(module).upper(), terminal_width))
            getattr(self, '_{}_environment'.format(module))()

        sh.zsh(hpath('.zshrc'), **SHARG)


if __name__ == "__main__":
    from docopt import docopt
    cmd_args = docopt(__doc__, version="v1.0")
    working_dir = os.path.dirname(os.path.abspath(__file__))

    setup = Setup()
    setup.start()
