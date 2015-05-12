import wx
import sys
from capture import *
import netifaces
import wx.lib.buttons
from sniffer_socket import *
from help_window import *
from scanner import *
class ListCtrlLeft(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'wxBitmapButton', size=(300, 350))
        self.list1=[]
        capture_image = "images/capture.jpg"
        image1 = wx.Image(capture_image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.capture_button = wx.BitmapButton(parent, id=-1, bitmap=image1,pos=(70, 70), size = (200, 100))
        self.capture_button.Bind(wx.EVT_BUTTON, self.capture)

        interface_image = "images/interface.jpg"
        image2 = wx.Image(interface_image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.interface_button = wx.BitmapButton(parent, id=-1, bitmap=image2,pos=(70, 200), size = (200, 100))
        self.interface_button.Bind(wx.EVT_BUTTON, self.OnSelect)
        self.parent=parent

        scanner_image = "images/scanner.jpg"
        image2 = wx.Image(scanner_image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.interface_button = wx.BitmapButton(parent, id=-1, bitmap=image2,pos=(70, 330), size = (200, 100))
        self.interface_button.Bind(wx.EVT_BUTTON, self.OnScannerSelect)
        self.parent=parent

    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-5)
        event.Skip()

    def OnScannerSelect(self, event):
        self.scan_initiater = scanner_window(None,-1, 'Online Hosts',"lo")
        self.scan_initiater.Show()

    def OnSelect(self, event):
        window = self.parent.GetGrandParent().FindWindowByName('interface_list')
        window.LoadData()

    def OnDeSelect(self, event):
        index = event.GetIndex()
        self.SetItemBackgroundColour(index, 'WHITE')

    def OnFocus(self, event):
        self.SetItemBackgroundColour(0, 'red')

    def capture(self, event):
        window = self.parent.GetGrandParent().FindWindowByName('interface_list')
        interface_selected=window = window.OnSelect1()
        print interface_selected    
  
    def OnQuit(self, e):    #to quit the program through menu item in file menu
        self.Close()
        # if 'scan_initiater' in locals():
        self.scan_initiater.Close()

class interface_list(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
        #self.listbox = wx.ListBox(parent, id)
        self.parent = parent
        self.interface_list=[]
        self.selection=""

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selected_interface)

        self.InsertColumn(0, '')

    def selected_interface(self,event):
        index = event.GetIndex()
        self.selection=self.interface_list[len(self.interface_list)-index-1]
        print self.selection

    def OnSelect1(self):
        if self.selection != "":
            self.capture_frame = Nacsnif(self,-1, 'nacsnif',self.selection)
            self.capture_frame.Show()
        else:
            pass  #Add warning window        

    def OnSize(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x-5)
        event.Skip()

    def LoadData(self):
        
        self.DeleteAllItems()
        list2=netifaces.interfaces()
        for item in list2:
            self.InsertStringItem(0,item)
            self.interface_list.append(item)

    def OnQuit(self, e):    #to quit the program through menu item in file menu
        self.Close()
        self.capture_frame.Close()

class Reader(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(700,600))
        disp_menu_bar(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(splitter, -1)
        panel1.SetBackgroundColour('blue')
        panel11 = wx.Panel(panel1, -1, size=(-1, 240))
        panel11.SetBackgroundColour('BLUE')
        st1 = wx.StaticText(panel11, -1, 'CAPTURE', (135, 5))
        st1.SetForegroundColour('WHITE')

        panel12 = wx.Panel(panel1, -1, style=wx.BORDER_SUNKEN)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.list1 = ListCtrlLeft(panel12, -1)

        vbox.Add(self.list1, 1, wx.EXPAND)
        panel12.SetSizer(vbox)
        #panel12.SetBackgroundColour('green')


        vbox1.Add(panel11, 0, wx.EXPAND)
        vbox1.Add(panel12, 1, wx.EXPAND)

        panel1.SetSizer(vbox1)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(splitter, -1)
        panel21 = wx.Panel(panel2, -1, size=(-1, 40), style=wx.NO_BORDER)
        st2 = wx.StaticText(panel21, -1, 'INTERFACES', (135, 5))
        st2.SetForegroundColour('WHITE')
        panel21.SetBackgroundColour('BLUE')
        panel22 = wx.Panel(panel2, -1, style=wx.BORDER_RAISED)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        self.list2 = interface_list(panel22, -1)
        self.list2.SetName('interface_list')
        vbox3.Add(self.list2, 1, wx.EXPAND)
        panel22.SetSizer(vbox3)


        panel22.SetBackgroundColour('WHITE')
        vbox2.Add(panel21, 0, wx.EXPAND)
        vbox2.Add(panel22, 1, wx.EXPAND)
        
        panel2.SetSizer(vbox2)
        
        #tool_obj=Toolbar()
        #tool_obj.toolbar_icons()
        self.toolbar_icons()
        hbox.Add(splitter, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        self.SetSizer(hbox)
        self.CreateStatusBar()
        splitter.SplitVertically(panel1, panel2)
        self.Centre()
        self.Show(True)

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

        self.Bind(wx.EVT_TOOL, self.OnQuit, id=1)
        self.Bind(wx.EVT_TOOL, self.OnUndo, id=9)
        self.Bind(wx.EVT_TOOL, self.OnRedo, id=10)
    	self.Bind(wx.EVT_TOOL,self.OnHelp,id=2)
 
            
    def OnQuit(self, e):    #to quit the program through menu item in file menu
        self.list1.Close()
        self.list2.Close()
        #
        #self.l.OnClose()
        self.Close()
    def OnHelp(self,e):
        self.l=HelpWindow(None, -1, 'HelpWindow')

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

    def OnSave(self, e):
        pass
	
	def OnOpen(self, e):
		pass

def disp_menu_bar(tempo):
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
    #tempo.Bind(wx.EVT_MENU,tempo.OnOpen,open_item)
    # wx.EVT_MENU(tempo,101,tempo.OnSave )

app = wx.App()
#app.setStyle('cleanlooks')
#sys.stderr=open("test.txt")
Reader(None, -1, 'NACSNIFF')
app.MainLoop()