#!/usr/bin/env python3
import argparse

VERSION=0.1

parser = argparse.ArgumentParser(
    description='Re-port server side.',
    epilog='More info at https://github.com/StayPirate/re-port'
    )
parser.add_argument('--address',
    default='',
    help='Address where %(prog)s starts listening. Default all interfaces.'
    )
parser.add_argument('-p', '--port',
    type=int,
    default=80,
    help='Port where %(prog)s starts listening. Default %(default)s.'
    )
parser.add_argument('-v', '--verbose',
    action='count',
    default=0,
    help='Verbose mode, you can specify this option\
    many times to add more verbosity.'
    )
parser.add_argument('--version',
    action='version',
    version='%(prog)s version {}'.format(VERSION)
    )
args = parser.parse_args()
