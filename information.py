import wx

class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
        
        self.InitUI()
        
        
    def InitUI(self):

        text=wx.StaticText(self, label='nacsniff', pos=(260,20))
        underline=wx.StaticText(self, label='-----------', pos=(258,31))
        font=wx.Font(20,wx.DECORATIVE,wx.ITALIC,wx.BOLD)
        text.SetFont(font)
        underline.SetFont(font)
        font1=wx.Font(11,wx.DECORATIVE,wx.NORMAL,wx.NORMAL)
        self.st1 = wx.StaticText(self, label='', pos=(0, 80))
        self.st1.SetFont(font1)
        
        self.SetSize((670, 400))
        self.SetTitle('Information')
        self.Centre()
        self.Show(True)
        info='''
        nacsniff is a simple network packet analyzer and scanner. It is a sniffer (also
        known as a network analyzer) that looks at network traffic, decode it, and give
        meaningful data that a network administrator uses to diagnose problems on the
        network. It is also a tool for network exploration. It can be used to determine
        what hosts are available on the network, what services (application name and
        version) those hosts are offering, what operating systems (and OS versions) they
        are running, what type of packet filters/firewalls are being used, and dozens of
        other characteristics.
        It can be used to find what computers on the network are causing problems such
        as using too much bandwidth, having the wrong network settings or running
        malware."
        '''
        self.st1.SetLabel(info)

def info_view():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

