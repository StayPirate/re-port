#!/usr/bin/env python
import argparse
import time
from report import Report

VERSION=1.0

parser = argparse.ArgumentParser(
    description='Re-port is a tool to actively enumerate firewall rules.',
    epilog='More info at https://github.com/StayPirate/re-port'
    )
parser.add_argument('pcap',
    help='PCAP dump of receiving scan traffic',
    type=str
    )
parser.add_argument('--address',
    type=str,
    default=None,
    help='scanners\'s IP address. If unset, all the packets in the PCAP will be used to enumerate closed ports'
    )
parser.add_argument('--open',
    action='store_true',
    help='print open ports instead of closed ones'
    )
parser.add_argument('--version',
    action='version',
    version='%(prog)s version {}'.format(VERSION)
    )
parser.add_argument('-u', '--udp',
    action='store_true',
    help='search for UDP open ports instead of TCP'
    )
parser.add_argument("-v", "--verbose", 
    action="store_true",
    help="increase output verbosity"
    )
args = parser.parse_args()

start_time = time.time()

to_check_proto = 'tcp'
if args.udp:
    to_check_proto = 'udp'

with Report(pcap=args.pcap) as r:
    r.enumerate_ports(to_check_proto, args.address)
    r.print_ports(args.open)
    if args.verbose:
        print('\nProto: {} - Open: {} - Closed: {} - Total: {}'.format(to_check_proto, r.open, r.closed, r.open+r.closed))

if args.verbose:
    print('----- %.2f seconds -----' % (time.time() - start_time))