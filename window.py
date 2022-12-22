import RRt
import wx
import SaveAndLoad
from Tree import Vertex, Tree
from config import *


OBST_BUTTON = wx.NewIdRef()
START_BUTTON = wx.NewIdRef()
END_BUTTON = wx.NewIdRef()
EXEC_RRT_BUTTON = wx.NewIdRef()
SET_ITER_BUTTON = wx.NewIdRef()
SAVE_BUTTON = wx.NewIdRef()
LOAD_BUTTON = wx.NewIdRef()
CLEAR_BUTTON = wx.NewIdRef()

BUTTON_SIZE = wx.Size(150, 50)

obstacles = []


def convert_for_RRT_usage(array):
    return [[Vertex(*(i.Get())) for i in j] for j in array]


class MyFrame(wx.Frame):
    def __init__(self, parent, title):

        super().__init__(parent, title=title, size=(WIDTH + 500, HEIGHT + 20))
        self.SetBackgroundColour("WHITE")
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.pos = []
        self.starting_point, self.exit_point = 0, 0
        self.getting_position_for_obs = False
        self.getting_position_for_points = [False, False]
        self.rrt_result, self.rrt_tree = 0, 0
        self.iter_num = 0
        fg = wx.BoxSizer(wx.VERTICAL)

        define_obstacle_button = wx.Button(self, OBST_BUTTON, label="Add triangle", size=BUTTON_SIZE)
        define_obstacle_button.Bind(wx.EVT_BUTTON, self.addObstacle)

        define_start_button = wx.Button(self, START_BUTTON, label="Add Start point", size=BUTTON_SIZE)
        define_start_button.Bind(wx.EVT_BUTTON, self.addPoint)

        define_end_button = wx.Button(self, END_BUTTON, label="Add End point", size=BUTTON_SIZE)
        define_end_button.Bind(wx.EVT_BUTTON, self.addPoint)

        execute_rrt = wx.Button(self, EXEC_RRT_BUTTON, label="Find Path", size=BUTTON_SIZE)
        execute_rrt.Bind(wx.EVT_BUTTON, self.executeRRT)

        set_iter_text_bar = wx.StaticText(self, label="Enter algorithm\niteration  number")
        self.set_iter_text_ctrl = wx.TextCtrl(self, size=(100, 30))

        bg1 = wx.BoxSizer(wx.HORIZONTAL)
        bg1.AddMany([(set_iter_text_bar, 0, wx.RIGHT, 5), (self.set_iter_text_ctrl, 0, wx.LEFT, 5)])

        set_iter_button = wx.Button(self, SET_ITER_BUTTON, label="Enter", size=(100, 30))
        set_iter_button.Bind(wx.EVT_BUTTON, self.setIter)

        save_button = wx.Button(self, SAVE_BUTTON, label="Save", size=(75, 25))
        save_button.Bind(wx.EVT_BUTTON, self.save_map)

        load_button = wx.Button(self, LOAD_BUTTON, label="Load", size=(75, 25))
        load_button.Bind(wx.EVT_BUTTON, self.load_map)

        bg2 = wx.BoxSizer(wx.HORIZONTAL)
        bg2.AddMany([(save_button, 0, wx.RIGHT, 5), (load_button, 0, wx.LEFT, 5)])

        clear_button = wx.Button(self, CLEAR_BUTTON, label="Clear Scene", size=(75, 25))
        clear_button.Bind(wx.EVT_BUTTON, self.clear_map)

        fg.Add(define_start_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
        fg.Add(define_end_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
        fg.Add(define_obstacle_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
        fg.Add(execute_rrt, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
        fg.Add(bg1, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
        fg.Add(set_iter_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
        fg.Add(bg2, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)
        fg.Add(clear_button, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 20)

        self.SetSizer(fg)

        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)

    def addObstacle(self, event):
        self.getting_position_for_obs = True
        event.Skip()

    def addPoint(self, event):
        if event.GetEventObject().GetId() == START_BUTTON:
            self.getting_position_for_points[0] = True
        else:
            self.getting_position_for_points[1] = True
        event.Skip()

    def onLeftDown(self, event):
        current_pos = event.GetPosition()
        if self.getting_position_for_obs:
            self.pos.append(current_pos)
            if len(self.pos) == 3:
                obstacles.append(self.pos.copy())
                self.Refresh()
                self.pos.clear()
                self.getting_position_for_obs = False
        if any(self.getting_position_for_points):
            if self.getting_position_for_points[0]:
                self.starting_point = current_pos
                self.getting_position_for_points[0] = False
            else:
                self.exit_point = current_pos
                self.getting_position_for_points[1] = False
            self.Refresh()
            self.pos = []

        event.Skip()

    def executeRRT(self, event):
        if self.starting_point and self.exit_point:

            self.rrt_result, self.rrt_tree = RRt.RRT(self.iter_num, Vertex(*(self.starting_point.Get())),
                                                     Vertex(*(self.exit_point.Get())),
                                                     convert_for_RRT_usage(obstacles)
                                                     )
            if type(self.rrt_result) == int:
                dlg = wx.MessageBox("Cannot build a path")
            self.Refresh()
        else:
            dlg = wx.MessageBox("You should mark Start and Exit points!")

    def setIter(self, event):
        try:
            if int(self.set_iter_text_ctrl.GetLineText(0)) != float(self.set_iter_text_ctrl.GetLineText(0)):
                dlg = wx.MessageBox("Number of iterations must be an integer number")
            else:
                self.iter_num = int(self.set_iter_text_ctrl.GetLineText(0))
        except ValueError:
            dlg = wx.MessageBox("Number of iterations must be an integer number")
        event.Skip()

    def save_map(self, event):
        dlg = wx.FileDialog(self, "Выбор файла сохранения ", "D:/University/2_course/MPIAA/RGZ/maps",
                            style=wx.FD_DEFAULT_STYLE)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            SaveAndLoad.save_map(dlg.GetPath(), self.starting_point, self.exit_point, obstacles)

    def load_map(self, event):
        dlg = wx.FileDialog(self, "Выбор карты: ", "D:/University/2_course/MPIAA/RGZ/maps",
                            style=wx.FD_DEFAULT_STYLE)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            global obstacles
            self.starting_point, self.exit_point, obstacles = SaveAndLoad.load_map(dlg.GetPath())
            self.rrt_tree = 0
            self.Refresh()

    def clear_map(self, event):
        obstacles.clear()
        self.rrt_result, self.rrt_tree = 0, 0
        self.Refresh()

    def onPaint(self, event):
        dc = wx.PaintDC(self)

        dc.DrawLine(wx.Point(WIDTH, 0), wx.Point(WIDTH, HEIGHT))
        dc.DrawLine(wx.Point(0, HEIGHT), wx.Point(WIDTH, HEIGHT))
        dc.SetBrush(wx.Brush("#454545"))
        for i in obstacles:
            dc.DrawPolygon(tuple(wx.Point(j.x, j.y) for j in i))

        if self.starting_point:
            dc.SetBrush(wx.Brush("GREEN"))
            dc.DrawCircle(self.starting_point, 2)
            dc.SetBrush(wx.Brush("#454545"))

        if self.exit_point:
            dc.SetBrush(wx.Brush("RED"))
            dc.DrawCircle(self.exit_point, 2)
            dc.SetBrush(wx.Brush("#454545"))

        if self.rrt_result and self.rrt_tree:
            graph_verts = self.rrt_tree.get_vertices()
            graph_verts = [[wx.Point(i.x, i.y), i.parent] for i in graph_verts]

            for i in range(1, len(graph_verts)):
                dc.DrawLine(graph_verts[i][0], graph_verts[graph_verts[i][1]][0])

            dc.SetPen(wx.Pen("RED"))
            for i in range(len(self.rrt_result) - 1):
                dc.DrawLine(self.rrt_result[i][0], self.rrt_result[i + 1][0])


app = wx.App()
frame = MyFrame(None, "Hello world!")
frame.Show()
app.MainLoop()
