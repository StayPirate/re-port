#!/usr/bin/env python3
import argparse
from port import PortList

VERSION=0.1

parser = argparse.ArgumentParser(
    description='Re-port client side.',
    epilog='More info at https://github.com/TuxMeaLux/re-port'
    )
parser.add_argument('address',
    help='Address of the server where to send test packets to.'
    )
parser.add_argument('--server-port',
    type=int,
    default=80,
    help='Communication channel\'s port where the server is listeing.'
    )
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--port',
    action='append',
    help='You can specify this options multiple times\
    (e.g. -p 5000 -p 10000-12000 -p 22,80,443).\
    To get more info check the website below.'
    )
group.add_argument('-f',
    dest='file_list',
    type=argparse.FileType('r'),
    help='You can specify a file which contains the list of ports to test.'
    )
parser.add_argument('--version',
    action='version',
    version='%(prog)s version {}'.format(VERSION)
    )
args = parser.parse_args()

ports = PortList(args.port)
