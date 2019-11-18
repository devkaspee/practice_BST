class Node:
    def __init__(self):
        self.ptr = []
        self.data = []
        self.leaf = True

    def insertData(self, data):
        self.data.append(data)
        self.data.sort()

    def insertPtr(self, data):
        self.ptr.append(data)


class BT:
    def __init__(self, m):
        self.root = None
        self.m = m


    def inorder(self, m, T):
        if T.ptr:
            self.inorder(m, T.ptr[0])
            for i in range(len(T.data)):
                print(T.data[i], end=' ')
                self.inorder(m, T.ptr[i+1])

        else:
            for i in range(len(T.data)):
                print(T.data[i], end=' ')


    def getNode(self, data, Noleaf=True):
        tmp = Node()
        tmp.insertData(data)
        tmp.leaf = Noleaf
        return tmp

    def insertNotFull(self, x, key, ad1=None, ad2=None):
        if ad1 is None:
            x.insertData(key)
            return

        if key < x.data[0]:
            del x.ptr[0]
            x.ptr.insert(0,ad2)
            x.ptr.insert(0,ad1)
            x.insertData(key)

        else:
            for i in range(len(x.data)-1,-1,-1):
                if x.data[i] < key:
                    del x.ptr[i+1]
                    x.ptr.insert(i+1, ad2)
                    x.ptr.insert(i+1, ad1)
                    x.insertData(key)
                    break
        return

    def splitChild(self, p, data, a1=None, a2= None):
        if p.leaf:
            p.data.append(data)
            tmplist = sorted(p.data)
            a, b, c = tmplist[:self.m // 2], tmplist[self.m // 2], tmplist[self.m // 2 + 1:]
            aNode = self.getNode(0)
            aNode.data = a
            cNode = self.getNode(0)
            cNode.data = c
            return b, aNode, cNode

        else:
            if data < p.data[0]:
                del p.ptr[0]
                p.ptr.insert(0, a2)
                p.ptr.insert(0, a1)

            else:
                for i in range(len(p.data)-1,-1,-1):
                    if p.data[i] < data:
                        del p.ptr[i+1]
                        p.ptr.insert(i+1,a2)
                        p.ptr.insert(i+1,a1)
                        break
            p.insertData(data)
            aNode = self.getNode(0,False)
            cNode = self.getNode(0,False)
            aNode.data = p.data[:self.m // 2]
            b = p.data[self.m // 2]
            cNode.data = p.data[self.m//2 +1:]
            aNode.ptr = p.ptr[:self.m//2+1]
            cNode.ptr = p.ptr[self.m//2+1:]
            return b, aNode, cNode

    def insertBT(self, m, data):
        if self.root == None:
            self.root = self.getNode(data)
            return

        find = False
        p = self.root
        stack = []

        while not find:
            if p.leaf:
                if data in p.data:
                    return
                find = True
                break
            stack.append(p)
            if p.data[-1] < data:
                p = p.ptr[-1]
            else:
                for i in range(len(p.data)):
                    if data < p.data[i]:
                        p = p.ptr[i]
                        break

        a1 = a2 = None

        while True:
            if len(p.data) < self.m-1:
                self.insertNotFull(p, data, a1, a2)
                return

            elif len(p.data) ==self.m-1:
                data, a1, a2 = self.splitChild(p, data, a1, a2)

                if stack:
                    p = stack.pop()
                else:
                    temp = self.getNode(data,False)
                    temp.ptr = [a1, a2]
                    self.root = temp
                    return


cin1 = [40, 11, 77, 33, 20, 90, 99, 70, 88, 80]
cin2 = [66, 10, 22, 30, 44, 55, 50, 60, 100, 28]
cin3 = [18, 9, 5, 17, 6, 3, 1, 4, 2, 7]
cin4 = [8, 73, 12, 13, 14, 16, 15, 25, 24, 28]
cin5 = [45, 49, 42, 43, 41, 47, 48, 46, 63, 68]
cin6 = [61, 62, 64, 69, 67, 65, 54, 59, 58, 51]
cin7 = [53, 57, 52, 56, 83, 81, 82, 84, 75, 89]

T1 = BT(3)  # m == 3일때

for i in range(len(cin1)):
    T1.insertBT(3, cin1[i]); T1.inorder(3, T1.root); print()
for i in range(len(cin2)):
    T1.insertBT(3, cin2[i]); T1.inorder(3, T1.root); print()
for i in range(len(cin3)):
    T1.insertBT(3, cin3[i]); T1.inorder(3, T1.root); print()
for i in range(len(cin4)):
    T1.insertBT(3, cin4[i]); T1.inorder(3, T1.root); print()
for i in range(len(cin5)):
    T1.insertBT(3, cin5[i]); T1.inorder(3, T1.root); print()
for i in range(len(cin6)):
    T1.insertBT(3, cin6[i]); T1.inorder(3, T1.root); print()
for i in range(len(cin7)):
    T1.insertBT(3, cin7[i]); T1.inorder(3, T1.root); print()

T2 = BT(4)  # m == 4 일때
for i in range(len(cin1)):
    T2.insertBT(4, cin1[i]); T2.inorder(4, T2.root); print()
for i in range(len(cin2)):
    T2.insertBT(4, cin2[i]); T2.inorder(4, T2.root); print()
for i in range(len(cin3)):
    T2.insertBT(4, cin3[i]); T2.inorder(4, T2.root); print()
for i in range(len(cin4)):
    T2.insertBT(4, cin4[i]); T2.inorder(4, T2.root); print()
for i in range(len(cin5)):
    T2.insertBT(4, cin5[i]); T2.inorder(4, T2.root); print()
for i in range(len(cin6)):
    T2.insertBT(4, cin6[i]); T2.inorder(4, T2.root); print()
for i in range(len(cin7)):
    T2.insertBT(4, cin7[i]); T2.inorder(4, T2.root); print()