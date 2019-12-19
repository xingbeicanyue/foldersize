import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from fileUtils import ByteUnit, byteUnitCountDic, DirManager


class MainWindow(tk.Tk):
    """ 主界面 """

    def __init__(self):
        """ 初始化 """
        super().__init__()
        self.title('Folder Size')
        width, height = 1600, 900
        xOff, yOff = (self.winfo_screenwidth() - width) // 2, (self.winfo_screenheight() - height) // 2
        self.geometry(f'{width}x{height}+{xOff}+{yOff}')

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

        self.__loadDirButton = tk.Button(self.__topFrame, text='扫描', command=self.__clickLoadDirButton)
        self.__loadDirButton.pack(side=tk.LEFT)
        self.__refreshButton = tk.Button(self.__topFrame, text='刷新', command=self.__clickRefreshButton)
        self.__refreshButton.pack(side=tk.LEFT)
        self.__openButton = tk.Button(self.__topFrame, text='打开', command=self.__clickOpenButton)
        self.__openButton.pack(side=tk.LEFT)
        ttk.Separator(self.__topFrame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=3)
        self.__changeUnitButton = tk.Button(self.__topFrame, width=3, text='B', command=self.__clickChangeUnitButton)
        self.__changeUnitButton.pack(side=tk.LEFT)

        self.__searchButton = tk.Button(self.__topFrame, text='搜索', command=self.__clickSearchButton)
        self.__searchButton.pack(side=tk.RIGHT)
        self.__searchEntry = tk.Entry(self.__topFrame, width=30)
        self.__searchEntry.pack(side=tk.RIGHT)
        self.__searchEntry.bind('<Return>', lambda event: self.__clickSearchButton())

        self.__ignoreCaseButton = tk.Checkbutton(self.__topFrame, text='忽略大小写', variable=self.__ignoreCase)
        self.__ignoreCaseButton.pack(side=tk.RIGHT)
        self.__regexButton = tk.Checkbutton(self.__topFrame, text='正则', variable=self.__regex)
        self.__regexButton.pack(side=tk.RIGHT)

        self.__refreshButton.configure(state='disabled')
        self.__openButton.configure(state='disabled')
        self.__searchButton.configure(state='disabled')
        self.__searchEntry.configure(state='disabled')

    def __initDataFrame(self):
        """ 初始化数据页面 """
        self.__scrollbar = tk.Scrollbar(self)
        self.__scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.__treeView = ttk.Treeview(self, yscrollcommand=self.__scrollbar.set, columns=(None,)*5)
        self.__treeView.heading('#0', text='路径')
        self.__treeView.heading('#1', text='大小（不包含子文件夹）')
        self.__treeView.heading('#2', text='大小（包含子文件夹）')
        self.__treeView.heading('#3', text='百分比（包含子文件夹）')
        self.__treeView.heading('#4', text='文件夹数')
        self.__treeView.heading('#5', text='文件数')
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
        if not self.__dirManager:
            return
        self.__clearData()
        self.__nodeItemDic = {None: ''}
        if self.__unit == ByteUnit.byte:
            for curNode in self.__dirManager.dirTree.preorderTraversal():
                parentItem = self.__nodeItemDic[curNode.parent] if curNode.parent in self.__nodeItemDic else ''
                self.__nodeItemDic[curNode] = self.__treeView.insert(
                    parentItem, curNode.depth, text=curNode.dirName,
                    values=(curNode.selfSize, curNode.allSize, f'{curNode.sizePercent:.3f}%',
                            curNode.folderCount, curNode.fileCount, curNode.pathDirName),
                    tags='' if curNode.canVisit else 'cannotVisit'
                )
        else:
            unitRate = byteUnitCountDic[self.__unit]
            for curNode in self.__dirManager.dirTree.preorderTraversal():
                parentItem = self.__nodeItemDic[curNode.parent] if curNode.parent in self.__nodeItemDic else ''
                self.__nodeItemDic[curNode] = self.__treeView.insert(
                    parentItem, curNode.depth, text=curNode.dirName,
                    values=(f'{curNode.selfSize / unitRate:.3f}', f'{curNode.allSize / unitRate:.3f}',
                            f'{curNode.sizePercent:.3f}%', curNode.folderCount, curNode.fileCount, curNode.pathDirName),
                    tags='' if curNode.canVisit else 'cannotVisit'
                )
        self.__treeView.tag_configure('cannotVisit', background="yellow")

    def __clickLoadDirButton(self):
        """ 点击加载路径 """
        dirName = filedialog.askdirectory()
        if dirName:
            self.__dirManager = DirManager(dirName)
            self.__showData()
        self.__refreshButton.configure(state='normal')
        self.__openButton.configure(state='normal')
        self.__searchButton.configure(state='normal')
        self.__searchEntry.configure(state='normal')

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
        self.__showData()

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
