import wx

class Filterdialog(wx.Dialog):
    
    def __init__(self, *args, **kw):
        super(Filterdialog, self).__init__(*args, **kw) 
            
        self.InitUI()
        self.SetSize((350, 300))
        self.SetTitle("Set Filter")
        
        
    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Set Filter')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL) 
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
        option = wx.StaticText(pnl,label="Filter Option:")
        hbox1.Add(option)
        self.filter_option = wx.TextCtrl(pnl,wx.ID_ANY, size=(200,30))
        hbox1.Add(self.filter_option, flag=wx.CENTER, border=5)

        sbs.Add(hbox1)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        option2 = wx.StaticText(pnl,label="Filter String: " )
        hbox3.Add(option2)
        self.filter_string = wx.TextCtrl(pnl,wx.ID_ANY, size=(200,30))
        hbox3.Add(self.filter_string, flag=wx.CENTER, border=5)
        sbs.Add(hbox3)
        
        pnl.SetSizer(sbs)
       
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, 
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, 
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        
        # print hbox3.GetItem(0)
        
    def OnClose(self, e):
        print self.filter_option.GetValue() , self.filter_string.GetValue()
        self.Destroy()

    def GetFilterValue(self):
        return self.filter_option.GetValue(),self.filter_string.GetValue()
class Example(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
            
        self.InitUI()
        
        
    def InitUI(self):    
    
        ID_DEPTH = wx.NewId()

        self.SetSize((300, 200))
        self.SetTitle('Custom dialog')
        self.Centre()
        self.Show(True)
        chgdep = Filterdialog(None, 
            title='Change Color Depth')
        chgdep.ShowModal()
        chgdep.Destroy()        
        
        
    def OnChangeDepth(self, e):
        
        chgdep = Filterdialog(None, 
            title='Change Color Depth')
        chgdep.ShowModal()
        chgdep.Destroy()        


def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()