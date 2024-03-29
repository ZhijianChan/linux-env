#! env python
'''
Usage:
    command.py route
    command.py fixssh
    command.py addkey --host=<host> --user=<user> --public-key=<key>
    command.py adduser --host=<host> --name=<name> [--public-key=<key>] [--shell=<shell> | --zsh]
    command.py [--host=<host> | <host>] [--command=<command>] [--user=<user>]
               [--jump-host=<jump_host> | --jump]

Options:
    --host=<host>, -h <host>                        remote host.
    --command=<command>, -c <command>               remote run command.
    --user=<user>, -u <user>                        remote login user.
    --jump-host=<jump_host>, -J <jump_host>         jump host.
    --jump, -j                                      use default jump host [default: false].
'''

import os
import sh

COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_DEFAULT = '\033[0m'


class MyCommand(object):

    def __init__(self):
        import yaml
        with open(os.path.join(working_dir, 'config.yaml')) as config_file:
            self.config = yaml.load(config_file.read())
        self._default_user = os.environ['USER']

    def get_host_by_type(self, host_type):
        import json
        import requests
        resp = requests.get('http://172.25.52.7:8888/getGPUClients?type={}'.format(host_type))
        assert resp.status_code == 200, resp.text
        return json.loads(resp.text)

    def fixssh(self):
        import pwd
        import glob
        # find /tmp -path '/tmp/ssh-*' -name 'agent*' -user ${USER}
        for path in glob.glob('/tmp/ssh-*/agent*', recursive=True):
            if os.stat(path).st_uid == pwd.getpwnam(self._default_user).pw_uid:
                link_file = os.path.expanduser('~/.ssh/ssh_auth_sock')
                # rm -rf ~/.ssh/ssh_auth_sock
                sh.rm('-rf', link_file, _fg=True)
                # ln -s ${ssh_agent_file} ~/.ssh/ssh_auth_sock
                sh.ln('-s', path, link_file, _fg=True)
                # ssh-add -l
                sh.Command('ssh-add')('-l', _fg=True)
                return
        print('not found ssh agent tmp file, please login again.')

    def route(self):
        # sudo route delete -net 172.25.52.0/24 192.168.1.250
        sh.sudo('route', 'delete', '-net', '172.25.52.0/24', '192.168.1.250', _fg=True)
        # sudo route add -net 172.25.52.0/24 192.168.1.250
        sh.sudo('sudo', 'route', 'add', '-net', '172.25.52.0/24', '192.168.1.250', _fg=True)
        # ssh-add -D
        sh.Command('ssh-add')('-D', _fg=True)
        # ssh-add ${HOME}/.ssh/id_rsa
        sh.Command('ssh-add')(os.path.expanduser('~/.ssh/id_rsa'), _fg=True)

    def _remote_host_command(self, host, command=None):
        if not host:
            print('\033[31mhost invalid!\033[0m host: {}'.format(host))
            return

        user = cmd_args['--user'] or self.config['username'] or self._default_user
        host = '{}@{}'.format(user, self._match_short_host(host))

        jump = None
        if cmd_args['--jump'] and self.config.get('jump_host'):
            jump = self.config['jump_host']
        elif cmd_args['--jump-host']:
            jump = cmd_args['--jump-host']

        print('\033[1;32m=======> host: {} jump: {} command: {}\033[0m'.format(host, jump, command))

        try:
            if jump and command:
                sh.ssh('-At', host, '-J', jump, command, _fg=True)
            elif jump:
                sh.ssh('-At', host, '-J', jump, _fg=True)
            elif command:
                sh.ssh('-At', host, command, _fg=True)
            else:
                sh.ssh('-At', host, _fg=True)
        except sh.ErrorReturnCode:
            print('{}ERROR{}'.format(COLOR_RED, COLOR_DEFAULT))

    def _match_short_host(self, host):
        for num in range(256):
            if host == '{}'.format(num):
                return '172.26.3.{}'.format(host)

            if host in ['2.{}'.format(num), '3.{}'.format(num)]:
                return '172.26.{}'.format(host)

            if host in ['52.{}'.format(num), ]:
                return '172.25.{}'.format(host)

            if host in ['1.{}'.format(num), ]:
                return '192.168.{}'.format(host)
        return host

    def remote_command(self):
        host = cmd_args['--host'] or cmd_args['<host>']
        if host in ['api', 'train', 'web']:
            if cmd_args['--command']:
                cmd_args['--user'] = 'zhangjiguo'
                for _host in self.get_host_by_type(host):
                    self._remote_host_command(host=_host, command=cmd_args['--command'])
                return
            print('command is None!')
            return

        host_key = '{}_host'.format(host)
        if isinstance(self.config.get(host_key, None), (list, tuple)):
            if cmd_args['--command']:
                for _host in self.config[host_key]:
                    self._remote_host_command(host=_host, command=cmd_args['--command'])
                return
            print('command is None!')
            return

        if host_key in self.config:
            host = self.config[host_key]

        if ',' in host:
            if cmd_args['--command']:
                for _host in host.split(','):
                    self._remote_host_command(host=_host, command=cmd_args['--command'])
                return
            print('command is None!')
            return

        self._remote_host_command(host=host, command=cmd_args['--command'])

    def create_user(self):
        pass

    def append_public_key(self):
        pass


if __name__ == "__main__":
    from docopt import docopt
    cmd_args = docopt(__doc__, version='1.0')
    # print(cmd_args)
    working_dir = os.path.dirname(os.path.abspath(__file__))

    my_command = MyCommand()
    if cmd_args['route']:
        my_command.route()
    elif cmd_args['fixssh']:
        my_command.fixssh()
    elif cmd_args['adduser']:
        my_command.create_user()
    elif cmd_args['addkey']:
        my_command.append_public_key()
    else:
        my_command.remote_command()
