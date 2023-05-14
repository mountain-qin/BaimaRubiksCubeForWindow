#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from winsound import Beep
import wx
from keyboard_listener_window import KeyboardListenerWindow
from rubiks_cube import RubiksCube

import translater
if not translater.init(): _=lambda x:x


class RubiksCubeWindow(KeyboardListenerWindow):
	def __init__(self, parent=None,  id=-1, title=_("Baima Rubiks Cube"), *args, **kw):
		super().__init__(parent, id, title, *args, **kw)

		self.rubiks_cube=RubiksCube()
		super().show_message(_("Please press the arrow keys to view the block information. %s"%self.rubiks_cube.get_focus_block_information()))
		

	def on_char_hook(self, event:wx.KeyEvent):
		self.view_block(event)
		event.Skip()


	def view_block(self,event:wx.KeyEvent):
		# 不按下任何修饰键
		if event.GetModifiers()>0:return

		key_code=event.GetKeyCode()
		viewed=False
		if key_code==wx.WXK_LEFT:viewed=self.rubiks_cube.view_left()
		elif key_code==wx.WXK_UP:viewed=self.rubiks_cube.view_up()
		elif key_code==wx.WXK_RIGHT:viewed=self.rubiks_cube.view_right()
		elif key_code==wx.WXK_DOWN:viewed=self.rubiks_cube.view_down()
		else:return
		
		if viewed:
			super().show_message(self.rubiks_cube.get_focus_block_information())
		else:Beep(440,50)
