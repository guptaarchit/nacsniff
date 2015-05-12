import wx

class packet_information(wx.Frame):
           
    def __init__(self,packet_info_list, *args, **kw):
        wx.Frame.__init__(self, None, -1)
#       
        self.InitUI(packet_info_list)
        
        
    def InitUI(self, packet_info_list):
        dest_mac_addr=wx.StaticText(self,     label='Destination MaC Address', pos=(10,30))
        src_mac_addr=wx.StaticText(self,   label='Source Mac Address', pos=(10,50))
        eth_protocol=wx.StaticText(self, label='Ethernet Protocol', pos=(10,70))
        ip_version=wx.StaticText(self,   label='IP Version', pos=(10,90))
        ihl=wx.StaticText(self,  label='IHL', pos=(10,110))
        ttl=wx.StaticText(self, label='TTL', pos=(10,130))
        source_addr=wx.StaticText(self,    label='Sorurce IP', pos=(10,150))
        dest_addr=wx.StaticText(self,    label='Destination IP', pos=(10,170))
        protocol=wx.StaticText(self,    label='Protocol', pos=(10,190))
        
        font1=wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        y=30
        for count in range(1,10):
            colon=wx.StaticText(self,label=' : ', pos=(240,y))
            colon.SetFont(font1)
            y=y+20

        dest_mac_addr.SetFont(font1)
        src_mac_addr.SetFont(font1)    
        eth_protocol.SetFont(font1)
        ip_version.SetFont(font1)
        ihl.SetFont(font1)
        ttl.SetFont(font1)
        source_addr.SetFont(font1)
        dest_addr.SetFont(font1)
        protocol.SetFont(font1)
        
        font2=wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        
        self.st1 = wx.StaticText(self, label='', pos=(260, 30))
        self.st2 = wx.StaticText(self, label='', pos=(260, 50))
        self.st3 = wx.StaticText(self, label='', pos=(260, 70))
        self.st4 = wx.StaticText(self, label='', pos=(260, 90))
        self.st5 = wx.StaticText(self, label='', pos=(260, 110))
        self.st6 = wx.StaticText(self, label='', pos=(260, 130))
        self.st7 = wx.StaticText(self, label='', pos=(260, 150))
        self.st8 = wx.StaticText(self, label='', pos=(260, 170))
        self.st9 = wx.StaticText(self, label='', pos=(260, 190))
        self.st10 = wx.StaticText(self, label='', pos=(260, 210))
        self.st11 = wx.StaticText(self, label='', pos=(260, 230))
        self.st12 = wx.StaticText(self, label='', pos=(260, 250)) 
        self.st13 = wx.StaticText(self, label='', pos=(260, 270)) 

        self.st1.SetFont(font2)
        self.st2.SetFont(font2)
        self.st3.SetFont(font2)
        self.st4.SetFont(font2)
        self.st5.SetFont(font2)
        self.st6.SetFont(font2)
        self.st7.SetFont(font2)        
        self.st8.SetFont(font2)        
        self.st9.SetFont(font2)        
        self.st10.SetFont(font2)
        self.st11.SetFont(font2)        
        self.st12.SetFont(font2)        
        self.st13.SetFont(font2)        

        x1=packet_info_list['dest_mac_addr']
        x2=packet_info_list['src_mac_addr']
        x3=packet_info_list['eth_protocol']
        x4=packet_info_list['ip_version']
        x5=packet_info_list['ihl']
        x6=packet_info_list['ttl']
        x7=packet_info_list['source_addr']
        x8=packet_info_list['dest_addr']
        x9=packet_info_list['protocol']
        self.st1.SetLabel(str(x1))
        self.st2.SetLabel(str(x2))
        self.st3.SetLabel(str(x3))
        self.st4.SetLabel(str(x4))
        self.st5.SetLabel(str(x5))
        self.st6.SetLabel(str(x6))
        self.st7.SetLabel(str(x7))
        self.st8.SetLabel(str(x8))
        self.st9.SetLabel(str(x9))
        if x9=="TCP":
            source_port=wx.StaticText(self,     label='Source Port', pos=(10,210))
            sequence=wx.StaticText(self,   label='Sequence', pos=(10,230))
            tcp_header_length=wx.StaticText(self, label='TCP Header Length', pos=(10,250))
            #data=wx.StaticText(self, label='Data', pos=(10,270))
            source_port.SetFont(font1)
            sequence.SetFont(font1)    
            tcp_header_length.SetFont(font1)
            #data.SetFont(font1)
            for count in range(1,4):
                colon=wx.StaticText(self,label=' : ', pos=(240,y))
                colon.SetFont(font1)
                y=y+20
            x10=packet_info_list['source_port']
            x11=packet_info_list['sequence']
            x12=packet_info_list['tcp_header_length']
            # x13=packet_info_list['data']
            self.st10.SetLabel(str(x10))
            self.st11.SetLabel(str(x11))
            self.st12.SetLabel(str(x12))
            # self.st13.SetLabel(str(x13))
        
            
        elif x9=="UDP":
            source_port=wx.StaticText(self,     label='Source Port', pos=(10,210))
            dest_port=wx.StaticText(self,     label='Destination Port', pos=(10,230))
            length=wx.StaticText(self,   label='Length', pos=(10,250))
            checksum=wx.StaticText(self, label='Checksum', pos=(10,270))
            #data=wx.StaticText(self, label='Data', pos=(10,270))
            source_port.SetFont(font1)
            sequence.SetFont(font1)    
            tcp_header_length.SetFont(font1)
            dest_port.SetFont(font1)
            
            #data.SetFont(font1)
            for count in range(1,5):
                colon=wx.StaticText(self,label=' : ', pos=(240,y))
                colon.SetFont(font1)
                y=y+20
            x10=packet_info_list['source_port']
            x11=packet_info_list['dest_port']
            x12=packet_info_list['length']
            x13=packet_info_list['checksum']
            # x13=packet_info_list['data']
            self.st10.SetLabel(str(x10))
            self.st11.SetLabel(str(x11))
            self.st12.SetLabel(str(x12))
            self.st13.SetLabel(str(x13))

        elif x9=="ICMP":
            pass

        self.SetSize((500, 400))
        self.SetTitle('Packet Information')
        self.Centre()
        self.Show(True)  
