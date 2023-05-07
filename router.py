from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController, Controller, OVSKernelSwitch, Node, Host
from mininet.link import TCLink, Link
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
import heapq
import sys


#REFERENCE: https://intronetworks.cs.luc.edu/current/html/mininet.html

class udprouter():

    # 5. Run the link-state routing protocol to flood the network with link state packets and compute routing tables at each router

    def get_links(node, net):
        links = {}
        for intf in node.intfList():
            link = node.connectionsTo(intf.node)
            if link:
                neighbor = link[0][1]
                cost = int(intf.bw)
                links[neighbor.name] = cost
            for dest in ['d1', 'd2', 'd3']:
                if dest != node.name:
                    link = node.connectionsTo(net.get(dest))[0]
                    cost = int(link[0].bw)
                    links[dest] = cost
        return links

    def compute_shortest_paths(graph, start):
        # Create a dictionary to store the distance from the start node to each node in the graph
        distance = {}
        for node in graph:
            distance[node] = sys.maxsize
        distance[start] = 0

        # Create a priority queue to store the nodes to visit and their distances from the start node
        heap = [(0, start)]

        while heap:
            # Pop the node with the smallest distance from the heap
            (dist, node) = heapq.heappop(heap)

            # Update the distances to the node's neighbors
            for neighbor, cost in graph[node]:
                new_dist = dist + cost
                if new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor))

        return distance

    def compute_routing_tables(net):
        for node in net.hosts:
            graph = {}
            for n in net.hosts:
                if n != node:
                    graph[n.name] = get_links(n, net)
            routing_table = compute_shortest_paths(graph, node.name)
            print(node.name)
            for dest, nexthop in routing_table.items():
                print(dest, nexthop)

if __name__ == '__main__':
    print("Router Started...")
    udp_router = udprouter()
