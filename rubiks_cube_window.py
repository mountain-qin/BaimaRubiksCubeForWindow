#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import locale
import json
import os
import sys
from pygame import mixer
from winsound import Beep
import wx

from keyboard_listener_window import KeyboardListenerWindow
from rubiks_cube import RubiksCube
from select_rubiks_cube_num_window  import SelectRubiksCubeNumWindow

import translater
if not translater.init(): _=lambda x:x


class RubiksCubeWindow(KeyboardListenerWindow):
	def __init__(self, parent=None,  id=-1, title=_("Baima Rubiks Cube"), *args, **kw):
		super().__init__(parent, id, title, *args, **kw)

		self.main_dir_path=os.path.dirname(os.path.abspath(sys.argv[0]))

		self.user_setting=self.read_user_setting()
		
		self.rubiks_cube_num=self.user_setting["rubiks_cube_num"]
		self.rubiks_cube=RubiksCube(self.rubiks_cube_num)
		self.Bind(wx.EVT_CLOSE,self.on_window_close)
		self.init_mixer()
		self.show_first_help()
		super().show_message(_("Please press the arrow keys to view the block information. %s") %self.rubiks_cube.get_focus_block_information())


	def read_user_setting(self):
		self.user_setting_path=os.path.join(self.main_dir_path,"config\\user_setting.json")
		if os.path.exists(self.user_setting_path):
			with open(self.user_setting_path,"r", encoding="utf-8") as f:
				return json.load(fp=f)

		else: return {
			"rubiks_cube_num":2,
			"bgm":{
				"volume":0.5,
				"play":True
			},
			"sound":{
				"volume":30,
				"play":True
			}
		}



	def init_mixer(self):
		mixer.init()
		mixer.music.load(os.path.join(self.main_dir_path,"sounds\\bgm\\bgm.wav"))
		volume=self.user_setting["bgm"]["volume"]
		self.play_bgm=self.user_setting["bgm"]["play"]
		mixer.music.set_volume(volume)
		if self.play_bgm: mixer.music.play(-1)

		self.sound_boundary=mixer.Sound(os.path.join(self.main_dir_path,"sounds\\boundary\\boundary.wav"))
		self.sound_rotate=mixer.Sound(os.path.join(self.main_dir_path,"sounds\\rotate\\rotate.wav"))
		self.sound_congratulation=mixer.Sound(os.path.join(self.main_dir_path,"sounds\\congratulation\\congratulation.wav"))

		self.volume_sound=self.user_setting["sound"]["volume"]
		self.sound_play=self.user_setting["sound"]["play"]

		self.set_sound_volume(self.volume_sound)



	def set_sound_volume(self,volume):
		self.volume_sound=volume
		for sound in [self.sound_boundary,self.sound_rotate,self.sound_congratulation]:
			sound.set_volume(volume/100)


	def on_char_hook(self, event:wx.KeyEvent):
		self.view_block(event)
		self.rotate_block(event)
		self.rotate_entire(event)
		self.control_bgm(event)
		self.control_sound(event)

		key_code=event.GetKeyCode()
		if event.GetModifiers()==0:
			if key_code==wx.WXK_F1:self.show_help()
			# 重新调整顺序 
			if key_code==wx.WXK_F5:
				self.rubiks_cube.restore()
				super().show_message(_("The Rubiks Cube has been restored %s")%self.rubiks_cube.get_focus_block_information())
# 打乱顺序
			elif key_code==wx.WXK_F6:
				self.rubiks_cube.disrupt_order()
				super().show_message(_("The order has been disrupted. %s")%self.rubiks_cube.get_focus_block_information())

		elif event.GetModifiers()==wx.MOD_CONTROL:
			if key_code==ord("N"):
				SelectRubiksCubeNumWindow(self, self.on_select_rubiks_cube_num)
				self.Show(False)

		event.Skip()


	def on_select_rubiks_cube_num(self, num):
		self.rubiks_cube_num=num
		self.rubiks_cube=RubiksCube(self.rubiks_cube_num)
		super().show_message(_("The number of the rubiks cube is %s .")%num)


	def control_sound(self,event:wx.KeyEvent):
		if event.GetModifiers()!=wx.MOD_CONTROL:return
		key_code=event.GetKeyCode()
		if key_code==wx.WXK_F9:
			self.sound_play=not self.sound_play
			if self.sound_play:super().show_message(_("sound on."))
			else: super().show_message(_("sound off."))
		elif key_code==wx.WXK_F11:
			if self.volume_sound>0:self.volume_sound-=1
			self.set_sound_volume(self.volume_sound)
			super().show_message(_("sound volume %s")%self.volume_sound)
		elif key_code==wx.WXK_F12:
			if self.volume_sound<100:self.volume_sound+=1
			self.set_sound_volume(self.volume_sound)
			super().show_message(_("sound volume %s")%self.volume_sound)


	def control_bgm(self,event:wx.KeyEvent):
		if event.GetModifiers()>0:return
		key_code=event.GetKeyCode()
		if key_code==wx.WXK_F9:
			if mixer.music.get_busy():mixer.music.stop()
			else:mixer.music.play(-1)
			self.play_bgm=not self.play_bgm
		elif key_code==wx.WXK_F11:mixer.music.set_volume(mixer.music.get_volume()-0.01)
		elif key_code==wx.WXK_F12:mixer.music.set_volume(mixer.music.get_volume()+0.01)



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
		self.play_sound(self.sound_rotate)


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
		self.play_sound(self.sound_rotate)
		if self.rubiks_cube.check_successful():
			super().show_message(_("congratulations! You have restored the Rubik's Cube!"))
			self.play_sound(self.sound_congratulation)


	def play_sound(self, sound):
		if self.sound_play:sound.play()


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
		else:self.play_sound(self.sound_boundary)


	def show_first_help(self):
		first_path=os.path.join(self.main_dir_path, "config\\.first")
		if not os.path.exists(first_path):
			self.show_help()
			if not os.path.exists(os.path.dirname(first_path)):os.makedirs(os.path.dirname(first_path))
			with open(first_path,"w"):pass


	def show_help(self):
		self.help_path=os.path.join(self.main_dir_path,"documentation\\%s\\readme.html"%locale.getdefaultlocale()[0])
		if not os.path.exists(self.help_path):self.help_path=os.path.join(self.main_dir_path,"readme.html")
		if os.path.exists(self.help_path):os.startfile(self.help_path)



	def on_window_close(self,event):
		self.write_user_setting()
		mixer.quit()
		self.Destroy()

		baima_mini_game_path=os.path.join(os.path.dirname(self.main_dir_path),"BaimaMiniGame.exe")
		if os.path.exists(baima_mini_game_path):os.startfile(baima_mini_game_path)



	def write_user_setting(self):
		user_setting={
			"rubiks_cube_num":self.rubiks_cube_num,
			"bgm":{
				"volume":mixer.music.get_volume(),
				"play":self.play_bgm
			},
			"sound":{
				"volume":self.volume_sound,
				"play":self.sound_play
			}
		}

		if user_setting==self.user_setting:return

# 写到本地
		if not os.path.exists(os.path.dirname(self.user_setting_path)):os.makedirs(os.path.dirname(self.user_setting_path))
		with open(self.user_setting_path,"w",encoding="utf-8") as f:
			json.dump(user_setting,f)