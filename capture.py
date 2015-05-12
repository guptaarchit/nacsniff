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
from separate_dialog import Filterdialog

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

class Nacsnif(wx.Frame):
    def __init__(self, parent, id, title,arg):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, id, title, size=(1000, 600))
        self.interface_name=arg
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1)

        display_menu_bar(self)

        self.list = SortedListCtrl(panel)
        self.list.InsertColumn(0, 'No.', width=100)
        self.list.InsertColumn(1, 'Time', width=130)
        self.list.InsertColumn(2,'Source',width=130)
        self.list.InsertColumn(3,'Destination',width=130)
        self.list.InsertColumn(4,'Length',width=130)
        self.list.InsertColumn(5,'Protocol',width=130)
        self.list.InsertColumn(6,'TTL',width=130)
              
        
        # self.start()
        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)
        self.toolbar_icons()
        self.Centre()
        self.Show(True)  
        self.sniffer_obj = sniffer(arg)
        self.sniffer_obj.event_packet_is_received += self.handle_ip_packet

        self.data_store = datamanager()
        self.dirname = ''
        #self.list.SetSelection(0)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelection)        # self.start(self.sniffer_obj)
        # self.sniffer_obj.start()
        self.has_filter = False
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
        self.Bind(wx.EVT_TOOL, self.OnOpen, id=3)
        self.Bind(wx.EVT_TOOL,self.OnHelp,id=2)
        self.Bind(wx.EVT_TOOL,self.Onfilter,id=5)

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
        self.sniffer_obj.close()
        print "Capture Window Closed"
        self.list.OnQuit(e)
        # if self.packet_info != None:
        #     self.packet_info.Close()
        #self.On
        self.Close()

    def OnStart(self,event):
        self.thread_stop = threading.Event()
        self.thread = threading.Thread(target=self.new ,args=(1,self.thread_stop))
        self.thread.setDaemon(True)
        self.thread.start()
        print "started"

    def OnSelection(self,e):
        index = e.GetIndex()
        #k=self.list.GetItemText(index)
        values0=self.list.GetItem(itemId=index,col=0)
        # values1=self.list.GetItem(itemId=index,col=1)
        # values2=self.list.GetItem(itemId=index,col=2)

        if int(values0.GetText()) in self.data_store.packet_list:
            print "yeah",values0.GetText()
            ip_packet = self.data_store.packet_list[int(values0.GetText())]
            data_array = {}
            data_array['dest_mac_addr'] = ip_packet.dest_mac_addr
            data_array['src_mac_addr'] = ip_packet.src_mac_addr
            data_array['eth_protocol'] = ip_packet.eth_protocol
            data_array['ip_version'] = ip_packet.ip_version
            data_array['ihl'] = ip_packet.ihl
            data_array['ttl'] = ip_packet.ttl
            data_array['source_addr'] = ip_packet.source_addr
            data_array['dest_addr'] = ip_packet.dest_addr
            proto = ip_packet.getprotocol()
            data_array['protocol'] = proto
            if proto == "TCP":
                tcp_packet = ip_packet.handletcppacket()
                data_array['source_port'] = tcp_packet.source_port
                data_array['sequence'] = tcp_packet.sequence
                data_array['tcp_header_length'] = tcp_packet.tcp_header_length
                data_array['data'] = tcp_packet.data
            
                #data_array['acknowledgement'] = data_array.acknowledgement

            elif proto == "UDP":
                udp_packet = ip_packet.handleudp()
                data_array['source_port'] = udp_packet.source_port
                data_array['dest_port'] = udp_packet.dest_port
                data_array['length'] = udp_packet.length
                data_array['checksum'] = udp_packet.checksum
                
            elif proto == "ICMP":
                pass

        self.packet_info = packet_information(data_array)
        self.packet_info.Show()
    def OnHelp(self,e):
        #app = wx.App()
        self.l=HelpWindow(None, -1, 'HelpWindow')
        #app.MainLoop()


    def OnStop(self,event):
        self.thread_stop.set()

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
        # Need to do this better
        while (not stop_event.is_set()):
            # print "Here"

            time.sleep(1)
            wx.CallAfter(self.capture)

        # wx.CallAfter(self.sniffer_obj.close)
    def Onfilter(self,event):
        appfilter = Filterdialog(None, 
            title='Apply Filter')
        appfilter.ShowModal()
        self.filter_option,self.filter_string = appfilter.GetFilterValue()
        appfilter.Destroy()
        self.has_filter=True

    def filter(self,filter_option,filter_string,packet):
        if isinstance(packet,ipv4datagram):
            print filter_option,packet.dict.keys()
            if filter_option in packet.dict.keys():
                print packet.dict[filter_option],filter_string
                if str(packet.dict[filter_option]) == str(filter_string):
                    return True
                else:
                    return False
            else:
                print "Not Found\n"
                return False

    def capture(self):
        self.sniffer_obj.running=True
        self.sniffer_obj.start_promisc()
        input_list = [self.sniffer_obj.sock,sys.stdin]
        inputready,outputready,exceptready = select.select(input_list,[],[])
        for s in inputready:
            if s == self.sniffer_obj.sock:
                try:
                    packet = self.sniffer_obj.sock.recvfrom(65565);    
                except socket.timeout, e:
                    err = e.args[0]
                    if err == 'timed out':
                        sleep(1)
                        print 'recv timed out, retry later'
                        continue
                    else:
                        print e
                        # continue
                        sys.exit(1)
                except socket.error, e:
                    print e
                    sys.exit(1)
                else:
                    # forward packet
                    sender = packet[0]
                    packet = packet[0]

                    dest_mac, source_mac, eth_protocol = self.sniffer_obj.parse_ethernet_header(packet)
                    # self.sniffer_obj.packetisreceived(eth_protocol)
                    #str(serial)
                    
                    if eth_protocol == 8:
                        print "IP Packet"
                        self.sniffer_obj.parse_ip_packet(packet)
                        ip_packet = ipv4datagram(source_mac,dest_mac,eth_protocol,packet)
                        if self.has_filter:
                            val = self.filter(self.filter_option,self.filter_string,ip_packet)
                            print "Filter Value \n\n",val
                            if val:
                                self.data_store.add_packet(ip_packet)
                                data_ = {1: (str(ip_packet.id),str(time.clock()),str(ip_packet.source_addr),str(ip_packet.dest_addr),str(len(ip_packet.data)),ip_packet.getprotocol(),str(ip_packet.ttl))}  
                                items = data_.items()

                                for key, data in items:
                                    index = self.list.InsertStringItem(sys.maxint, data[0])
                                    self.list.SetStringItem(index, 1, data[1])
                                    self.list.SetStringItem(index, 2, data[2])
                                    self.list.SetStringItem(index, 3, data[3])
                                    self.list.SetStringItem(index, 4, data[4])
                                    self.list.SetStringItem(index, 5, data[5])
                                    self.list.SetStringItem(index, 6, data[6])
                        else:
                            self.data_store.add_packet(ip_packet)
                            data_ = {1: (str(ip_packet.id),str(time.clock()),str(ip_packet.source_addr),str(ip_packet.dest_addr),str(len(ip_packet.data)),ip_packet.getprotocol(),str(ip_packet.ttl))}  
                            items = data_.items()

                            for key, data in items:
                                index = self.list.InsertStringItem(sys.maxint, data[0])
                                self.list.SetStringItem(index, 1, data[1])
                                self.list.SetStringItem(index, 2, data[2])
                                self.list.SetStringItem(index, 3, data[3])
                                self.list.SetStringItem(index, 4, data[4])
                                self.list.SetStringItem(index, 5, data[5])
                                self.list.SetStringItem(index, 6, data[6])
                        
                        # ip_packet.parse_ip_packet(packet)
                        #fire event
                        #print "ip packet",ip_packet
                        self.sniffer_obj.packetisreceived(ip_packet)
                        # break
                        # continue
            if s  == sys.stdin:
                dummy = sys.stdin.readline()
                running = False
            else:
                continue

        # self.sniffer_obj.close_promisc()
        # self.sniffer_obj.sock.close()
        # print "Out"

    def open_packets(self,event):
        list_packets = self.data_store.readfile(None)

        for packet in list_packets:
            dest_mac, source_mac, eth_protocol = self.sniffer_obj.parse_ethernet_header(packet)
            if eth_protocol == 8:
                print "Loading IP Packet"
                # self.sniffer_obj.parse_ip_packet(packet)
                ip_packet = ipv4datagram(source_mac,dest_mac,eth_protocol,packet)
                self.data_store.add_packet(ip_packet)
                data_ = {1: (str(ip_packet.id),str(time.clock()),str(ip_packet.source_addr),str(ip_packet.dest_addr),str(eth_protocol),ip_packet.getprotocol(),str(ip_packet.ttl))}  
                items = data_.items()
                for key, data in items:
                    index = self.list.InsertStringItem(sys.maxint, data[0])
                    self.list.SetStringItem(index, 1, data[1])
                    self.list.SetStringItem(index, 2, data[2])
                    self.list.SetStringItem(index, 3, data[3])
                    self.list.SetStringItem(index, 4, data[4])
                    self.list.SetStringItem(index, 5, data[5])
                    self.list.SetStringItem(index, 6, data[6])


    def OnOpen(self,e):
        # In this case, the dialog is created within the method because
        # the directory name, etc, may be changed during the running of the
        # application. In theory, you could create one earlier, store it in
        # your frame object and change it when it was called to reflect
        # current parameters / values
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*|*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()

            filehandle=open(os.path.join(self.dirname, self.filename),'rb')
            print os.path.join(self.dirname, self.filename)
            list_packets = self.data_store.readfile(filehandle)
            
            #self.control.SetValue(filehandle.read())

        dlg.Destroy()
        

        for packet in list_packets:
            dest_mac, source_mac, eth_protocol = self.sniffer_obj.parse_ethernet_header(packet)
            if eth_protocol == 8:
                print "Loading IP Packet"
                # self.sniffer_obj.parse_ip_packet(packet)
                ip_packet = ipv4datagram(source_mac,dest_mac,eth_protocol,packet)
                self.data_store.add_packet(ip_packet)
                data_ = {1: (str(ip_packet.id),str(time.clock()),str(ip_packet.source_addr),str(ip_packet.dest_addr),str(eth_protocol),ip_packet.getprotocol(),str(ip_packet.ttl))}  
                items = data_.items()
                for key, data in items:
                    index = self.list.InsertStringItem(sys.maxint, data[0])
                    self.list.SetStringItem(index, 1, data[1])
                    self.list.SetStringItem(index, 2, data[2])
                    self.list.SetStringItem(index, 3, data[3])
                    self.list.SetStringItem(index, 4, data[4])
                    self.list.SetStringItem(index, 5, data[5])
                    self.list.SetStringItem(index, 6, data[6])

            filehandle.close()

    def OnReload(self,e):
        # self.sniffer_obj.close()
        self.list.DeleteAllItems()

    def handle_ip_packet(self,sender,earg):
        print "In Handler"
        if isinstance(earg,ipv4datagram):
            # print earg.dest_mac_addr
            pass
    

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
    tempo.Bind(wx.EVT_MENU,tempo.OnOpen,open_item)
    # wx.EVT_MENU(tempo,101,tempo.OnSave )

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
