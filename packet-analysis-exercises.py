# Imports
from scapy.all import *
import sys
import re
import ipaddress

# I need some way to keep track of relationships
class Connection:
    def __init__(self, source, destination, size):
        self.source = source
        self.destination = destination
        self.packets = 1
        self.bytes = size

    def __str__(self):
        return f"SRC: {self.source:^15}\tDST: {self.destination:^15}\tPKTS: {self.packets:^8}\tBYTES: {self.bytes:^8}"

# Utility class for tracking hosts - now I can make a collection of hosts & search through them
class Host:
    def __init__(self, IP="", MAC="", name=""): # name is for future implementation
        self.IP = IP
        self.MAC = MAC
        self.name = name

    def __str__(self):
        return f"IP: {self.IP:^15}\tMAC: {self.MAC:^19}\tHostname: {self.name}"

    def __hash__(self):
        return hash((self.IP, self.MAC, self.name))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.MAC == other.MAC and self.IP == other.IP and self.name == other.name


def getProtocols(pkts):
    stats = {}

    def tallyProtocol(proto):
        namedProtocols = {443:"HTTPS", 22:"SSH", 80:"HTTP", 25:"SMTP", 139:"NetBios", 445:"MS-RPC",
                          69:"TFTP", 20:"FTP-data", 21:"FTP-command", 23:"Telnet", 53:"DNS"}
        nonlocal stats
        nonlocal pkt
        if(proto in namedProtocols.keys()):
            proto = namedProtocols[proto]
        if proto in stats.keys():
            stats[proto] = stats[proto]+1
        else:
            stats[proto] = 1
        return stats

    for pkt in pkts:
        # We'll track "TCP" and "UDP" separately from protocols.
        if pkt.haslayer(TCP):
            stats = tallyProtocol("TCP")
            if pkt.getlayer(TCP).dport < 1025:
                stats = tallyProtocol(pkt.getlayer(TCP).dport)
                #print("DEBUG: tcp.dport < 1025")
            elif pkt.getlayer(TCP).sport < 1025:
                stats = tallyProtocol(pkt.getlayer(TCP).sport)
                #print("DEBUG: tcp.sport < 1025")
        elif pkt.haslayer(UDP):
            stats = tallyProtocol("UDP")
            if pkt.getlayer(UDP).dport < 1025:
                stats = tallyProtocol(pkt.getlayer(UDP).dport)
                #print("DEBUG: udp.dport < 1025")
            elif pkt.getlayer(UDP).sport < 1025:
                stats = tallyProtocol(pkt.getlayer(UDP).sport)
                #print("DEBUG: udp.sport < 1025")
        elif pkt.haslayer(ARP):
            stats = tallyProtocol("ARP")

    return stats

def getConnections(pkts):
    connections = []

    def logConnection(pkt):
        nonlocal connections
        match = False
        if pkt.haslayer(IP):
            src = pkt.getlayer(IP).src
            dst = pkt.getlayer(IP).dst
            bts = len(pkt)
            conn = Connection(src, dst, bts)
            # De-duplicate
            for c in connections:
                if (c.source == src) and (c.destination == dst):
                    c.packets+=1
                    match = True
            if match is False:
                connections.append(conn)
        #TODO: Account for reversing of endpoints -- not sure this is worthwhile
        return connections

    for pkt in pkts:
        if(pkt.haslayer(IP)):
            logConnection(pkt)
    return connections


# Task3:
# Identify important nodes, such as: Default Gateway, Nameservers, Domain Controllers
# or other significant servers (Significant == several hits?)
# AND, other significant servers outside of the network ** Requires understanding what "Outside" is
# The existence of a default gateway presupposes we are on an internal LAN segment.
# Geez. That's really not a fun thing to think about...how would I *assuredly* find the default gw?

# A gateway will satisfy the following rules:
# src mac of > 1 IPs
# Then to find its IP, examine ARP requests for one where it is the source address

# So the algorithm is, 'find the most common hwaddr' + 'determine which of its IP addresses are private'
def findDefaultGateway(pkts, hosts):
    hwaddrFrequency = {}
    # We set gateway to a default string, in case we fail to find a Default GW.
    gateway = "UNABLE TO DETERMINE GATEWAY USING MULTIPLE IP TO SINGLE HWADDR METHOD"
    for hostKey, hostValue in hosts.items():
        if hostValue.IP is not "":
            if not hostValue.MAC in hwaddrFrequency.keys():
                hwaddrFrequency[hostValue.MAC] = 1
            else:
                hwaddrFrequency[hostValue.MAC] += 1
    for addr in hwaddrFrequency.keys():
        if hwaddrFrequency[addr] > 1: # If this breaks, increase to 2, but admittedly this is a hack
            gateway = Host()
            gateway.MAC = addr

    # SO NOW WE HAVE THE GATEWAY'S MAC...let's find its IP address.
    for hostKey, hostValue in hosts.items():
        if hostValue.MAC == gateway:
            if ipaddress.IPv4Address(hostValue.IP).is_private:
                gateway = Host()
                gateway = hosts[hostKey]
    # Return either the hwaddr or the IP of the gateway, or neither if we couldn't find it.
    return gateway


# Utility function: construct a dictionary of hosts
# "In which the author says, 'ain't nobody got time for PEP-8"
def getHosts(pkts):
    hosts = {} # amg i'm totes going to use a tuple for a key
    for pkt in pkts:
        if pkt.haslayer(IP) and (pkt.getlayer(Ether).src, pkt.getlayer(IP).src) not in hosts.keys(): # I'm making an assumption, all IP rides on Ether for my purposes
            hosts[(pkt.getlayer(Ether).src, pkt.getlayer(IP).src)]=Host(IP=pkt.getlayer(IP).src, MAC=pkt.getlayer(Ether).src)
        elif pkt.haslayer(ARP): #If it has ARP, we can assume it has Ether...in this day and age...
            if pkt.getlayer(ARP).psrc and (pkt.getlayer(Ether).src, pkt.getlayer(ARP).psrc) not in hosts.keys():
                hosts[(pkt.getlayer(Ether).src, pkt.getlayer(ARP).psrc)]=Host(MAC=pkt.getlayer(Ether).src, IP=pkt.getlayer(ARP).psrc)
            else:
                hosts[(pkt.getlayer(Ether).src, "")]=Host(MAC=pkt.getlayer(Ether).src)
    return hosts

# Get servers by ports. Such as, 25 for Mail, etc etc...can handle TCP && UDP.
# Dear reader, I realize I haven't made any effort to 'polish' this code, such as with try/except,
# or graceful error handling, etc etc...but this is Python, neh? :D That stuff takes more time than I have.
def getSystemByPorts(pkts, hosts, ports=[], protos=[TCP]):
    selection = set()
    for pkt in pkts:
        for proto in protos:
            if pkt.haslayer(proto) and pkt.getlayer(proto).sport in ports:
                for k, v in hosts.items():
                    if pkt.getlayer(IP).src == v.IP:
                        selection.add(hosts[k])
    return selection

if __name__ == "__main__":
    # Requirements:
    # Read from a capture file or live traffic

    print("[*] Simple Packet Analysis Script")
    # Check for file name in command-line arguments; if yes, try as pcap.
    if len(sys.argv) > 1 and re.search(sys.argv[1], ".+pcap"):
        capFile = sys.argv[1]
        fromFile = True # Set this to true for future tests as needed
    else:
        fromFile = False

    # We read from other the file, or iface
    # TODO: Briefly consider refactoring to support large files - then get over it
    if fromFile:
        pkts = sniff(offline=capFile)
    else:
        pkts = sniff(count=2000, timeout=10, iface=ifaces.dev_from_index(33).name)

    # I've decided I want a dictionary of hosts.
    hosts = getHosts(pkts)
    # DEBUG: If you want to see all the hosts.
    #for mac_ip_tuple in hosts.keys():
        #print(hosts[mac_ip_tuple])

    # First, let's construct a dictionary of protocols seen & number of such packets
    protocolStats = getProtocols(pkts)

    # Now we look for connections & get the number of packets between endpoints.
    connectionStats = getConnections(pkts)

    # Let's find the default gateway
    gw = findDefaultGateway(pkts, hosts)

    # How about some nameservers yo
    #nameservers = getNameServers(pkts, hosts)
    nameservers = getSystemByPorts(pkts, hosts, [53], [TCP,UDP])

    # Any Domain Controllers?
    #domaincontrollers = getDomainControllers(pkts, hosts)
    domaincontrollers = getSystemByPorts(pkts, hosts, [88,389], [TCP])

    # How about mail servers
    #mailservers = getMailServers(pkts, hosts)
    mailservers = getSystemByPorts(pkts, hosts, [25,110], [TCP])

    # Final print
    print("[*] Protocol Frequency breakdown")
    print(f"\t{protocolStats}\n")
    print("[*] Connection statistics")
    for conn in connectionStats:
        print(f"\t{conn}")
    if gw.IP is "":
        print("[*] Default Gateway. Gateway IP not discovered in capture.")
    else:
        print("[*] Default Gateway.")
    print(f"\t{gw}")
    if len(nameservers) == 0:
        print("[!] No DNS Servers detected in capture")
    else:
        print("[*] DNS Servers")
        for ns in nameservers:
            print(f"\t{ns}")
    if len(domaincontrollers) == 0:
        print("[!] No Domain Controllers detected in capture")
    else:
        print("[*] Domain Controllers")
        for dc in domaincontrollers:
            print(f"\t{dc}")
    if len(mailservers) == 0:
        print("[!] No Mail Servers detected in capture")
    else:
        print("[*] Mail Servers")
        for mail in mailservers:
            print(f"\t{mail}")
