import wx
import threading
import scan
from host_info import *
import nmap
import math
from datetime import datetime
import os
from wx.lib.mixins.listctrl import ColumnSorterMixin
class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ColumnSorterMixin.__init__(self,7)
        # self.itemDataMap = nacsnif

    def GetListCtrl(self):
        return self

    def OnQuit(self,event):
        print "Sorted List Closed"
        self.Close()
class host_information(wx.Frame):
    def __init__(self, parent, id, title,arg):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, id, title, size=(600, 600))
        self.host=arg
        #panel = wx.Panel(self, -1)

        #display_menu_bar(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1,size=(400,400))
        #display_menu_bar(self)

        self.list = SortedListCtrl(panel)
        self.list.InsertColumn(0, 'port', width=300)
        self.list.InsertColumn(1, 'status', width=300)
        hbox.Add(self.list, 1, wx.EXPAND)

        panel.SetSizer(hbox)
        # hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # panel2 = wx.Panel(self, -1,size=(400,200))
        # hbox1.Add(self.list, 1, wx.EXPAND)

        # panel.SetSizer(hbox1)
        
        #
        #self.toolbar_icons()
        self.Centre()
        self.Show(True)  



    def OnStart(self,host):
        self.thread_stop = threading.Event()
        self.thread = threading.Thread(target=self.get_port_scan ,args=(host,self.thread_stop))
        self.thread.setDaemon(True)
        self.thread.start()
        print "started"

    def get_port_scan(self,host,stop_event):
        if not stop_event.is_set():
            nm = nmap.PortScanner()
            if (os.getuid() == 0):
                nm.scan(host, arguments='-sS -vv -n -PN --max-rtt-timeout 500ms -T4 -A -p 22-1000')      # scan host ports from 22 to 1000
                print nm.scaninfo()
                for host in nm.all_hosts():
                    if 'osclass' in nm[host]:
                        for osclass in nm[host]['osclass']:
                            print('OsClass.type : {0}'.format(osclass['type']))
                            print('OsClass.vendor : {0}'.format(osclass['vendor']))
                            print('OsClass.osfamily : {0}'.format(osclass['osfamily']))
                            print('OsClass.osgen : {0}'.format(osclass['osgen']))
                            print('OsClass.accuracy : {0}'.format(osclass['accuracy']))
                            print('')

                    if 'osmatch' in nm[host]:
                        for osmatch in nm[host]['osmatch']:
                            print('OsMatch.name : {0}'.format(osmatch['name']))
                            print('OsMatch.accuracy : {0}'.format(osmatch['accuracy']))
                            print('OsMatch.line : {0}'.format(osmatch['line']))
                            print('')

                    if 'hostscript' in nm[host]:
                        for hscript in nm[host]['hostscript']:
                            print('HostScript Results : {0}'.format(hscript['output']))
                
                    for proto in nm[host].all_protocols():
                        print('----------')
                        print('Protocol : {0}'.format(proto))
                        print nm[host][proto]

                        if proto == "addresses" or proto == "tcp" or proto == "udp":
                            lport = list(nm[host][proto].keys())
                            lport.sort()
                            for port in lport:
                                print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port]))
                    print nm[host].all_tcp()           # get all ports for tcp protocol (sorted version)
                    print nm[host].all_udp()           # get all ports for udp protocol (sorted version)
                    self.thread_stop.set()
if __name__ == "__main__":
    app = wx.App(False)
    frame = packet_information(None,-1)
    frame.Show()
    app.MainLoop()