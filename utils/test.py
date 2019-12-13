import unittest
from utils.container import LinkedList
import utils.geometryUtils.geometry as geometry


# region container

# region 双向链表

class LinkedListTester(unittest.TestCase):
    """ 双向链表测试类 """

    def __checkLinkedList(self, linkedList: LinkedList, datas: list):
        """ 检查链表是否与datas数据相同 """
        self.assertEqual(len(datas), linkedList.length())
        curNode = linkedList.head()
        i = 0
        while curNode:
            self.assertEqual(datas[i], curNode.data)
            curNode = curNode.next
            i += 1
        if len(datas) > 0:
            self.assertEqual(datas[-1], linkedList.tail().data)

    def test__getItem__(self):
        """ 测试__getItem__ """
        linkedList = LinkedList([])
        with self.assertRaises(IndexError):
            _ = linkedList[0]

        linkedList = LinkedList([1, 2, 3, 4, 5])
        self.assertEqual(3, linkedList[2].data)
        self.assertEqual(4, linkedList[-2].data)
        with self.assertRaises(IndexError):
            _ = linkedList[5]
        with self.assertRaises(IndexError):
            _ = linkedList[-6]

    def testClone(self):
        """ 测试clone """
        def testAddress(linkedList1, linkedList2: LinkedList) -> bool:
            """ 测试两个链表地址是否不同 """
            if id(linkedList1) == id(linkedList2):
                return False
            curNode1, curNode2 = linkedList1.head(), linkedList2.head()
            while curNode1:
                if id(curNode1) == id(curNode2):
                    return False
                curNode1 = curNode1.next
                curNode2 = curNode2.next
            return True

        linkedList = LinkedList()
        linkedList2 = linkedList.clone()
        self.__checkLinkedList(linkedList2, [])
        self.assertEqual(True, testAddress(linkedList, linkedList2))

        datas = [1, 2, 3]
        linkedList = LinkedList(datas)
        linkedList2 = linkedList.clone()
        self.__checkLinkedList(linkedList2, datas)
        self.assertEqual(True, testAddress(linkedList, linkedList2))

    def testInit(self):
        """ 测试init """
        datas = []
        linkedList = LinkedList(datas)
        self.__checkLinkedList(linkedList, datas)

        datas = [1]
        linkedList = LinkedList(datas)
        self.__checkLinkedList(linkedList, datas)

        datas = [1, 2, 3, 4, 5]
        linkedList = LinkedList(datas)
        self.__checkLinkedList(linkedList, datas)

    def testAppend(self):
        """ 测试append """
        linkedList = LinkedList([])
        linkedList.append(1)
        self.__checkLinkedList(linkedList, [1])

        linkedList = LinkedList([1])
        linkedList.append(2)
        self.__checkLinkedList(linkedList, [1, 2])

        linkedList = LinkedList([1, 2, 3, 4, 5])
        linkedList.append(6)
        self.__checkLinkedList(linkedList, [1, 2, 3, 4, 5, 6])

    def testAppendLeft(self):
        """ 测试appendLeft """
        linkedList = LinkedList([])
        linkedList.appendLeft(1)
        self.__checkLinkedList(linkedList, [1])

        linkedList = LinkedList([1])
        linkedList.appendLeft(2)
        self.__checkLinkedList(linkedList, [2, 1])

        linkedList = LinkedList([1, 2, 3, 4, 5])
        linkedList.appendLeft(6)
        self.__checkLinkedList(linkedList, [6, 1, 2, 3, 4, 5])

    def testExtend(self):
        """ 测试extend """
        linkedList = LinkedList([])
        linkedList.extend([])
        self.__checkLinkedList(linkedList, [])

        linkedList.extend((1,))
        self.__checkLinkedList(linkedList, [1])

        linkedList.extend((2, 3, 4, 5))
        self.__checkLinkedList(linkedList, [1, 2, 3, 4, 5])

        linkedList.extend([6, 7])
        self.__checkLinkedList(linkedList, [1, 2, 3, 4, 5, 6, 7])

    def testExtendLeft(self):
        """ 测试extendLeft """
        linkedList = LinkedList([])
        linkedList.extendLeft([])
        self.__checkLinkedList(linkedList, [])

        linkedList.extendLeft((1,))
        self.__checkLinkedList(linkedList, [1])

        linkedList.extendLeft((2, 3, 4, 5))
        self.__checkLinkedList(linkedList, [5, 4, 3, 2, 1])

        linkedList.extendLeft([6, 7])
        self.__checkLinkedList(linkedList, [7, 6, 5, 4, 3, 2, 1])

    def testInsert(self):
        """ 测试insert """
        linkedList = LinkedList([1])
        node = linkedList.head()
        linkedList.insert(node, 2)
        self.__checkLinkedList(linkedList, [1, 2])
        linkedList.insert(linkedList[0], 3)
        self.__checkLinkedList(linkedList, [1, 3, 2])
        linkedList.insert(linkedList[2], 4)
        self.__checkLinkedList(linkedList, [1, 3, 2, 4])

    def testInsertBefore(self):
        """ 测试insertBefore """
        linkedList = LinkedList([1])
        node = linkedList.tail()
        linkedList.insertBefore(node, 2)
        self.__checkLinkedList(linkedList, [2, 1])
        linkedList.insertBefore(linkedList[0], 3)
        self.__checkLinkedList(linkedList, [3, 2, 1])
        linkedList.insertBefore(linkedList[2], 4)
        self.__checkLinkedList(linkedList, [3, 2, 4, 1])

    def testClear(self):
        """ 测试clear """
        linkedList = LinkedList([])
        linkedList.clear()
        self.__checkLinkedList(linkedList, [])

        linkedList = LinkedList([1, 2, 3])
        linkedList.clear()
        self.__checkLinkedList(linkedList, [])

    def testRemoveNode(self):
        """ 测试removeNode """
        linkedList = LinkedList([1, 2, 3, 4])
        linkedList.removeNode(linkedList[3])
        self.__checkLinkedList(linkedList, [1, 2, 3])
        linkedList.removeNode(linkedList[1])
        self.__checkLinkedList(linkedList, [1, 3])
        linkedList.removeNode(linkedList[0])
        self.__checkLinkedList(linkedList, [3])
        linkedList.removeNode(linkedList[0])
        self.__checkLinkedList(linkedList, [])

    def testPop(self):
        """ 测试pop """
        linkedList = LinkedList([1, 2])
        self.assertEqual(2, linkedList.pop())
        self.__checkLinkedList(linkedList, [1])
        self.assertEqual(1, linkedList.pop())
        self.__checkLinkedList(linkedList, [])
        with self.assertRaises(IndexError):
            linkedList.pop()

    def testPopLeft(self):
        """ 测试popLeft """
        linkedList = LinkedList([1, 2])
        self.assertEqual(1, linkedList.popLeft())
        self.__checkLinkedList(linkedList, [2])
        self.assertEqual(2, linkedList.popLeft())
        self.__checkLinkedList(linkedList, [])
        with self.assertRaises(IndexError):
            linkedList.popLeft()

    def testReverse(self):
        """ 测试reverse """
        linkedList = LinkedList()
        linkedList.reverse()
        self.__checkLinkedList(linkedList, [])

        linkedList = LinkedList([1])
        linkedList.reverse()
        self.__checkLinkedList(linkedList, [1])

        linkedList = LinkedList([1, 2, 3, 4, 5])
        linkedList.reverse()
        self.__checkLinkedList(linkedList, [5, 4, 3, 2, 1])

    def testAll(self):
        """ 综合测试 """
        linkedList = LinkedList([1, 2, 3, 4])
        self.__checkLinkedList(linkedList, [1, 2, 3 ,4])

        linkedList.append(5)
        self.__checkLinkedList(linkedList, [1, 2, 3, 4, 5])

        node = linkedList[-3]
        self.assertEqual(3, node.data)

        self.assertEqual(1, linkedList.popLeft())
        self.__checkLinkedList(linkedList, [2, 3, 4, 5])

        linkedList.clear()
        self.__checkLinkedList(linkedList, [])

        linkedList.appendLeft(6)
        self.__checkLinkedList(linkedList, [6])

        linkedList.extendLeft([7, 8, 9])
        self.__checkLinkedList(linkedList, [9, 8, 7, 6])

        with self.assertRaises(IndexError):
            _ = linkedList[6]

        node = linkedList[3]
        linkedList.insertBefore(node, 10)
        self.__checkLinkedList(linkedList, [9, 8, 7, 10, 6])

        linkedList.reverse()
        self.__checkLinkedList(linkedList, [6, 10, 7, 8, 9])

        linkedList.removeNode(linkedList[0])
        self.__checkLinkedList(linkedList, [10, 7, 8, 9])

# endregion

# endregion


# region geometry

class GeometryTester(unittest.TestCase):
    """ 图形库测试类 """

    def testPolylineConvexHull(self):
        """ 测试polylineConvexHull """

        def testOneCase(polyline: list, expectedConvexHull: list):
            """ 测试一个用例 """
            convexHull = geometry.polylineConvexHull(polyline)
            self.assertEqual(True, geometry.polygonIsSame(expectedConvexHull, convexHull))

        testOneCase([], [])
        testOneCase([(1, 0)], [(1, 0)])
        testOneCase([(1, 0), (2, 0)], [(1, 0), (2, 0), (1, 0)])
        testOneCase([(1, 0), (2, 0), (3, 0)], [(2, 0), (3, 0), (1, 0), (2, 0)])
        testOneCase([(1, 0), (1, 0)], [(1, 0), (1, 0)])
        testOneCase([(0, 0), (5, 5), (3, -1)], [(0, 0), (3, -1), (5, 5), (0, 0)])
        testOneCase(
            [(0, 0), (-1, -2), (-3, -6), (1, 3), (-3, -6), (0, 1), (-1, 4)],
            [(-3, -6), (-3, -6), (-1, -2), (0, 0), (1, 3), (-1, 4), (-3, -6)]
        )
        testOneCase(
            [(10, 4), (3, 4), (12, 6), (3, 3), (3, 3), (6, 4), (12, 3), (10, 7), (3, 3), (8, 6), (10, 4), (6, 7),
             (4, 2), (5, 5)],
            [(10, 7), (6, 7), (3, 4), (3, 3), (4, 2), (12, 3), (12, 6), (10, 7)]
        )
        testOneCase(
            [(-1, 6), (20, 2), (20, 3), (19, 10), (-1, 6), (18, 0), (19, 10), (20, 1), (17, 11), (20, 4), (10, 13),
             (-2, 3), (-5, 12), (-5, -1), (-4, -3), (15, -2), (18, 0), (-4, 12), (7, 8), (14, 12), (6, 2), (6, -2),
             (20, 4), (3, -2), (3, 3), (-5, 12), (-5, 12), (-1, -2), (19, -0.5), (3, 10)],
            [(20, 1), (20, 2), (20, 3), (20, 4), (19, 10), (17, 11), (14, 12), (10, 13), (-5, 12), (-5, -1), (-4, -3),
             (15, -2), (19, -0.5), (20, 1)]
        )

    def testPolygonRelationWithPt(self):
        """ 测试polygonRelationWithPt """
        polygon = []
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (0, 0)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (10, -10)))

        polygon = [(1, 2)]
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (0, 0)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (1, 2)))

        polygon = [(2, 2), (2, 2)]
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (-1, 2)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (0, 10)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (2, 2)))

        polygon = [(0, 0), (1, 0), (1, 7), (-1, 6)]
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (0, 0)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (1, 0)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (0, 6.5)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (1, 3)))
        self.assertEqual(geometry.RelationType.In, geometry.polygonRelationWithPt(polygon, (0, 6)))
        self.assertEqual(geometry.RelationType.In, geometry.polygonRelationWithPt(polygon, (0.5, 2)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (2, 0)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (0, 6.6)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (-5, -5)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (-1, 7)))

        polygon = [(12, 5), (10, 8), (10, 8), (10, 7), (6, 15), (0, 12), (-2, 5), (-3, 5), (-3, 5), (-1, -1), (1, 3),
                   (5, 5), (4, -3), (8, 0), (10, 2), (14, 5), (13, 5), (12, 5)]
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (12, 5)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (-2, 5)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (-3, 5)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (9, 1)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (-2, 2)))
        self.assertEqual(geometry.RelationType.On, geometry.polygonRelationWithPt(polygon, (6, 15)))
        self.assertEqual(geometry.RelationType.In, geometry.polygonRelationWithPt(polygon, (0, 5)))
        self.assertEqual(geometry.RelationType.In, geometry.polygonRelationWithPt(polygon, (10, 5)))
        self.assertEqual(geometry.RelationType.In, geometry.polygonRelationWithPt(polygon, (2, 9)))
        self.assertEqual(geometry.RelationType.In, geometry.polygonRelationWithPt(polygon, (-2, 3)))
        self.assertEqual(geometry.RelationType.In, geometry.polygonRelationWithPt(polygon, (8, 10)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (-4, 5)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (16, 5)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (-1, -3)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (0, -1)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (12.5, 0)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (9.9, 7.5)))
        self.assertEqual(geometry.RelationType.Out, geometry.polygonRelationWithPt(polygon, (8, 15)))

# endregion


if __name__ == '__main__':
    unittest.main()
