#!/usr/bin/python

# reader.py


import wx
from module1 import *
import netifaces

class ListCtrlLeft(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)

        images = ['image.jpg', 'image2.jpg', 'cstrike.ico']

        self.parent = parent

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)

        self.il = wx.ImageList(64, 32)
        for i in images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')

        for i in range(3):
            self.InsertStringItem(0, '')
            self.SetItemImage(0, i)

    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-5)
        event.Skip()

    def OnSelect(self, event):
        window = self.parent.GetGrandParent().FindWindowByName('interface_list')
        index = event.GetIndex()
        window.LoadData(index)

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'red')

class interface_list(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
        #self.listbox = wx.ListBox(parent, id)
        self.parent = parent

        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.InsertColumn(0, '')


    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-5)
        event.Skip()

    def LoadData(self, index):
        self.DeleteAllItems()
        list1=netifaces.interfaces()
        
        for item in list1:
            self.InsertStringItem(0, item)


class Reader(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(700,500))
        display_menu_bar(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(splitter, -1)
        panel1.SetBackgroundColour('blue')
        panel11 = wx.Panel(panel1, -1, size=(-1, 240))
        panel11.SetBackgroundColour('BLUE')
        st1 = wx.StaticText(panel11, -1, 'CAPTURE', (135, 5))
        st1.SetForegroundColour('WHITE')

        panel12 = wx.Panel(panel1, -1, style=wx.BORDER_SUNKEN)
        vbox = wx.BoxSizer(wx.VERTICAL)
        list1 = ListCtrlLeft(panel12, -1)

        vbox.Add(list1, 1, wx.EXPAND)
        panel12.SetSizer(vbox)
        #panel12.SetBackgroundColour('green')


        vbox1.Add(panel11, 0, wx.EXPAND)
        vbox1.Add(panel12, 1, wx.EXPAND)

        panel1.SetSizer(vbox1)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(splitter, -1)
        panel21 = wx.Panel(panel2, -1, size=(-1, 40), style=wx.NO_BORDER)
        st2 = wx.StaticText(panel21, -1, 'INTERFACES', (135, 5))
        st2.SetForegroundColour('WHITE')
        panel21.SetBackgroundColour('BLUE')
        panel22 = wx.Panel(panel2, -1, style=wx.BORDER_RAISED)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        list2 = interface_list(panel22, -1)
        list2.SetName('interface_list')
        vbox3.Add(list2, 1, wx.EXPAND)
        panel22.SetSizer(vbox3)


        panel22.SetBackgroundColour('WHITE')
        vbox2.Add(panel21, 0, wx.EXPAND)
        vbox2.Add(panel22, 1, wx.EXPAND)

        panel2.SetSizer(vbox2)
        self.toolbar_icons()
        
        hbox.Add(splitter, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 3)
        self.SetSizer(hbox)
        self.CreateStatusBar()
        splitter.SplitVertically(panel1, panel2)
        self.Centre()
        self.Show(True)

    def toolbar_icons(self):
        toolbar = self.CreateToolBar()
        self.count=5
        toolbar.AddLabelTool(1, 'Exit', wx.Bitmap('close.png'))
        toolbar.AddLabelTool(2,'help',wx.Bitmap('help.png'))
        toolbar.AddLabelTool(3,'open',wx.Bitmap('open.png'))

        toolbar.AddLabelTool(4,'start',wx.Bitmap('start.png'))

        toolbar.AddLabelTool(5,'list',wx.Bitmap('list.png'))

        toolbar.AddLabelTool(6,'pause',wx.Bitmap('pause.png'))

        toolbar.AddLabelTool(7,'Restart',wx.Bitmap('restart.png'))
        toolbar.AddLabelTool(8,'stop',wx.Bitmap('stop.png'))
        toolbar.AddLabelTool(9,'undo',wx.Bitmap('undo.png'))
        toolbar.AddLabelTool(10,'redo',wx.Bitmap('redo.png'))

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.ExitApp, id=1)
        self.Bind(wx.EVT_TOOL, self.OnUndo, id=9)
        self.Bind(wx.EVT_TOOL, self.OnRedo, id=10)
    
 
            
    def OnQuit(self, e):    #to quit the program through menu item in file menu
        self.Close()

    def ExitApp(self, event):
        self.Close()
    def OnUndo(self, e):
        if self.count > 1 and self.count <= 5:
            self.count = self.count - 1

        if self.count == 1:
            self.toolbar.EnableTool(wx.ID_UNDO, False)

        if self.count == 4:
            self.toolbar.EnableTool(wx.ID_REDO, True)

    def OnRedo(self, e):
        if self.count < 5 and self.count >= 1:
            self.count = self.count + 1

        if self.count == 5:
            self.toolbar.EnableTool(wx.ID_REDO, False)

        if self.count == 2:
            self.toolbar.EnableTool(wx.ID_UNDO, True)   




app = wx.App()
Reader(None, -1, 'Nacsniff')
app.MainLoop()