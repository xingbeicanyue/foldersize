import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import fileUtils


class MainWindow(tk.Tk):
    """ 主界面 """

    def __init__(self):
        """ 初始化 """
        super().__init__()
        self.title('Folder Size')
        width, height = 1600, 900
        xOff, yOff = (self.winfo_screenwidth() - width) // 2, (self.winfo_screenheight() - height) // 2
        self.geometry(f'{width}x{height}+{xOff}+{yOff}')
        self.__initWidget()
        self.__dirManager = None
        self.__nodeItemDic = {}

    def __initWidget(self):
        """ 初始化控件 """
        self.__initTopFrame()
        self.__initDataFrame()

    def __initTopFrame(self):
        """ 初始化顶部工具栏 """
        self.__topFrame = tk.Frame(self, height=30)
        self.__topFrame.pack(side=tk.TOP, fill=tk.X)

        self.__loadDirButton = tk.Button(self.__topFrame, text='扫描', command=self.__clickLoadDirButton)
        self.__loadDirButton.pack(side=tk.LEFT)
        self.__refreshButton = tk.Button(self.__topFrame, text='刷新', command=self.__clickRefreshButton)
        self.__refreshButton.pack(side=tk.LEFT)
        self.__openButton = tk.Button(self.__topFrame, text='打开', command=self.__clickOpenButton)
        self.__openButton.pack(side=tk.LEFT)
        self.__searchButton = tk.Button(self.__topFrame, text='搜索', command=self.__clickSearchButton)
        self.__searchButton.pack(side=tk.RIGHT)
        self.__searchEntry = tk.Entry(self.__topFrame, width=30)
        self.__searchEntry.pack(side=tk.RIGHT)
        self.__searchEntry.bind('<Return>', lambda event: self.__clickSearchButton())

    def __initDataFrame(self):
        """ 初始化数据页面 """
        self.__scrollbar = tk.Scrollbar(self)
        self.__scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.__treeView = ttk.Treeview(self, yscrollcommand=self.__scrollbar.set, columns=('大小', '百分比'))
        self.__treeView.heading('#0', text='路径')
        self.__treeView.heading('大小', text='大小')
        self.__treeView.heading('百分比', text='百分比')
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
        for curNode in self.__dirManager.dirTree.preorderTraversal():
            parentItem = self.__nodeItemDic[curNode.parent] if curNode.parent in self.__nodeItemDic else ''
            self.__nodeItemDic[curNode] = self.__treeView.insert(parentItem, curNode.depth, text=curNode.dirName,
                values=(curNode.allSize, f'{curNode.sizePercent:.3f}%', curNode.data))

    def __clickLoadDirButton(self):
        """ 点击加载路径 """
        dirName = filedialog.askdirectory()
        if dirName:
            self.__dirManager = fileUtils.DirManager(dirName)
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
        os.system('start explorer ' + item['values'][2].replace('/', '\\'))

    def __clickSearchButton(self):
        """ 点击搜索 """
        text = self.__searchEntry.get()
        if self.__dirManager and text:
            self.__clearSelection()
            nodes = self.__dirManager.searchNode(text, True)
            for node in nodes:
                _id = self.__nodeItemDic[node]
                self.__treeView.selection_add(_id)
                self.__treeView.see(_id)
