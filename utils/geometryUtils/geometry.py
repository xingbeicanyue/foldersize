import enum
import math
import re
import sys
from utils import pyUtils
from utils.pyUtils import floatCompare, floatEq, floatNEq, floatLe, floatLeEq, floatGr, floatGrEq, floatBetween


# region 常量

geoTol = 1e-9  # 图形计算容差
emptyAabb = (sys.float_info.max, -sys.float_info.max, sys.float_info.max, -sys.float_info.max)  # 标准空aabb包围盒
ptZero = (0, 0)  # 零点


class RelationType(enum.Enum):
    """ 图形关系类型 """
    On = 0  # 在上面
    In = 1  # 在里面
    Out = 2  # 在外面
    Left = 3  # 在左侧
    Right = 4  # 在右侧
    Down = 5  # 在下侧
    Up = 6  # 在上侧
    Contain = 7  # 包含
    Contained = 8  # 被包含
    Overlap = 9  # 重叠
    Intersect = 10  # 相交
    InternallyTangent = 11  # 内切
    ExternallyTangent = 12  # 外切
    Disjoint = 13  # 相离


class DirType(enum.Enum):
    """ 方向类型 """
    Horizon = 0  # 横向
    Vertical = 1  # 纵向
    Left = 2  # 向左
    Right = 3  # 向右
    Bottom = 4  # 向下
    Top = 5  # 向上
    LeftBottom = 6  # 向左下
    LeftUp = 7  # 向左上
    RightBottom = 8  # 向右下
    RightTop = 9  # 向右上

# endregion


# region 通用函数

def _strToNumberStrs(string: str) -> list:
    """ 提取字符串中的数字列表，数字间需用“非数字、小数点、负号”的字符作间隔
    :returns: [数字字符串]
    """
    pattern = re.compile(r'[^0-9.-]+')
    return list(filter(None, re.split(pattern, string)))

# endregion


# region 点

"""
点用tuple表示，2个元素分别是x、y坐标，均为float
"""

def ptToStr(p: tuple) -> str:
    """ 点转字符串 """
    return f'({p[0]}, {p[1]})'


def strToPt(string: str) -> tuple:
    """ 字符串转点 """
    numberStrs = _strToNumberStrs(string)
    return float(numberStrs[0]), float(numberStrs[1])


def ptRound(p: tuple, precision: int=0) -> tuple:
    """ 舍入至小数点后precision位，银行家舍入法 """
    return round(p[0], precision), round(p[1], precision)


def ptAabb(p: tuple) -> tuple:
    """ aabb包围盒 """
    return p[0], p[0], p[1], p[1]


def ptQuadrant(p: tuple) -> int:
    """ 返回所在象限
    :returns: 1~4:1~4象限; 0:零点; -1:x轴正方向; -2:y轴正方向; -3:x轴负方向; -4:y轴负方向
    """
    if floatGr(p[0], 0, abs_tol=geoTol):
        if floatGr(p[1], 0, abs_tol=geoTol):
            return 1
        elif floatLe(p[1], 0, abs_tol=geoTol):
            return 4
        return -1
    elif floatLe(p[0], 0, abs_tol=geoTol):
        if floatGr(p[1], 0, abs_tol=geoTol):
            return 2
        elif floatLe(p[1], 0, abs_tol=geoTol):
            return 3
        return -3
    if floatGr(p[1], 0, abs_tol=geoTol):
        return -2
    elif floatLe(p[1], 0, abs_tol=geoTol):
        return -4
    return 0


def ptNeg(p: tuple) -> tuple:
    """ 返回以零点中心对称的点 """
    return -p[0], -p[1]


def ptEq(p1: tuple, p2: tuple) -> bool:
    """ 判断是否重合: p1==p2 """
    return floatEq(p1[0], p2[0], abs_tol=geoTol) and floatEq(p1[1], p2[1], abs_tol=geoTol)


def ptCloseTo(p1: tuple, p2: tuple, dist: float) -> bool:
    """ 判断点p1、p2之间的直线距离是否<=dist """
    return floatLeEq(math.hypot((p1[0] - p2[0]), abs(p1[1] - p2[1])), dist, abs_tol=geoTol)


def ptDistanceTo(p1: tuple, p2: tuple, distType: int = 0) -> float:
    """ 返回点p1、p2之间的距离
    :param distType: 距离种类 0: 欧式距离
    """
    if distType == 0:
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def ptVec(p1: tuple, p2: tuple) -> tuple:
    """ 返回点p1至p2的向量 """
    return p2[0] - p1[0], p2[1] - p1[1]


def ptCompareByXY(p1: tuple, p2: tuple) -> float:
    """ 比较p1、p2，严格按x、y顺序
    :returns: 负数:p1<p2; 0:p1=p2; 正数:p1>p2
    """
    result = p1[0] - p2[0]
    return result if result != 0 else p1[1] - p2[1]


def ptCompareByYX(p1: tuple, p2: tuple) -> float:
    """ 比较p1、p2，严格按y、x顺序
    :returns: 负数:p1<p2; 0:p1=p2; 正数:p1>p2
    """
    result = p1[1] - p2[1]
    return result if result != 0 else p1[0] - p2[0]


def ptTranslate(p: tuple, transVec: tuple) -> tuple:
    """ 平移 """
    return p[0] + transVec[0], p[1] + transVec[1]


def ptRotate(p: tuple, radian: float, center: tuple=ptZero) -> tuple:
    """ 旋转（逆时针）
    :param radian: 旋转弧度
    :param center: 旋转中心
    """
    return ptTranslate(center, vecRotate(ptVec(center, p), radian))


def ptScale(p: tuple, xRate: float, yRate: float, center: tuple=ptZero) -> tuple:
    """ 缩放 """
    return (p[0] - center[0]) * xRate + center[0], (p[1] - center[1]) * yRate + center[1]


def ptReflect(p: tuple, axis) -> tuple:
    """ 镜像
    :param axis: 传入直线表示镜像轴，可以用tuple表示直线，也可以是以下字符串值：
                 "x":以x轴为镜像轴; "y":以y轴为镜像轴; "y=x":以直线y=x为镜像轴; "y=-x":以直线y=-x为镜像轴
    """
    if axis == 'x':
        return p[0], -p[1]
    elif axis == 'y':
        return -p[0], p[1]
    elif axis == 'y=x':
        return p[1], p[0]
    elif axis == 'y=-x':
        return -p[1], -p[0]
    projectionPoint = lineProjection(axis, p)
    return projectionPoint[0] * 2 - p[0], projectionPoint[1] * 2 - p[1]

# endregion


# region 向量

"""
向量用tuple表示，2个元素分别是终点x、y坐标，起点为零点
"""

def createVec(**kw) -> tuple:
    """ 创建向量
    :param kw: 可以提供以下参数组合
               1. 长度len(float)、从x轴正方向起的弧度rad(float)
               2. 起点spt(tuple)、终点ept(tuple)
    :raises ValueError: 参数错误
    """
    if 'len' in kw and 'rad' in kw:
        return kw['len'] * math.cos(kw['rad']), kw['len'] * math.sin(kw['rad'])
    if 'spt' in kw and 'ept' in kw:
        return kw['ept'][0] - kw['spt'][0], kw['ept'][1] - kw['spt'][1]
    raise ValueError('[Error] createVec: 参数错误')


def vecToStr(vec: tuple) -> str:
    """ 向量转字符串 """
    return f'({vec[0]}, {vec[1]})'


def vecRound(vec: tuple, precision: int=0) -> tuple:
    """ 舍入至小数点后precision位，银行家舍入法 """
    return round(vec[0], precision), round(vec[1], precision)


def vecAdd(vec1: tuple, vec2: tuple) -> tuple:
    """ 向量相加：vec1+vec2 """
    return vec1[0] + vec2[0], vec1[1] + vec2[1]


def vecSub(vec1: tuple, vec2: tuple) -> tuple:
    """ 向量相减：vec1-vec2 """
    return vec1[0] - vec2[0], vec1[1] - vec2[1]


def vecMul(vec: tuple, num: float) -> tuple:
    """ 向量数乘：vec*num """
    return vec[0] * num, vec[1] * num


def vecDotMul(vec1: tuple, vec2: tuple) -> float:
    """ 向量点乘：vec·vec2 """
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def vecTruediv(vec: tuple, num: float) -> tuple:
    """ 向量数除（真除法）：vec/num """
    return vec[0] / num, vec[1] / num


def vecNeg(vec: tuple) -> tuple:
    """ 向量反向：-vec """
    return -vec[0], -vec[1]


def vecLength(vec: tuple) -> float:
    """ 返回向量长度 """
    return math.hypot(vec[0], vec[1])


def vecEq(vec1: tuple, vec2: tuple) -> bool:
    """ 判断向量是否相等: vec1==vec2 """
    return floatEq(vec1[0], vec2[0], abs_tol=geoTol) and floatEq(vec1[1], vec2[1], abs_tol=geoTol)


def vecAngleTo(vec1: tuple, vec2: tuple, canClockwise: bool=False) -> float:
    """ 返回向量vec1、vec2之间的夹角
    :param canClockwise: True: 计算最小夹角弧度，范围为[0, PI];
                         False: 计算vec1逆时针转至vec2的弧度，范围为[0, 2PI)
    """
    radian = math.acos(vecDotMul(vec1, vec2) / (vecLength(vec1) * vecLength(vec2)))  # 夹角弧度
    if canClockwise:
        return radian
    area = polygonArea([ptZero, vec1, vec2])  # 根据面积符号判断左右
    return radian if area >= 0 else pyUtils.doublePi - radian


def vecAngle(vec: tuple) -> float:
    """ 返回x轴正方向至vec之间的夹角 """
    result = math.acos(vec[0] / math.hypot(vec[0], vec[1]))
    return result if vec[1] >= 0 else pyUtils.doublePi - result


def vecRotate(vec: tuple, radian: float) -> tuple:
    """ 旋转（逆时针）
    :param radian: 旋转弧度
    """
    cosR = math.cos(radian)
    sinR = math.sin(radian)
    return cosR * vec[0] - sinR * vec[1], sinR * vec[0] + cosR * vec[1]


def vecScale(vec: tuple, xRate: float, yRate: float) -> tuple:
    """ 缩放（以零点为中心） """
    return vec[0] * xRate, vec[1] * yRate


def vecReflect(vec: tuple, axis) -> tuple:
    """ 镜像（返回值依然以零点为起点）
    :param axis: 传入直线表示镜像轴，可以用tuple表示直线，也可以是以下字符串值：
                 "x":以x轴为镜像轴; "y":以y轴为镜像轴; "y=x":以直线y=x为镜像轴; "y=-x":以直线y=-x为镜像轴
    """
    return ptVec(ptReflect(ptZero, axis), ptReflect(vec, axis))


def vecStretch(vec: tuple, length: float) -> tuple:
    """ 将向量拉伸至长度length """
    rate = length / vecLength(vec)
    return vecScale(vec, rate, rate)

# endregion


# region aabb包围盒

"""
aabb包围盒用tuple表示，4个元素分别是左、右、下、上界限，均为float
“标准aabb包围盒”是指左界限<=右界限、下界限<=上界限的aabb包围盒，如果是空aabb包围盒则必须等于invalidAabb
"""

def aabbToStr(aabb: tuple) -> str:
    """ aabb包围盒转字符串 """
    return f'({aabb[0]}, {aabb[1]}, {aabb[2]}, {aabb[3]})'


def aabbToStandard(aabb: tuple) -> tuple:
    """ 返回标准aabb包围盒 """
    if floatGr(aabb[0], aabb[1], abs_tol=geoTol) or floatGr(aabb[2], aabb[3], abs_tol=geoTol):
        return emptyAabb
    return aabb[0], aabb[1], aabb[2], aabb[3]


def aabbRound(aabb: tuple, precision: int=0) -> tuple:
    """ 舍入至小数点后precision位，银行家舍入法 """
    if aabbIsEmpty(aabb):
        return emptyAabb
    return round(aabb[0], precision), round(aabb[1], precision), round(aabb[2], precision), round(aabb[3], precision)


def aabbIsEmpty(aabb: tuple) -> bool:
    """ 返回aabb包围盒是否为空 """
    return floatGr(aabb[0], aabb[1], abs_tol=geoTol) or floatGr(aabb[2], aabb[3], abs_tol=geoTol)


def aabbWidth(aabb: tuple) -> float:
    """ 返回aabb包围盒宽度 """
    return None if aabbIsEmpty(aabb) else aabb[1] - aabb[0]


def aabbHeight(aabb: tuple) -> float:
    """ 返回aabb包围盒高度 """
    return None if aabbIsEmpty(aabb) else aabb[3] - aabb[2]


def aabbArea(aabb: tuple) -> float:
    """ 返回aabb包围盒面积 """
    return None if aabbIsEmpty(aabb) else (aabb[1] - aabb[0]) * (aabb[3] - aabb[2])


def aabbPerimeter(aabb: tuple) -> float:
    """ 返回aabb包围盒周长 """
    return None if aabbIsEmpty(aabb) else (aabb[1] - aabb[0] + aabb[3] - aabb[2]) * 2


def aabbCenter(aabb: tuple) -> tuple:
    """ 返回aabb包围盒中心点 """
    return None if aabbIsEmpty(aabb) else (aabb[0] + aabb[1]) / 2, (aabb[2] + aabb[3]) / 2


def aabbEq(aabb1: tuple, aabb2: tuple) -> bool:
    """ 判断aabb包围盒是否相等
    :remarks: 只有四个界限值都相等才算相等
    """
    return floatEq(aabb1[0], aabb2[0], abs_tol=geoTol) and floatEq(aabb1[1], aabb2[1], abs_tol=geoTol) and\
           floatEq(aabb1[2], aabb2[2], abs_tol=geoTol) and floatEq(aabb1[3], aabb2[3], abs_tol=geoTol)


def aabbRelationWithPt(aabb: tuple, p: tuple) -> bool:
    """ 判断点p是否在aabb包围盒内（包括包围盒边界上） """
    return floatLeEq(aabb[0], p[0], abs_tol=geoTol) and floatLeEq(p[0], aabb[1], abs_tol=geoTol) and\
           floatLeEq(aabb[2], p[1], abs_tol=geoTol) and floatLeEq(p[1], aabb[3], abs_tol=geoTol)


def aabbRelationWithAabb(aabb1: tuple, aabb2: tuple):
    """ 判断aabb2相对于aabb1的位置关系
    :returns: 可能的返回值：Contain、Contained、Overlap、Intersect、Disjoint
    :remarks: 如果有非标准包围盒，则返回Disjoint
    """
    if aabbIsEmpty(aabb1) or aabbIsEmpty(aabb2):
        return RelationType.Disjoint
    if aabbEq(aabb1, aabb2):
        return RelationType.Overlap
    unionAabb = aabbExpandByAabb(aabb1, aabb2)
    if aabbEq(unionAabb, aabb2):
        return RelationType.Contain
    intersectAabb = aabbIntersection(aabb1, aabb2)
    if aabbEq(intersectAabb, aabb2):
        return RelationType.Contained
    if aabbIsEmpty(intersectAabb):
        return RelationType.Disjoint
    return RelationType.Intersect


def aabbTranslate(aabb: tuple, transVec: tuple) -> tuple:
    """ 平移 """
    if aabbIsEmpty(aabb):
        return emptyAabb
    return aabb[0] + transVec[0], aabb[1] + transVec[0], aabb[2] + transVec[1], aabb[3] + transVec[1]


def aabbScale(aabb: tuple, xRate: float, yRate: float, center: tuple=ptZero) -> tuple:
    """ 缩放 """
    if aabbIsEmpty(aabb):
        return emptyAabb
    return (aabb[0] - center[0]) * xRate + center[0], (aabb[1] - center[0]) * xRate + center[0],\
           (aabb[2] - center[1]) * yRate + center[1], (aabb[3] - center[1]) * yRate + center[1]


def aabbOffset(aabb: tuple, dist: float) -> tuple:
    """ 返回扩张或收缩后的aabb包围盒，dist>0时为扩张 """
    if aabbIsEmpty(aabb):
        return emptyAabb
    return aabb[0] - dist, aabb[1] + dist, aabb[2] - dist, aabb[3] + dist


def aabbIntersection(aabb1: tuple, aabb2: tuple) -> tuple:
    """ 返回两个aabb包围盒的重叠包围盒 """
    result = max(aabb1[0], aabb2[0]), min(aabb1[1], aabb2[1]), max(aabb1[2], aabb2[2]), min(aabb1[3], aabb2[3])
    return aabbToStandard(result)


def aabbExpandByPt(aabb: tuple, p: tuple) -> tuple:
    """ 返回能包含aabb包围盒和点p的最小aabb包围盒 """
    result = (min(aabb[0], p[0]), max(aabb[1], p[0]), min(aabb[2], p[1]), max(aabb[3], p[1]))
    return aabbToStandard(result)


def aabbExpandByAabb(aabb1: tuple, aabb2: tuple) -> tuple:
    """ 返回能包含两个aabb包围盒的最小aabb包围盒 """
    result = min(aabb1[0], aabb2[0]), max(aabb1[1], aabb2[1]), min(aabb1[2], aabb2[2]), max(aabb1[3], aabb2[3])
    return aabbToStandard(result)

# endregion


# region 圆

"""
圆用tuple表示，2个元素分别是圆心和半径
"""

def circleToStr(circle: tuple) -> str:
    """ 圆转字符串 """
    return f'({ptToStr(circle[0])}, {circle[1]})'


def circleRelationWithPt(circle: tuple, p: tuple) -> RelationType:
    """ 判断点p对于圆的位置关系
    :returns: 可能的返回值：In、On、Out
    """
    compareResult = floatCompare(ptDistanceTo(circle[0], p), circle[1], abs_tol=geoTol)
    if compareResult < 0:
        return RelationType.In
    elif compareResult > 0:
        return RelationType.Out
    return RelationType.rlOn


def circleRelationWithCircle(circle1: tuple, circle2: tuple):
    """ 判断圆2对于圆1的位置关系
    :returns: 可能的返回值Contain、Contained、Overlap、Intersect、InternallyTangent、ExternallyTangent、Disjoint
    """
    centerDist = ptDistanceTo(circle1[0], circle2[0])
    if floatEq(centerDist, 0, abs_tol=geoTol) and floatEq(circle1[1], circle2[1]):
        return RelationType.Overlap
    addCompareResult = floatCompare(circle1[1] + circle2[1], centerDist)
    if addCompareResult > 0:
        return RelationType.Disjoint
    elif addCompareResult == 0:
        return RelationType.ExternallyTangent
    subCompareResult = floatCompare(abs(circle1[1] - circle2[1]), centerDist)
    if subCompareResult > 0:
        return RelationType.Contain if circle1[1] < circle2[1] else RelationType.Contained
    return RelationType.Intersect if subCompareResult < 0 else RelationType.InternallyTangent

# endregion


# region 椭圆

"""
椭圆用tuple表示，前2项是焦点，第3项等于2a（长轴长度）
"""

def createEllipse(**kw) -> tuple:
    """ 创建椭圆
    :param kw: 可以提供以下参数组合
               1. aabb(tuple)，创建包围盒为aabb的椭圆，该椭圆的焦点连线总为水平或竖直方向且总为坐标轴正方向
               2. circle(tuple)，创建与圆等价的椭圆
    :raises ValueError: 参数错误
    """
    if 'aabb' in kw:
        aabb = kw['aabb']
        width, height, center = aabbWidth(aabb), aabbHeight(aabb), aabbCenter(aabb)
        type_ = floatCompare(width, height, abs_tol=geoTol)  # 0:圆; 1:焦点连线水平; -1:焦点连线竖直
        if type_ == 0:
            return center, center, width
        else:
            a, b = max(width, height) / 2, min(width, height) / 2
            c = (a ** 2 - b ** 2) ** 0.5
            if type_ == 1:
                return (center[0] - c, center[1]), (center[0] + c, center[1]), a * 2
            return (center[0], center[1] - c), (center[0], center[1] + c), a * 2
    elif 'circle' in kw:
        circle = kw['circle']
        return circle[0], circle[0], circle[1] * 2
    raise ValueError('[Error] createBezier: 参数错误')


def ellipseToStr(ellipse: tuple) -> str:
    """ 椭圆转字符串 """
    return f'({ellipse[0]}, {ellipse[1]}, {ellipse[2]})'


def strToEllipse(string: str) -> tuple:
    """ 字符串转椭圆 """
    numberStrs = _strToNumberStrs(string)
    return (float(numberStrs[0]), float(numberStrs[1])), (float(numberStrs[2]), float(numberStrs[3])),\
        float(numberStrs[4])


def ellipseToStd(ellipse: tuple) -> tuple:
    """ 返回椭圆中心为原点、长轴与x轴重合、焦点组成的向量方向为x轴正方向的全等椭圆 """
    c = ptDistanceTo(ellipse[0], ellipse[1]) / 2
    return (-c, 0), (c, 0), ellipse[2]


def ellipseAabb(ellipse: tuple) -> tuple:
    """ 返回椭圆aabb包围盒 """
    a, b, c = ellipseABC(ellipse)
    slope = seglineSlope((ellipse[0], ellipse[1]))  # 交点向量斜率
    if slope is None:
        return ellipse[0][0] - b, ellipse[0][0] + b,\
               min(ellipse[0][1], ellipse[1][1]) - a + c, max(ellipse[0][1], ellipse[1][1]) + a - c
    if floatEq(slope, 0, abs_tol=geoTol):
        return min(ellipse[0][0], ellipse[1][0]) - a + c, max(ellipse[0][0], ellipse[1][0]) + a - c,\
               ellipse[0][1] - b, ellipse[0][1] + b
    else:
        param = math.atan(b / (a * slope)) / (math.pi * 2)  # 决定坐标界限的点参数
        yPt1 = ellipsePointByParam(ellipse, param)
        yPt2 = ellipsePointByParam(ellipse, param + 0.5)
        xPt1 = ellipsePointByParam(ellipse, param + 0.25)
        xPt2 = ellipsePointByParam(ellipse, param + 0.75)
        return min(xPt1[0], xPt2[0]), max(xPt1[0], xPt2[0]), min(yPt1[1], yPt2[1]), max(yPt1[1], yPt2[1])


def ellipseObb(ellipse: tuple) -> list:
    """ 返回椭圆的obb包围盒 """
    stdEllipse = ellipseToStd(ellipse)
    result = createPolyline(aabb=ellipseAabb(stdEllipse))
    radian = 0 if ellipseIsCircle(ellipse) else vecAngleTo((1,0), ptVec(ellipse[0], ellipse[1]))
    transVec = ptVec(seglineRotate((stdEllipse[0], stdEllipse[1]), radian)[0], ellipse[0])
    return polylineTranslate(polylineRotate(result, radian), transVec)


def ellipseABC(ellipse: tuple) -> tuple:
    """ 返回椭圆的a、b、c参数（长轴长/2、短轴长/2、焦点距离/2）
    :raises ValueError: 长轴长度与焦点距离不符
    """
    a = ellipse[2] / 2
    c = ptDistanceTo(ellipse[0], ellipse[1]) / 2
    compareResult = floatCompare(a, c, abs_tol=geoTol)
    if compareResult > 0:
        b = (a ** 2 - c ** 2) ** 0.5
    elif compareResult == 0:
        b = 0
    else:
        raise ValueError('[Error] ellipseABC: 长轴长度与焦点距离不符')
    return a, b, c


def ellipseB(ellipse: tuple) -> float:
    """ 返回椭圆短轴长 / 2 """
    c = ptDistanceTo(ellipse[0], ellipse[1]) / 2
    a = ellipse[2] / 2
    return (a ** 2 - c ** 2) ** 0.5


def ellipseC(ellipse: tuple) -> float:
    """ 返回椭圆焦点距离 / 2 """
    return ptDistanceTo(ellipse[0], ellipse[1]) / 2


def ellipseIsCircle(ellipse: tuple) -> bool:
    """ 返回椭圆是否为圆 """
    return ptEq(ellipse[0], ellipse[1])


def ellipsePointByParam(ellipse: tuple, param: float) -> tuple:
    """ 返回椭圆上参数param位置的点 """
    a, b, c = ellipseABC(ellipse)
    actParam = param * pyUtils.doublePi
    result = (a * math.cos(actParam), b * math.sin(actParam))

    radian = vecAngleTo((1, 0), ptVec(ellipse[0], ellipse[1]))
    transVec = ptVec((c, 0), ptRotate(ellipse[1], -radian))
    return ptRotate(ptTranslate(result, transVec), radian)


def ellipseTranslate(ellipse: tuple, transVec: tuple) -> tuple:
    """ 平移 """
    return ptTranslate(ellipse[0], transVec), ptTranslate(ellipse[1], transVec), ellipse[2]


def ellipseRotate(ellipse: tuple, radian: float, center: tuple=ptZero) -> tuple:
    """ 旋转（逆时针）
    :param radian: 旋转弧度
    :param center: 旋转中心
    """
    return ptRotate(ellipse[0], radian, center), ptRotate(ellipse[1], radian, center), ellipse[2]


def ellipseScale(ellipse: tuple, xRate: float, yRate: float, center: tuple=ptZero) -> tuple:
    """ 缩放 """
    center1 = ptScale(ellipse[0], xRate, yRate, center)
    center2 = ptScale(ellipse[1], xRate, yRate, center)
    rate = ptDistanceTo(center1, center2) / ptDistanceTo(ellipse[0], ellipse[1])
    return center1, center2, ellipse[2] * rate


def ellipseReflect(ellipse: tuple, axis) -> tuple:
    """ 镜像
    :param axis: 传入直线表示镜像轴，可以用tuple表示直线，也可以是以下字符串值：
                 "x":以x轴为镜像轴; "y":以y轴为镜像轴; "y=x":以直线y=x为镜像轴; "y=-x":以直线y=-x为镜像轴
    """
    return ptReflect(ellipse[0], axis), ptReflect(ellipse[1], axis), ellipse[2]

# endregion


# region 直线段

"""
直线段用tuple表示，2个元素分别是起点和终点
"""

def createSegline(**kw) -> tuple:
    """ 创建直线段
    :param kw: 可以提供以下参数组合：
               1. 起点sp(tuple)、长度len(float)、弧度rad(float)
    :raises ValueError: 参数错误
    """
    if 'sp' in kw and 'len' in kw and 'rad' in kw:
        vec = createVec(len=kw['len'], rad=kw['rad'])
        return kw['sp'], ptTranslate(kw['sp'], vec)
    raise ValueError('[Error] createSegline: 参数错误')


def seglineToStr(segline: tuple) -> str:
    """ 直线段转字符串 """
    return f'({ptToStr(segline[0])}, {ptToStr(segline[1])})'


def strToSegline(string: str) -> tuple:
    """ 字符串转直线段 """
    numberStrs = _strToNumberStrs(string)
    return (float(numberStrs[0]), float(numberStrs[1])), (float(numberStrs[2]), float(numberStrs[3]))


def seglineRound(segline: tuple, precision: int=0) -> tuple:
    """ 舍入至小数点后precision位，银行家舍入法 """
    return ptRound(segline[0], precision), ptRound(segline[1], precision)


def seglineAabb(segline: tuple) -> tuple:
    """ 返回直线段aabb包围盒 """
    return min(segline[0][0], segline[1][0]), max(segline[0][0], segline[1][0]),\
           min(segline[0][1], segline[1][1]), max(segline[0][1], segline[1][1])


def seglineSlope(segline: tuple):
    """ 返回直线段斜率（如果没有则返回None） """
    if floatEq(segline[0][0], segline[1][0], abs_tol=geoTol):
        return None
    return (segline[1][1] - segline[0][1]) / (segline[1][0] - segline[0][0])


def seglineLength(segline: tuple) -> float:
    """ 返回直线段长度 """
    return math.hypot(segline[0][0] - segline[1][0], segline[0][1] - segline[1][1])


def seglineVec(segline: tuple) -> tuple:
    """ 返回直线段对应的向量 """
    return ptVec(segline[0], segline[1])


def seglineMidPoint(segline: tuple) -> tuple:
    """ 返回直线段中点 """
    return (segline[0][0] + segline[1][0]) / 2, (segline[0][1] + segline[1][1]) / 2


def seglineParamByPoint(segline: tuple, p: tuple) -> float:
    """ 返回点p在直线段所在直线上对应的参数
        要求p在直线上
    """
    if floatEq(segline[0][0], segline[1][0], abs_tol=geoTol):  # 平行于y轴
        return (p[1] - segline[0][1]) / (segline[1][1] - segline[0][1])
    else:  # 不平行于y轴
        return (p[0] - segline[0][0]) / (segline[1][0] - segline[0][0])


def seglinePointByParam(segline: tuple, param: float) -> tuple:
    """ 返回直线段所在直线上参数param位置的点 """
    return ptTranslate(segline[0], vecScale(seglineVec(segline), param, param))


def seglineYByX(segline: tuple, x: float):
    """ 返回直线段所在直线上x坐标对应的y坐标，如果直线段平行于y轴则返回None """
    if floatNEq(segline[0][0], segline[1][0], abs_tol=geoTol):
        return segline[0][1] + (segline[1][1] - segline[0][1]) * (x - segline[0][0]) / (segline[1][0] - segline[0][0])
    return None


def seglineXByY(segline: tuple, y: float):
    """ 返回直线段所在直线上y坐标对应的x坐标，如果直线段平行于x轴则返回None """
    if floatNEq(segline[0][1], segline[1][1], abs_tol=geoTol):
        return segline[0][0] + (segline[1][0] - segline[0][0]) * (y - segline[0][1]) / (segline[1][1] - segline[0][1])
    return None


def seglineProjection(segline: tuple, p: tuple) -> tuple:
    """ 返回点p到直线段所在直线的垂足（投影） """
    if ptEq(segline[0], segline[1]):  # 若两点重合则返回该点
        return segline[0]

    k = seglineSlope(segline)
    if k is None:  # 没有斜率
        return segline[0][0], p[1]
    elif floatEq(k, 0):  # 垂线没有斜率
        return p[0], segline[0][1]

    k_1 = 1 / k
    x = (p[0] * k_1 + segline[0][0] * k - segline[0][1] + p[1]) / (k + k_1)
    y = k * (x - segline[0][0]) + segline[0][1]
    return x, y


def seglineDistanceTo(segline: tuple, p: tuple, isLine: bool=False) -> float:
    """ 返回点p到直线段segline的最短距离 
    :param isLine: 是否将直线段视为其所在的直线
    """
    if ptEq(segline[0], segline[1]):
        return ptDistanceTo(segline[1], p)
        
    projectionPoint = seglineProjection(segline, p)  # 投影
    if isLine:
        return ptDistanceTo(projectionPoint, p)
    pFParam = seglineParamByPoint(segline, projectionPoint)  # 投影对应的参数
    if floatLeEq(pFParam, 0):
        return ptDistanceTo(segline[0], p)
    elif floatGrEq(pFParam, 1):
        return ptDistanceTo(segline[1], p)
    else:
        return ptDistanceTo(projectionPoint, p)


def seglineRelationWithPt(segline: tuple, p: tuple, isLine: bool=False) -> RelationType:
    """ 判断直线段与点p的位置关系
    :param isLine: 是否将直线段视为其所在的直线
    :returns: 可能的返回值：On、Out、Left、Right
    """
    compareResult = floatCompare(polygonArea([segline[0], segline[1], p]), 0, abs_tol=geoTol)
    if compareResult < 0:
        return RelationType.Left
    elif compareResult > 0:
        return RelationType.Right
    else:
        if isLine or floatEq(seglineDistanceTo(segline, p, False), 0, abs_tol=geoTol):
            return RelationType.On
        return RelationType.Out


def seglineCrossWithSegline(segline1: tuple, segline2: tuple, isLine1: bool=False, isLine2: bool=False) -> tuple:
    """ 计算两条直线段的交点
    :param segline1: 第一条直线段
    :param segline2: 第二条直线段
    :param isLine1: 第一条线段是否视为直线段所在的直线
    :param isLine2: 第二条线段是否视为直线段所在的直线
    :returns: ((交点), (交线段))  若直线与直线重合则交线段返回segline1
    """

    def calcArea2(p1: tuple, p2: tuple, p3: tuple) -> float:
        """ 计算三点组成的三角形面积*2 """
        return p1[0]*p2[1]+p1[1]*p3[0]+p2[0]*p3[1] - (p1[0]*p3[1]+p1[1]*p2[0]+p2[1]*p3[0])

    def calcCrossPt(areaA: float, areaB: float) -> tuple:
        """ 计算交点 """
        return areaA / (areaA - areaB) * (segline1[1][0] - segline1[0][0]) + segline1[0][0],\
               areaA / (areaA - areaB) * (segline1[1][1] - segline1[0][1]) + segline1[0][1]

    def calcCommonLine(segline1: tuple, segline2: tuple) -> tuple:
        """ 处理共线的情况
        :returns: 返回值与父函数相同
        """
        # 平行于y轴则比较y坐标，否则比较x坐标
        did = 1 if floatEq(segline1[0][0], segline1[1][0], abs_tol=geoTol) else 0
        if segline1[0][did] > segline1[1][did]:
            segline1 = (segline1[1], segline1[0])
        if segline2[0][did] > segline2[1][did]:
            segline2 = (segline2[1], segline2[0])
        leftPt = segline1[0] if segline1[0][did] >= segline2[0][did] else segline2[0]
        rightPt = segline1[1] if segline1[1][did] <= segline2[1][did] else segline2[1]
        compareResult = floatCompare(leftPt[did], rightPt[did], abs_tol=geoTol)
        if compareResult > 0:
            return (), ()
        elif compareResult == 0:
            return (leftPt,), ()
        return (), ((leftPt, rightPt),)

    # 设segline1为线段AB，segline2为线段CD
    lengthAB, lengthCD = seglineLength(segline1), seglineLength(segline2)
    tolAB, tolCD = geoTol * lengthCD, geoTol * lengthAB  # 分别用于areaA、areaB|areaC、areaD的误差范围
    if lengthAB <= geoTol:
        if lengthCD <= geoTol:  # 点-点
            if ptEq(segline1[0], segline2[0]):
                return (segline1[0],), ()
            return (), ()
        else:  # 点-线
            if seglineRelationWithPt(segline2, segline1[0], isLine2) == RelationType.On:
                return (segline1[0]), ()
            return (), ()
    else:
        if lengthCD <= geoTol:  # 线-点
            if seglineRelationWithPt(segline1, segline2[0], isLine1) == RelationType.On:
                return (segline2[0]), ()
            return (), ()
    # 线-线
    areaA = calcArea2(segline2[0], segline2[1], segline1[0])
    areaB = calcArea2(segline2[0], segline2[1], segline1[1])
    areaC = calcArea2(segline1[0], segline1[1], segline2[0])
    areaD = calcArea2(segline1[0], segline1[1], segline2[1])
    if isLine1:
        if isLine2:
            if floatEq(areaA, areaB, abs_tol=tolAB):
                if floatEq(areaA, 0, abs_tol=tolAB):  # 重合
                    return (), (segline1,)
                else:  # 平行
                    return (), ()
            return (calcCrossPt(areaA, areaB),), ()
        else:
            if floatEq(areaC, 0, abs_tol=tolCD):
                if floatEq(areaD, 0, abs_tol=tolCD):  # 重合
                    return (), (segline2,)
                else:  # 交于C点
                    return (segline2[0],), ()
            elif floatEq(areaD, 0, abs_tol=tolCD):  # 交于D点
                return (segline2[1],), ()
            if (areaC < 0 and areaD < 0) or (areaC > 0 and areaD > 0):  # 不相交
                return (), ()
            return (calcCrossPt(areaA, areaB),), ()
    else:
        if isLine2:
            if floatEq(areaA, 0, abs_tol=tolAB):
                if floatEq(areaB, 0, abs_tol=tolAB):  # 重合
                    return (), (segline1,)
                else:  # 交于A点
                    return (segline1[0],), ()
            elif floatEq(areaB, 0, abs_tol=tolAB):  # 交于B点
                return (segline1[1],), ()
            if (areaA < 0 and areaB < 0) or (areaA > 0 and areaB > 0):  # 不相交
                return (), ()
            return (calcCrossPt(areaA, areaB),), ()
        else:
            # 包围盒检测
            if floatGr(min(segline1[0][0], segline1[1][0]), max(segline2[0][0], segline2[1][0]), abs_tol=geoTol) or\
               floatLe(max(segline1[0][0], segline1[1][0]), min(segline2[0][0], segline2[1][0]), abs_tol=geoTol) or \
               floatGr(min(segline1[0][1], segline1[1][1]), max(segline2[0][1], segline2[1][1]), abs_tol=geoTol) or \
               floatLe(max(segline1[0][1], segline1[1][1]), min(segline2[0][1], segline2[1][1]), abs_tol=geoTol):
                return (), ()
            # 跨立实验
            areaAResult = floatCompare(areaA, 0, abs_tol=tolAB)
            areaBResult = floatCompare(areaB, 0, abs_tol=tolAB)
            areaCResult = floatCompare(areaC, 0, abs_tol=tolCD)
            areaDResult = floatCompare(areaD, 0, abs_tol=tolCD)
            if (areaAResult < 0 and areaBResult < 0) or (areaAResult > 0 and areaBResult > 0) or\
               (areaCResult < 0 and areaDResult < 0) or (areaCResult > 0 and areaDResult > 0):  # 不相交
                return (), ()

            if areaAResult == 0 and areaBResult == 0:  # 共线
                return calcCommonLine(segline1, segline2)
            return (calcCrossPt(areaA, areaB),), ()


def seglineTranslate(segline: tuple, transVec: tuple) -> tuple:
    """ 平移 """
    return ptTranslate(segline[0], transVec), ptTranslate(segline[1], transVec)


def seglineRotate(segline: tuple, radian: float, center: tuple=ptZero) -> tuple:
    """ 旋转（逆时针）
    :param radian: 旋转弧度
    :param center: 旋转中心
    """
    return ptRotate(segline[0], radian, center), ptRotate(segline[1], radian, center)


def seglineScale(segline: tuple, xRate: float, yRate: float, center: tuple=ptZero) -> tuple:
    """ 缩放 """
    return ptScale(segline[0], xRate, yRate, center), ptScale(segline[1], xRate, yRate, center)


def seglineReflect(segline: tuple, axis) -> tuple:
    """ 镜像
    :param axis: 传入直线表示镜像轴，可以用tuple表示直线，也可以是以下字符串值：
                 "x":以x轴为镜像轴; "y":以y轴为镜像轴; "y=x":以直线y=x为镜像轴; "y=-x":以直线y=-x为镜像轴
    """
    return ptReflect(segline[0], axis), ptReflect(segline[1], axis)


def seglineStretch(segline: tuple, length: float, type_: int=0) -> tuple:
    """ 将直线段拉伸至长度length
    :param type_: 拉伸方式 0:固定起点; 1:固定终点; 2:固定中点
    """
    if ptEq(segline[0], segline[1]):
        return segline
    resultVec = vecStretch(seglineVec(segline), length)  # 拉伸后线段对应的向量
    if type_ == 0:
        return segline[0], ptTranslate(segline[0], resultVec)
    elif type_ == 1:
        return ptTranslate(segline[1], vecNeg(resultVec)), segline[1]
    else:
        midP = seglineMidPoint(segline)
        resultVec = vecScale(resultVec, 0.5, 0.5)
        return ptTranslate(midP, vecNeg(resultVec)), ptTranslate(midP, resultVec)

# endregion


# region 直线

"""
直线用tuple表示，3个元素分别为a,b,c，表示直线ax+by+c=0
"""

def createLine(**kw) -> tuple:
    """ 创建直线
    :param kw: 需提供直线上任意一段长度>0的直线段segline(tuple)
    :raises ValueError: 参数错误
    """
    if 'segline' in kw:
        segline = kw['segline']
        a = segline[1][1] - segline[0][1]
        b = segline[0][0] - segline[1][0]
        c = segline[1][0] * segline[0][1] - segline[0][0] * segline[1][1]
        return a, b, c
    raise ValueError('[Error] createLine: 参数错误')


def lineProjection(line: tuple, p: tuple) -> tuple:
    """ 返回点p到直线的垂足（投影）
    :raises ValueError: 参数错误
    """
    if floatEq(line[0], 0):
        if floatEq(line[1], 0):
            raise ValueError('[Error] lineProjection: 参数错误')
        return p[0], -line[2] / line[1]  # 平行于x轴
    if floatEq(line[1], 0):  # 平行于y轴
        return -line[2] / line[0], p[1]
    x = (line[1] ** 2 * p[0] - line[0] * line[1] * p[1] - line[0] * line[2]) / (line[0] ** 2 + line[1] ** 2)
    y = -(line[0] * x + line[2]) / line[1]
    return x, y

# endregion


# region 圆弧

"""
圆弧用tuple表示
第1项为圆心，第2项为半径
第3项是起始弧度，用float表示，取值范围为[0, pi*2)，起始弧度为0时起点在圆心右侧（x轴正方向）
第4项是弧度范围宽度，用float表示，正/负数为逆/顺时针
"""

def createArc(**kw) -> tuple:
    """ 创建圆弧
    :param kw: 可以提供以下参数组合
               1. circle(tuple)，创建圆对应的圆弧
                  可以额外提供参数clockwise(bool)以表示方向，不提供默认为逆时针
    :raises ValueError: 参数错误
    """
    if 'circle' in kw:
        circle = kw['circle']
        clockwise = kw.get('clockwise', False)
        return circle[0], circle[1], 0, -pyUtils.doublePi if clockwise else pyUtils.doublePi
    raise ValueError('[Error] createArc: 参数错误')


def arcToStr(arc: tuple) -> str:
   """ 圆弧转字符串 """
   return f'({ptToStr(arc[0])}, {arc[1]}, {arc[2]}, {arc[3]})'


def strToArc(string: str) -> tuple:
    """ 字符串转圆弧 """
    numberStrs = _strToNumberStrs(string)
    return (float(numberStrs[0]), float(numberStrs[1])),\
        float(numberStrs[2]), float(numberStrs[3]), float(numberStrs[4])

# endregion


# region 贝塞尔曲线段

"""
三次贝塞尔曲线段用tuple表示，4个元素分别是四个控制点
"""

def createBezier(**kw) -> tuple:
    """ 创建贝塞尔曲线段
    :param kw: 需提供线段segline(tuple)，创建等同于直线段的贝塞尔曲线段
    :raises ValueError: 参数错误
    """
    if 'segline' in kw:
        segline = kw['segline']
        vec = vecTruediv(seglineVec(segline), 3)
        return segline[0], ptTranslate(segline[0], vec), ptTranslate(segline[1], vecNeg(vec)), segline[1]
    raise ValueError('[Error] createBezier: 参数错误')


def bezierToStr(bezier: tuple) -> str:
    """ 贝塞尔曲线段转字符串 """
    return f'({ptToStr(bezier[0])}, {ptToStr(bezier[1])}, {ptToStr(bezier[2])}, {ptToStr(bezier[3])})'


def strToBezier(string: str) -> tuple:
    """ 字符串转贝塞尔曲线段 """
    numberStrs = _strToNumberStrs(string)
    return float(numberStrs[0]), float(numberStrs[1]), float(numberStrs[2]), float(numberStrs[3])


def bezierAabb(bezier: tuple) -> tuple:
    """ 返回贝塞尔曲线段aabb包围盒 """
    def calcRange(axis: int) -> tuple:
        """ 计算坐标方向上的包围盒范围 """
        a = -bezier[0][axis] + bezier[1][axis] * 3 - bezier[2][axis] * 3 + bezier[3][axis]
        b = (bezier[0][axis] - bezier[1][axis] * 2 + bezier[2][axis]) * 2
        c = -bezier[0][axis] + bezier[1][axis]
        params = pyUtils.solveQuadraticEquation(a, b, c)
        candidateValues = [bezier[0][axis], bezier[3][axis]]  # 包围盒可能的边界值列表
        for param in params:
            if floatBetween(0, 1, param):
                candidateValues.append(bezierPointByParam(bezier, param)[axis])
        return min(candidateValues), max(candidateValues)
    
    return calcRange(0) + calcRange(1)


def bezierIsSegline(bezier: tuple) -> bool:
    """ 返回贝塞尔曲线段是否直线段 """
    return floatEq(polygonArea([bezier[0], bezier[1], bezier[2]]), 0, abs_tol=geoTol) and\
           floatEq(polygonArea([bezier[1], bezier[2], bezier[3]]), 0, abs_tol=geoTol)


def bezierLength(bezier: tuple, step: float) -> float:
    """ 返回贝塞尔曲线段的长度
    :param step: 采样步长
    """
    return polylineLength(bezierSample(bezier, step=step))


def bezierPointByParam(bezier: tuple, param: float) -> tuple:
    """ 返回贝塞尔曲线段在参数param位置的点 """
    p_1 = 1 - param
    param0 = p_1 ** 3
    param1 = param * p_1 ** 2
    param2 = param ** 2 * p_1
    param3 = param ** 3
    return bezier[0][0] * param0 + (bezier[1][0] * param1 + bezier[2][0] * param2) * 3 + bezier[3][0] * param3,\
           bezier[0][1] * param0 + (bezier[1][1] * param1 + bezier[2][1] * param2) * 3 + bezier[3][1] * param3


def bezierParamByPoint(bezier: tuple, pt: tuple):
    """ 返回点在贝塞尔曲线段上的参数（要求点在曲线段上，如果不在返回None） """
    a = bezier[3][0] - 3 * (bezier[2][0] - bezier[1][0]) - bezier[0][0]
    b = 3 * (bezier[2][0] - 2 * bezier[1][0] + bezier[0][0])
    c = 3 * (bezier[1][0] - bezier[0][0])
    d = bezier[0][0] - pt[0]
    roots = pyUtils.solveCubicEquation(a, b, c, d, False)
    for root in roots:
        if floatBetween(root, 0, 1) and floatEq(pt[1], bezierPointByParam(bezier, root)[1], abs_tol=geoTol):
            return root
    return None


def bezierTangentVec(bezier: tuple, param: float) -> tuple:
    """ 返回贝塞尔曲线段在参数param位置的切向量 """
    return (((-bezier[0][0] + bezier[1][0] * 3 - bezier[2][0] * 3 + bezier[3][0]) * param ** 2 +
            (bezier[0][0] * 2 - bezier[1][0] * 4 + bezier[2][0] * 2) * param - bezier[0][0] + bezier[1][0]) * 3,
            ((-bezier[0][1] + bezier[1][1] * 3 - bezier[2][1] * 3 + bezier[3][1]) * param ** 2 +
            (bezier[0][1] * 2 - bezier[1][1] * 4 + bezier[2][1] * 2) * param - bezier[0][1] + bezier[1][1]) * 3)


def bezierSample(bezier: tuple, **kw) -> list:
    """ 返回贝塞尔曲线段的采样点列表（多段线）
    :param kw: 允许的参数组包括
               1. step: float 采样参数步长，取值范围为(0, 1]
               2. count: int 采样点数量，取值范围为[2, +∞)
    :raises ValueError: 参数错误
    """
    if 'step' in kw:
        count = math.ceil(1 / kw['step'])
    elif 'count' in kw:
        count = kw['count'] - 1
    else:
        raise ValueError('[Error] bezierSample: 参数错误')
    step = 1 / count
    param = step
    result = [bezier[0]]
    for _ in range(count - 1):
        result.append(bezierPointByParam(bezier, param))
        param += step
    result.append(bezier[3])
    return result


def bezierCrossWithSegline(bezier: tuple, segline: tuple, isLine: bool=False) -> tuple:
    """ 返回贝塞尔曲线段与直线段|直线的交点
    :param isLine: 是否将segline视为直线段所在的直线
    :returns: ((交点), (交线段))
    """
    if bezierIsSegline(bezier):
        # todo
        return NotImplemented

    # 将segline旋转平移至与x轴重合
    rotateRadian = -vecAngleTo((1, 0), seglineVec(segline))
    bezier2 = bezierTranslate(bezierRotate(bezier, rotateRadian), (0, -ptRotate(segline[0], rotateRadian)[1]))
    a = bezier2[3][1] - 3 * (bezier2[2][1] - bezier2[1][1]) - bezier2[0][1]
    b = 3 * (bezier2[2][1] - 2 * bezier2[1][1] + bezier2[0][1])
    c = 3 * (bezier2[1][1] - bezier2[0][1])
    d = bezier2[0][1]
    roots = pyUtils.solveCubicEquation(a, b, c, d, False)
    result = []
    for root in roots:
        crossPt = bezierPointByParam(bezier, root)
        if isLine or floatBetween(0, 1, seglineParamByPoint(segline, crossPt)):
            result.append(crossPt)
    return tuple(result), ()


def bezierReverse(bezier: tuple) -> tuple:
    """ 逆向 """
    return bezier[3], bezier[2], bezier[1], bezier[0]


def bezierTranslate(bezier: tuple, transVec: tuple):
    """ 平移 """
    return ptTranslate(bezier[0], transVec), ptTranslate(bezier[1], transVec),\
           ptTranslate(bezier[2], transVec), ptTranslate(bezier[3], transVec)


def bezierRotate(bezier: tuple, radian: float, center: tuple=ptZero) -> tuple:
    """ 旋转（逆时针）
    :param radian: 旋转弧度
    :param center: 旋转中心
    """
    return ptRotate(bezier[0], radian, center), ptRotate(bezier[1], radian, center),\
           ptRotate(bezier[2], radian, center), ptRotate(bezier[3], radian, center)


def bezierScale(bezier: tuple, xRate: float, yRate: float, center: tuple=ptZero) -> tuple:
    """ 缩放（以零点为中心） """
    return ptScale(bezier[0], xRate, yRate, center), ptScale(bezier[1], xRate, yRate, center),\
           ptScale(bezier[2], xRate, yRate, center), ptScale(bezier[3], xRate, yRate, center)


def bezierReflect(bezier: tuple, axis) -> tuple:
    """ 镜像
    :param axis: 传入直线表示镜像轴，可以用tuple表示直线，也可以是以下字符串值：
                 "x":以x轴为镜像轴; "y":以y轴为镜像轴; "y=x":以直线y=x为镜像轴; "y=-x":以直线y=-x为镜像轴
    """
    return ptReflect(bezier[0], axis), ptReflect(bezier[1], axis),\
           ptReflect(bezier[2], axis), ptReflect(bezier[3], axis)

# endregion


# region 路径段

"""
路径段用tuple表示，第一项表示路径段类型（SegPathType），第二项为对应的直线段、椭圆弧或三次贝塞尔曲线段
"""

class SegPathType(enum.Enum):
    """ 路径段类型 """
    Segline = 0  # 直线段
    Arc = 1  # 圆弧
    Bezier = 2  # 三次贝塞尔曲线段


def segPathToStr(segPath: tuple) -> str:
    """ 路径段转字符串 """
    if segPath[0] == SegPathType.Segline:
        return f'{segPath[0].value} {seglineToStr(segPath[1])}'
    elif segPath[0] == SegPathType.Arc:
        return f'{segPath[0].value} {arcToStr(segPath[1])}'
    else:
        return f'{segPath[0].value} {bezierToStr(segPath[1])}'


def _numberStrsToSegPath(numberStrs: list) -> tuple:
    """ [数字字符串]转路径段 """
    segType = SegPathType(int(numberStrs[0]))
    if segType == SegPathType.Segline:
        return segType, ((float(numberStrs[1]), float(numberStrs[2])), (float(numberStrs[3]), float(numberStrs[4])))
    elif segType == SegPathType.Arc:
        return segType, ((float(numberStrs[1]), float(numberStrs[2])),
            float(numberStrs[3]), float(numberStrs[4]), float(numberStrs[5]))
    else:
        return segType, ((float(numberStrs[1]), float(numberStrs[2])), (float(numberStrs[3]), float(numberStrs[4])),
                         (float(numberStrs[5]), float(numberStrs[6])), (float(numberStrs[7]), float(numberStrs[8])))


def strToSegPath(string: str) -> tuple:
    """ 字符串转路径段 """
    numberStrs = _strToNumberStrs(string)
    return _numberStrsToSegPath(numberStrs)


def segPathAabb(segPath: tuple) -> tuple:
    """ 返回路径段包围盒 """
    if segPath[0] == SegPathType.Segline:
        return seglineAabb(segPath[1])
    elif segPath[0] == SegPathType.Arc:
        return NotImplemented
    else:
        return bezierAabb(segPath[1])


def segPathStartPt(segPath: tuple) -> tuple:
    """ 返回路径段起点 """
    if segPath[0] == SegPathType.Arc:
        return NotImplemented
    else:
        return segPath[1][0]


def segPathEndPt(segPath: tuple) -> tuple:
    """ 返回路径段终点 """
    if segPath[0] == SegPathType.Segline:
        return segPath[1][1]
    elif segPath[0] == SegPathType.Arc:
        return NotImplemented
    else:
        return segPath[1][3]


def segPathIsSegline(segPath: tuple) -> bool:
    """ 返回路径段是否直线段或用贝塞尔表示的直线段 """
    if segPath[0] == SegPathType.Segline:
        return True
    if segPath[0] == SegPathType.Bezier:
        return bezierIsSegline(segPath[1])
    return False


def segPathPointByParam(segPath: tuple, param: float) -> tuple:
    """ 返回路径段上参数param位置的点 """
    if segPath[0] == SegPathType.Segline:
        return seglinePointByParam(segPath[1], param)
    elif segPath[1] == SegPathType.Arc:
        return NotImplemented
    else:
        return bezierPointByParam(segPath[1], param)


def segPathReverse(segPath: tuple) -> tuple:
    """ 逆向 """
    if segPath[0] == SegPathType.Segline:
        return SegPathType.Segline, (segPath[1][1], segPath[1][0])
    elif segPath[0] == SegPathType.Arc:
        return NotImplemented
    else:
        return SegPathType.Bezier, bezierReverse(segPath[1])


def segPathTranslate(segPath: tuple, transVec: tuple) -> tuple:
    """ 平移 """
    if segPath[0] == SegPathType.Segline:
        return SegPathType.Segline, seglineTranslate(segPath[1], transVec)
    elif segPath[0] == SegPathType.Arc:
        return NotImplemented
    else:
        return SegPathType.Bezier, bezierTranslate(segPath[1], transVec)


def segPathRotate(segPath: tuple, radian: float, center: tuple=ptZero) -> tuple:
    """ 旋转（逆时针）
    :param radian: 旋转弧度
    :param center: 旋转中心
    """
    if segPath[0] == SegPathType.Segline:
        return SegPathType.Segline, seglineRotate(segPath[1], radian, center)
    elif segPath[0] == SegPathType.Arc:
        return NotImplemented
    else:
        return SegPathType.Bezier, bezierRotate(segPath[1], radian, center)


def segPathScale(segPath: list, xRate: float, yRate: float, center: tuple=ptZero) -> tuple:
    """ 缩放（以零点为中心） """
    if segPath[0] == SegPathType.Segline:
        return SegPathType.Segline, seglineScale(segPath[1], xRate, yRate, center)
    elif segPath[0] == SegPathType.Arc:
        return NotImplemented
    else:
        return SegPathType.Bezier, bezierScale(segPath[1], xRate, yRate, center)


def segPathReflect(segPath: list, axis) -> tuple:
    """ 镜像
    :param axis: 传入直线表示镜像轴，可以用tuple表示直线，也可以是以下字符串值：
                 "x":以x轴为镜像轴; "y":以y轴为镜像轴; "y=x":以直线y=x为镜像轴; "y=-x":以直线y=-x为镜像轴
    """
    if segPath[0] == SegPathType.Segline:
        return SegPathType.Segline, seglineReflect(segPath[1], axis)
    elif segPath[0] == SegPathType.Arc:
        return NotImplemented
    else:
        return SegPathType.Bezier, bezierReflect(segPath[1], axis)

# endregion


# region 多段线

"""
多段线用list表示，每一项都是点
有时可以视为封闭多边形
"""

def polylineToStr(polyline: list) -> str:
    """ 多段线转字符串 """
    pointStrs = [ptToStr(point) for point in polyline]
    return f'({", ".join(pointStrs)})'


def strToPolyline(string: str) -> list:
    """ 字符串转多段线 """
    numberStrs = _strToNumberStrs(string)
    return [(float(numberStrs[i]), float(numberStrs[i+1])) for i in range(0, len(numberStrs), 2)]


def createPolyline(**kw) -> list:
    """ 创建多段线
    :param kw: 需提供以下参数组合之一
               1. 直线段segline(tuple)，创建等同于直线段的多段线
               2. 矩形aabb(tuple)，创建等同于矩形的多段线
                  可以额外提供参数clockwise(bool)以表示方向，不提供默认为逆时针
    :raises ValueError: 参数错误
    """
    if 'segline' in kw:
        segline = kw['segline']
        return [segline]
    if 'aabb' in kw:
        aabb = kw['aabb']
        clockwise = kw.get('clockwise', False)
        if clockwise:
            return [(aabb[1], aabb[3]), (aabb[1], aabb[2]), (aabb[0], aabb[2]), (aabb[0], aabb[3]), (aabb[1], aabb[3])]
        return [(aabb[1], aabb[3]), (aabb[0], aabb[3]), (aabb[0], aabb[2]), (aabb[1], aabb[2]), (aabb[1], aabb[3])]
    raise ValueError('[Error] createPolyline: 参数错误')


def polylineClone(polyline: list) -> list:
    """ 拷贝多段线 """
    result = []
    result.extend(polyline)
    return result


def polylineRound(polyline: list, precision: int=0, inplace: bool=True) -> list:
    """ 舍入至小数点后precision位，银行家舍入法 """
    result = polyline if inplace else polyline[:]
    for i in range(len(result)):
        result[i] = ptRound(result[i], precision)
    return result


def polylineAabb(polyline: list) -> tuple:
    """ 返回多段线包围盒 """
    if len(polyline) == 0:
        return emptyAabb
    result = emptyAabb
    for p in polyline:
        result = aabbExpandByPt(result, p)
    return result


def polylineLength(polyline: list) -> float:
    """ 返回多段线总长度 """
    result = 0
    for i in range(len(polyline) - 1):
        result += ptDistanceTo(polyline[i], polyline[i + 1])
    return result


def poylineDistanceTo(polyline: list, p: tuple) -> float:
    """ 返回点p到多段线的最短距离
    :raises ValueError: 多段线为空
    """
    length = len(polyline)
    if length == 0:
        raise ValueError('[Error] poylineDistanceTo: 多段线为空')
    if length == 1:
        return ptDistanceTo(polyline[0], p)
    else:
        result = seglineDistanceTo((polyline[0], polyline[1]), p, False)
        for i in range(1, length - 1):
            result = min(result, seglineDistanceTo((polyline[i], polyline[i+1]), p, False))
        return result


def polylineReverse(polyline: list, inplace: bool=True) -> list:
    """ 逆向 """
    result = polyline if inplace else polyline[:]
    length = len(polyline)
    for i in range(length // 2):
        result[i], result[length - 1 - i] = result[length - 1 - i],  result[i]
    return result


def polylineTranslate(polyline: list, transVec: tuple, inplace: bool=True) -> list:
    """ 平移 """
    result = polyline if inplace else polyline[:]
    for i in range(len(result)):
        result[i] = ptTranslate(result[i], transVec)
    return result
    

def polylineRotate(polyline: list, radian: float, center: tuple=ptZero, inplace: bool=True) -> list:
    """ 旋转（逆时针）
    :param radian: 旋转弧度
    :param center: 旋转中心
    """
    result = polyline if inplace else polyline[:]
    for i in range(len(result)):
        result[i] = ptRotate(result[i], radian, center)
    return result


def polylineScale(polyline: list, xRate: float, yRate: float, center: tuple=ptZero, inplace: bool=True) -> list:
    """ 缩放（以零点为中心） """
    result = polyline if inplace else polyline[:]
    for i in range(len(result)):
        result[i] = ptScale(result[i], xRate, yRate, center)
    return result


def polylineReflect(polyline: list, axis, inplace: bool=True) -> list:
    """ 镜像
    :param axis: 传入直线表示镜像轴，可以用tuple表示直线，也可以是以下字符串值：
                 "x":以x轴为镜像轴; "y":以y轴为镜像轴; "y=x":以直线y=x为镜像轴; "y=-x":以直线y=-x为镜像轴
    """
    result = polyline if inplace else polyline[:]
    for i in range(len(result)):
        result[i] = ptReflect(result[i], axis)
    return result


def polylineRemoveAdjacentPt(polyline: list, tol: float, inplace: bool=True) -> list:
    """ 去除相邻的临近点（首尾点不变）
    :param tol: 阈值，<=此距离的相邻点将被去除
    """
    resultPoly = [] if len(polyline) == 0 else [polyline[0]]  # 简化结果
    for i in range(1, len(polyline)):
        if not ptCloseTo(resultPoly[-1], polyline[i], tol):
            resultPoly.append(polyline[i])

    if inplace:
        polyline[:] = resultPoly
        return polyline
    return resultPoly


def polylineConHeadTail(polyline: list, inplace: bool=True) -> list:
    """ 连接首尾点 """
    result = polyline if inplace else polyline[:]
    if len(result) >= 2 and not ptEq(result[0], result[-1]):
        result.append(result[0])
    return result


def polylineSimplifyByDP(polyline: list, tol: float, inplace: bool=True) -> list:
    """ 通过Douglas–Peucker算法简化多段线
    :param tol: 阈值
    """
    def DoSimplify(startId: int, endId: int) -> int:
        """ 在polyline[startId, endId)范围内做简化
        :returns: 如果能简化返回startId，如果不能简化返回分裂点下标
        """
        segline = (polyline[startId], polyline[endId - 1])  # 简化后的线段
        dists = [seglineDistanceTo(segline, polyline[i], False) for i in range(startId + 1, endId - 1)]  # 距离列表
        maxDist, maxDistId = -1, -1
        for i in range(len(dists)):
            if dists[i] > maxDist:
                maxDist, maxDistId = dists[i], startId + 1 + i
        return maxDistId if maxDist >= tol else startId

    resultPoly = [] if len(polyline) == 0 else [polyline[0]]  # 简化结果
    if len(polyline) >= 2:
        simplifyRanges = [(0, len(polyline))]  # 待简化范围列表（栈）
        while len(simplifyRanges) > 0:
            curRange = simplifyRanges.pop()
            splitId = DoSimplify(*curRange)
            if splitId == curRange[0]:  # 可以简化
                resultPoly.append(polyline[curRange[1] - 1])
            else:  # 分裂，递归简化
                simplifyRanges.append((splitId, curRange[1]))
                simplifyRanges.append((curRange[0], splitId + 1))

    if inplace:
        polyline[:] = resultPoly
        return polyline
    return resultPoly


def polylineConvexHull(polyline: list) -> list:
    """ 多段线凸包
    :returns: 多段线少于2个点时凸包为原多段线，凸包为一条线时该线会折返形成封闭图形，凸包会去除连续重合顶点（首尾点除外）
    """
    if len(polyline) <= 1:
        return polyline[:]
    # 寻找左下点
    bottomLeftPt, bottomLeftId = polyline[0], 0
    for i, pt in enumerate(polyline):
        if ptCompareByYX(pt, bottomLeftPt) < 0:
            bottomLeftPt, bottomLeftId = pt, i
    # 按角度排序
    ptRadianDists = []
    for i, pt in enumerate(polyline):
        if i == bottomLeftId:
            continue
        radian = 0 if ptEq(pt, bottomLeftPt) else vecAngle(ptVec(bottomLeftPt, pt))
        ptRadianDists.append((pt, radian, ptDistanceTo(bottomLeftPt, pt)))
    ptRadianDists.sort(key=lambda x: (x[1], x[2]))
    ptRadianDists.append((bottomLeftPt, 0, 0))
    # 扫描
    result = [bottomLeftPt, ptRadianDists[0][0]]
    i = 1
    while i < len(ptRadianDists):
        if floatGrEq(polygonArea([result[-2], result[-1], ptRadianDists[i][0]]), 0, geoTol):
            if not ptEq(ptRadianDists[i][0], result[-1]):
                result.append(ptRadianDists[i][0])
            i += 1
        else:
            result.pop()
    return result


def polygonIsSame(polygon1: list, polygon2: list) -> bool:
    """ 判断两个多边形（首尾相连）是否相同
        判断标准：节点数相同且节点位置相同，起点可以不同
    """

    def checkSame(id1: int) -> bool:
        """ 从polygon1[id1]、polygon2[0]开始检查多边形是否相同 """
        maxId = len(polygon1) - 2
        curId1, curId2 = id1, 0
        while True:
            if not ptEq(polygon1[curId1], polygon2[curId2]):
                return False
            curId1 = curId1 + 1 if curId1 != maxId else 0
            curId2 = curId2 + 1 if curId2 != maxId else 0
            if curId1 == id1:
                break
        return True

    len1, len2 = len(polygon1), len(polygon2)
    if len1 != len2:
        return False
    if len1 == 0:
        return True
    elif len1 == 1:
        return ptEq(polygon1[0], polygon2[0])

    for i in range(len1 - 1):
        if ptEq(polygon2[0], polygon1[i]) and checkSame(i):
            return True
    return False


def polygonArea(polygon: list, isPositive: bool=False) -> float:
    """ 返回多边形面积
    :param polygon: 多边形，首尾会视为相连
    :param isPositive: 是否转为非负数（即是否无视时针方向）（逆时针为正面积）
    """
    if len(polygon) <= 2:
        return 0
    result = 0
    for i in range(len(polygon) - 1):
        result += (polygon[i][0] * polygon[i+1][1] - polygon[i+1][0] * polygon[i][1])
    result += (polygon[-1][0] * polygon[0][1] - polygon[0][0] * polygon[-1][1])
    return abs(result * 0.5) if isPositive else result * 0.5


def polygonClockwise(polygon: list):
    """ 返回多边形的时针方向
    :param polygon: 多边形，首尾会视为相连
    :returns: True:顺时针; False:逆时针; None:无法判断时针方向
    """
    area = polygonArea(polygon)
    if floatGr(area, 0, abs_tol=geoTol):
        return False
    elif floatLe(area, 0, abs_tol=geoTol):
        return True
    return None


def polygonSetClockwise(polygon: list, clockwise: bool, inplace: bool=True) -> list:
    """ 设置多边形的时针方向
    :param polygon: 多边形，首尾会视为相连
    """
    oriClockwise = polygonClockwise(polygon)
    if oriClockwise is None or oriClockwise == clockwise:
        exit(polygon if inplace else polygon[:])
    resultPoly = polygon[::-1]
    if inplace:
        polygon[:] = resultPoly
        return polygon
    return resultPoly


def polygonRelationWithPt(polygon: list, p: tuple) -> RelationType:
    """ 判断多边形（不自交）与点p的位置关系
    :param polygon: 多边形，首尾会视为相连
    :returns: 可能的返回值：On、In、Out（内外与多边形时针方向无关）
    """
    def calcUpDownByY(y: float) -> RelationType:
        """ 根据y坐标判断与点p的上下关系 """
        cmpResult = floatCompare(y, p[1], abs_tol=geoTol)
        if cmpResult < 0:
            return RelationType.Down
        elif cmpResult > 0:
            return RelationType.Up
        else:
            return RelationType.On

    # 判断组成多边形的众线段在点p左侧经过几次（线段下侧与p齐平不算经过）
    if not polygon:
        return RelationType.Out
    polygon.append(polygon[0])
    try:
        leftCount = 0
        lastPt, lastRel = polygon[0], calcUpDownByY(polygon[0][1])
        for i in range(1, len(polygon)):
            curPt = polygon[i]
            curRel = calcUpDownByY(curPt[1])
            if curRel == lastRel:
                if curRel == RelationType.On:  # 水平且与p齐平
                    left, right = min(curPt[0], lastPt[0]), max(curPt[0], lastPt[0])
                    if floatLeEq(left, p[0], abs_tol=geoTol) and floatLeEq(p[0], right, abs_tol=geoTol):
                        return RelationType.On
            else:
                if not((lastRel == RelationType.On and lastPt[1] < curPt[1]) or  # 线段下侧不与p齐平
                       (curRel == RelationType.On and curPt[1] < lastPt[1])):
                    cmpResult = floatCompare(seglineXByY((lastPt, curPt), p[1]), p[0], abs_tol=geoTol)
                    if cmpResult < 0:
                        leftCount += 1
                    elif cmpResult == 0:
                        return RelationType.On
            lastPt, lastRel = curPt, curRel
        return RelationType.In if leftCount % 2 else RelationType.Out
    finally:
        polygon.pop()

# endregion


# region 路径

"""
路径用list表示，每一项都是路径段，且相邻路径段相连
有时可以视为封闭路径
"""

def createPath(**kw) -> list:
    """ 创建路径
    :param kw: 需提供以下参数组合之一
               1. 直线段segline(tuple)，创建等同于直线段的路径
               2. 多段线polyline(list)，创建等同于多段线的路径
               3. 矩形aabb(tuple)，创建等同于矩形的路径
               4. 椭圆ellipse(tuple)，创建用贝塞尔拟合的椭圆
               组合1、2、3可以额外提供参数toBezier(bool)表示是否用贝塞尔拟合，不提供默认为False
               组合3、4可以额外提供参数clockwise(bool)以表示方向，不提供默认为逆时针
    :raises ValueError: 参数错误
    """
    toBezier = kw.get('toBezier', False)  # 是否用贝塞尔拟合
    if 'segline' in kw:
        segline = kw['segline']
        if toBezier:
            return [(SegPathType.Bezier, createBezier(segline=segline))]
        else:
            return [(SegPathType.Segline, segline)]
    if 'polyline' in kw:
        polyline = kw['polyline']
        if len(polyline) == 0:
            return []
        if toBezier:
            if len(polyline) == 1:
                return [(SegPathType.Bezier, (polyline[0], polyline[0], polyline[0], polyline[0]))]
            return [(SegPathType.Bezier, createBezier(segline=(polyline[i], polyline[i+1])))
                   for i in range(len(polyline) - 1)]
        else:
            if len(polyline) == 1:
                return [(SegPathType.Segline, (polyline[0], polyline[0]))]
            return [(SegPathType.Segline, (polyline[i], polyline[i+1])) for i in range(len(polyline) - 1)]
    elif 'aabb' in kw:
        aabb = kw['aabb']
        clockwise = kw.get('clockwise', False)
        if toBezier:
            if clockwise:
                return [
                    (SegPathType.Bezier, createBezier(segline=((aabb[1], aabb[3]), (aabb[1], aabb[2])))),
                    (SegPathType.Bezier, createBezier(segline=((aabb[1], aabb[2]), (aabb[0], aabb[2])))),
                    (SegPathType.Bezier, createBezier(segline=((aabb[0], aabb[2]), (aabb[0], aabb[3])))),
                    (SegPathType.Bezier, createBezier(segline=((aabb[0], aabb[3]), (aabb[1], aabb[3]))))
                ]
            return [
                (SegPathType.Bezier, createBezier(segline=((aabb[1], aabb[3]), (aabb[0], aabb[3])))),
                (SegPathType.Bezier, createBezier(segline=((aabb[0], aabb[3]), (aabb[0], aabb[2])))),
                (SegPathType.Bezier, createBezier(segline=((aabb[0], aabb[2]), (aabb[1], aabb[2])))),
                (SegPathType.Bezier, createBezier(segline=((aabb[1], aabb[2]), (aabb[1], aabb[3]))))
            ]
        else:
            if clockwise:
                return [
                    (SegPathType.Segline, ((aabb[1], aabb[3]), (aabb[1], aabb[2]))),
                    (SegPathType.Segline, ((aabb[1], aabb[2]), (aabb[0], aabb[2]))),
                    (SegPathType.Segline, ((aabb[0], aabb[2]), (aabb[0], aabb[3]))),
                    (SegPathType.Segline, ((aabb[0], aabb[3]), (aabb[1], aabb[3])))
                ]
            return [
                (SegPathType.Segline, ((aabb[1], aabb[3]), (aabb[0], aabb[3]))),
                (SegPathType.Segline, ((aabb[0], aabb[3]), (aabb[0], aabb[2]))),
                (SegPathType.Segline, ((aabb[0], aabb[2]), (aabb[1], aabb[2]))),
                (SegPathType.Segline, ((aabb[1], aabb[2]), (aabb[1], aabb[3])))
            ]
    elif 'ellipse' in kw:
        ellipse = kw['ellipse']
        clockwise = kw.get('clockwise', False)
        a, b, c = ellipseABC(ellipse)
        k = 0.551915024494  # 拟合常数
        if clockwise:
            result = [
                (SegPathType.Bezier, ((a, 0), (a, -b*k), (a*k, -b), (0, -b))),
                (SegPathType.Bezier, ((0, -b), (-a*k, -b), (-a, -b*k), (-a, 0))),
                (SegPathType.Bezier, ((-a, 0), (-a, b*k), (-a*k, b), (0, b))),
                (SegPathType.Bezier, ((0, b), (a*k, b), (a, b*k), (a, 0)))
            ]
        else:
            result = [
                (SegPathType.Bezier, ((a, 0), (a, b*k), (a*k, b), (0, b))),
                (SegPathType.Bezier, ((0, b), (-a*k, b), (-a, b*k), (-a, 0))),
                (SegPathType.Bezier, ((-a, 0), (-a, -b*k), (-a*k, -b), (0, -b))),
                (SegPathType.Bezier, ((0, -b), (a*k, -b), (a, -b*k), (a, 0)))
            ]
        radian = 0 if ellipseIsCircle(ellipse) else vecAngleTo((1, 0), ptVec(ellipse[0], ellipse[1]))
        transVec = ptVec((c, 0), ptRotate(ellipse[1], -radian))
        return pathRotate(pathTranslate(result, transVec), radian)
    raise ValueError('[Error] createPath: 参数错误')


def pathToStr(path: list) -> str:
    """ 路径转字符串 """
    segPathStrs = [segPathToStr(segPath) for segPath in path]
    return f'({", ".join(segPathStrs)})'


def strToPath(string: str) -> list:
    """ 字符串转路径 """
    result = []
    numberStrs = _strToNumberStrs(string)
    i = 0
    while i < len(numberStrs):
        segType = SegPathType(int(numberStrs[i]))
        if segType == SegPathType.Segline:
            result.append(_numberStrsToSegPath(numberStrs[i:i+5]))
            i += 5
        elif segType == SegPathType.Arc:
            result.append(_numberStrsToSegPath(numberStrs[i:i+6]))
            i += 6
        else:
            result.append(_numberStrsToSegPath(numberStrs[i:i+9]))
            i += 9
    return result


def pathClone(path: list) -> list:
    """ 拷贝路径 """
    result = []
    result.extend(path)
    return result


def pathAabb(path: list) -> tuple:
    """ 返回路径包围盒 """
    result = emptyAabb
    for segPath in path:
        result = aabbExpandByAabb(result, segPathAabb(segPath))
    return result


def pathIsPolyline(path: list) -> bool:
    """ 返回路径是否多段线 """
    return all([segPathIsSegline(segPath) for segPath in path])


def pathPointByParam(path: list, param: float) -> tuple:
    """ 返回路径上参数param位置的点 """
    bezierId = int(param)
    return segPathPointByParam(path[bezierId], param - bezierId)


def pathReverse(path: list, inplace: bool=True) -> list:
    """ 逆向 """
    result = path if inplace else path[:]
    length = len(result)
    for i in range(length // 2):
        result[i], result[length - 1 - i] = segPathReverse(result[length - 1 - i]), segPathReverse(result[i])
    return result


def pathTranslate(path: list, transVec: tuple, inplace: bool=True) -> list:
    """ 平移 """
    result = path if inplace else path[:]
    for i in range(len(result)):
        result[i] = segPathTranslate(result[i], transVec)
    return result
    

def pathRotate(path: list, radian: float, center: tuple=ptZero, inplace: bool=True) -> list:
    """ 旋转（逆时针）
    :param radian: 旋转弧度
    :param center: 旋转中心
    """
    result = path if inplace else path[:]
    for i in range(len(result)):
        result[i] = segPathRotate(result[i], radian, center)
    return result


def pathScale(path: list, xRate: float, yRate: float, center: tuple=ptZero, inplace: bool=True) -> list:
    """ 缩放（以零点为中心） """
    result = path if inplace else path[:]
    for i in range(len(result)):
        result[i] = segPathScale(result[i], xRate, yRate, center)
    return result


def pathReflect(path: list, axis, inplace: bool=True) -> list:
    """ 镜像
    :param axis: 传入直线表示镜像轴，可以用tuple表示直线，也可以是以下字符串值：
                 "x":以x轴为镜像轴; "y":以y轴为镜像轴; "y=x":以直线y=x为镜像轴; "y=-x":以直线y=-x为镜像轴
    """
    result = path if inplace else path[:]
    for i in range(len(path)):
        result[i] = segPathReflect(result[i], axis)
    return result

# endregion


# region 角

"""
角用tuple表示，3个元素分别是形成角的三个点（按顺序）
"""

def angleBisector(angle: tuple) -> tuple:
    """ 返回角平分线 """
    side1, side2 = seglineStretch((angle[1], angle[0]), 1), seglineStretch((angle[1], angle[2]), 1)
    result = (angle[1], seglineMidPoint((side1[1], side2[1])))
    if floatEq(seglineLength(result), 0, abs_tol=geoTol):  # 平角
        result = seglineRotate(side1, pyUtils.halfPi, side1[0])
    return result

# endregion
