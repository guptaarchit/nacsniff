#!/usr/bin/python

import wx
import time
import os
import sys
import select
from wx.lib.mixins.listctrl import ColumnSorterMixin
from sniffer_socket import sniffer
from help_window import *
from packet_info import *
from datagram import ipv4datagram,datamanager
import threading
import scan
from host_info import *
import nmap
import scapy.config
import scapy.layers.l2
import scapy.route
import math
from datetime import datetime

serial_num = 0

class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES)
        ColumnSorterMixin.__init__(self,7)
        # self.itemDataMap = nacsnif
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

    def GetListCtrl(self):
        return self

    def OnGetItemText(self, item, col):
        index=self.itemIndexMap[item]
        s = self.itemDataMap[index][col]
        return s

    def OnQuit(self,event):
        print "Sorted List Closed"
        self.Close()

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()



    def OnColClick(self,event):
        event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        print('OnItemSelected: "%s", "%s", "%s", "%s"\n' %
                           (self.currentItem,
                            self.GetItemText(self.currentItem),
                            self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2)))
        host_address=self.GetItemText(self.currentItem)
        self.host_window=host_information(None,-1, 'nacsnif',str(host_address))
        self.host_window.Show()


    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        print("OnItemActivated: %s\nTopItem: %s\n" %
                           (self.GetItemText(self.currentItem), self.GetTopItem()))

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemDeselected(self, evt):
        print("OnItemDeselected: %s" % evt.m_itemIndex)
        
    def OnQuit(self, event):
        self.host_window.Close()
        self.Close()


class scanner_window(wx.Frame):
    def __init__(self, parent, id, title,arg):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, id, title, size=(600, 500))
        self.interface_name=arg
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1)

        display_menu_bar(self)

        self.list = SortedListCtrl(panel)
        self.list.InsertColumn(0, 'Host', width=200)
        self.list.InsertColumn(1, 'Mac Address', width=200)
        self.list.InsertColumn(2, 'Host Name', width=200)
        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)
        self.toolbar_icons()
        self.Centre()
        self.Show(True)  
        # self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelection)
        self.hosts_list = []
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
        self.Bind(wx.EVT_TOOL, self.OnReload, id=7)
        self.Bind(wx.EVT_TOOL, self.OnStart, id=4)
        self.Bind(wx.EVT_TOOL, self.OnStop, id=8)
#        self.Bind(wx.EVT_TOOL, self.OnOpen, id=3)
        self.Bind(wx.EVT_TOOL,self.OnHelp,id=2)
        # self.Bind(wx.EVT_TOOL, self.OnSave, id=6)
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
        #self.data_store.save()
        
        print "Capture Window Closed"
        self.list.OnQuit(e)
        # if self.packet_info != None:
        #     self.packet_info.Close()
        #self.On
        self.Close()

    def OnStart(self,event):
        self.thread_stop = threading.Event()
        self.thread = threading.Thread(target=self.scan ,args=(1,self.thread_stop))
        self.thread.setDaemon(True)
        self.thread.start()
        print "started"
        # hosts_list = scan.main()

    def OnSelection(self,e):
    	pass


    def OnHelp(self,e):
        #app = wx.App()
        self.l=HelpWindow(None, -1, 'HelpWindow')
        #app.MainLoop()


    def OnStop(self,event):
        self.thread_stop.set()
        print "Foo"

    def OnSave(self, event):
        # Open the file, do an RU sure check for an overwrite!
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*|*", \
                wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            
            # Open the file for write, write, close
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'wb')
            self.data_store.save(filehandle)
            #filehandle.write(itcontains)
            filehandle.close()
        # Get rid of the dialog to keep things tidy
        dlg.Destroy()

    def new(self,arg,stop_event):
        if not stop_event.is_set():
            wx.CallAfter(self.scan)
            self.thread_stop.wait()
            print "Completed"
            for host,status,hostname,mac in self.hosts_list:
                print host,status,hostname,mac
                if status == 'up':
                    index = self.list.InsertStringItem(sys.maxint, '0')
                    self.list.SetStringItem(index, 1, host)
                    self.list.SetStringItem(index, 2, mac)
                    self.list.SetStringItem(index, 3, hostname)
    
    def foo(self):
        host_count = 0
        # time.sleep(5)
        d = {host:(host,mac,hostname) for host,state,hostname,mac in self.hosts_list if state == "up"}
        print d
        self.list.itemDataMap = d 
        self.list.itemIndexMap = d.keys()
        self.list.SetItemCount(len(d))
        # if len(self.hosts_list) != 0 :
        #     for host,state,hostname,mac in self.hosts_list:
        #         # print host,state,hostname,mac   
        #         host_count+=1
        #         if state == 'up':
        #             data_={1:(str(host),str(mac),str(hostname))}
        #             items=data_.items()
        #             for key, data in items:
        #                 print key,data
        #                 index=self.list.InsertStringItem(sys.maxint,data[0])
        #                 self.list.SetStringItem(index,1,str(data[1]))
        #                 self.list.SetStringItem(index,2,str(data[2]))

    def scan(self,arg,stop_event):
        if not stop_event.is_set():
            hosts_list = []
            for network, netmask, _, interface, address in scapy.config.conf.route.routes:

                # skip loopback network and default gateway
                if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
                    continue

                if netmask <= 0 or netmask == 0xFFFFFFFF:
                    continue

                net = scan.to_CIDR_notation(network, netmask)

                if interface != scapy.config.conf.iface:
                    # see http://trac.secdev.org/scapy/ticket/537
                    print("skipping %s because scapy currently doesn't support arping on non-primary network interfaces", net)
                    continue

                if net:
                    print "Arping" ,net ,"on",interface
                    # nm = nmap.PortScannerAsync()
                    nm = nmap.PortScanner()
                    t1 = datetime.now()
                    # nma.scan(hosts=net,arguments="-sP -T4", callback=callback_result)
                    nm.scan(hosts=net,arguments="-sP -T4 -n --max-rtt-timeout 500ms")
                    #print nm.scaninfo()
                    #or maybe this
                    # hosts_list = [(x, nm[x]['status']['state'],nm[x].hostname()) for x in nm.all_hosts()]
                    # for host, status in hosts_list:
                    #   print('{0}:{1}'.host)

                    host_count = 0
                    # while nm.still_scanning():
                    #     print "Scanning"
                    #     time.sleep(2)

                    # global host_count
                    last_host = ""
                    for host in nm.all_hosts():
                        print('----------------------------------------------------')
                        print('Host : {0} ({1})'.format(host, nm[host].hostname()))
                        print('State : {0}'.format(nm[host].state()))
                        host_count+=1
                        for proto in nm[host].all_protocols():
                            print('----------')
                            print('Protocol : {0}'.format(proto))

                            lport = list(nm[host][proto].keys())
                            lport.sort()
                            for port in lport:
                                print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port])) 
                                if port == "mac":
                                    if str(nm[host].hostname()) != '':        
                                        # data_={1:(str(host),str(nm[host].hostname()),str(nm[host][proto][port]))}
                                        self.hosts_list.append((host,nm[host].state(),nm[host].hostname(),nm[host][proto][port]))
                                    else:
                                        # data_={1:(str(host),"None",str(nm[host][proto][port]))}
                                        self.hosts_list.append((host,nm[host].state(),"None",nm[host][proto][port]))
                                
                        if len(nm[host].all_protocols()) == 0:
                            self.hosts_list.append((host,nm[host].state(),"None","None"))                            
                        

                        last_host = host       
                    print host_count
                    # print hosts_list[0]
                    t2 = datetime.now()

                    # Calculates the difference of time, to see how long it took to run the script
                    total =  t2 - t1

                    # Printing the information to screen
                    print 'Scanning Completed in: ', total

        self.thread_stop.set()                
        self.foo()
        # return hosts_list

    def OnReload(self,e):
        # self.sniffer_obj.close()
        self.list.DeleteAllItems()

    

def display_menu_bar(tempo):
    menubar = wx.MenuBar()
    fileMenu = wx.Menu()
    new_item = fileMenu.Append(wx.ID_NEW,   'New', 'New application')
    open_item = fileMenu.Append(wx.ID_OPEN,   'Open', 'Open application')
    save_as_item = fileMenu.Append(wx.ID_SAVE,   'Save', 'Save application')        
    exit_item = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
    menubar.Append(fileMenu, '&File')
        
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
    
    help_menu=wx.Menu()
    Help=help_menu.Append(wx.ID_ANY,'Help','about application')
    menubar.Append(help_menu,'&Help')

    tempo.SetMenuBar(menubar)
    
    tempo.Bind(wx.EVT_MENU, tempo.OnQuit, exit_item)
    tempo.Bind(wx.EVT_MENU,tempo.OnHelp,Help)
    tempo.Bind(wx.EVT_MENU,tempo.OnSave,save_as_item)
#    tempo.Bind(wx.EVT_MENU,tempo.OnOpen,open_item)
    # wx.EVT_MENU(tempo,101,tempo.OnSave )


if __name__ == "__main__":
    app = wx.App(False)
    frame = scanner_window(None,-1, 'nacsnif',"lo")
    frame.Show()
    app.MainLoop()
