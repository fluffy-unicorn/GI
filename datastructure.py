class DoublyLinkedList(object):
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def append(self, value):
        if (self._size == 0):
            self._head = Node(None, value, None)
            self._tail = self._head
        else:
            newNode = Node(self._tail, value, None)
            self._tail.setNext(newNode)
            self._tail = newNode
        self._size += 1
    
    def prepend(self, value):
        if (self._size == 0):
            self._head = Node(None, value, None)
            self._tail = self._head
        else:
            newNode = Node(None, value, self._head)
            self._head.setPrevious(newNode)
            self._head = newNode
        self._size += 1

    def pophead(self):
        #Remove head element from list
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
        #Remove tail element from list.
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
        #Remove an item by index

        if (index >= size):
            break

        #Select a node, current_node, to be removed
        current_node = self._head
        for i in range(0,index):
            current_node = current_node.next

        #Remove the selected node.
        remove(current_node)

    def removeByValue(self, value):
        #remove an item by value

        current_node = self._head
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
            #This was the head node.
            this._head = node.next

        if node.next is not None:
            node.next.setPrevious(node.previous)
        else:
            #This was the tail node.
            this._tail = node.previous
        this._size -= 1


    def __iter__(self):
        return self

    def __next__(self):
        #to be implemented.
        

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

