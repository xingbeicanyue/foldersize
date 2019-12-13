from collections import deque


# region 多叉树

class MultiTreeNode:
    """ 多叉树节点 """

    def __init__(self, data):
        """ 初始化方法 """
        self.data = data
        self.parent = None  # 父节点
        self.children = []  # [子节点]
        self.depth = 0  # 深度（根节点为0）

    def appendChild(self, node):
        """ 将node添加至[子节点]最后 """
        self.children.append(node)
        node.parent = self
        node.depth = self.depth + 1

    def appendLeftChild(self, node):
        """ 将node添加至[子节点]最前 """
        self.children.insert(0, node)
        node.parent = self
        node.depth = self.depth + 1

    def popChild(self, id_: int):
        """ 移除下标为id_的子节点
        :returns: 返回移除的节点
        """
        return self.children.pop(id_)

    def preorderTraversal(self) -> list:
        """ 前序遍历
        :returns: [节点]
        """
        result = []
        nodeStack = [self]
        while nodeStack:
            curNode = nodeStack.pop()
            result.append(curNode)
            nodeStack.extend(reversed(curNode.children))
        return result

    def postorderTraversal(self) -> list:
        """ 后序遍历
        :returns: [节点]
        """
        result = []
        nodeStack = [self]
        while nodeStack:
            curNode = nodeStack.pop()
            result.append(curNode)
            nodeStack.extend(curNode.children)
        result.reverse()
        return result

    def levelTraversal(self) -> list:
        """ 层序遍历
        :returns: [节点]
        """
        result = []
        nodeQueue = deque()
        nodeQueue.append(self)
        while nodeQueue:
            curNode = nodeQueue.popleft()
            result.append(curNode)
            nodeQueue.extend(curNode.children)
        return result

# endregion
