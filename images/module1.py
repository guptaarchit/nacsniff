#!/usr/bin/python

# sorted.py

import wx
import sys
from wx.lib.mixins.listctrl import ColumnSorterMixin
serial='1'
t='.49'
s='172.16.98.100'
d='172.16.98.190'
p='ssdp'
l='175'
i='M-SEARCH'
nacsnif = {
#1 : ('jessica alba', 'pomona', '1981')

1: (serial,t,s,d,p,l,i)
#1 : ('1','.49','172.16.98.100','12.16.98.190','ssdp','175','M-SEARCH')
}


class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, len(nacsnif))
        self.itemDataMap = nacsnif

    def GetListCtrl(self):
        return self

class Nacsnif(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1000, 400))

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1)

        display_menu_bar(self)

        self.list = SortedListCtrl(panel)
        self.list.InsertColumn(0, 'No.', width=140)
        self.list.InsertColumn(1, 'Time', width=130)
        #self.list.InsertColumn(2, 'year', wx.LIST_FORMAT_RIGHT, 90)
        self.list.InsertColumn(2,'Source',width=130)
        self.list.InsertColumn(3,'Destinator',width=130)
        self.list.InsertColumn(4,'Protocol',width=130)
        self.list.InsertColumn(5,'Length',width=130)
        self.list.InsertColumn(6,'Info',width=130)
  
        items = nacsnif.items()

        for key, data in items:
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetStringItem(index, 2, data[2])
            self.list.SetStringItem(index, 3, data[3])
            self.list.SetStringItem(index, 4, data[4])
            self.list.SetStringItem(index, 5, data[5])
            self.list.SetStringItem(index, 6, data[6])
            
            self.list.SetItemData(index, key)

        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

    def OnQuit(self, e):    #to quit the program through menu item in file menu
        self.Close()

def display_menu_bar(tempo):
    menubar = wx.MenuBar()
    fileMenu = wx.Menu()
    new_item = fileMenu.Append(wx.ID_NEW,   'New', 'New application')
    open_item = fileMenu.Append(wx.ID_OPEN,   'Open', 'Open application')
    save_as_item = fileMenu.Append(wx.ID_SAVE,   'Save As', 'Save application')        
    exit_item = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
    menubar.Append(fileMenu, '&File')
    
    tempo.Bind(wx.EVT_MENU, tempo.OnQuit, exit_item)

    edit_menu = wx.Menu()
    copy_item = edit_menu.Append(wx.ID_COPY,   'Copy', 'Copy application')
    find_packet_item = edit_menu.Append(wx.ID_ANY,   'Find Packet', 'Find packet application')
    find_next_item = edit_menu.Append(wx.ID_ANY,   'Find Next', 'Finding next packet application')
    find_previous_item = edit_menu.Append(wx.ID_ANY,   'Find Previous', 'finding Previous packet application')        
    menubar.Append(edit_menu, '&Edit')

    go_menu = wx.Menu()
    back = go_menu.Append(wx.ID_ANY,   'Back', 'back application')
    forward = go_menu.Append(wx.ID_ANY,   'Forward', 'forward application')
    go_to_packet = go_menu.Append(wx.ID_ANY,   'Go to Packet', 'go to packet application')
    go_to_corresponding_packet = go_menu.Append(wx.ID_ANY,   'Go to corresponding Packet', 'go to corrsponding packet application')        
    menubar.Append(go_menu, '&Go')
    tempo.SetMenuBar(menubar)

def temp():
    app = wx.App()
    Nacsnif(None, -1, 'nacsnif')
    app.MainLoop()