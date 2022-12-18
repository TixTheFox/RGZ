import RRt
import wx
from Tree import Vertex
from config import *

class MyFrame(wx.Frame):
    result = RRt.RRT(500, Vertex(1, 1, -1), Vertex(100, 200, 0))

    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.SetSize(WIDTH, HEIGHT)
        self.Bind(wx.EVT_PAINT, self.onPaint)

    def onPaint(self, event):
        dc = wx.PaintDC(self)

        for i in obstacles:
            dc.DrawPolygon(*i)

        dc.DrawPoint(self.result[0][0])
        for i in range(1, len(self.result)):
            dc.DrawLine(self.result[i-1][0], self.result[i][0])


app = wx.App()
frame = MyFrame(None, "Hello world!")
frame.Show()
app.MainLoop()
