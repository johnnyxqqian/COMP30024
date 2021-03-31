# different heap function

import sys


class MinHeap:
    """
    A class to hold a MinHeap data structure to utilise as a priority queue.
    Original code from: https://www.geeksforgeeks.org/min-heap-in-python/
    Edits made to ensure it works with an object with an attribute "Cost" as a float or integer.
    """
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0] * (self.maxsize + 1)
        self.Heap[0] = test(-1 * sys.maxsize)
        self.FRONT = 1

    # Function to return the position of
    # parent for the node currently
    # at pos
    @staticmethod
    def parent(pos):
        return pos // 2

    # Function to return the position of
    # the left child for the node currently
    # at pos
    @staticmethod
    def leftChild(pos):
        return 2 * pos

    # Function to return the position of
    # the right child for the node currently
    # at pos
    @staticmethod
    def rightChild(pos):
        return (2 * pos) + 1

    # Function that returns true if the passed
    # node is a leaf node
    def isLeaf(self, pos):
        if pos == self.size == 1:
            return True
        if pos >= (self.size // 2) and pos <= self.size:
            return True
        return False

    # Function to swap two nodes of the heap
    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]

    # Function to heapify the node at pos
    def minHeapify(self, pos):

        # If the node is a non-leaf node and greater
        # than any of its child
        if not self.isLeaf(pos):
            if (self.Heap[pos].cost > self.Heap[self.leftChild(pos)].cost or
                    self.Heap[pos].cost > self.Heap[self.rightChild(pos)].cost):

                # Swap with the left child and heapify
                # the left child
                if self.Heap[self.leftChild(pos)].cost < self.Heap[self.rightChild(pos)].cost:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))

                # Swap with the right child and heapify
                # the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))

    # Function to insert a node into the heap
    def insert(self, element):
        if self.size >= self.maxsize:
            return
        self.size += 1
        self.Heap[self.size] = element

        current = self.size

        if current == 1:
            return

        while self.Heap[current].cost < self.Heap[self.parent(current)].cost:
            self.swap(current, self.parent(current))
            current = self.parent(current)

    # Function to print the contents of the heap
    def Print(self):
        for i in range(1, (self.size // 2) + 1):
            print(" PARENT : " + str(self.Heap[i].cost) + " LEFT CHILD : " +
                  str(self.Heap[2 * i].cost) + " RIGHT CHILD : " +
                  str(self.Heap[2 * i + 1].cost))

    # Function to build the min heap using
    # the minHeapify function
    def minHeap(self):

        for pos in range(self.size // 2, 0, -1):
            self.minHeapify(pos)

    # Function to remove and return the minimum
    # element from the heap
    def remove(self):
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size -= 1

        if self.size == 0:
            return popped
        self.minHeapify(self.FRONT)
        return popped

    def is_empty(self):
        return self.size == 0

class test(object):
    def __init__(self, value):
        self.cost = value

def unittest():
    testcases = [test(i) for i in range(0,100,4)]\
                +[test(i) for i in range(24,30,1)]\
                +[test(i) for i in range(50,60,3)]

    queue = MinHeap(100000)

    for tc in testcases:
        queue.insert(tc)

    remove_order = []
    flag = True
    while flag:
        try:
            remove_order.append(queue.remove().cost)
        except:
            flag = False

    print(remove_order)
    sorted_remove_order = sorted(remove_order)

    print(sorted_remove_order==remove_order)