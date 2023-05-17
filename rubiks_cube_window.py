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
		super().show_message(_("Please press the arrow keys to view the block information. %s") %self.rubiks_cube.get_focus_block_information())
		

	def on_char_hook(self, event:wx.KeyEvent):
		self.view_block(event)
		self.rotate_block(event)
		self.rotate_entire(event)

		key_code=event.GetKeyCode()
		if event.GetModifiers()==0:
			# 重新调整顺序 
			if key_code==wx.WXK_F5:
				self.rubiks_cube.adjust_order()
				super().show_message(_("The order has been adjusted. %s")%self.rubiks_cube.get_focus_block_information())
		event.Skip()


	def rotate_entire(self,event:wx.KeyEvent):
		# 要按下ctrl +shift
		if event.GetModifiers()!=wx.MOD_CONTROL+wx.MOD_SHIFT:return
		key_code=event.GetKeyCode()
		if key_code==wx.WXK_LEFT:self.rubiks_cube.rotate_left_entire()
		elif key_code==wx.WXK_UP:self.rubiks_cube.rotate_up_entire()
		elif key_code==wx.WXK_RIGHT:self.rubiks_cube.rotate_right_entire()
		elif key_code==wx.WXK_DOWN:self.rubiks_cube.rotate_down_entire()
		elif key_code==wx.WXK_PAGEUP:self.rubiks_cube.rotate_clockwise_entire()
		elif key_code==wx.WXK_HOME:self.rubiks_cube.rotate_anticlockwise_entire()
		else:return

		super().show_message(self.rubiks_cube.get_focus_block_information())


	def rotate_block(self, event:wx.KeyEvent):
		# 要按下ctrl
		if event.GetModifiers()!=wx.MOD_CONTROL:return
		key_code=event.GetKeyCode()
		if key_code==wx.WXK_LEFT:self.rubiks_cube.rotate_left()
		elif key_code==wx.WXK_UP:self.rubiks_cube.rotate_up()
		elif key_code==wx.WXK_RIGHT:self.rubiks_cube.rotate_right()
		elif key_code==wx.WXK_DOWN:self.rubiks_cube.rotate_down()
		elif key_code==wx.WXK_PAGEUP:self.rubiks_cube.rotate_clockwise()
		elif key_code==wx.WXK_HOME:self.rubiks_cube.rotate_anticlockwise()
		else:return

		super().show_message(self.rubiks_cube.get_focus_block_information())
		if self.rubiks_cube.check_successful():Beep(880, 500)


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
