import sys
sys.setrecursionlimit(10**6)

class TreeNode:

    def __init__(self, num, index):
        self.num = num
        self.left = None
        self.right = None
        self.parent = None
        self.index = index


class Tree:

    def __init__(self):
        self.head = None
        self.array = []
        self.size = 0

    def insert(self, n):
        e = TreeNode(n, self.size)
        self.array.append(e)
        self.size += 1
        done = False
        if self.head is None:
            self.head = e
        else:
            n = self.head
            while not done:
                if e.num > n.num:
                    if n.right is None:
                        n.right = e
                        e.parent = n
                        done = True
                    else:
                        n = n.right
                        continue
                else:
                    if n.left is None:
                        n.left = e
                        e.parent = n
                        done = True
                    else:
                        n = n.left
                        continue

class AVLTreeNode:

    def __init__(self, num, index):
        self.num = num
        self.left = None
        self.right = None
        self.height = 1
        self.parent = None
        self.index = index


def level(n):
    if n is None:
        return 0
    return n.height


def get_balance_factor(e):
    left = 0
    if e.left is not None:
        left = e.left.height
    right = 0
    if e.right is not None:
        right = e.right.height
    return left - right


def rightmost(e):
    if e.right is None:
        return e
    return rightmost(e.right)


def leftmost(e):
    if e.left is None:
        return e
    return leftmost(e.left)


def top(e):
    if e.parent is None:
        return e
    return top(e.parent)


def update_height(e):
    e.height = 1 + max(level(e.left), level(e.right))


def rotate(e):
    # print(f"Checking {e.num}")
    # printTree(top(e))
    # print()
    bf = get_balance_factor(e)
    pr = e.parent
    # Return the new head of the tree
    newhead = None
    if bf > 1:
        # print(f"Rotating {e.num}")
        bf_c = get_balance_factor(e.left)
        lft = e.left
        if bf_c > 0:
            if pr is None:
                newhead = lft
                lft.parent = None
            else:
                if lft.num < pr.num:
                    pr.left = lft
                else:
                    pr.right = lft
                lft.parent = pr
            subtree = lft.right
            e.parent = lft
            lft.right = e
            e.left = subtree
            if subtree is not None:
                subtree.parent = e
            update_height(e)
            update_height(lft.left)
            update_height(lft)
            return newhead
        else:
            lftrt = lft.right
            subtree = lftrt.left
            lftrt.left = lft
            lftrt.parent = lft.parent
            lft.parent = lftrt
            lft.right = subtree
            if subtree is not None:
                subtree.parent = lft
            e.left = lftrt
            update_height(lft)
            update_height(lftrt)
            return rotate(e)

    elif bf < -1:
        # print(f"Rotating {e.num}")
        bf_c = get_balance_factor(e.right)
        rt = e.right
        if bf_c < 0:
            if pr is None:
                newhead = rt
                rt.parent = None
            else:
                if rt.num< pr.num:
                    pr.left = rt
                else:
                    pr.right = rt
                rt.parent = pr
            subtree = rt.left
            e.parent = rt
            rt.left = e
            e.right = subtree
            if subtree is not None:
                subtree.parent = e
            update_height(e)
            update_height(rt.right)
            update_height(rt)
            return newhead
        else:
            rtlft = rt.left
            subtree = rtlft.right
            rtlft.right = rt
            rtlft.parent = rt.parent
            rt.parent = rtlft
            rt.left = subtree
            if subtree is not None:
                subtree.parent = rt
            e.right = rtlft
            update_height(rt)
            update_height(rtlft)
            return rotate(e)

    else:
        if e.parent is None:
            # print("Done")
            return
        # print(f"Parent:{e.parent.num}")
        return rotate(e.parent)


#
# def printTree(nd):
#     if nd is None:
#         print("-", end="")
#         return
#     if nd.left is None and nd.right is None:
#         print(str(nd.num) + "|" + str(nd.height) + "|" + str(get_balance_factor(nd)), end="")
#         return
#     print("(", end="")
#     printTree(nd.left)
#     print(" " + str(nd.num) + "|" + str(nd.height) + "|" + str(get_balance_factor(nd)) + " ", end="")
#     printTree(nd.right)
#     print(")", end="")
#

def up_height(e):
    if e.parent is None:
        return
    exp = e.height + 1
    if e.parent.height < exp:
        e.parent.height = exp
        up_height(e.parent)




class AVLTree:

    def __init__(self):
        self.head = None
        self.array = []
        self.size = 0

    def insert(self, n):
        e = AVLTreeNode(n, self.size)
        self.array.append(e)
        self.size += 1
        done = False
        if self.head is None:
            self.head = e
            # print(f"Inserted {e.num}")
        else:
            n = self.head
            while not done:
                if e.num > n.num:
                    if n.right is None:
                        n.right = e
                        e.parent = n
                        up_height(e)
                        done = True
                        # print(f"Inserted {e.num}")
                        nh = rotate(e)
                        if nh is not None:
                            self.head = nh
                    else:
                        n = n.right
                        continue
                else:
                    if n.left is None:
                        n.left = e
                        e.parent = n
                        up_height(e)
                        done = True
                        # print(f"Inserted {e.num}")
                        nh = rotate(e)
                        if nh is not None:
                            self.head = nh
                    else:
                        n = n.left
                        continue
        # printTree(self.head)
        # print()


def printTree(nd):
    if nd is None:
        print("-", end="")
        return
    if nd.left is None and nd.right is None:
        print(str(nd.num), end="")
        return
    print("(", end="")
    printTree(nd.left)
    print(" " + str(nd.num) + " ", end="")
    printTree(nd.right)
    print(")", end="")


def presuc(t, x):
    """Returns a list: [predecessor, successor]"""
    pred = None
    succ = None
    n = t.head
    if n.num < x:
        pred = n
        succ = n
        while succ.num < x:
            pred = succ
            succ = succ.right
            if succ is None:
                return [pred, succ]
        while True:
            temp = succ.left
            while True:
                if temp is None:
                    return [pred, succ]
                if temp.num < x:
                    pred = temp
                    succ = pred.parent
                    break
                if temp.left is None:
                    succ = temp
                    return [pred, succ]
                temp = temp.left
            temp = pred.right
            while True:
                if temp is None:
                    return [pred, succ]
                if temp.num > x:
                    succ = temp
                    pred = succ.parent
                    break
                if temp.right is None:
                    pred = temp
                    return [pred, succ]
                temp = temp.right
    else:
        # num > x
        succ = n
        pred = n
        while pred.num > x:
            succ = pred
            pred = pred.left
            if pred is None:
                return [pred, succ]
        while True:
            temp = pred.right
            while True:
                if temp is None:
                    return [pred, succ]
                if temp.num > x:
                    succ = temp
                    pred = succ.parent
                    break
                if temp.right is None:
                    pred = temp
                    return [pred, succ]
                temp = temp.right
            temp = succ.left
            while True:
                if temp is None:
                    return [pred, succ]
                if temp.num < x:
                    pred = temp
                    succ = pred.parent
                    break
                if temp.left is None:
                    succ = temp
                    return [pred, succ]
                temp = temp.left


def getnum(n):
    if n is None:
        return -1
    return n.num

def preorder(n):
    output_str = ""
    output_str += str(n.num)
    output_str += " "
    if n.left is not None:
        output_str += preorder(n.left)
    if n.right is not None:
        output_str += preorder(n.right)
    return output_str


def AVL_BST(elements):
    """Returns the head of the BST."""
    bst = Tree()
    avl = AVLTree()
    bst.insert(int(elements[0]))
    avl.insert(int(elements[0]))
    for x_str in elements[1:]:
        x = int(x_str)
        # printTree(bst.head)
        # print()
        # printTree(avl.head)
        # print()
        # print(f"Inserting {x}")
        node = TreeNode(x, bst.size)
        bst.array.append(node)
        bst.size += 1
        ps = presuc(avl, x)
        if ps[0] is None:
            leftnode = None
            rightnode_idx = ps[1].index
            rightnode = bst.array[rightnode_idx]
            # print(f"{node.num}'s pred is {getnum(leftnode)}, succ is {getnum(rightnode)}")
        elif ps[1] is None:
            rightnode = None
            leftnode_idx = ps[0].index
            leftnode = bst.array[leftnode_idx]
            # print(f"{node.num}'s pred is {getnum(leftnode)}, succ is {getnum(rightnode)}")
        else:
            leftnode_idx = ps[0].index
            rightnode_idx = ps[1].index
            leftnode = bst.array[leftnode_idx]
            rightnode = bst.array[rightnode_idx]
            # print(f"{node.num}'s pred is {getnum(leftnode)}, succ is {getnum(rightnode)}")
        avl.insert(x)
        if leftnode is None:
            rightnode.left = node
            # print(f"{rightnode.num}'s child is {node.num}")
            continue
        if rightnode is None:
            leftnode.right = node
            # print(f"{leftnode.num}'s child is {node.num}")
            continue
        if leftnode.right is not None:
            rightnode.left = node
            # print(f"{rightnode.num}'s child is {node.num}")
            continue
        if rightnode.left is not None:
            leftnode.right = node
            # print(f"{leftnode.num}'s child is {node.num}")
            continue

    return bst

# input_lines = "20\n54 20 71 24 49 83 8 87 96 10 33 3 88 35 55 6 66 43 41 98"
input_lines = sys.stdin.read().strip()
# print(input_lines)
input_list = input_lines.split('\n')
num_elem = int(input_list[0])
elems_list = input_list[1].split(' ')

bst = AVL_BST(elems_list)

# printTree(bst.head)
# print("")

print(preorder(bst.head))
