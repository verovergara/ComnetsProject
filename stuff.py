from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController, Controller, OVSKernelSwitch, Node, Host
from mininet.link import TCLink, Link
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
import heapq
import sys

# 2. Defining network topology
class MyTopo(Topo):
    def build(self):
        # Add hosts
        s = self.addHost('s', ip = '10.0.0.1/24')
        d1 = self.addHost('d1', ip = '10.0.0.9/24')
        d2 = self.addHost('d2', ip = '10.0.0.10/24')
        d3 = self.addHost('d3', ip = '10.0.0.11/24')
        # Add routers
        r1 = self.addHost('r1', ip = '10.0.0.2/24')
        r2 = self.addHost('r2', ip = '10.0.0.3/24')
        r3 = self.addHost('r3', ip = '10.0.0.4/24')
        r4 = self.addHost('r4', ip = '10.0.0.5/24')
        r5 = self.addHost('r5', ip = '10.0.0.6/24')
        r6 = self.addHost('r6', ip = '10.0.0.7/24')
        r7 = self.addHost('r7', ip = '10.0.0.8/24')

        # Add links
        self.addLink(s, r1, bw=10)
        self.addLink(r1, r2, bw=10)
        self.addLink(r1, r3, bw=10)
        self.addLink(r2, r3, bw=10)
        self.addLink(r2, r6, bw=10)
        self.addLink(r3, r4, bw=10)
        self.addLink(r3, r5, bw=10)
        self.addLink(r4, d2, bw=10)
        self.addLink(r5, d3, bw=10)
        self.addLink(r6, r7, bw=10)
        self.addLink(r7, d1, bw=10)

# 3. Configure IP addresses for each node
def configure_ips(net):
    s, r1, r2, r3, r4, r5, r6, r7, d1, d2, d3 = net.get('s', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'd1', 'd2', 'd3')

    # Set IP addresses
    s.setIP('10.0.0.1/24')
    r1.setIP('10.0.0.2/24')
    r2.setIP('10.0.0.3/24')
    r3.setIP('10.0.0.4/24')
    r4.setIP('10.0.0.5/24')
    r5.setIP('10.0.0.6/24')
    r6.setIP('10.0.0.7/24')
    r7.setIP('10.0.0.8/24')
    d1.setIP('10.0.0.9/24')
    d2.setIP('10.0.0.10/24')
    d3.setIP('10.0.0.11/24')


# 4. Start the network topology
def start_network():
    setLogLevel('info')
    topo = MyTopo()
    net = Mininet(topo=topo, controller=RemoteController, link=TCLink)
    net.start()
    configure_ips(net)
    dumpNodeConnections(net.hosts)
    compute_routing_tables(net)
    CLI(net)

# 5. Run the link-state routing protocol to flood the network with link state packets and compute routing tables at each router
if __name__ == '__main__':
    start_network()
