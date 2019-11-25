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

    def olim(self, intiger):
        return (intiger // 1 + 1) if intiger % 1 else intiger

    def inorder(self, m, T):
        if T == None:
            return
        if T.ptr:
            self.inorder(m, T.ptr[0])
            for i in range(len(T.data)):
                print(T.data[i], end=' ')
                self.inorder(m, T.ptr[i + 1])

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
            x.ptr.insert(0, ad2)
            x.ptr.insert(0, ad1)
            x.insertData(key)

        else:
            for i in range(len(x.data) - 1, -1, -1):
                if x.data[i] < key:
                    del x.ptr[i + 1]
                    x.ptr.insert(i + 1, ad2)
                    x.ptr.insert(i + 1, ad1)
                    x.insertData(key)
                    break
        return

    def splitChild(self, p, data, a1=None, a2=None):
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
                for i in range(len(p.data) - 1, -1, -1):
                    if p.data[i] < data:
                        del p.ptr[i + 1]
                        p.ptr.insert(i + 1, a2)
                        p.ptr.insert(i + 1, a1)
                        break
            p.insertData(data)
            aNode = self.getNode(0, False)
            cNode = self.getNode(0, False)
            aNode.data = p.data[:self.m // 2]
            b = p.data[self.m // 2]
            cNode.data = p.data[self.m // 2 + 1:]
            aNode.ptr = p.ptr[:self.m // 2 + 1]
            cNode.ptr = p.ptr[self.m // 2 + 1:]
            return b, aNode, cNode

    def insertBT(self, m, data):
        if self.root == None:
            self.root = self.getNode(data)
            return

        p = self.root
        stack = []

        while True:
            if p.leaf:
                if data in p.data:
                    return
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
            if len(p.data) < self.m - 1:
                self.insertNotFull(p, data, a1, a2)
                return

            elif len(p.data) == self.m - 1:
                data, a1, a2 = self.splitChild(p, data, a1, a2)

                if stack:
                    p = stack.pop()
                else:
                    temp = self.getNode(data, False)
                    temp.ptr = [a1, a2]
                    self.root = temp
                    return

    def DeleteBT(self, m, oldKey):
        p = self.root
        if p.ptr == [] and len(p.data) ==1 and p.data[0] == oldKey:
            self.root = None
            return

        stack = []  # 루트부터 말단까지 저장
        swap = False  # 스왑이 되는지 여부
        swapTemp = False
        swaptuple = (None, -1)

        while True:
            stack.append(p)
            if not p.leaf:
                if oldKey in p.data:
                    swap = True  # internal 노드에 있으면 스왑
                if not swap:
                    if oldKey > p.data[-1]:
                        p = p.ptr[-1]
                        continue
                    else:
                        for i in range(len(p.data)):
                            if oldKey < p.data[i]:
                                p = p.ptr[i]
                                break
                if swap:
                    if not swapTemp:
                        for i in range(len(p.data)):
                            if oldKey == p.data[i]:
                                swaptuple = (p, i)
                                p = p.ptr[i + 1]
                                swapTemp = True
                                break

                    else:
                        p = p.ptr[0]

            else:
                if not swap and oldKey not in p.data:
                    return
                else:
                    break

        if swap: # 스왑해줌
            swapNode, swapIdx = swaptuple
            swapNode.data[swapIdx], p.data[0] = p.data[0], swapNode.data[swapIdx] # 후행 키와 변경
        stack.pop()
        finish = True

        for i in range(len(p.data)):
            if p.data[i] == oldKey:
                p.data.pop(i)
                break

        y = None
        if stack:
            y = stack.pop()

        while finish:
            if self.root == p or len(p.data) >= self.olim(self.m / 2) - 1:
                finish = False
            elif self.AvailavleSibling(p, y): # 형제에 여유가 있으면
                self.real(p, y) # 형제에서 빌려옴
                finish = False
            else:
                self.Merge(p, y)  # 형제도 여유가 없으면 병합
                p = y
                if stack:
                    y = stack.pop()
        if not y is None and len(y.data)==0:
            self.root = p.ptr[0]

    def real(self, x, y):
        tidx = y.ptr.index(x)
        left = right = None
        if tidx - 1 >= 0: left = y.ptr[tidx - 1]
        if tidx + 1 < len(y.ptr):
            right = y.ptr[tidx + 1]
        minimum = self.olim(self.m / 2) - 1

        if left and len(left.data) > minimum:
            if len(left.ptr) > 0:
                llp = left.ptr.pop()
                x.ptr.insert(0, llp)

            key = y.data[tidx - 1]
            x.data.insert(0, key)

            llk = left.data.pop()
            y.data[tidx - 1] = llk

        elif right and len(right.ptr) > minimum:
            if len(right.ptr) > 0:
                rfp = right.ptr.pop(0)
                x.ptr.append(rfp)

            key = y.data[tidx]
            x.data.append(key)

            rfk = right.data.pop(0)
            y.data[tidx] = rfk

    def AvailavleSibling(self, x, y):  # 형제에 여유가 있는지 살펴
        tempIdx = -1
        for i in range(len(y.ptr)):
            if y.ptr[i] == x:
                tempIdx = i

        if tempIdx == 0:
            if len(y.ptr[1].data) <= self.olim(self.m / 2) - 1:
                return False
            else:
                return True
        elif tempIdx == len(y.ptr) - 1:
            if len(y.ptr[len(y.ptr) - 2].data) <= self.olim(self.m / 2) - 1:
                return False
            else:
                return True

        else:
            if len(y.ptr[tempIdx - 1].data) <= self.olim(self.m / 2) - 1:
                if len(y.ptr[tempIdx - 1].data) <= self.olim(self.m / 2) - 1:
                    return False

        return True

    def Merge(self, x, y):
        temp = -1
        for i in range(len(y.ptr)):
            if y.ptr[i] == x:
                temp = i
                break

        if temp == len(y.ptr) - 1:
            z = y.ptr[-2]
            z.data.append(y.data[-1])
            z.data += x.data
            z.ptr += x.ptr
            y.data.pop()
            y.ptr.pop()
            return

        z = y.ptr[temp + 1]
        x.data.append(y.data[temp])
        x.data += z.data
        x.ptr += z.ptr
        y.data.remove(y.data[temp])
        y.ptr.pop(temp + 1)
        return

#삽입키
cin1 = [40, 11, 77, 33, 20, 90, 99, 70, 88, 80]
cin2 = [66, 10, 22, 30, 44, 55, 50, 60, 100, 28]
cin3 = [18, 9, 5, 17, 6, 3, 1, 4, 2, 7]
cin4 = [8, 73, 12, 13, 14, 16, 15, 25, 24, 28]
cin5 = [45, 49, 42, 43, 41, 47, 48, 46, 63, 68]
cin6 = [61, 62, 64, 69, 67, 65, 54, 59, 58, 51]
cin7 = [53, 57, 52, 56, 83, 81, 82, 84, 75, 89]


#삭제
cout1 = [66, 10, 22, 30, 44, 55, 50, 60, 100, 28]
cout2 = [18, 9, 5, 17, 6, 3, 1, 4, 2, 7]
cout3 = [8, 73, 12, 13, 14, 16, 15, 25, 24, 28]
cout4 = [40, 11, 77, 33, 20, 90, 99, 70, 88, 80]
cout5 = [45, 49, 42, 43, 41, 47, 48, 46, 63, 68]
cout6 = [61, 62, 64, 69, 67, 65, 54, 59, 58, 51]
cout7 = [53, 57, 52, 56, 83, 81, 82, 84, 75, 89]

T1 = BT(3)  # m == 3일때

for i in range(len(cin1)):
    T1.insertBT(3, cin1[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cin2)):
    T1.insertBT(3, cin2[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cin3)):
    T1.insertBT(3, cin3[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cin4)):
    T1.insertBT(3, cin4[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cin5)):
    T1.insertBT(3, cin5[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cin6)):
    T1.insertBT(3, cin6[i])
    T1.inorder(3, T1.root)
    print()
for i in range(len(cin7)):
    T1.insertBT(3, cin7[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cout1)):
    T1.DeleteBT(3, cout1[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cout2)):
    T1.DeleteBT(3, cout2[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cout3)):
    T1.DeleteBT(3, cout3[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cout4)):
    T1.DeleteBT(3, cout4[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cout5)):
    T1.DeleteBT(3, cout5[i])
    T1.inorder(3, T1.root)
    print()

for i in range(len(cout6)):
    T1.DeleteBT(3, cout6[i])
    T1.inorder(3, T1.root)
    print()
for i in range(len(cout7)):
    T1.DeleteBT(3, cout7[i])
    T1.inorder(3, T1.root)
    print()

T2 = BT(4)  # m == 키4일때

for i in range(len(cin1)):
    T2.insertBT(4, cin1[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cin2)):
    T2.insertBT(4, cin2[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cin3)):
    T2.insertBT(4, cin3[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cin4)):
    T2.insertBT(4, cin4[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cin5)):
    T2.insertBT(4, cin5[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cin6)):
    T2.insertBT(4, cin6[i])
    T2.inorder(4, T2.root)
    print()
for i in range(len(cin7)):
    T2.insertBT(4, cin7[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cout1)):
    T2.DeleteBT(4, cout1[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cout2)):
    T2.DeleteBT(4, cout2[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cout3)):
    T2.DeleteBT(4, cout3[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cout4)):
    T2.DeleteBT(4, cout4[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cout5)):
    T2.DeleteBT(4, cout5[i])
    T2.inorder(4, T2.root)
    print()

for i in range(len(cout6)):
    T2.DeleteBT(4, cout6[i])
    T2.inorder(4, T2.root)
    print()
for i in range(len(cout7)):
    T2.DeleteBT(4, cout7[i])
    T2.inorder(4, T2.root)
    print()
