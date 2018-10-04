#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description='Re-port server side.', epilog='More info at https://github.com/TuxMeaLux/re-port')
parser.add_argument('--address', default='', help='Address where %(prog)s starts listening. Default all interfaces.')
parser.add_argument('-p', '--port', type=int, default=80, help='Port where %(prog)s starts listening. Default 80.')
parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbose mode, you can specify this option many times to add more verbosity.')
parser.add_argument('--version', action='version', version='%(prog)s version 0.1')
args = parser.parse_args()
