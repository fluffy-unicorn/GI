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
            self._last.next = newNode
            self._last = newNode
        self._size += 1
    
    def prepend(self, value):
        if (self._size == 0):
            self._first = Node(None, value, None)
            self._last = self._first
        else:
            newNode = Node(None, value, self._first)
            self._first.previous = newNode
            self._first = newNode
        self._size += 1

    def pop(self):
    
    def remove(self, index):

    def __next__(self)    
    @property
    def first(self) -> "Node":
        return self._first
    
    @property
    def last(self) -> "Node":
        return self._last

    @property
    def size(self) -> int:
        return self._size

class Node(object):
    def __init__(self, previous, value, next):
        self._previous = previous
        self._value = value
        self._next = next

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

