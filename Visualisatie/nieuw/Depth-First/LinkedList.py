class Node(object):
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.nexts = []
        self.nexts.append(next)


class LinkedList(object):
    head = None
    tail = None

    def append(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node

    def show(self):
        current_node = self.head
        while current_node is not None:
            print current_node.prev.data if hasattr(current_node.prev, "data") else None,
            print current_node.data,
            print current_node.next.data if hasattr(current_node.next, "data") else None
            current_node = current_node.next



d = LinkedList()
d.append(5)
d.append(6)
d.append(9)
d.append('hallo')

d.show()