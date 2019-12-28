"""
气泡提示框
"""

import tkinter as tk
import time


class ToolTip(tk.Toplevel):
    """
    气泡提示框
    在初始化函数中传入要绑定的控件
    """

    def __init__(self, widget, msg: str='', delay=1, follow=False):
        """ 初始化方法
        :param widget: 要绑定的控件
        :param msg: 提示字符串
        :param delay: 延迟时间（秒）
        :param follow: 是否跟随鼠标
        """
        super().__init__(widget.master, bg='black', padx=1, pady=1)
        self.withdraw()
        self.overrideredirect(True)

        self._delay = delay
        self._follow = follow
        self._visible = 0
        self._lastMotionTime = 0

        tk.Message(self, text=msg, bg='#FFFFDD', aspect=1000).grid()
        widget.bind('<Enter>', self._spawn, '+')
        widget.bind('<Leave>', self._hide, '+')
        widget.bind('<Motion>', self._move, '+')

    def _spawn(self, _):
        """ 准备显示 """
        self.visible = 1
        self.after(int(self._delay * 1000), self._show)

    def _show(self):
        """ 显示 """
        if self.visible == 1 and time.time() - self._lastMotionTime > self._delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def _hide(self, _):
        """ 隐藏 """
        self.visible = 0
        self.withdraw()

    def _move(self, event):
        """ 鼠标移动 """
        self._lastMotionTime = time.time()
        if not self._follow:
            self.visible = 1
            self.withdraw()
        self.geometry(f'+{event.x_root + 10}+{event.y_root + 10}')
        self.after(int(self._delay * 1000), self._show)
