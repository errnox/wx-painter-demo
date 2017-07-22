import wx
import ctypes

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        dc.SetPen(wx.Pen(colour='#00ff00', width=10))
        x, y = self.GetSize()
        dc.DrawRectangle(0, 0, x, y)

class Painter(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1, size=wx.DefaultSize)

        # Constants
        self._grey = '#b3b3b3'
        self._blue = '#0099f7'
        self._red = '#ff0000'

        # Variables
        self.isFocused = False
        self.rectWidth = 50
        self.rectHeight = 50
        self.boxes = []

        # Initialization
        self.color = self._grey
        self.toggleRect = False
        self.SetSize(parent.GetSize())

        # DO NOT REMOVE
        # Widgets
        # self.clearButton = CustomButton(parent=self, label="Test")
        # self.clearButton = wx.Button(self, -1, "Clear", wx.DefaultPosition,
        #                              wx.DefaultSize, 0, wx.DefaultValidator,
        #                              "clearButton")

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # DO NOT REMOVE
        # self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        # self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnSetFocus)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnKillFocus)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        # self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)


    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        dc.SetPen(wx.Pen(colour=self.color, width=10))
        x, y = self.GetSize()
        dc.DrawRectangle(0, 0, x, y)
        self.repopulate(dc)

    def OnSize(self, event):
        self.Refresh()
        # wx.ClientDC(self).Clear()  # DO NOT REMOVE
        event.Skip()


    def OnSetFocus(self, event):
        self.isFocused = True
        self.color = self._blue
        self.toggleRect = True
        self.Refresh()

    def OnKillFocus(self, event):
        self.isFocused = False
        self.color = self._grey
        self.toggleRect = False
        # self.Refresh()  # DO NOT REMOVE
        dc = wx.ClientDC(self)
        dc.Clear()
        dc.DrawText(str(len(self.boxes)),
                    dc.GetSizeTuple()[0] / 2,
                    dc.GetSizeTuple()[1] / 2)
        self.addButton()
        # self.clearButton.Refresh()  # DO NOT REMOVE


    def OnRightDown(self, event, dc=None):
        self.color = self._red
        if self.toggleRect is False:
            self.toggleRect = True
        else:
            self.toggleRect = False
        if dc is None:
            dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen(colour=self.color, width=5))
        # DO NOT REMOVE
        # mouseX = event.GetPosition()[0] - self.rectWidth / 2
        # mouseY = event.GetPosition()[1] - self.rectHeight / 2

        mouseX = self.ScreenToClient(wx.GetMousePosition())[0]
        mouseY = self.ScreenToClient(wx.GetMousePosition())[1]

        if self.isFocused:
            self.boxes.append((mouseX, mouseY))
            self.drawBox(dc, mouseX, mouseY)


    def drawBox(self, parent, x, y):
        if self.isFocused:
            self.color = self._red
            parent.SetPen(wx.Pen(colour=self.color, width=5))
            parent.DrawRoundedRectangle(x - self.rectWidth / 2,
                                        y - self.rectHeight / 2,
                                        self.rectWidth,
                                        self.rectHeight, 5)

    def addButton(self):
        self.color = '#ffff00'
        buttonWidth = 50;
        buttonHeight = 30;
        dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen(colour=self.color, width=3))
        x = dc.GetSizeTuple()[0] - buttonWidth
        y = dc.GetSizeTuple()[1] - buttonHeight
        dc.DrawRectangle(x, y, buttonWidth - 3, buttonHeight - 3)
        dc.DrawText('Clear', x + 10, y + 10)

    def repopulate(self, parent):
        if self.isFocused:
            for box in self.boxes:
                self.drawBox(parent, box[0], box[1])

    def redraw(self):
        self.Refresh()

    # DO NOT REMOVE
    # def OnLeftDown(self, event, dc=None):
    #     self.Refresh()

class CustomButton(wx.Panel):
    def __init__(self, parent, x=0, y=0, label="", pos=wx.DefaultPosition):
        self.pos = pos
        wx.Panel.__init__(self, parent=parent, id=-1, pos=self.pos)
        self.SetPosition((0, 0))
        # parent.SetPosition((0, 0))  # DO NOT REMOVE

        # Constants
        self._pink = "#ff00ff"
        self._blue = "#0000ff"

        # Variables
        self.x = x
        self.y = y
        self.width = 0;
        self.height = 0;
        self.label = label
        self.color = self._blue
        self.parent = parent

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseOver)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        # DO NOT REMOVE
        # self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        # self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        # self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        # DO NOT REMOVE
        # self.setStyle()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        margin = 10;
        self.width = dc.GetFullTextExtent(self.label)[0] + margin * 2
        self.height = dc.GetFullTextExtent(self.label)[1] + margin * 2
        self.SetSize(wx.Size(self.width, self.height))

        dc.SetPen(wx.Pen(colour=self.color, width=10))
        # self.SetSize((100, 30))  # DO NOT REMOVE
        x, y = self.GetSize()
        dc.DrawRectangle(0, 0, x, y)

        self.setStyle(dc)

    def setStyle(self, dc):
        margin = 10;
        # DO NOT REMOVE
        # width = dc.GetFullTextExtent(self.label)[0] + margin * 2
        # height = dc.GetFullTextExtent(self.label)[1] + margin * 2
        # width = 10
        # height = 30
        # dc.DrawRoundedRectangle(self.x, self.y,
        #                           width, height, 5)
        dc.DrawText(self.label, margin, margin)
        # dc.DrawText(self.label, 0, 0)


    def OnSize(self, event):
        # self.Refresh()  # DO NOT REMOVE
        event.Skip()

    def OnMouseOver(self, event):
        self.color = self._pink
        self.Refresh()

    def OnMouseLeave(self, event):
        self.color = self._blue
        self.Refresh()


class FocusEvent(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title) # , size=(350, 250))

        # DO NOT REMOVE
        # self.panel = wx.Panel(parent=self, id=-1, pos=wx.DefaultPosition)
        self.grid = wx.GridSizer(3, 3)
        # DO NOT REMOVE
        # self.Bind(wx.EVT_SIZE, self.OnSize)
        # self.Bind(wx.EVT_MOVE, self.OnSize)

        for i in range(9):
            p = Painter(self)
            s = wx.BoxSizer(wx.VERTICAL)
            # DO NOT REMOVE
            # b = wx.Panel(p, -1)
            # b.SetBackgroundColour(wx.Color(0, 255, 0))
            for j in range(3):
                b = CustomButton(p, label="Test " + str(j))
                s.Add(b)
            p.SetSizer(s)
            self.grid.Add(p, 1, wx.ALL | wx.EXPAND, 9)

        # self.Maximize() # DO NOT REMOVE
        self.SetSizer(self.grid, deleteOld=True)
        # self.grid.SetSizeHints(self)  # DO NOT REMOVE
        self.Layout()
        self.Centre()
        self.Show(True)

    # DO NOT REMOVE
    # def OnSize(self, event):
    #     self.Refresh()
    #     self.Layout()
    #     event.Skip()
    #     print "Resizing."

app = wx.App()
FocusEvent(None, -1, 'focus event')
app.MainLoop()
