class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
    def __str__(self):
        return str(self.data)


def pwRev(node):
    output = node.next 
    if not node or not output:
        return node

    while node:
        node = doRev(node)
    return output

def doRev(node):
    temp = node # A
    next = node.next # B
    if not next:
        return None
    nextnext = next.next # C
    node = next    # B->C (A)
    node.next = temp # B->A->B
    if nextnext and nextnext.next:
        node.next.next = nextnext.next
    else:
        node.next.next = nextnext
    return nextnext 

def printList(node):
    iter = node
    while iter:
        print iter
        iter = iter.next

a = Node(1)
b = Node(2)
c = Node(3)
d = Node(4)
e = Node(5)
f = Node(6)

#Test a single item list
single = pwRev(a)
print "Single "
printList(single)

a.next = b
b.next = c
c.next = d
d.next = e

rev = pwRev(a)
print "Five "
printList(rev)

a.next = b
b.next = c
c.next = d
d.next = e
e.next = f
six = pwRev(a)
print "Six "
printList(six)
