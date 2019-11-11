class Node:
    def __init__(self, key, bf=0, rightChild=None, leftChild=None):
        self.key = key
        self.rightChild = rightChild
        self.leftChild = leftChild
        self.bf = bf


class BST:
    def __init__(self):
        self.root = None

    def getNode(self, key, bf=0):
        return Node(key, bf)
    def findKey(self,key):
        pNode = self.root
        try:
            while True:
                if key > pNode.key:
                    pNode = pNode.rightChild
                elif key < pNode.key:
                    pNode = pNode.leftChild
                else:
                    break
        except:
            return False

        return True


    def noNodes(self, Node):
        cnt = 1
        if Node.rightChild is not None:
            cnt += self.noNodes(Node.rightChild)
        if Node.leftChild is not None:
            cnt += self.noNodes(Node.leftChild)
        return cnt

    def maxNode(self, Node):
        pNode = Node
        while pNode.rightChild is not None:
            pNode = pNode.rightChild
        return pNode.key

    def minNode(self, Node):
        pNode = Node
        while pNode.leftChild is not None:
            pNode = pNode.leftChild
        return pNode.key

    def height(self, Node):  # using BFS
        cnt = 1
        queue = []
        if Node.leftChild is not None:
            queue.append(Node.leftChild)
        if Node.rightChild is not None:
            queue.append(Node.rightChild)

        while queue:
            newQueue = []
            while queue:
                NewNode = queue.pop(0)
                if NewNode.leftChild is not None:
                    newQueue.append(NewNode.leftChild)
                if NewNode.rightChild is not None:
                    newQueue.append(NewNode.rightChild)
            cnt += 1
            queue = newQueue
        return cnt

    def setBalance(self, T, newKey):
        if T.key == newKey: return

        p = T
        rl = lt = 0
        if p.rightChild is not None: rl = self.height(p.rightChild)
        if p.leftChild is not None: lt = self.height(p.leftChild)
        p.bf = rl - lt

        if newKey > p.key:
            self.setBalance(p.rightChild, newKey)
        elif newKey < p.key:
            self.setBalance(p.leftChild, newKey)

    def checkBalance(self, T, newKey):
        self.setBalance(T, newKey)
        stack = []
        ptr = self.root

        while True:
            if newKey > ptr.key:
                stack.append((ptr, 1))
                ptr = ptr.rightChild
            elif newKey < ptr.key:
                stack.append((ptr, 0))
                ptr = ptr.leftChild
            else:
                stack.append((ptr, 0))
                break
        temp = []
        for i in range(len(stack)):
            temp.append(stack[i])

        cnt = 0

        while stack:

            crtNode, d = stack.pop()
            if not (-1 <= crtNode.bf <= 1):

                dir = temp[len(temp) - cnt][1]
                if not stack:
                    if dir == d == 0:
                        return crtNode, None, "LL", 0
                    elif dir == d:
                        return crtNode, None, "RR", 0
                    elif d == 0:
                        return crtNode, None, "LR", 0
                    else:
                        return crtNode, None, "RL", 0
                else:
                    parent, direction = stack.pop()
                    if dir == d == 0:
                        return crtNode, parent, "LL", direction
                    elif dir == d:
                        return crtNode, parent, "RR", direction
                    elif d == 0:
                        return crtNode, parent, "LR", direction
                    else:
                        return crtNode, parent, "RL", direction
            cnt += 1
        return None, None, "No", 0

    def insertAVL(self, newKey):
        if self.findKey(newKey):
            print("No", end= " ")
            return

        self.insertBST(newKey)
        A, B, C, D = self.checkBalance(self.root, newKey)

        self.rotateTree(A,B,C,D)

    def rotateTree(self, A, B, C, D, part = 0):
        if not part:print(C, end = ' ')
        if C == "No":
            return
        if C == "LL":
            temp = A.leftChild
            A.leftChild = temp.rightChild
            temp.rightChild = A
            if B == None:
                self.root = temp
            else:
                if D:
                    B.rightChild = temp
                else:
                    B.leftChild = temp

        elif C == "RR":
            temp = A.rightChild
            A.rightChild = temp.leftChild
            temp.leftChild = A
            if B == None:
                self.root = temp
            else:
                if D:
                    B.rightChild = temp
                else:
                    B.leftChild = temp

        elif C == 'RL':
            BR = A.rightChild
            BRL = BR.leftChild

            BR.leftChild = BRL.rightChild
            BRL.rightChild = BR
            A.rightChild = BRL
            self.rotateTree(A,B,'RR',D,1)

        elif C == 'LR':
            BL = A.leftChild
            BLR = BL.rightChild

            BL.rightChild = BLR.leftChild
            BLR.leftChild = BL
            A.leftChild = BLR
            self.rotateTree(A,B,'LL',D,1)

    def insertBST(self, key):
        if self.root is None:
            self.root = self.getNode(key)
            return

        pNode = self.root
        while True:
            if key == pNode.key:
                return
            elif key > pNode.key:
                if pNode.rightChild is not None:
                    pNode = pNode.rightChild
                else:
                    pNode.rightChild = self.getNode(key)
                    return
            elif key < pNode.key:
                if pNode.leftChild is not None:
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

            if (pNode.rightChild is None) and (pNode.leftChild is None):
                self.root = None
                return

            elif pNode.rightChild is None:

                self.root = pNode.leftChild

            elif pNode.leftChild is None:

                self.root = pNode.rightChild

            else:
                if self.height(pNode.leftChild) == self.height(pNode.rightChild):
                    if self.noNodes(pNode.leftChild) >= self.noNodes(pNode.rightChild):
                        temp = self.maxNode(pNode.leftChild)

                    else:
                        temp = self.minNode(pNode.rightChild)

                elif self.height(pNode.leftChild) > self.height(pNode.rightChild):
                    temp = self.maxNode(pNode.leftChild)

                else:
                    temp = self.minNode(pNode.rightChild)

                self.deleteBST(temp)

                self.root.key = temp
                return
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
                    if self.height(qNode.leftChild) == self.height(qNode.rightChild):
                        if self.noNodes(qNode.leftChild) >= self.noNodes(qNode.rightChild):
                            temp = self.maxNode(qNode.leftChild)

                        else:
                            temp = self.minNode(qNode.rightChild)

                    elif self.height(qNode.leftChild) > self.height(qNode.rightChild):
                        temp = self.maxNode(qNode.leftChild)

                    else:
                        temp = self.minNode(qNode.rightChild)



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


if __name__ == "__main__":

    bst = BST()

    cin = [40, 11, 77, 33, 20, 90, 99, 70, 88, 80, 66, 10, 22, 30, 44, 55, 50, 60,
           100, 28, 18, 9, 5, 17, 6, 3, 1, 4, 2, 7, 8, 10, 12, 13, 14, 16, 15]
    for i in range(len(cin)):
        bst.insertAVL(cin[i])

        bst.inorder()
        print()