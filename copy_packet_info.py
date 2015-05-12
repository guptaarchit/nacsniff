import wx

class packet_information(wx.Frame):
           
    def __init__(self,packet_info_list, *args, **kw):
        wx.Frame.__init__(self, None, -1)
#       
        self.InitUI(packet_info_list)
        
        
    def InitUI(self, packet_info_list):

        no=wx.StaticText(self,     label='No.', pos=(10,30))
        time=wx.StaticText(self,   label='Time', pos=(10,50))
        source=wx.StaticText(self, label='Source', pos=(10,70))
        dest=wx.StaticText(self,   label='Destination', pos=(10,90))
        proto=wx.StaticText(self,  label='Length', pos=(10,110))
        length=wx.StaticText(self, label='Protocol', pos=(10,130))
        ttl=wx.StaticText(self,    label='TTL', pos=(10,150))
        
        font1=wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.BOLD)
        y=30
        for count in range(1,8):
            colon=wx.StaticText(self,label=' : ', pos=(150,y))
            colon.SetFont(font1)
            y=y+20

        no.SetFont(font1)
        time.SetFont(font1)    
        source.SetFont(font1)
        dest.SetFont(font1)
        proto.SetFont(font1)
        length.SetFont(font1)
        ttl.SetFont(font1)
        
        font2=wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        
        self.st1 = wx.StaticText(self, label='', pos=(180, 30))
        self.st2 = wx.StaticText(self, label='', pos=(180, 50))
        self.st3 = wx.StaticText(self, label='', pos=(180, 70))
        self.st4 = wx.StaticText(self, label='', pos=(180, 90))
        self.st5 = wx.StaticText(self, label='', pos=(180, 110))
        self.st6 = wx.StaticText(self, label='', pos=(180, 130))
        self.st7 = wx.StaticText(self, label='', pos=(180, 150))
        self.st1.SetFont(font2)
        self.st2.SetFont(font2)
        self.st3.SetFont(font2)
        self.st4.SetFont(font2)
        self.st5.SetFont(font2)
        self.st6.SetFont(font2)
        self.st7.SetFont(font2)
        x1=packet_info_list['protocol']
        
        x2=packet_info_list[1]
        x3=packet_info_list[2]
        x4=packet_info_list[3]
        x5=packet_info_list[4]
        x6=packet_info_list[5]
        x7=packet_info_list[6]
        self.st1.SetLabel(str(x1))
        self.st2.SetLabel(str(x2))
        self.st3.SetLabel(str(x3))
        self.st4.SetLabel(str(x4))
        self.st5.SetLabel(str(x5))
        self.st6.SetLabel(str(x6))
        self.st7.SetLabel(str(x7))

        self.SetSize((600, 600))
        self.SetTitle('Packet Information')
        self.Centre()
        self.Show(True)  


# def view_packet_info(packet_info_list):
#     #print "hsabbkfjasfkjasndkjasndas"
#     ex = wx.App()
#     Example(packet_info_list)
#     ex.MainLoop()    

#if __name__ == "__main__":
#    view_packet_info([1,2,3,4])
