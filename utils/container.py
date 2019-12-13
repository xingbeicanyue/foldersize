from collections import Iterable


# region 双向链表

class LinkedListNode:
    """ 双向链表节点 """

    def __init__(self, data):
        """ 初始化 """
        self.data = data  # 数据
        self.next = None  # 下一个节点
        self.prev = None  # 上一个节点


class LinkedList:
    """ 双向链表 """

    def __init__(self, datas: Iterable=None):
        """ 初始化
        :param datas: [初始数据]
        """
        self._head = None  # 首节点
        self._tail = None  # 尾节点
        self._count = 0  # 节点数
        if datas:
            self.extend(datas)

    def __getitem__(self, id_: int) -> LinkedListNode:
        """ 返回下标为id_的节点
        :raises IndexError: 下标越界
        """
        if id_ >= 0:
            if id_ >= self._count:
                raise IndexError('[Error] LinkedList.__getitem__: 下标越界')
            curNode = self._head
            for i in range(id_):
                curNode = curNode.next
        else:
            if -id_ > self._count:
                raise IndexError('[Error] LinkedList.__getitem__: 下标越界')
            curNode = self._tail
            for i in range(-id_ - 1):
                curNode = curNode.prev
        return curNode

    def clone(self):
        """ 克隆链表及其所有节点 """
        result = LinkedList()
        curNode = self._head
        while curNode:
            result.append(curNode.data)
            curNode = curNode.next
        return result

    def head(self):
        """ 返回首节点，链表为空则返回None """
        return self._head

    def tail(self):
        """ 返回尾节点，链表为空则返回None """
        return self._tail

    def length(self) -> int:
        """ 返回节点数 """
        return self._count

    def append(self, data):
        """ 在链表尾添加数据 """
        newNode = LinkedListNode(data)
        if self._count == 0:
            self._head = self._tail = newNode
            self._count = 1
        else:
            self._tail.next = newNode
            newNode.prev = self._tail
            self._tail = newNode
            self._count += 1

    def appendLeft(self, data):
        """ 在链表头添加数据 """
        newNode = LinkedListNode(data)
        if self._count == 0:
            self._head = self._tail = newNode
            self._count = 1
        else:
            self._head.prev = newNode
            newNode.next = self._head
            self._head = newNode
            self._count += 1

    def extend(self, datas: Iterable):
        """ 在链表尾添加[数据] """
        for data in datas:
            newNode = LinkedListNode(data)
            if self._count == 0:
                self._head = self._tail = newNode
                self._count = 1
            else:
                self._tail.next = newNode
                newNode.prev = self._tail
                self._tail = newNode
                self._count += 1

    def extendLeft(self, datas: Iterable):
        """ 在链表头添加[数据]，[数据]顺序反转 """
        for data in datas:
            newNode = LinkedListNode(data)
            if self._count == 0:
                self._head = self._tail = newNode
                self._count = 1
            else:
                self._head.prev = newNode
                newNode.next = self._head
                self._head = newNode
                self._count += 1

    def insert(self, node: LinkedListNode, data):
        """ 将数据插入至node后 """
        newNode = LinkedListNode(data)
        newNode.prev = node
        newNode.next = node.next
        node.next = newNode
        if newNode.next:
            newNode.next.prev = newNode
        if self._tail == node:
            self._tail = newNode
        self._count += 1

    def insertBefore(self, node: LinkedListNode, data):
        """ 将数据插入至node前 """
        newNode = LinkedListNode(data)
        newNode.prev = node.prev
        newNode.next = node
        node.prev = newNode
        if newNode.prev:
            newNode.prev.next = newNode
        if self._head == node:
            self._head = newNode
        self._count += 1

    def clear(self):
        """ 清空 """
        self._head = self._tail = None
        self._count = 0

    def removeNode(self, node: LinkedListNode):
        """ 从链表中移除node """
        if self._count == 1:
            self._head = self._tail = None
        else:
            if node.prev:
                node.prev.next = node.next
            else:
                self._head = node.next
            if node.next:
                node.next.prev = node.prev
            else:
                self._tail = node.prev

        self._count -= 1
        node.prev = node.next = None

    def pop(self):
        """ 移除链表尾节点，并返回尾节点的数据
        :raises IndexError: 链表内没有节点
        """
        if self._count == 0:
            raise IndexError('[Error] LinkedList.pop: 链表为空')
        result = self._tail.data
        if self._count == 1:
            self._head = self._tail = None
        else:
            self._tail = self._tail.prev
            self._tail.next.prev = None
            self._tail.next = None
        self._count -= 1
        return result

    def popLeft(self):
        """ 移除链表首节点，并返回首节点的数据
        :raises IndexError: 链表内没有节点
        """
        if self._count == 0:
            raise IndexError('[Error] LinkedList.popLeft: 链表为空')
        result = self._head.data
        if self._count == 1:
            self._head = self._tail = None
        else:
            self._head = self._head.next
            self._head.prev.next = None
            self._head.prev = None
        self._count -= 1
        return result

    def reverse(self):
        """ 反向 """
        if self._count <= 1:
            return
        curNode = self._head
        while curNode:
            curNode.next, curNode.prev = curNode.prev, curNode.next
            curNode = curNode.prev
        self._head, self._tail = self._tail, self._head

# endregion
