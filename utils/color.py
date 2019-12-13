import random

"""
rgb颜色用tuple表示，三个元素分别为r、g、b值，均为int，范围为[0,255]
rgba颜色用tuple表示，前三个元素为rgb值，第四个元素为透明度(float)，范围为[0, 1]
hsv颜色用tuple表示，三个元素分别为h、s、v值，h为int，范围为[0, 360)，s、v均为float，范围为[0, 1]
"""

# region 颜色常量

rgbBlack = (0, 0, 0)  # 黑色
rgbaBlack = (0, 0, 0, 1)  # 黑色，不透明

rgbNavy = (0, 0, 128)  # 藏青
rgbaNavy = (0, 0, 128, 1)  # 藏青，不透明

rgbDarkBlue = (0, 0, 139)  # 深蓝
rgbaDarkBlue = (0, 0, 139, 1)  # 深蓝，不透明

rgbBlue = (0, 0, 255)  # 蓝色
rgbaBlue = (0, 0, 255, 1)  # 蓝色，不透明

rgbDarkGreen = (0, 100, 0)  # 深绿
rgbaDarkGreen = (0, 100, 0, 1)  # 深绿，不透明

rgbGreen = (0, 128, 0)  # 调和绿
rgbaGreen = (0, 128, 0, 1)  # 调和绿，不透明

rgbDarkCyan = (0, 139, 139)  # 深青
rgbaDarkCyan = (0, 139, 139, 1)  # 深青，不透明

rgbLime = (0, 255, 0)  # 绿色
rgbaLime = (0, 255, 0, 1)  # 绿色，不透明

rgbCyan = (0, 255, 255)  # 青色
rgbaCyan = (0, 255, 255, 1)  # 青色，不透明

rgbDimGray = (105, 105, 105)  # 昏灰
rgbaDimGray = (105, 105, 105, 1)  # 昏灰，不透明

rgbLawnGreen = (124, 252, 0)  # 草坪绿
rgbaLawnGreen = (124, 252, 0, 1)  # 草坪绿，不透明

rgbMaroon = (128, 0, 0)  # 栗色
rgbaMaroon = (128, 0, 0, 1)  # 栗色，不透明

rgbPurple = (128, 0, 128)  # 紫色
rgbaPurple = (128, 0, 128, 1)  # 紫色，不透明

rgbOlive = (128, 128, 0)  # 橄榄色
rgbaOlive = (128, 128, 0, 1)  # 橄榄色，不透明

rgbGray = (128, 128, 128)  # 灰色
rgbaGray = (128, 128, 128, 1)  # 灰色，不透明

rgbSkyBlue = (135, 206, 235)  # 天蓝
rgbaSkyBlue = (135, 206, 235, 1)  # 天蓝，不透明

rgbDarkRed = (139, 0, 0)  # 深红
rgbaDarkRed = (139, 0, 0, 1)  # 深红，不透明

rgbDarkMagenta = (139, 0, 139)  # 深品红
rgbaDarkMagenta = (139, 0, 139, 1)  # 深品红，不透明

rgbLightGreen = (144, 238, 144)  # 浅绿
rgbaLightGreen = (144, 238, 144)  # 浅绿，不透明

rgbBrown = (165, 42, 42)  # 褐色
rgbaBrown = (165, 42, 42)  # 褐色，不透明

rgbDarkGray = (169, 169, 169)  # 暗灰
rgbaDarkGray = (169, 169, 169, 1)  # 暗灰，不透明

rgbLightBlue = (173, 216, 230)  # 浅蓝
rgbaLightBlue = (173, 216, 230, 1)  # 浅蓝，不透明

rgbSilver = (192, 192, 192)  # 银色
rgbaSilver = (192, 192, 192, 1)  # 银色，不透明

rgbLightGray = (211, 211, 211)  # 亮灰
rgbaLightGray = (211, 211, 211, 1)  # 亮灰，不透明

rgbLightCyan = (224, 255, 255)  # 浅青
rgbaLightCyan = (224, 255, 255, 1)  # 浅青，不透明

rgbRed = (255, 0, 0)  # 红色
rgbaRed = (255, 0, 0, 1)  # 红色，不透明

rgbMagenta = (255, 0, 255)  # 洋红
rgbaMagenta = (255, 0, 255, 1)  # 洋红，不透明

rgbOrange = (255, 165, 0)  # 橙色
rgbaOrange = (255, 165, 0, 1)  # 橙色，不透明

rgbPink = (255, 192, 203)  # 粉色
rgbaPink = (255, 192, 203, 1)  # 粉色，不透明

rgbGold = (255, 215, 0)  # 金色
rgbaGold = (255, 215, 0, 1)  # 金色，不透明

rgbYellow = (255, 255, 0)  # 黄色
rgbaYellow = (255, 255, 0, 1)  # 黄色，不透明

rgbLightYellow = (255, 255, 224)  # 浅黄
rgbaLightYellow = (255, 255, 224, 1)  # 浅黄，不透明

rgbWhite = (255, 255, 255)  # 白色
rgbaTransparentWhite = (255, 255, 255, 0)  # 白色，透明
rgbaWhite = (255, 255, 255, 1)  # 白色，不透明

# endregion


# region rgb

def rgbToStr(rgb: tuple) -> str:
    """ rgb颜色 -> rgb字符串#RRGGBB """

    def valueToHex(value: int) -> str:
        """ 将rgb值转为十六进制字符串 """
        result = str(hex(value))[2:].upper()
        return result if len(result) == 2 else '0' + result

    return f'#{valueToHex(rgb[0])}{valueToHex(rgb[1])}{valueToHex(rgb[2])}'


def rgbToHsv(rgb: tuple) -> tuple:
    """ rgb颜色 -> hsv颜色 """
    minValue = min(rgb[0], rgb[1], rgb[2])
    maxValue = max(rgb[0], rgb[1], rgb[2])
    # 计算h
    if minValue == maxValue:
        h = 0
    elif maxValue == rgb[0]:
        h = (rgb[1] - rgb[2]) / (maxValue - minValue) * 60 if rgb[1] >= rgb[2]\
            else (rgb[1] - rgb[2]) / (maxValue - minValue) * 60 + 360
    elif maxValue == rgb[1]:
        h = (rgb[2] - rgb[0]) / (maxValue - minValue) * 60 + 120
    else:
        h = (rgb[0] - rgb[1]) / (maxValue - minValue) * 60 + 240
    h = round(h)
    # 计算s
    s = 0 if maxValue == 0 else 1 - minValue / maxValue
    # 计算b
    v = maxValue / 255
    return h, s, v


def strToRgb(color: str) -> tuple:
    """ rgb字符串#RRGGBB -> rgb颜色 """
    return int('0x' + color[1:3], 16), int('0x' + color[3:5], 16), int('0x' + color[5:7], 16)


def rgbToGrey(rgb: tuple) -> int:
    """ rgb颜色 -> 灰度值 """
    return round((rgb[0] ** 2.2 * 0.2973 + rgb[1] ** 2.2 * 0.6274 + rgb[2] ** 2.2 * 0.0753) ** (1 / 2.2))


def randomRGB() -> tuple:
    """ 随机rgb颜色 """
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def rgbDist(rgb1: tuple, rgb2: tuple) -> int:
    """ 色差 """
    rMean = (rgb1[0] + rgb2[0]) / 2
    r = rgb1[0] - rgb2[0]
    g = rgb1[1] - rgb2[1]
    b = rgb1[2] - rgb2[2]
    return ((2+rMean/256)*(r**2) + 4*(g**2) + (2+(255-rMean)/256)*(b**2))**0.5

# endregion


# region rgba

def rgbaToStr(rgba: tuple) -> str:
    """ rgba颜色 -> rgba字符串 """
    return f'{(rgba[0], rgba[1], rgba[2], rgba[3])}'


def strToRgba(color: str) -> tuple:
    """ rgba字符串 -> rgba颜色 """
    numberStrs = color[1:-1].split(',')
    return int(numberStrs[0]), int(numberStrs[1]), int(numberStrs[2]), float(numberStrs[3])

# endregion


# region hsv

def hsvToRgb(hsv: tuple) -> tuple:
    """ hsv颜色 -> rgb颜色 """
    h2 = int(hsv[0] / 60) % 6
    f = hsv[0] / 60 - h2
    p = hsv[2] * (1 - hsv[1])
    q = hsv[2] * (1 - f * hsv[1])
    t = hsv[2] * (1 - (1 - f) * hsv[1])
    if h2 == 0:
        r, g, b = hsv[2], t, p
    elif h2 == 1:
        r, g, b = q, hsv[2], p
    elif h2 == 2:
        r, g, b = p, hsv[2], t
    elif h2 == 3:
        r, g, b = p, q, hsv[2]
    elif h2 == 4:
        r, g, b = t, p, hsv[2]
    else:
        r, g, b = hsv[2], p, q
    r, g, b = round(r * 255), round(g * 255), round(b * 255)
    return r, g, b

# endregion
