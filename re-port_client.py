#!/usr/bin/env python3
import argparse

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

#parse input ports
port_list = []
try:
    for item in args.port:
        if '-' in item:
            min, max = item.split('-')
            for i in range(int(min), int(max)+1):
                port_list.append(i)
        elif ',' in item:
            for i in item.split(','):
                port_list.append(int(i))
        else:
            port_list.append(int(item))
except ValueError:
    print('Please input proper ports values.')

#check if there are values gragter then 65535 or smaller than 1
for port in port_list:
    if port < 1 or port > 65535:
        print('Port '+str(port)+' is not valid.')
