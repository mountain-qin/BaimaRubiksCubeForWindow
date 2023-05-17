import wx

from keyboard_listener_window import KeyboardListenerWindow

import translater
if not translater.init(): _=lambda x:x


class SelectRubiksCubeNumWindow(KeyboardListenerWindow):
	def __init__(self, parent,on_select_rubiks_cube_num, id=-1, title=_("Baima Rubiks Cube - select number"), *args, **kw):
		super().__init__(parent, id, title, *args, **kw)

		self.select_rubiks_cube_num=on_select_rubiks_cube_num
		self.num=2
		self.Bind(wx.EVT_CLOSE, self.on_window_close)
		super().show_message(_("Please press the up and down arrow keys to select the number of the Rubik's Cube, and press Enter to confirm. %s")%self.num)


	def on_char_hook(self, event:wx.KeyEvent):
		key_code= event.GetKeyCode()
		if key_code==wx.WXK_UP:
			if self.num>2:self.num-=1
			super().show_message(str(self.num))
		elif key_code==wx.WXK_DOWN:
			self.num+=1
			super().show_message(str(self.num))
		elif key_code==wx.WXK_RETURN:
			self.select_rubiks_cube_num(self.num)
			self.Close()

		event.Skip()


	def on_window_close(self,event):
		self.GetParent().Show()
		self.Destroy()