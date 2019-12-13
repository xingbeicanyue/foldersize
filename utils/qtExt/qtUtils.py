try:
    import PySide2
    from PySide2.QtGui import QColor
    from PySide2.QtWidgets import QLabel


# region 颜色

    def rgbToQColor(rgb: tuple) -> QColor:
        """ rgb -> QColor """
        return QColor(*rgb, 255)


    def qColorToRgb(color: QColor) -> tuple:
        """ QColor -> rgb """
        return color.red(), color.green(), color.blue()


    def rgbaToQColor(rgba: tuple) -> QColor:
        """ rgba -> QColor """
        return QColor(rgba[0], rgba[1], rgba[2], int(rgba[3] * 255))


    def qColorToRgba(color: QColor) -> tuple:
        """ QColor -> rgba """
        return color.red(), color.green(), color.blue(), color.alpha() / 255

# endregion


# region 控件绑定数据

    class LabelStrVar:
        """ 与QLabel绑定的str数据 """

        def __init__(self, label: QLabel, string: str=''):
            """ 初始化 """
            self._label = label  # 绑定的QLabel
            self._string = string  # 数据
            self.setVal(string)

        def setVal(self, string: str):
            """ 赋值 """
            self._string = string
            if self._label is not None:
                self._label.setText(self._string)

        def getVal(self) -> str:
            """ 获取数值 """
            return self._string

# endregion

except:
    pass
