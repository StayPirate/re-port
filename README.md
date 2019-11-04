# 📋 Re-port

Re-port can be used to actively probe firewalls to enumerate outgoing or ingoing blocking rules. Use it properly and you'll be able to get the firewall's configuration.  
I mainly developed it to help me in troubleshooting issues with a distributed network scanner I'm currently developing.

## How it works

This piece of code is just a PCAP parser, which means you have to provide it with a properly acquired network packet dump to get it works. The tool then will print out ports which _(according to the PCAP)_ are blocked by the firewall.

In order to use it, you need access at least to two machines. One sits behind the firewall you want to test and the other one on the other side.

There are two possible use cases:

* Enumerating outgoing rules.
  * The machine behind the firewall is used to fire probing packets, while the other one is used to receive and save them into a PCAP file.
* Enumerating ingoing rules.
  * The machine behind the firewall is used to receive and save probing packets into a PCAP file, while the other one is used to fire them.

You will need tools like tcpdump, tshark or wireshark to capture and save the network traffic (or any other sniffer), and tools like nmap or masscan to craft and send the probing packets. In the following examples, I will use masscan and tcpdump.

In case there is one more firewall right before the external machine (not the one behind the firewall you are going to test) it would be better to know what are the in-place rules. But that's not mandatory, you still can figure it out making more tests from different locations.

## How to use it

Following the below steps will help you to get an accurate outcome.  

Let's pretend we want to enumerate outgoing rules because we plan to run a network scanner later on that machine and so we want to be sure that no outgoing traffic will be blocked by our egress firewall.  
The machine behind the firewall has the ip `a.a.a.a` while the outside machine has `b.b.b.b`. This second machine would be the one where we will run the packet sniffer (in this case `tcpdump`) and the first one we are going to configure.

1. __PCAP Acquisition__

    We need to start a packet sniffer here in order to see which probing packets won't arrive to the destination. Considering this machine has the public ip `b.b.b.b` associated to the network interface `eth0` and __no firewall is running__. We run tcpdump as follow

        tcpdump -ni eth0 -w re-port.pcap src host a.a.a.a

    a file `re-port.pcap` will be generated and, after we finish our test, is the file we will pass to this tool. But we will see this part later.

2. __Probing traffic__

    We are going to generate 65535 `SYN` packets from the machine behind the firewall and send them to `b.b.b.b`.  
    To do that I use `masscan`. It allows us to set the rate with `--rate` option and how many packets craft for each specified port with `--retries` option. Both these options are important for us because we have to be sure all packets which can reach the destination would to it. Based on the bandwitdh you have on the source/destination packets could be lost due to the sending high rate. For this test we need to go slow and safe. In Italy we have a proverb which stands: _who goes slowly goes far_ that seems appropiate to me here.

        masscan -Pn -n -p 1-65535 --wait 5 -e eth0 --rate 350 --retries 2 --open b.b.b.b
    
    doing some tests I figure out that 350 packets per second sent twice per port, for a total of 131072 (128k) packets, takes around nine minutes without packet loss.

3. __Enumerate firewall rules__

    At this point we can use `Re-port` to get the list of the closed ports. Go back to the first machine, stop the packets sniffer `CTRL+C` and copy the `re-port.pcap` to the directory where you have the Re-port tool. You can now run it as following:

        ./enumerate.py re-port.pcap
    
## Enumerate UDP block rules

The previous examples were enumerating TCP blocking rules. If you want a list of all blocked UDP ports follow the above steps changing commands as follow:

    # Machine with b.b.b.b IP
    tcpdump -ni eth0 -w re-port.pcap src host a.a.a.a

    # Machine with a.a.a.a IP
    masscan -Pn -n -p U:1-65535 --wait 5 -e eth0 --rate 350 --retries 2 --open b.b.b.b

    # Re-port
    ./enumerate.py re-port.pcap --udp

## Re-port options

Run ./enumerate.py --help to show all the options

    $./enumerate.py --help
    usage: enumerate.py [-h] [--address ADDRESS] [--open] [--version] [-u] [-v] pcap

    Re-port is a tool to actively enumerate firewall rules.

    positional arguments:
    pcap               PCAP dump of receiving scan traffic

    optional arguments:
    -h, --help         show this help message and exit
    --address ADDRESS  scanners's IP address. If unset, all the packets in the
                        PCAP will be used to enumerate closed ports
    --open             print open ports instead of closed ones
    --version          show program's version number and exit
    -u, --udp          search for UDP open ports instead of TCP
    -v, --verbose      increase output verbosity

## Class report

Report is a python class and you can use/extend it as you like.  
It is iterable and you use it within a `with` statement.

    with Report('dump.pcap') as r:
        r.enumerate_ports('tcp', '127.0.0.1')
        r.print_ports()

or

    r = Report('dump.pcap')
    r.enumerate_ports('tcp', '127.0.0.1')
    for port in r:
        print('Open %d' % port)

## Acknowledgements

@r4d10n: for the simple idea behind this tool.