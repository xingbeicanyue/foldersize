"""
文件、文件夹相关功能
"""

from enum import Enum
import re
import queue
import os
import pypinyin


class ByteUnit(Enum):
    """ 文件大小单位 """
    byte = 0
    kiloByte = 1
    megaByte = 2
    gigaByte = 3


byteUnitCountDic = {ByteUnit.byte: 1, ByteUnit.kiloByte: 1024, ByteUnit.megaByte: 1024**2, ByteUnit.gigaByte: 1024**3}


class DirTreeNode:
    """ 文件夹树节点 """

    def __init__(self, pathDirName: str, dirName: str):
        """ 初始化 """
        self.parent = None
        self.children = []
        self.depth = 0

        self.pathDirName = pathDirName
        self.dirName = dirName
        self.dirNamePinyin = pypinyin.lazy_pinyin(self.dirName.lower(), errors=lambda item: '0'+item)
        self.selfSize = 0
        self.allSize = 0
        self.sizePercent = 0
        self.dirCount = 0
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

    __keyFuncs = {'name': lambda node: node.dirNamePinyin,
                  'allSize': lambda node: node.allSize,
                  'selfSize': lambda node: node.selfSize,
                  'dirCount': lambda node: node.dirCount,
                  'fileCount': lambda node: node.fileCount}

    def __init__(self, pathDirName: str):
        self.__sortInOrders = {'name': True, 'allSize': True, 'selfSize': True, 'dirCount': True, 'fileCount': True}
        self.__pathDirName = pathDirName
        self.__buildDirTree()

    @property
    def dirTree(self):
        """ 获取文件夹信息树 """
        return self.__dirTree

    def reload(self):
        """ 重新计算 """
        self.__buildDirTree()

    def searchNode(self, text: str, ignoreCase: bool, regex: bool) -> list:
        """ 搜索匹配的节点 """
        result = []
        nodes = self.__dirTree.preorderTraversal()
        try:
            if regex:
                if ignoreCase:
                    result = [node for node in nodes if re.search(text, node.dirName, re.IGNORECASE) is not None]
                else:
                    result = [node for node in nodes if re.search(text, node.dirName) is not None]
            else:
                if ignoreCase:
                    text = text.lower()
                    result = [node for node in nodes if node.dirName.lower().find(text) >= 0]
                else:
                    result = [node for node in nodes if node.dirName.find(text) >= 0]
        except:
            pass
        return result

    def sort(self, key: str):
        """ 排序 """
        if self.__dirTree is None:
            return
        self.__sortInOrders[key] = not self.__sortInOrders[key]
        keyFunc = DirManager.__keyFuncs[key]
        inOrder = self.__sortInOrders[key]
        nodeStack = [self.__dirTree]
        while nodeStack:
            curNode = nodeStack.pop()
            curNode.children.sort(key=keyFunc, reverse=inOrder)
            nodeStack.extend(curNode.children)

    def export(self, file):
        """ 导出文件夹（包括文件）树状图至文件 """

        def writeOneNode(node):
            """ 记录一个节点 """
            file.write(f'{indentStr * node.depth}*{node.dirName}\n')
            # 记录子文件夹
            for child in node.children:
                writeOneNode(child)
            # 记录文件
            for fileName in os.listdir(node.pathDirName):
                if os.path.isfile(os.path.join(node.pathDirName, fileName).replace('\\', '/')):
                    file.write(f'{indentStr * (node.depth + 1)}{fileName}\n')

        if self.__dirTree is None:
            return
        indentStr = '    '  # 缩进字符串
        writeOneNode(self.__dirTree)

    def __buildDirTree(self):
        """ 建立文件夹信息树 """
        try:
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
                            curNode.dirCount += 1
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
                node.dirCount += sum([child.dirCount for child in node.children])
                node.fileCount += sum([child.fileCount for child in node.children])
            nodes[-1].sizePercent = 100
        except:
            self.__dirTree = None

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
