import argparse

import pandas  # noqa: F401

from .log import config_log
config_log()  # has to happen here to make sure the config taking effect
from .settings import init_settings
from .actions import show_info
from .actions.doctor import self_check
from .actions.routine import show_routine
from .actions.algo import show_algo
from .actions.env import show_env
from .actions.install import plugin_install
from .actions.uninstall import plugin_remove
from .actions.intf import show_intf
from .actions.run import run_routine
from .actions.config import config_settings


def main():
    # Initialize the Badger settings
    init_settings()

    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Badger the optimizer')
    parser.add_argument('-g', '--gui', action='store_true',
                        help='launch the GUI')
    parser.add_argument('-ga', '--gui-acr', action='store_true',
                        help='launch the GUI for ACR')
    parser.add_argument('-l', '--log', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
                        default='WARNING', const='WARNING', nargs='?',
                        help='change the log level')
    parser.set_defaults(func=show_info)
    subparsers = parser.add_subparsers(help='Badger commands help')

    # Parser for the 'doctor' command
    parser_doctor = subparsers.add_parser(
        'doctor', help='Badger status self-check')
    parser_doctor.set_defaults(func=self_check)

    # Parser for the 'routine' command
    parser_routine = subparsers.add_parser('routine', help='Badger routines')
    parser_routine.add_argument('routine_name',
                                nargs='?', type=str, default=None)
    parser_routine.add_argument('-r', '--run', action='store_true',
                                help='run the routine')
    parser_routine.add_argument('-y', '--yes', action='store_true',
                                help='run the routine without confirmation')
    parser_routine.add_argument('-v', '--verbose', type=int, choices=[0, 1, 2],
                                default=2, const=2, nargs='?',
                                help='verbose level of optimization progress')
    parser_routine.set_defaults(func=show_routine)

    # Parser for the 'algo' command
    parser_algo = subparsers.add_parser('algo', help='Badger algorithms')
    parser_algo.add_argument('algo_name', nargs='?', type=str, default=None)
    parser_algo.set_defaults(func=show_algo)

    # Parser for the 'intf' command
    parser_intf = subparsers.add_parser('intf', help='Badger interfaces')
    parser_intf.add_argument('intf_name', nargs='?', type=str, default=None)
    parser_intf.set_defaults(func=show_intf)

    # Parser for the 'env' command
    parser_env = subparsers.add_parser('env', help='Badger environments')
    parser_env.add_argument('env_name', nargs='?', type=str, default=None)
    parser_env.set_defaults(func=show_env)

    # Parser for the 'install' command     
    parser_inst = subparsers.add_parser('install', help='Badger install plugin')
    parser_inst.add_argument('plugin_type', nargs='?', type=str, default=None)
    parser_inst.add_argument('plugin_specific', nargs='?', type=str, default=None)
    parser_inst.set_defaults(func=plugin_install)

    # Parser for the 'remove' command     
    parser_remove = subparsers.add_parser('remove', help='Badger remove plugin')
    parser_remove.add_argument('plugin_type', nargs='?', type=str, default=None)
    parser_remove.add_argument('plugin_specific', nargs='?', type=str, default=None)
    parser_remove.set_defaults(func=plugin_remove)

    
    # Parser for the 'run' command
    parser_run = subparsers.add_parser('run', help='run routines')
    parser_run.add_argument('-a', '--algo', required=True,
                            help='algorithm to use')
    parser_run.add_argument('-ap', '--algo_params',
                            help='parameters for the algorithm')
    parser_run.add_argument('-e', '--env', required=True,
                            help='environment to use')
    parser_run.add_argument('-ep', '--env_params',
                            help='parameters for the environment')
    parser_run.add_argument('-c', '--config', required=True,
                            help='config for the routine')
    parser_run.add_argument('-s', '--save', nargs='?', const='',
                            help='the routine name to be saved')
    parser_run.add_argument('-y', '--yes', action='store_true',
                            help='run the routine without confirmation')
    parser_run.add_argument('-v', '--verbose', type=int, choices=[0, 1, 2],
                            default=2, const=2, nargs='?',
                            help='verbose level of optimization progress')
    parser_run.set_defaults(func=run_routine)

    # Parser for the 'config' command
    parser_config = subparsers.add_parser('config', help='Badger configurations')
    parser_config.add_argument('key', nargs='?', type=str, default=None)
    parser_config.set_defaults(func=config_settings)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
