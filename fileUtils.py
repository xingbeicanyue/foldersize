import queue
import os


class DirTreeNode:
    """ 文件夹树节点 """

    def __init__(self, pathDirName: str, dirName: str):
        """ 初始化 """
        self.parent = None
        self.children = []
        self.depth = 0

        self.pathDirName = pathDirName
        self.dirName = dirName
        self.selfSize = 0
        self.allSize = 0
        self.sizePercent = 0
        self.folderCount = 0
        self.fileCount = 0
        self.canVisit = True

    def appendChild(self, node):
        """ 添加子节点 """
        self.children.append(node)
        node.parent = self
        node.depth = self.depth + 1

    def preorderTraversal(self) -> list:
        """ 前序遍历 """
        result = []
        nodeStack = [self]
        while nodeStack:
            curNode = nodeStack.pop()
            result.append(curNode)
            nodeStack.extend(reversed(curNode.children))
        return result

    def postorderTraversal(self) -> list:
        """ 后序遍历 """
        result = []
        nodeStack = [self]
        while nodeStack:
            curNode = nodeStack.pop()
            result.append(curNode)
            nodeStack.extend(curNode.children)
        result.reverse()
        return result


class DirManager:
    """ 文件夹信息管理 """

    def __init__(self, pathDirName: str):
        self.__pathDirName = pathDirName
        self.__buildDirTree()

    @property
    def dirTree(self):
        """ 获取文件夹信息树 """
        return self.__dirTree

    def reload(self):
        """ 重新计算 """
        self.__buildDirTree()

    def searchNode(self, text: str, ignoreCase: bool) -> list:
        """ 搜索匹配的节点 """
        result = []
        nodes = self.__dirTree.preorderTraversal()
        if ignoreCase:
            text = text.lower()
            for node in nodes:
                if node.dirName.lower().find(text) >= 0:
                    result.append(node)
        else:
            for node in nodes:
                if node.dirName.find(text) >= 0:
                    result.append(node)
        return result

    def __buildDirTree(self):
        """ 建立文件夹信息树 """
        self.__dirTree = DirTreeNode(self.__pathDirName.replace('\\', '/'), self.__pathDirName)
        dirNodeQueue = queue.Queue()
        dirNodeQueue.put(self.__dirTree)
        while not dirNodeQueue.empty():
            curNode = dirNodeQueue.get()
            try:
                for dirName in os.listdir(curNode.pathDirName):
                    pathDirName = os.path.join(curNode.pathDirName, dirName).replace('\\', '/')
                    if os.path.isdir(pathDirName):
                        newNode = DirTreeNode(pathDirName, dirName)
                        curNode.appendChild(newNode)
                        dirNodeQueue.put(newNode)
                        curNode.folderCount += 1
                    else:
                        curNode.fileCount += 1
            except PermissionError:
                curNode.canVisit = False

        nodes = self.__dirTree.postorderTraversal()
        for i in range(len(nodes)):
            node = nodes[i]
            node.selfSize = max(DirManager.__getDirSizeWithoutSubdirs(node.pathDirName), 0)
            node.allSize = node.selfSize + sum([child.allSize for child in node.children])
            if node.allSize:
                for child in node.children:
                    child.sizePercent = child.allSize / node.allSize * 100
            node.folderCount += sum([child.folderCount for child in node.children])
            node.fileCount += sum([child.fileCount for child in node.children])
        nodes[-1].sizePercent = 100

    @staticmethod
    def __getDirSizeWithoutSubdirs(pathDirName: str) -> int:
        """ 获取文件夹中直属文件的总大小
        :returns: 返回负数表示获取失败
        """
        try:
            return sum([os.path.getsize(os.path.join(pathDirName, fileName)) for fileName in os.listdir(pathDirName)
                        if os.path.isfile(os.path.join(pathDirName, fileName))])
        except:
            return -1
