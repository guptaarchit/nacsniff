import wx
import threading
import scan
from host_info import *
import nmap
import math
from datetime import datetime
import os
from wx.lib.mixins.listctrl import ColumnSorterMixin
from time import sleep
import sys 
import logging

LOG_FILENAME = 'host_info_log.out'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.INFO,
                    )

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


class host_information(wx.Frame):
           
    def __init__(self,host_address ,*args, **kw):
        wx.Frame.__init__(self, None, -1)
        self.SetSize((600, 500))
        self.SetTitle('Host Information')
        self.Centre()
        self.host = host_address
 
        self.port_list = []
        panel = wx.Panel(self, wx.ID_ANY)
        log = wx.TextCtrl(panel, wx.ID_ANY, size=(300,400),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        btn = wx.Button(panel, wx.ID_ANY, 'Start!')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(log, 0, wx.ALL|wx.EXPAND)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER)
        panel.SetSizer(sizer)

        self.redir=RedirectText(log)
        # sys.stdout=self.redir

        self.Bind(wx.EVT_BUTTON, self.onButton, btn)
        self.Show(True)  

    def onButton(self, event):        
        print "You pressed the button!"
        self.OnStart(self.host)

    def OnStart(self,host):
        self.thread_stop = threading.Event()
        self.thread = threading.Thread(target=self.new ,args=(host,self.thread_stop))
        self.thread.setDaemon(True)
        self.thread.start()
        print "started"
        # self.thread_stop.wait()
        # self.view()

    def new(self,arg,stop_event):
        # Need to do this better
        if (not stop_event.is_set()):
            sleep(1)
            wx.CallAfter(self.get_port_scan,self.host,self.thread_stop)
            # self.thread_stop.set()

    def view(self,ret_str):
        self.thread_stop.set()
        self.redir.write(ret_str)
        # for item in self.port_list :
        #     self.redir.write(str(item[0]))
        #     self.redir.write(str(item[1]))

            # port=wx.StaticText(self,label='Port : ', pos=(port_x_pos,port_y_pos)) 
            # port.SetFont(font1)
            # self.st1 = wx.StaticText(self, label=str(item[0]), pos=(port_x_pos+60, port_y_pos))
            # port_x_pos+=200
            # self.st2 = wx.StaticText(self, label=str(item[1]), pos=(port_x_pos+20, port_y_pos))
            # port_y_pos+=25
            # port_x_pos=20

    def get_port_scan(self,host,stop_event):
        ret_str = ""
        if not stop_event.is_set():
            nm = nmap.PortScanner()
            if (os.getuid() == 0):
                print "Doing OS scan"
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
                            ret_str = ret_str + 'OsClass.type: ' + osclass['type'] +"\n"+ 'OsClass.vendor :' + osclass['vendor'] + '\n'+ 'OsClass.osgen :'+ osclass['osgen'] + "\n"
                            logging.info(ret_str)
                    if 'osmatch' in nm[host]:
                        for osmatch in nm[host]['osmatch']:
                            print('OsMatch.name : {0}'.format(osmatch['name']))
                            print('OsMatch.accuracy : {0}'.format(osmatch['accuracy']))
                            print('OsMatch.line : {0}'.format(osmatch['line']))
                            print('')
                            ret_str = ret_str + 'OsMatch.name :' + osmatch['name'] + "\n"
                            logging.info(ret_str)
                    if 'hostscript' in nm[host]:
                        for hscript in nm[host]['hostscript']:
                            print('HostScript Results : {0}'.format(hscript['output']))
                            ret_str = ret_str + hscript['output'] + "\n"
                            logging.info(ret_str)
                    if 'uptime' in nm[host]:
                        ret_str = ret_str + 'Last Boot: '+ nm[host]['uptime']['lastboot'] +"\n"
                        logging.info(ret_str)
                    for proto in nm[host].all_protocols():
                        print('----------')
                        print('Protocol : {0}'.format(proto))
                        print nm[host][proto]
                        logging.info(nm[host][proto])
                        # if proto == "addresses" or proto == "tcp" or proto == "udp":
                        #     lport = list(nm[host][proto].keys())
                        #     lport.sort()
                        #     for port in lport:
                        #         print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port]))
                        #         ret_str = ret_str + 'port : ' + str(port) + " " + 'state : '+ str(nm[host][proto][port]) + "\n"
                        #         print "here"


                        if proto == "tcp" or proto == "udp":
                            lport = list(nm[host][proto].keys())
                            lport.sort()
                            for port in lport:
                                self.port_list.append((port,nm[host][proto][port]['product']))
                                ret_str = ret_str + 'Port : ' + str(port) + " " + 'state : '+ str(nm[host][proto][port]) + "\n"\
                                + "Name: " + nm[host][proto][port]['name'] + "\n" + 'Product: ' + ' ' + nm[host][proto][port]['product'] + "\n"
                                logging.info(ret_str)
                            print self.port_list

                    print nm[host].all_tcp()           # get all ports for tcp protocol (sorted version)
                    print nm[host].all_udp()           # get all ports for udp protocol (sorted version)
            
            self.view(ret_str)

    def get_port_scan_(self,host):
        ret_str = ""
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
                        ret_str = ret_str + 'OsClass.type: ' + osclass['type'] +"\n"+ 'OsClass.vendor :' + osclass['vendor'] + '\n'+ 'OsClass.osgen :'+ osclass['osgen'] + "\n"

                if 'osmatch' in nm[host]:
                    for osmatch in nm[host]['osmatch']:
                        print('OsMatch.name : {0}'.format(osmatch['name']))
                        print('OsMatch.accuracy : {0}'.format(osmatch['accuracy']))
                        print('OsMatch.line : {0}'.format(osmatch['line']))
                        print('')
                        ret_str = ret_str + 'OsMatch.name :' + osmatch['name'] + "\n"

                if 'hostscript' in nm[host]:
                    for hscript in nm[host]['hostscript']:
                        print('HostScript Results : {0}'.format(hscript['output']))
                        ret_str = ret_str + hscript['output'] + "\n"
                
                if 'uptime' in nm[host]:
                    ret_str = ret_str + 'Last Boot: '+ nm[host]['lastboot'] +"\n"

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

if __name__ == "__main__":
    app = wx.App(False)
    frame = host_information('172.16.100.47')
    frame.Show()
    app.MainLoop()