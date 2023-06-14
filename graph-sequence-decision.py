"""
This is a python program that determines the sequence of graphs and draws a corresponding simple graph.
Author:Cui Guangcan
Contact information:277021921 at qq dot com
"""
import networkx as nx
import matplotlib.pyplot as plt


# Represents each item in the graph sequence as a node in the graph
class GraphNode(object):
    def __init__(self, num, degree):
        self.num = num
        self.degree = degree
        self.next = None


# A single linked list of nodes organized using a given graph sequence
class GraphNodeLink(object):
    def __init__(self):
        self.head = None

    # Adds a node to the tail of the linked list
    def append(self, item):
        if self.head is None:
            self.head = item
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = item

    def length(self):
        x = 0
        cur = self.head
        while cur is not None:
            cur = cur.next
            x += 1
        return x

    # Returns the node at the given location (not deleted)
    def position(self, pos):
        if self.length() == 0:
            print('The linked list is empty!')
            return None
        if pos >= self.length():
            print('Find a location that exceeds the list length!')
            exit(-1)
        elif pos < 0:
            print('The position cannot be negative!')
            exit(-1)
        cur = self.head
        while pos > 0:
            cur = cur.next
            pos -= 1
        return cur

    # Sort by degree increment using bubble method
    def smalltolarge(self):
        for i in range(self.length() - 1):
            for j in range(i + 1, self.length()):
                nodef = self.position(i)
                if i != 0:
                    nodefp = self.position(i - 1)
                nodes = self.position(j)
                nodesp = self.position(j - 1)
                if nodes.degree < nodef.degree:
                    if j - i == 1:
                        if i == 0:
                            self.head = nodes
                        else:
                            nodefp.next = nodes
                        temp = nodes.next
                        nodes.next = nodef
                        nodef.next = temp
                    else:
                        if i == 0:
                            self.head = nodes
                        else:
                            nodefp.next = nodes
                        temp = nodes.next
                        nodes.next = nodef.next
                        nodesp.next = nodef
                        nodef.next = temp

    # Display the serial number and corresponding degree in two rows
    def show(self):
        num_list = []
        degree_list = []
        cur = self.head
        while cur is not None:
            num_list.append(cur.num)
            degree_list.append(cur.degree)
            cur = cur.next
        print('number column:', num_list)
        print('degree column:', degree_list)

    # Returns and deletes the last node in the linked list
    def popnode(self):
        cur = self.head
        if self.length() == 0:
            print('The length of the node list is 0 and cannot be ejected!')
            exit(-1)
        elif self.length() == 1:
            self.head = None
            return cur
        else:
            while cur.next.next is not None:
                cur = cur.next
            node = cur.next
            cur.next = None
            return node

    # Calculate the degree sum of all nodes in the node list
    def degree_sum(self):
        sumdegree = 0
        cur = self.head
        while cur is not None:
            sumdegree += cur.degree
            cur = cur.next
        return sumdegree


# Determines whether the input sequence is a graph sequence
def graph_judeg(degree_list):
    degree_list.sort()
    if degree_list[0] < 0 or degree_list[-1] > len(degree_list) - 1:
        return False
    degree_sum = sum(degree_list)
    if degree_sum % 2 == 1:
        return False
    if degree_sum == 0:
        return True
    last_num = degree_list.pop()
    for i in range(last_num):
        degree_list[-1 - i] -= 1
    return graph_judeg(degree_list)


# Create a simple undirected graph corresponding to the sequence of available graphs
def graph_creat(degree_list):
    graph = nx.Graph()
    graph_node_link = creat_node_link(degree_list)
    # Create the nodes of the graph
    for i in range(len(degree_list)):
        graph.add_node(i)
    # Create the edges of the graph
    while graph_node_link.degree_sum() != 0:
        node = graph_node_link.popnode()
        for i in range(node.degree):
            nodei = graph_node_link.position(graph_node_link.length() - (i + 1))
            nodei.degree -= 1
            graph.add_edge(node.num, nodei.num)
        graph_node_link.smalltolarge()
    return graph


# Draw the simple undirected graphs
def graph_draw(graph):
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()


# Creates a linked list of nodes with the given graph sequence
def creat_node_link(degree_list):
    node_link = GraphNodeLink()
    x = 0
    for i in degree_list:
        node = GraphNode(x, i)
        node_link.append(node)
        x += 1
    return node_link


def main():
    # Enter the sequence to be determined
    degree_list_str = input('Please enter a sequence of numbers separated by commas:')
    # Separates the sequence of degrees by commas to create a list of members of type str
    degree_strlist = degree_list_str.split(',')
    # Converted to an int availability sequence
    degree_list = []
    for i in degree_strlist:
        degree_list.append(int(i))
    degree_list.sort()
    print('The input degree sequence is:', degree_list)
    # Determine whether the input degree sequence is a graph sequence and plot it
    if graph_judeg(degree_list.copy()):
        new_graph = graph_creat(degree_list.copy())
        graph_draw(new_graph)
        print(degree_list_str, 'is a sequence of graphs, the corresponding graph is：')
    else:
        print(degree_list_str, 'is not a sequence of graphs!')


main()
