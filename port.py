from random import shuffle

class Port:
    """This object abstracts a network port."""
    def __init__(self, port):
        """Initialize a port with the integer value of the argument."""
        self.port = self.validate(int(port))

    def validate(self, value=None):
        """Validate the port and return itself.

        A port to be valid needs to be an integer number in between 1 and 65535.
        """
        if value is not None:
            if value < 1 or value > 65535:
                raise ValueError("Port value has to be in between 1 and 65535.")
            else:
                return value
        else:
            print("Please pass a value to validate.")

    def _has_valid_operand(self, other):
        """Check if the object has an attribute called port."""
        return hasattr(other, 'port')

    def __eq__(self, other):
        try:
            if self._has_valid_operand(other):
                return self.port == other.port
            return self.port == int(other)
        except ValueError as err:
            print("Compare error. {0}".format(err))
            raise
        else:
            return NotImplemented

    def __ne__(self, other):
        try:
            if self._has_valid_operand(other):
                return self.port != other.port
            return self.port != int(other)
        except ValueError as err:
            print("Compare error. {0}".format(err))
            raise
        else:
            return NotImplemented

    def __lt__(self, other):
        try:
            if self._has_valid_operand(other):
                return self.port < other.port
            return self.port < int(other)
        except ValueError as err:
            print("Compare error. {0}".format(err))
            raise
        else:
            return NotImplemented

    def __le__(self, other):
        try:
            if self._has_valid_operand(other):
                return self.port <= other.port
            return self.port <= int(other)
        except ValueError as err:
            print("Compare error. {0}".format(err))
            raise
        else:
            return NotImplemented

    def __gt__(self, other):
        try:
            if self._has_valid_operand(other):
                return self.port > other.port
            return self.port > int(other)
        except ValueError as err:
            print("Compare error. {0}".format(err))
            raise
        else:
            return NotImplemented

    def __ge__(self, other):
        try:
            if self._has_valid_operand(other):
                return self.port >= other.port
            return self.port >= int(other)
        except ValueError as err:
            print("Compare error. {0}".format(err))
            raise
        else:
            return NotImplemented


class PortList:
    """Create and manage a list of Port.

    A PortList object can be used to manage a list of Port objects.
    For instance could be useful to manage a series of ports to scan.
    """
    def __init__(self, unparsed_list=None):
        self.ports = []
        self.add(unparsed_list)
        self.index = 0 # Index to keep track of iterations

    def parse(self, unparsed_list):
        """Parse ports or port ranges and return a list of int.

        It can be passed a single value or a list of values to parse."""
        parsed_port = []
        try:
            for item in unparsed_list:
                if '-' in item:
                    min, max = item.split('-')
                    for i in range(int(min), int(max)+1):
                        parsed_port.append(i)
                elif ',' in item:
                    for i in item.split(','):
                        parsed_port.append(i)
                elif int(item):
                    parsed_port.append(item)
                else:
                    raise PortListFormatError(Exception)
        except ValueError as err:
            print('{0} Range port error.'.format(err))
            range_usage()
        except PortListFormatError:
            range_usage()
        else:
            return parsed_port

    def add(self, value=None):
        """Add ports to the list.

        The accepted format are specified on the class documentation.
        """
        if value is not None:
            for port_number in self.parse(value):
                if Port(port_number) not in self.ports:
                    self.ports.append(Port(port_number))
                else:
                    print("Port {0} was already in the list.".format(port_number))

    def remove(self, value=None):
        """Remove ports from the list.

        The accepted format are specified on the class documentation.
        """
        if value is not None:
            for port_number in self.parse(value):
                if Port(port_number) not in self.ports:
                    self.ports.remove(Port(port_number))
                else:
                    print("Port {0} was not present in the list.".format(port_number))

    def sort(self):
        """Sort ports in the list in numerical order."""
        self.port.sort()

    def shuffle(self):
        """Shuffle ports in the list. Useful for not sequential scans."""
        shuffle(self.ports)

    def range_usage(self):
        msg = """This program accepts three different way to specify ports.
            Single port: --port 22
            Multiple ports: --port 22,80,443
            Port range: --port 2000-2500
            The option --port or -p can be specified several times in the same command line.
        """
        print(msg)

    def __iter__(self):
        return self

    def __next__(self):
        if self.ports == None or self.index >= len(self.ports):
            raise StopIteration
        else:
            self.index = self.index + 1
            return self.ports[self.index - 1]


class PortListFormatError(Exception):
    """doc"""
    pass
