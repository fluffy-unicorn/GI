class DoublyLinkedList(object):
    def __init__(self):
        """Constructor"""
        self._head = None
        self._tail = None
        self._size = 0

    def append(self, value):
        """Add a value to the end of the list."""
        if (self._size == 0):
            self._head = Node(None, value, None)
            self._tail = self._head
        else:
            newNode = Node(self._tail, value, None)
            self._tail.setNext(newNode)
            self._tail = newNode
        self._size += 1
        
    def prepend(self, value):
        """Add a value to the beginning of the list."""
        if (self._size == 0):
            self._head = Node(None, value, None)
            self._tail = self._head
        else:
            newNode = Node(None, value, self._head)
            self._head.setPrevious(newNode)
            self._head = newNode
        self._size += 1

    def pophead(self):
        """Remove the first element from the list."""
        if (self._size>1):
            #Set previous node of second element to None
            self._head.next.setPrevious(None)
            #Set second element to be the head
            self._head = self._head.next
            #Decrement size
            self._size -= 1
        elif (self._size == 1):
            #If list contains only one element, empty the list.
            self._head = None
            self._tail = None
            self._size = 0
        return


    def poptail(self):
        """Remove the last element from the list."""
        if (self._size>1):
            #Set next node of second tail element to None
            self._tail.previous.setNext(None)
            #Set second tail node to be the tail
            self._tail = self._tail.previous
            #Decrement size
            self._size -= 1

        elif (self._size==1):
            #If list contains only one element, empty the list.
            self._tail = None
            self._head = None
            self._size = 0

    def removeByIndex(self, index):
        """Remove an item from the list by a given index."""

        if (index >= self._size):
            return

        #Select a node, current_node, to be removed
        current_node = self._head
        for i in range(0,index):
            current_node = current_node.next

        #Remove the selected node.
        self.remove(current_node)

    def removeByValue(self, value):
        """Remove an item with a specific value from the list."""

        current_node = self._head
        while current_node.value is not value:
            current_node = current_node.next
            if current_node is None:
                #The value was not found
                break

        if current_node is not None:
            self.remove(current_node)

    def remove(self, node: "Node"):
        """Remove a node from the list."""
        if node.previous is not None:
            #There was a previous node, 
            #so we can simply refer to the next node as the previous' next node
            node.previous.setNext(node.next)
        else:
            #This was the head node.
            self._head = node.next

        if node.next is not None:
            node.next.setPrevious(node.previous)
        else:
            #This was the tail node.
            self._tail = node.previous
        self._size -= 1


    def __iter__(self):
        """Iterator for the DoublyLinkedList."""
        current_node = self._head

        while current_node is not None:
            yield current_node
            current_node = current_node.next

    @property
    def head(self) -> "Node":
        return self._head
    
    @property
    def tail(self) -> "Node":
        return self._tail

    @property
    def size(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return "DoublyLinkedList of size " + str(self._size)

    def __str__(self) -> str:
        return "DoublyLinkedList of size " + str(self._size)

class Node(object):
    def __init__(self, previous, value, next):
        """Constructor"""
        self._previous = previous
        self._value = value
        self._next = next

    def setNext(self, node:"Node"):
        """Set the next node of this node."""
        self._next = node

    def setPrevious(self, node:"Node"):
        """Set the previous node of this node."""
        self._previous = node

    @property
    def previous(self) -> "Node":
        return self._previous

    @property
    def value(self):
        return self._value
    
    @property
    def next(self) -> "Node":
        return self._next

    def __repr__(self):
        """
        A programmer-friendly representation of the node.
        :return: The string to approximate the constructor arguments of the `Node'
        """
        return "[" + str(self._previous) + " | " + str(self._value) + " | " + str(self._next) + "]"

    def __str__(self) -> str:
        """
        A user-friendly representation of the vertex, that is, its label.
        :return: The string representation of the label.
        """
        return str(self._value)