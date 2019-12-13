import enum
import math
import os
import re
import time


# region 常量数值

sqrt2 = 1.4142135623730951  # 根号2
sqrt3 = 1.7320508075688772  # 根号3
sqrt5 = 2.23606797749979  # 根号5

doublePi = 6.283185307179586  # pi*2
halfPi = 1.5707963267948966  # pi/2
oneThirdOfPi = 1.0471975511965976  # pi/3
oneSixthOfPi = 0.5235987755982988  # pi/6
oneEighthOfPi = 0.39269908169872414  # pi/8
oneTenthOfPi = 0.3141592653589793  # pi/10

floatTol = 1e-9  # 浮点数计算容差

# endregion


# region 数值计算

# region 基础运算

def root(num: float, power: int) -> float:
    """ 计算num的power次实数开根
    :param power: 开根次数，>0
    :raises ValueError: 对负数开偶次方根
    """
    if num > 0:
        return num ** (1 / power)
    if num < 0:
        if power % 2 == 0:
            raise ValueError('[Error] root: 对负数开偶次方根')
        return - (-num) ** (1 / power)
    return 0


def isPrime(num: int) -> bool:
    """ 判断自然数是否质数 """
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def gcds(nums: tuple) -> int:
    """ 计算一组正整数的最大公约数 """
    result = nums[0] if len(nums) > 0 else 0
    for i in range(1, len(nums)):
        result = math.gcd(result, nums[i])
    return result


def lcms(nums: tuple) -> int:
    """ 计算一组正整数的最小公倍数 """
    result = nums[0] if len(nums) > 0 else 0
    for i in range(1, len(nums)):
        result = result * nums[i] // math.gcd(result, nums[i])
    return result


def cycleAdd(summand: float, addend: float, left: float, right: float):
    """ 循环增加（将summand+addend调整至区间[left, right)内） """
    return left + (summand + addend - left) % (right - left)


def toRange(value: float, left: float, right: float) -> float:
    """ 将value调整至区间[left, right]内最近的值 """
    return max(left, min(right, value))

# endregion


# region 浮点数比较

def floatCompare(a: float, b: float, rel_tol: float=0.0, abs_tol: float=floatTol) -> int:
    """ 浮点数比较
    :returns: 在rel_tol或abs_tol容差内，a<b返回-1，a==b返回0，a>b返回1
    """
    if math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol):
        return 0
    return -1 if a < b else 1


def floatEq(a: float, b: float, rel_tol: float=0.0, abs_tol: float=floatTol) -> bool:
    """ 判断浮点数是否满足a==b """
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def floatNEq(a: float, b: float, rel_tol: float=0.0, abs_tol: float=floatTol) -> bool:
    """ 判断浮点数是否满足a!=b """
    return not math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def floatLe(a: float, b: float, rel_tol: float=0.0, abs_tol: float=floatTol) -> bool:
    """ 判断浮点数是否满足a<b """
    return a < b and not math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def floatGr(a: float, b: float, rel_tol: float=0.0, abs_tol: float=floatTol) -> bool:
    """ 判断浮点数是否满足a>b """
    return a > b and not math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def floatLeEq(a: float, b: float, rel_tol: float=0.0, abs_tol: float=floatTol) -> bool:
    """ 判断浮点数是否满足a<=b """ 
    return a < b or math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def floatGrEq(a: float, b: float, rel_tol: float=0.0, abs_tol: float=floatTol) -> bool:
    """ 判断浮点数是否满足a>=b """
    return a > b or math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def floatBetween(left: float, right: float, value: float, rel_tol: float=0.0, abs_tol: float=floatTol) -> bool:
    """ 判断浮点数是否满足left<=value<=right """
    return floatLeEq(left, value, rel_tol, abs_tol) and floatLeEq(value, right, rel_tol, abs_tol)

# endregion


# region 罗马数字

"""
罗马数字用字符串表示，每个字符均为大写，表示的范围为[1, 3999]
"""

romanLetterToNumDic = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
numToRomanLetters = [
    ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
    ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'],
    ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM'],
    ['', 'M', 'MM', 'MMM']
]


def romanToInt(roman: str) -> int:
    """ 罗马数字 -> 整数 """
    result, length = 0, len(roman)
    for i, c in enumerate(roman):
        if i + 1 == length or romanLetterToNumDic[c] >= romanLetterToNumDic[roman[i+1]]:
            result += romanLetterToNumDic[c]
        else:
            result -= romanLetterToNumDic[c]
    return result


def intToRoman(num: int) -> str:
    """ 整数 -> 罗马数字 """
    romans = []
    for i in range(4):
        num, val = divmod(num, 10)
        romans.append(numToRomanLetters[i][val])
    return ''.join(reversed(romans))

# endregion

# endregion


# region 方程

def solveQuadraticEquation(a: float, b: float, c: float, complexResult: bool=False) -> tuple:
    """ 解一元二次方程 ax^2 + bx + c = 0
    :param complexResult: 是否包含复数解
    :returns: 返回(解)，如果没有解或有无数解都返回空元组
    """
    if a != 0:  # 二次方程
        d = b ** 2 - 4 * a * c
        if floatEq(d, 0):
            return -b / (2 * a),
        if d < 0 and not complexResult:
            return ()
        d = d ** 0.5
        return (-d - b) / (2 * a), (d - b) / (2 * a)
    elif b != 0:  # 一次方程
        return -c / b,
    return ()


def solveCubicEquation(a: float, b: float, c: float, d: float, complexResult: bool = False) -> tuple:
    """ 解一元三次方程 ax^3 + bx^2 + cx + d = 0
    :param complexResult: 是否包含复数解
    :returns: 返回(解)，如果没有解或有无数解都返回空元组
    """
    if a != 0:  # 三次方程
        # 盛金公式
        A = b ** 2 - 3 * a * c
        B = b * c - 9 * a * d
        C = c ** 2 - 3 * b * d
        delta = B ** 2 - 4 * A * C
        if floatEq(A, 0) and floatEq(B, 0):  # 一个实数解
            return -b / (3 * a),
        if floatGr(delta, 0):  # 一个实数解 + 两个共轭复数解
            y1 = A * b + 1.5 * a * (-B + delta ** 0.5)
            y2 = A * b + 1.5 * a * (-B - delta ** 0.5)
            if complexResult:
                return (
                    (-b - root(y1, 3) - root(y2, 3)) / (3 * a),
                    (-b + 0.5 * (root(y1,3) + root(y2,3)) + (sqrt3 / 2 * (root(y1,3) - root(y2,3))) * 1j) / (3 * a),
                    (-b + 0.5 * (root(y1,3) + root(y2,3)) - (sqrt3 / 2 * (root(y1,3) - root(y2,3))) * 1j) / (3 * a)
                )
            return (-b - root(y1, 3) - root(y2, 3)) / (3 * a),
        if floatEq(delta, 0):  # 两个实数解
            k = B / A
            return -b / a + k, -k / 2
        # 三个实数解
        t = (2 * A * b - 3 * a * B) / (2 * A ** 1.5)
        theta = math.acos(t) / 3
        return (
            (-b - 2 * A ** 0.5 * math.cos(theta)) / (3 * a),
            (-b + A ** 0.5 * (math.cos(theta) + sqrt3 * math.sin(theta))) / (3 * a),
            (-b + A ** 0.5 * (math.cos(theta) - sqrt3 * math.sin(theta))) / (3 * a)
        )
    return solveQuadraticEquation(b, c, d, complexResult)

# endregion


# region 列表拓展函数

def binarySearch(datas, target, cmpFunc) -> int:
    """ 二分搜索，建议在无法使用bisect模块时使用本函数
    :param datas: 数据组（元组或列表），要求已按照cmpFunc的规则排序
    :param target: 要查找的元素值
    :param cmpFunc: 比较函数，小于返回负数，等于返回0，大于返回正数
    :returns: 返回大于等于target的第一项元素id，如果没有则返回数据组项数
    """
    left, right = 0, len(datas)
    while left != right:  # 每次进入子列表的搜索，规则与全列表相同
        middle = (left + right) // 2
        if cmpFunc(target, datas[middle]) <= 0:
            right = middle
        else:
            left = middle + 1
    return left

# endregion


# region 文件拓展函数

def validFileName(fileName: str) -> bool:
    """ 返回是否合法的windows文件名
    :param fileName: 文件名，utf-8编码
    """
    if len(fileName) == 0 or len(bytes(fileName, encoding="utf8")) > 260:
        return False
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    return False if reg.findall(fileName) else True


def fileExtension(pathFileName: str) -> str:
    """ 获取文件拓展名（不带'.'） """
    return os.path.splitext(pathFileName)[1][1:]


def fileNameWithoutExtension(pathFileName: str) -> str:
    """ 获取不带后缀的文件名 """
    fileName = os.path.basename(pathFileName)
    splitPos = fileName.rfind('.')
    return fileName[0:splitPos] if splitPos != -1 else fileName


def getFileLineCount(pathFileName: str) -> int:
    """ 获取文件行数（'\n'即换行）
    :raises IOError: 文件无法打开
    """
    result = 1
    with open(pathFileName, mode='rb') as file:
        while True:
            buffer = file.read(8388608)  # 8 * 1024 * 1024
            if not buffer:
                break
            result += buffer.count(b'\n')
    return result


def getDirSize(pathDirName: str) -> int:
    """ 获取文件夹中所有文件的总大小
    :returns: 返回负数表示获取失败
    """
    try:
        size = 0
        for rootDir, dirs, files in os.walk(pathDirName):
            size += sum([os.path.getsize(os.path.join(rootDir, fileName)) for fileName in files])
        return size
    except:
        return -1


def getDirSizeWithoutSubdirs(pathDirName: str) -> int:
    """ 获取文件夹中直属文件的总大小
    :returns: 返回负数表示获取失败
    """
    try:
        return sum([os.path.getsize(os.path.join(pathDirName, fileName)) for fileName in os.listdir(pathDirName)
                    if os.path.isfile(os.path.join(pathDirName, fileName))])
    except:
        return -1

# endregion


# region 计时

class TimeUnit(enum.Enum):
    """ 时间单位 """
    Nanosecond = 0  # 纳秒
    Microsecond = 1  # 微秒
    Millisecond = 2  # 毫秒
    Second = 3  # 秒
    Minute = 4  # 分钟
    Hour = 5  # 小时
    Day = 6  # 天
    Month = 7  # 月
    Year = 8  # 年
    Decade = 9  # 十年
    Century = 10  # 世纪


class Stopwatch:
    """ 计时器 """

    def __init__(self, start: bool=True, unit: TimeUnit=TimeUnit.Millisecond, includeSleep: bool=True):
        """ 初始化
        :param start: 是否进入计时状态
        :param unit: 时间单位
        :param includeSleep: 是否包含睡眠时间
        :raises ValueError: 时间单位错误
        """
        self.__getTime = time.perf_counter_ns if includeSleep else time.process_time_ns
        if unit not in Stopwatch.__unitRateDic:
            raise ValueError('[Error] Stopwatch.__init__: 不支持该时间单位')
        self.__unitRate = Stopwatch.__unitRateDic[unit]
        self.restart(start)

    def restart(self, start: bool=True):
        """ 累积量清零，重新开始
        :param start: 是否进入计时状态
        """
        self.__running = start
        self.__initTime = self.__getTime()
        self.__lastStartTime = self.__initTime if start else 0
        self.__accTime = 0

    def start(self):
        """ 继续计时，如果正处于计时状态不会开始新的计时片段 """
        if self.__running:
            return
        self.__running = True
        self.__lastStartTime = self.__getTime()

    def stop(self) -> float:
        """ 停止计时，如果不处于计时状态则返回0
        :returns: 返回当前片段的计时
        """
        if self.__running:
            self.__running = False
            result = self.__getTime() - self.__lastStartTime
            self.__accTime += result
            return result * self.__unitRate
        else:
            return 0

    def shutter(self) -> float:
        """ 停止并立即继续计时（开始新的计时片段），如果不处于计时状态则返回0
        :returns: 返回当前片段的计时
        """
        now = self.__getTime()
        if self.__running:
            result = now - self.__lastStartTime
            self.__lastStartTime = now
            self.__accTime += result
            return result * self.__unitRate
        else:
            self.__running = True
            self.__lastStartTime = now
            return 0

    def elapsed(self) -> float:
        """ 所有计时片段累计计时 """
        if self.__running:
            return (self.__accTime + self.__getTime() - self.__lastStartTime) * self.__unitRate
        else:
            return self.__accTime * self.__unitRate

    def elapsedAll(self) -> int:
        """ 总计时（包括暂停时间） """
        return (self.__getTime() - self.__initTime) * self.__unitRate

    @property
    def running(self) -> bool:
        """ 是否处于计时状态 """
        return self.__running

    __unitRateDic = {TimeUnit.Nanosecond: 1, TimeUnit.Microsecond: 1 / 1e3, TimeUnit.Millisecond: 1 / 1e6,
                     TimeUnit.Second: 1 / 1e9, TimeUnit.Minute: 1 / 6e10, TimeUnit.Hour: 1 / 3.6e12}

# endregion


# region 装饰器

def singleton(cls):
    """ 单例装饰器 """
    instances = {}
    def getInstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getInstance

# endregion