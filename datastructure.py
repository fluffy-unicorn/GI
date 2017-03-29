class DoublyLinkedList(object):
    def __init__(self):
        self._first = None
        self._last = None
        self._size = 0

    def append(self, value):
        if (self._size == 0):
            self._first = Node(None, value, None)
            self._last = self._first
        else:
            newNode = Node(self._last, value, None)
            self._last.setNext(newNode)
            self._last = newNode
        self._size += 1
    
    def prepend(self, value):
        if (self._size == 0):
            self._first = Node(None, value, None)
            self._last = self._first
        else:
            newNode = Node(None, value, self._first)
            self._first.setPrevious(newNode)
            self._first = newNode
        self._size += 1

    def popfirst(self):
        #Remove first element from list
        if (self._size>1):
            #Set previous node of second element to None
            self._first.next.setPrevious(None)
            #Set second element to be the first
            self._first = self._first.next
            #Decrement size
            self._size -= 1
        elif (self._size == 1):
            #If list contains only one element, empty the list.
            self._first = None
            self._last = None
            self._size = 0
        return


    def poplast(self):
        #Remove last element from list.
        if (self._size>1):
            #Set next node of second last element to None
            self._last.previous.setNext(None)
            #Set second last node to be the last
            self._last = self._last.previous
            #Decrement size
            self._size -= 1

        elif (self._size==1):
            #If list contains only one element, empty the list.
            self._last = None
            self._first = None
            self._size = 0

    def removeByIndex(self, index):
        #Remove an item by index

        if (index >= size):
            break

        #Select a node, current_node, to be removed
        current_node = self._first
        for i in range(0,index):
            current_node = current_node.next

        #Remove the selected node.
        remove(current_node)

    def removeByValue(self, value):
        #remove an item by value

        current_node = self._first
        while current_node.value is not value:
            current_node = current_node.next
            if current_node is None:
                #The value was not found
                break

        remove(current_node)

    def remove(self, node: "Node"):
        #Remove a node from the doubly linked list.
        if node.previous is not None:
            #There was a previous node, 
            #so we can simply refer to the next node as the previous' next node
            node.previous.setNext(node.next)
        else:
            #This was the first node.
            this._first = node.next

        if node.next is not None:
            node.next.setPrevious(node.previous)
        else:
            #This was the last node.
            this._last = node.previous
        this._size -= 1


    def __iter__(self):
        return self

    def __next__(self):
        #to be implemented.
        

    @property
    def first(self) -> "Node":
        return self._first
    
    @property
    def last(self) -> "Node":
        return self._last

    @property
    def size(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return "DoublyLinkedList of size " + str(self._size)

    def __str__(self) -> str:
        return "DoublyLinkedList of size " + str(self._size)

class Node(object):
    def __init__(self, previous, value, next):
        self._previous = previous
        self._value = value
        self._next = next

    def setNext(self, node):
        #Set the next value 
        self._next = node

    def setPrevious(self, node):
        #Set the previous value
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

