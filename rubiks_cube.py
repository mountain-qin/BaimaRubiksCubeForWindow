#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""魔方模块"""


import translater
if not translater.init(): _=lambda x:x


class RubiksCube():
	def __init__(self,
		num=2,
		titles=[_("red"), _("green"), _("orange"), _("blue"), _("yellow"), _("white")]
		):
		"""
		: param num 一行或者一列上方块的数目
		"""
		self.num=num
		self.side_focus,self.row_focus,self.col_focus=0,0,0
		self.list=[[[titles[s] for c in range(num)] for r in range(num)] for s in range(6)]


	def view_left(self):
		if self.col_focus>0:
			self.col_focus-=1
			return True
		return False


	def view_up(self):
		if self.row_focus>0:
			self.row_focus-=1
			return True
		return False


	def view_down(self):
		if self.row_focus<self.num-1:
			self.row_focus+=1
			return True
		return False

	def view_right(self):
		if self.col_focus<self.num-1:
			self.col_focus+=1
			return True
		return False


	def get_focus_block_information(self):
		return "%s, %s%s %s%s"%(self.list[self.side_focus][self.row_focus][self.col_focus], self.row_focus+1, _("row"), self.col_focus+1, _("column"))
