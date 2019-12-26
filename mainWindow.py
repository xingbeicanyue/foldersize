import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from toolTip import ToolTip
from fileUtils import ByteUnit, byteUnitCountDic, DirManager


class MainWindow(tk.Tk):
    """ 主界面 """

    __title = 'Folder Size'
    __initWidth = 1600
    __initHeight = 900
    __topOff = 50
    __toolTipDelay = 0.5

    def __init__(self):
        """ 初始化 """
        super().__init__()
        self.title(MainWindow.__title)
        xOff, yOff = (self.winfo_screenwidth() - MainWindow.__initWidth) // 2, MainWindow.__topOff
        self.geometry(f'{MainWindow.__initWidth}x{MainWindow.__initHeight}+{xOff}+{yOff}')

        self.__dirManager = None
        self.__unit = ByteUnit.byte
        self.__ignoreCase = tk.IntVar()
        self.__regex = tk.IntVar()
        self.__nodeItemDic = {}
        self.__initWidget()

    def __initWidget(self):
        """ 初始化控件 """
        self.__initTopFrame()
        self.__initDataFrame()

    def __initTopFrame(self):
        """ 初始化顶部工具栏 """
        self.__topFrame = tk.Frame(self, height=30)
        self.__topFrame.pack(side=tk.TOP, fill=tk.X)

        self.__loadDirButton = tk.Button(self.__topFrame, text='扫描', command=self.__clickLoadDirButton, relief='flat')
        self.__loadDirButton.pack(side=tk.LEFT)
        ToolTip(self.__loadDirButton, '扫描', delay=MainWindow.__toolTipDelay, follow=False)
        self.__refreshButton = tk.Button(self.__topFrame, text='刷新', command=self.__clickRefreshButton, relief='flat')
        self.__refreshButton.pack(side=tk.LEFT)
        ToolTip(self.__refreshButton, '刷新', delay=MainWindow.__toolTipDelay, follow=False)
        self.__openButton = tk.Button(self.__topFrame, text='打开', command=self.__clickOpenButton, relief='flat')
        self.__openButton.pack(side=tk.LEFT)
        ToolTip(self.__openButton, '打开', delay=MainWindow.__toolTipDelay, follow=False)
        ttk.Separator(self.__topFrame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=3)
        self.__changeUnitButton = tk.Button(self.__topFrame, width=3, text='B', command=self.__clickChangeUnitButton,
                                            relief='flat')
        self.__changeUnitButton.pack(side=tk.LEFT)
        ToolTip(self.__changeUnitButton, '切换单位', delay=MainWindow.__toolTipDelay, follow=False)
        ttk.Separator(self.__topFrame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=3)

        self.__searchButton = tk.Button(self.__topFrame, text='搜索', command=self.__clickSearchButton, relief='flat')
        self.__searchButton.pack(side=tk.RIGHT)
        ToolTip(self.__searchButton, '搜索', delay=MainWindow.__toolTipDelay, follow=False)
        self.__searchEntry = tk.Entry(self.__topFrame, width=30, justify=tk.RIGHT)
        self.__searchEntry.pack(side=tk.RIGHT)
        self.__searchEntry.bind('<Return>', lambda event: self.__clickSearchButton())

        self.__ignoreCaseButton = tk.Checkbutton(self.__topFrame, text='忽略大小写', variable=self.__ignoreCase)
        self.__ignoreCaseButton.pack(side=tk.RIGHT)
        ToolTip(self.__ignoreCaseButton, '忽略大小写', delay=MainWindow.__toolTipDelay, follow=False)
        self.__regexButton = tk.Checkbutton(self.__topFrame, text='正则', variable=self.__regex)
        self.__regexButton.pack(side=tk.RIGHT)
        ToolTip(self.__regexButton, '正则表达式', delay=MainWindow.__toolTipDelay, follow=False)

        self.__refreshButton.configure(state='disabled')
        self.__openButton.configure(state='disabled')
        self.__searchButton.configure(state='disabled')
        self.__searchEntry.configure(state='disabled')

    def __initDataFrame(self):
        """ 初始化数据页面 """
        self.__scrollbar = tk.Scrollbar(self)
        self.__scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.__treeView = ttk.Treeview(self, yscrollcommand=self.__scrollbar.set, columns=(None,)*5)
        self.__treeView.heading('#0', text='路径', command=lambda: self.__sort('name'))
        self.__treeView.heading('#1', text='大小（不包含子文件夹）', command=lambda: self.__sort('selfSize'))
        self.__treeView.heading('#2', text='大小（包含子文件夹）', command=lambda: self.__sort('allSize'))
        self.__treeView.heading('#3', text='百分比（包含子文件夹）', command=lambda: self.__sort('allSize'))
        self.__treeView.heading('#4', text='文件夹数', command=lambda: self.__sort('folderCount'))
        self.__treeView.heading('#5', text='文件数', command=lambda: self.__sort('fileCount'))
        self.__treeView.column('#0', width=500)
        self.__treeView.column('#1', anchor=tk.E)
        self.__treeView.column('#2', anchor=tk.E)
        self.__treeView.column('#3', anchor=tk.E)
        self.__treeView.column('#4', anchor=tk.E)
        self.__treeView.column('#5', anchor=tk.E)
        self.__treeView.pack(expand=1, fill=tk.BOTH)
        self.__scrollbar.config(command=self.__treeView.yview)

    def __clearData(self):
        """ 清空数据 """
        roots = self.__treeView.get_children()
        for root in roots:
            self.__treeView.delete(root)

    def __clearSelection(self):
        """ 清空选择 """
        self.__treeView.selection_remove(self.__treeView.selection())

    def __showData(self):
        """ 显示数据 """
        self.__clearData()
        self.__nodeItemDic = {None: ''}
        if self.__dirManager is None or self.__dirManager.dirTree is None:
            buttonState = 'disabled'
        else:
            buttonState = 'normal'
            unitRate = byteUnitCountDic[self.__unit]
            sizeFormat = '0f' if self.__unit == ByteUnit.byte else '3f'
            dirNodes = self.__dirManager.dirTree.preorderTraversal()
            for curNode in dirNodes:
                parentItem = self.__nodeItemDic[curNode.parent] if curNode.parent in self.__nodeItemDic else ''
                self.__nodeItemDic[curNode] = self.__treeView.insert(
                    parentItem, 'end', text=curNode.dirName, open=not curNode.parent,
                    values=(f'{curNode.selfSize / unitRate: .{sizeFormat}}',
                            f'{curNode.allSize / unitRate: .{sizeFormat}}',
                            f'{curNode.sizePercent:.3f}%', curNode.folderCount, curNode.fileCount, curNode.pathDirName),
                    tags='' if curNode.canVisit else 'cannotVisit'
                )
            self.__treeView.tag_configure('cannotVisit', background="yellow")

        self.__refreshButton.configure(state=buttonState)
        self.__openButton.configure(state=buttonState)
        self.__searchButton.configure(state=buttonState)
        self.__searchEntry.configure(state=buttonState)

    def __getNodeOpenDict(self) -> dict:
        """ 获取{节点, 展开状态} """
        return {key: self.__treeView.item(value, option='open') for key, value in self.__nodeItemDic.items()}

    def __setItemOpen(self, nodeOpenDict: dict):
        """ 设置节点展开状态 """
        for node, isOpen in nodeOpenDict.items():
            self.__treeView.item(self.__nodeItemDic[node], open=isOpen)

    # 按钮事件 ---------------------------------------------------------------------------------------------------------

    def __clickLoadDirButton(self):
        """ 点击加载路径 """
        dirName = filedialog.askdirectory()
        if dirName:
            self.__dirManager = DirManager(dirName)
            self.__showData()

    def __clickRefreshButton(self):
        """ 点击刷新 """
        if self.__dirManager:
            self.__dirManager.reload()
            self.__showData()

    def __clickOpenButton(self):
        """ 点击打开 """
        _ids = self.__treeView.selection()
        if len(_ids) != 1:
            return
        item = self.__treeView.item(_ids[0])
        os.system('start explorer ' + item['values'][-1].replace('/', '\\'))

    def __clickChangeUnitButton(self):
        """ 点击单位转换 """
        if self.__unit == ByteUnit.byte:
            self.__unit = ByteUnit.kiloByte
            self.__changeUnitButton['text'] = 'KB'
        elif self.__unit == ByteUnit.kiloByte:
            self.__unit = ByteUnit.megaByte
            self.__changeUnitButton['text'] = 'MB'
        elif self.__unit == ByteUnit.megaByte:
            self.__unit = ByteUnit.gigaByte
            self.__changeUnitButton['text'] = 'GB'
        else:
            self.__unit = ByteUnit.byte
            self.__changeUnitButton['text'] = 'B'

        unitRate = byteUnitCountDic[self.__unit]
        sizeFormat = '0f' if self.__unit == ByteUnit.byte else '3f'
        for node, item in self.__nodeItemDic.items():
            if node:
                self.__treeView.item(item, values=(f'{node.selfSize / unitRate: .{sizeFormat}}',
                                                   f'{node.allSize / unitRate: .{sizeFormat}}',
                                                   f'{node.sizePercent:.3f}%',
                                                   node.folderCount, node.fileCount, node.pathDirName))

    def __clickSearchButton(self):
        """ 点击搜索 """
        text = self.__searchEntry.get()
        if self.__dirManager and text:
            self.__clearSelection()
            nodes = self.__dirManager.searchNode(text, self.__ignoreCase.get() == 1, self.__regex.get() == 1)
            for node in nodes:
                _id = self.__nodeItemDic[node]
                self.__treeView.selection_add(_id)
                self.__treeView.see(_id)

    def __sort(self, key: str):
        """ 排序 """
        if self.__dirManager:
            self.__dirManager.sort(key)
            nodeOpenDict = self.__getNodeOpenDict()
            self.__showData()
            self.__setItemOpen(nodeOpenDict)
