#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import wx
from keyboard_listener_window import KeyboardListenerWindow
from rubiks_cube_window import RubiksCubeWindow

import translater
if not translater.init(): _=lambda x: x


class MainWindow(KeyboardListenerWindow):
    def __init__(self, title=_("Baima Rubiks Cube"), *args, **kw):
        super().__init__(title=title,*args,**kw)

        RubiksCubeWindow(None)
        self.Destroy()


app=wx.App(False)
MainWindow()
app.MainLoop()