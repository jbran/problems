class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
    def __str__(self):
        return str(self.data)


def pwRev(node):
    if not node or not node.next:
        return node

    output = node.next
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
        print iter,
        iter = iter.next
    print

def makeList(size):
    node = Node(1)
    if 1 == size:
        return node
    iter = node
    for i in xrange(2,size+1):
        next = Node(i)
        iter.next = next
        iter = next
    return node


print "None "
printList(pwRev(None))

print "Single "
printList(pwRev(makeList(1)))

print "Five "
printList(pwRev(makeList(5)))

print "Six "
printList(pwRev(makeList(6)))

print "Hundred "
printList(pwRev(makeList(101)))
