#!/usr/bin/python

# sorted.py

import wx
import time
import sys
from wx.lib.mixins.listctrl import ColumnSorterMixin
from sniffer_socket import sniffer
from datagram import ipv4datagram

serial='1'
t='.49'
s='172.16.98.100'
d='172.16.98.190'
p='ssdp'
l='175'
i='M-SEARCH'
nacsnif = {
1: (serial,t,s,d,p,l,i)
}


class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self, len(nacsnif))
        self.itemDataMap = nacsnif

    def GetListCtrl(self):
        return self

    def OnQuit(self,event):
        print "Sorted List Closed"
        self.Close()

class Nacsnif(wx.Frame):
    def __init__(self, parent, id, title,arg):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, id, title, size=(1000, 600))
        self.interface_name=arg
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
            print data[1]
            self.list.SetStringItem(index, 2, data[2])
            self.list.SetStringItem(index, 3, data[3])
            self.list.SetStringItem(index, 4, data[4])
            self.list.SetStringItem(index, 5, data[5])
            self.list.SetStringItem(index, 6, data[6])
            
            self.list.SetItemData(index, key)

        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)
        self.toolbar_icons()
        self.Centre()
        self.Show(True)
        self.start()
        print "start arg"
        print arg
        print "after arg"
        self.sniffer_obj = sniffer(arg)
        self.sniffer_obj.event_packet_is_received += self.handle_ip_packet
        #self.sniffer_obj.start()

    def toolbar_icons(self):
        toolbar = self.CreateToolBar()
        self.count=5
        toolbar.AddLabelTool(1, 'Exit', wx.Bitmap('images/close.png'))
        toolbar.AddLabelTool(2,'help',wx.Bitmap('images/help.png'))
        toolbar.AddLabelTool(3,'open',wx.Bitmap('images/open.png'))

        toolbar.AddLabelTool(4,'start',wx.Bitmap('images/start.png'))

        toolbar.AddLabelTool(5,'list',wx.Bitmap('images/list.png'))

        toolbar.AddLabelTool(6,'pause',wx.Bitmap('images/pause.png'))

        toolbar.AddLabelTool(7,'Restart',wx.Bitmap('images/restart.png'))
        toolbar.AddLabelTool(8,'stop',wx.Bitmap('images/stop.png'))
        toolbar.AddLabelTool(9,'undo',wx.Bitmap('images/undo.png'))
        toolbar.AddLabelTool(10,'redo',wx.Bitmap('images/redo.png'))

        toolbar.Realize()
        #self.Bind(wx.EVT_TOOL, self.start, id=4)
        self.Bind(wx.EVT_TOOL, self.OnQuit, id=1)
        self.Bind(wx.EVT_TOOL, self.OnUndo, id=9)
        self.Bind(wx.EVT_TOOL, self.OnRedo, id=10)
    
    # def start(self):
    #     # self.sniffer_obj = sniffer(self.arg)
    #     print "Here"
    #     # self.sniffer_obj.event_packet_is_received += self.handle_ip_packet

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

    def OnQuit(self, e):    #to quit the program through menu item in file menu
        self.sniffer_obj._close()
        print "Capture Window Closed"
        self.list.OnQuit(e)
        self.Close()


    def handle_ip_packet(self,sender,earg):
        print "In Handler"
        #if isinstance(earg,ipv4datagram):
        #   print ipv4datagram.dest_mac_addr

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

def capturewindow_start(parent,arg):
    app = wx.App(False)
    frame = Nacsnif(parent,-1, 'nacsnif',"lo")
    frame.Show()
    app.MainLoop()
    # self.sniffer_obj.start()


if __name__ == "__main__":
    app = wx.App(False)
    frame = Nacsnif(None,-1, 'nacsnif',"lo")
    frame.Show()
    app.MainLoop()