# 📋 Re-port

Re-port is a tool useful to test your firewall setup, even when you have no access to its configuration.
I've mainly built this tool to be sure my VPS provider does not interfere with the scanner I use to do my pentests.

## How it works

It's composed by two main python scripts, one which needs to run in a trusted server and the other on the machine where you want to test the firewall configuration.

* **Server**

 You need to be sure from the server side you can receive packets on every port you want to test on the firewall's client side, so double check your firewall rules.
 This script needs to be started at first, it will start listening on port 80/TCP. When the client will be executed, passing the IP of this server as the option, it will established a session with this server and it will use this port as the communication channel.

 After the successful negotiation of a session key, it will start listening on each port the client would like to test. All the coordination with the client will happen inside the communication channel. _Only one client at time can be connected to the server, due this script does not create any thread after a client connection. It is a well-wanted behavior because we want to leave many free ports as possible to permit the client to test as many ports as possible._

* **Client**

 That's the part you have to run on the machine where you want to test the firewall rules.

 After it has successfully connected to the server, it will negotiate a session key that it will be later used to authenticate each probe packets.
 It then will start to probe every port accordingly with the server while speaking on the communication channel.

## How to use

#### Client options

Ports you want to test can be specified with the same sintax nmap uses.
For instance, if you want to test ports 22, 80 and 443 you can just run

    ./re-port_client <server-ip> 22,80,443

while if you want to test the first 1024 ports

    ./re-port_client <server-ip> 0-10

without specifying any port, by default re-port will test the full range (0-65535), port 80 excluded, with TCP.

You can switch to test udp ports adding the `--udp` options

    ./re-port_client --udp <server-ip> [ports]

#### Server options

The server can be spawned with the following command. More options can be displayed with `--help`.

    ./re-port_server

By default it starts to listen on port 80.
