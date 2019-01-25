#! env python
'''
Usage:
    tupu.py route
    tupu.py fixssh
    tupu.py --host=<host> --command=<command> [--jump-host=<jump_host> | --jump]

Options:
    --host=<host>, -h <host>                        remote host.
    --command=<command>, -c <command>               remote run command.
    --jump-host=<jump_host>, -j <jump_host>         jump host [default: git.tuputech.com].
    --jump, -J                                      use default jump host [default: false].
'''

import os
import sh
import pwd
import glob
import yaml


class MyCommand(object):

    def __init__(self):
        with open(os.path.join(working_dir, 'config.yaml')) as config_file:
            self.config = yaml.load(config_file.read())

    def get_host(self):
        pass

    def fixssh(self):
        for path in glob.glob('/tmp/ssh-*/agent*', recursive=True):
            if os.stat(path).st_uid == pwd.getpwnam(os.environ['USER']).pw_uid:
                link_file = os.path.expanduser('~/.ssh/ssh_auth_sock')
                sh.rm('-rf', link_file, _fg=True)
                sh.ln('-s', path, link_file, _fg=True)
                sh.Command('ssh-add')('-l', _fg=True)
                return
        print('not found ssh agent tmp file, please login again.')

    def route(self):
        pass

    def remote_run_command(self, host, command):
        pass


if __name__ == "__main__":
    from docopt import docopt
    cmd_args = docopt(__doc__, version='1.0')
    print(cmd_args)
    working_dir = os.path.dirname(os.path.abspath(__file__))

    command = MyCommand()
    if cmd_args['route']:
        command.route()
    elif cmd_args['fixssh']:
        command.fixssh()
