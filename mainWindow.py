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
        self.geometry('1600x900')
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
        self.__searchEntry = tk.Entry(self.__topFrame)
        self.__searchEntry.pack(side=tk.RIGHT)

    def __initDataFrame(self):
        """ 初始化数据页面 """
        self.__treeView = ttk.Treeview(self, columns=('大小', '百分比'))
        self.__treeView.heading('#0', text='路径')
        self.__treeView.heading('大小', text='大小')
        self.__treeView.heading('百分比', text='百分比')
        self.__treeView.pack(expand=1, fill=tk.BOTH)

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
        for _id in self.__treeView.selection():
            item = self.__treeView.item(_id)
            os.system('start explorer ' + item['values'][2].replace('/', '\\'))

    def __clickSearchButton(self):
        """ 点击搜索 """
        text = self.__searchEntry.get()
        if self.__dirManager and text:
            self.__clearSelection()
            nodes = self.__dirManager.searchNode(text, True)
            for node in nodes:
                self.__treeView.selection_add(self.__nodeItemDic[node])
