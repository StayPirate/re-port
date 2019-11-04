import sys
import dpkt
import socket
from dpkt.compat import compat_ord

class Report:
    """PCAP parsing and port enumeration
    
    You can use this class inside a "with" statement.
    Example:
        with Report('dump.pcap') as r:
            r.enumerate_ports('tcp', '127.0.0.1')
            r.print_ports()
    """

    MAX_PORT = 65535

    def __init__(self, pcap):
        self.open_ports = None
        self.dump_pcap = pcap
        self.open = 0       # Number of open ports
        self.closed = 0     # Number of closed ports
        self.index = 0      # Iteration index

        self.f = open(self.dump_pcap, 'rb')
        self.pcap = dpkt.pcap.Reader(self.f)

    def __del__(self):
        self.f.close()

    def _mac_addr(self, address):
        """Convert a MAC address to a readable/printable string.

        Parameters:
            address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
        Returns:
            str: Printable/readable MAC address
        """
        return ':'.join('%02x' % compat_ord(b) for b in address)

    def _inet_to_str(self, inet):
        """Convert inet object to a string.

            Parameters:
                inet (inet struct): inet network address
            Returns:
                str: Printable/readable IP address
        """
        # First try ipv4 and then ipv6
        try:
            return socket.inet_ntop(socket.AF_INET, inet)
        except ValueError:
            return socket.inet_ntop(socket.AF_INET6, inet)

    def _str_to_inet(self, address):
        """Convert string to a inet object.

            Parameters:
                str: Printable/readable IP address
            Returns:
                inet (inet struct): inet network address
        """
        # First try ipv4 and then ipv6
        try:
            return socket.inet_pton(socket.AF_INET, address)
        except ValueError:
            return socket.inet_pton(socket.AF_INET6, address)

    def _validate_ethernet_frame(self, packet):
        """Check if packet has a valid frame.

        This metodh has been implemented since a pcap could contain raw 
        IP packets. Assume a PCAP taken from a tun interface.

        Parameters:
            packet (dpkt.ethernet.Ethernet): a PCAP's element
        Returns:
            (boolean): True or False
        """
        switcher = {
            dpkt.ethernet.ETH_TYPE_EDP: True,
            dpkt.ethernet.ETH_TYPE_PUP: True,
            dpkt.ethernet.ETH_TYPE_IP: True,
            dpkt.ethernet.ETH_TYPE_ARP: True,
            dpkt.ethernet.ETH_TYPE_AOE: True,
            dpkt.ethernet.ETH_TYPE_CDP: True,
            dpkt.ethernet.ETH_TYPE_DTP: True,
            dpkt.ethernet.ETH_TYPE_REVARP: True,
            dpkt.ethernet.ETH_TYPE_8021Q: True,
            dpkt.ethernet.ETH_TYPE_8021AD: True,
            dpkt.ethernet.ETH_TYPE_QINQ1: True,
            dpkt.ethernet.ETH_TYPE_QINQ2: True,
            dpkt.ethernet.ETH_TYPE_IPX: True,
            dpkt.ethernet.ETH_TYPE_IP6: True,
            dpkt.ethernet.ETH_TYPE_PPP: True,
            dpkt.ethernet.ETH_TYPE_MPLS: True,
            dpkt.ethernet.ETH_TYPE_MPLS_MCAST: True,
            dpkt.ethernet.ETH_TYPE_PPPoE_DISC: True,
            dpkt.ethernet.ETH_TYPE_PPPoE: True,
            dpkt.ethernet.ETH_TYPE_LLDP: True,
            dpkt.ethernet.ETH_TYPE_TEB: True,
        }

        return switcher.get(packet.type, False)

    def _sort_ports(self):
        if self.open_ports == None:
            pass
        else:
            self.open_ports.sort()

    def enumerate_ports(self, proto='tcp', address=None):
        """Enumerate open ports from a PCAP file.

        Parse pakets from a PCAP, then filter them for protocol and
        source IP. Create a list with all the destination ports and 
        count the number of processed packets.

        Parameters:
            proto (str): allowed strings are "tcp" and "udp"
            address (str): source IP address of the scanner. Pakets don't match this source address are discarded
        """

        self.open_ports = list()

        try:
            if proto == 'tcp':
                to_check_proto = dpkt.ip.IP_PROTO_TCP
            elif proto == 'udp':
                to_check_proto = dpkt.ip.IP_PROTO_UDP
            else:
                raise ProtocolError(proto)
        except ProtocolError as e:
            sys.exit()

        for _, buf in self.pcap:    
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if self._validate_ethernet_frame(eth):
                    if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                        continue
                    ip = eth.data
                else:
                    ip = dpkt.ip.IP(buf)
            except dpkt.dpkt.UnpackError:
                continue
            
            # Discard not matching protocol packets
            if ip.p != to_check_proto:
                continue

            # Discard not matching source IP address packets
            if address is not None and self._str_to_inet(address) != ip.src:
                continue

            lvl4 = ip.data
            self.open_ports.append(lvl4.dport)
        
        # Make unique elements
        self.open_ports = list(set(self.open_ports))

        #Count open and closed ports
        self.open = len(self.open_ports)
        self.closed = self.MAX_PORT - self.open

    def print_ports(self, print_open=False):
        """Print open ports to stdout.
        
        For each possible port check if it has been found open, then
        print closed ones.

        Parameters:
            print_open (boolean): reverse the output, instead of closed ports print all open ones
        """
        self._sort_ports()

        for i in range(1, self.MAX_PORT):
            if i in self.open_ports:
                if print_open:
                    print('%d' % i)
            elif not print_open:
                print('%d' % i)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.__del__()

    def __iter__(self):
        self._sort_ports()
        return self

    def __next__(self):
        try:
            if self.open_ports == None:
                raise EmptyPortError
            if self.index >= len(self.open_ports):
                raise StopIteration
            else:
                self.index += 1
                return self.open_ports[self.index - 1]
        except EmptyPortError:
            raise StopIteration

class ProtocolError(Exception):
    def __init__(self, message):
        super().__init__(message)
        print('\'%s\' is not a supported protocol. Acceptable protocols are: \'tcp\', \'udp\'.' % message)

class EmptyPortError(Exception):
    def __init__(self):
        super().__init__()
        print('No packet dump has been processed yet.')
