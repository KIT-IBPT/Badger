import argparse

from .actions import show_info
from .actions.doctor import self_check
from .actions.routine import show_routine
from .actions.algo import show_algo
from .actions.env import show_env
from .actions.intf import show_intf
from .actions.run import run_routine
from .actions.test import run_test


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Badger the optimizer')
    parser.set_defaults(func=show_info)
    subparsers = parser.add_subparsers(help='Badger commands help')

    # Parser for the 'doctor' command
    parser_doctor = subparsers.add_parser(
        'doctor', help='Badger status self-check')
    parser_doctor.set_defaults(func=self_check)

    # Parser for the 'routine' command
    parser_routine = subparsers.add_parser('routine', help='Badger routines')
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

    # Parser for the 'run' command
    parser_run = subparsers.add_parser('run', help='Run routines')
    parser_run.add_argument('-a', '--algo', required=True,
                            help='Algorithm to use')
    parser_run.add_argument('-ap', '--algo_params',
                            help='Parameters for the algorithm')
    parser_run.add_argument('-e', '--env', required=True,
                            help='Environment to use')
    parser_run.add_argument('-ep', '--env_params',
                            help='Parameters for the environment')
    parser_run.add_argument('-c', '--config', required=True,
                            help='Config for the routine')
    parser_run.add_argument('-s', '--save',
                            help='The routine name to be saved')
    parser_run.set_defaults(func=run_routine)

    # Parser for the 'test' command
    parser_test = subparsers.add_parser('test', help='For dev')
    parser_test.add_argument('-a', '--algo', required=True,
                             help='Algorithm to use')
    parser_test.add_argument('-ap', '--algo_params',
                             help='Parameters for the algorithm')
    parser_test.add_argument('-e', '--env', required=True,
                             help='Environment to use')
    parser_test.add_argument('-ep', '--env_params',
                             help='Parameters for the environment')
    parser_test.add_argument('-c', '--config', required=True,
                             help='Config for the routine')
    parser_test.add_argument('-s', '--save',
                             help='The routine name to be saved')
    parser_test.set_defaults(func=run_test)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
