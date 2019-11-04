class Node:
    def __init__(self, key, rightChild=None, leftChild=None):
        self.key = key
        self.rightChild = rightChild
        self.leftChild = leftChild


class BST:
    def __init__(self):
        self.root = None

    def getNode(self, key):
        return Node(key)

    def noNodes(self, Node):
        cnt = 1
        if Node.rightChild != None:
            cnt += self.noNodes(Node.rightChild)
        if Node.leftChild != None:
            cnt += self.noNodes(Node.leftChild)
        return cnt
    def maxNode(self, Node):
        pNode = Node
        while pNode.rightChild != None:
            pNode = pNode.rightChild
        return pNode.key

    def minNode(self, Node):
        pNode = Node
        while pNode.leftChild != None:
            pNode = pNode.leftChild
        return pNode.key


    def height(self, Node):
        cnt = 0
        queue = []
        if Node.leftChild != None:
            queue.append(Node.leftChild)
        if Node.rightChild != None:
            queue.append(Node.rightChild)

        while queue:
            newQueue = []
            while queue:
                NewNode = queue.pop(0)
                if NewNode.leftChild != None:
                    newQueue.append(NewNode.leftChild)
                if NewNode.rightChild != None:
                    newQueue.append(NewNode.rightChild)
            cnt += 1
            queue = newQueue
        return cnt

    def insertBST(self, key):
        if self.root is None:
            self.root = self.getNode(key)
            return

        pNode = self.root
        while True:
            if key == pNode.key:
                return
            elif key > pNode.key:
                if pNode.rightChild != None:
                    pNode = pNode.rightChild
                else:
                    pNode.rightChild = self.getNode(key)
                    return
            elif key < pNode.key:
                if pNode.leftChild != None:
                    pNode = pNode.leftChild
                else:
                    pNode.leftChild = self.getNode(key)
                    return

    def inorder(self, Node=None):
        if self.root is None:
            return
        if Node is None:
            Node = self.root

        if Node.leftChild is not None:
            self.inorder(Node.leftChild)
        print(Node.key, end=' ')

        if Node.rightChild is not None:
            self.inorder(Node.rightChild)

    def deleteBST(self, key):


        pNode = self.root

        direct = True  # from left -> True, from light -> False

        if key == pNode.key:
            if (pNode.rightChild is None) and pNode.leftChild is None:
                self.root = None
                return
            elif pNode.rightChild is None:
                self.root = pNode.leftChild

            elif pNode.leftChild is None:
                self.root = pNode.rightChild

            else:
                case = True  # True면 왼쪽, False면 오른쪽 서브트리에서 삭제
                if self.height(pNode.leftChild) == self.height(pNode.rightChild):
                    if self.noNodes(pNode.leftChild) >= self.noNodes(pNode.rightChild):
                        temp = self.maxNode(pNode.leftChild)
                        case = True
                    else:
                        temp = self.minNode(pNode.rightChild)
                        case = False
                elif self.height(pNode.leftChild) > self.height(pNode.rightChild):
                    temp = self.maxNode(pNode.leftChild)
                    case = True

                else:
                    temp = self.minNode(pNode.rightChild)

                self.deleteBST(temp)
                self.root.key = temp
                return


        qNode = pNode.rightChild if key > pNode.key else pNode.leftChild

        direct = False if key > pNode.key else True

        while True:
            if key == qNode.key:
                if (qNode.leftChild is None) and (qNode.rightChild is None):
                    if direct:
                        pNode.leftChild = None
                    else:
                        pNode.rightChild = None

                elif qNode.leftChild is None:
                    if direct:
                        pNode.leftChild = qNode.rightChild
                    else:
                        pNode.rightChild = qNode.rightChild
                elif qNode.rightChild is None:
                    if direct:
                        pNode.leftChild = qNode.leftChild
                    else:
                        pNode.rightChild = qNode.leftChild
                else:
                    case = True # True면 왼쪽, False면 오른쪽 서브트리에서 삭제
                    if self.height(qNode.leftChild) == self.height(qNode.rightChild):
                        if self.noNodes(qNode.leftChild) >= self.noNodes(qNode.rightChild):
                            temp = self.maxNode(qNode.leftChild)
                            case = True
                        else:
                            temp = self.minNode(qNode.rightChild)
                            case = False
                    elif self.height(qNode.leftChild) > self.height(qNode.rightChild):
                        temp = self.maxNode(qNode.leftChild)
                        case = True

                    else:
                        temp = self.minNode(qNode.rightChild)
                        case = False

                    self.deleteBST(temp)
                    qNode.key = temp
                return

            if key > qNode.key:
                pNode = qNode
                qNode = qNode.rightChild
                direct = False
            else:
                pNode = qNode
                qNode = qNode.leftChild
                direct = True


bst = BST()

insert = [40, 11, 77, 33, 20, 90, 99, 70, 88, 80, 66, 10, 22, 30, 44, 55, 50, 60, 100]
for i in range(len(insert)):
    bst.insertBST(insert[i])

bst.inorder()
print()
insert.reverse()
for i in range(len(insert)):
    bst.deleteBST(insert[i])
    bst.inorder()
    print()