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
import yaml


class MyCommand(object):

    def __init__(self):
        with open(os.path.join(working_dir, 'config.yaml')) as config_file:
            self.config = yaml.load(config_file.read())

    def get_host(self):
        pass

    def fixssh(self):
        agent_file = sh.find('/tmp', '-path', '/tmp/ssh-*', '-name', 'agent*', '-user', '${USER}',
                             _env=os.environ, _fg=True)
        print(agent_file)


if __name__ == "__main__":
    from docopt import docopt
    cmd_args = docopt(__doc__, version='1.0')
    print(cmd_args)
    working_dir = os.path.dirname(os.path.abspath(__file__))

    command = MyCommand()
    command.fixssh()
