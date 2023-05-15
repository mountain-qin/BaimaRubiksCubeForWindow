#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""魔方模块"""


import translater
if not translater.init(): _=lambda x:x


class RubiksCube():
	FLAG_ROTATE_CLOCKWISE=0
	FLAG_ROTATE_ANTICLOCKWISE=1
	FLAG_ROTATE_UP=2
	FLAG_ROTATE_DOWN=3

	FLAG_FORWARD=0
	FLAG_BACKWARD=1

	SIDE_FRONT,SIDE_RIGHT,SIDE_BACK,SIDE_LEFT,SIDE_TOP,SIDE_BOTTOM=0,1,2,3,4,5


	def __init__(self,
		num=2,
		titles=[_("red"), _("green"), _("orange"), _("blue"), _("yellow"), _("white")]
		):
		"""
		: param num 一行或者一列上方块的数目
		"""
		self.num=num
		self.titles=titles
		self.side_focus,self.row_focus,self.col_focus=0,0,0
		self.list=[[[self.titles[s] for c in range(self.num)] for r in range(self.num)] for s in range(6)]


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


	def __rotate_vertical(self,col,flag):
		list_srcs=[]
		# 前面的索引 
		list_srcs.append([[0, row ,col] for row in range(self.num)]) 
		# 上面的索引
		list_srcs.append([[4, row ,col] for row in range(self.num)]) 
		# 后面的索引 
		list_srcs.append([[2, self.num-1-row, self.num-1-col] for row in range(self.num)])
		# 下面的索引
		list_srcs.append([[5, row ,col] for row in range(self.num)]) 

		if flag==RubiksCube.FLAG_ROTATE_UP:self.__update_by_srcslist(list_srcs,RubiksCube.FLAG_BACKWARD)
		elif flag==RubiksCube.FLAG_ROTATE_DOWN :self.__update_by_srcslist(list_srcs=list_srcs,flag=RubiksCube.FLAG_FORWARD)

	def rotate_up_entire(self):
		self.rotate_up([i for i in range(self.num)])


	def rotate_up(self, arg=None):
		"""向上转动指定的列"""
		if arg==None:arg=self.col_focus
		if type(arg)==list:
			for col in arg:self.rotate_up(col)
			return

		self.__rotate_vertical(arg, RubiksCube.FLAG_ROTATE_UP)
		if arg==0:self.__update_side_anticlockwise(RubiksCube.SIDE_LEFT)
		elif arg==self.num-1:self.__update_side_clockwise(RubiksCube.SIDE_RIGHT)


	def rotate_down_entire(self):
		self.rotate_down([i for i in range(self.num)])


	def rotate_down(self,arg=None):
		"""向下转动指定的列"""
		if arg==None:arg=self.col_focus
		if type(arg)==list:
			for col in arg:self.rotate_down(col)
			return

		self.__rotate_vertical(arg, RubiksCube.FLAG_ROTATE_DOWN)
		if arg==0:self.__update_side_clockwise(RubiksCube.SIDE_LEFT)
		elif arg==self.num-1:self.__update_side_anticlockwise(RubiksCube.SIDE_RIGHT)


	def rotate_left_entire(self):
		"""整个向左转动"""
		self.rotate_left([i for i in range(self.num)])


	def rotate_left(self, arg=None):
		"""
		rotate_left(row)
		rotate_left(rows:list)
		向左转动指定的行
		"""
		if arg==None:arg=self.row_focus
		if type(arg)==list:
			for row in arg:self.rotate_left(row)
			return

		for s in range(3):
			for c in range(self.num):
				temp=self.list[s][arg][c]
				self.list[s][arg][c]=self.list[s+1][arg][c]
				self.list[s+1][arg][c]=temp

		if arg==0:self.__update_side_clockwise(RubiksCube.SIDE_TOP)
		elif arg==self.num-1:self.__update_side_anticlockwise(RubiksCube.SIDE_BOTTOM)


	def rotate_right_entire(self):
		self.rotate_right([i for i in range(self.num)])


	def rotate_right(self,arg=None):
		"""
		rotate_right(row)
		rotate_right(rows:list)
		向右转动指定的行"""
		if arg==None:arg=self.row_focus
		if type(arg)==list:
			for row in arg:self.rotate_right(row)
			return

		for s in range(3):
			for c in range(self.num):
				temp=self.list[0][arg][c]
				self.list[0][arg][c]=self.list[s+1][arg][c]
				self.list[s+1][arg][c]=temp

		if arg==0:self.__update_side_anticlockwise(RubiksCube.SIDE_TOP)
		elif arg==self.num-1:self.__update_side_clockwise(RubiksCube.SIDE_BOTTOM)



	def __rotate_clock(self,col,flag):
		"""沿时钟方向转动"""
		list_srcs=[]
		# 从左面那一面开始
		list_srcs.append([[3, row, col] for row in range(self.num)])
		list_srcs.append([[4,col,self.num-1- row] for row in range(self.num)])
		list_srcs.append([[1,self.num-1-row, self.num-1-col] for row in range(self.num)])
		list_srcs.append([[5,self.num-1-col, c] for c in range(self.num)])

		if flag==RubiksCube.FLAG_ROTATE_CLOCKWISE:self.__update_by_srcslist(list_srcs,RubiksCube.FLAG_BACKWARD)
		elif flag==RubiksCube.FLAG_ROTATE_ANTICLOCKWISE:self.__update_by_srcslist(list_srcs,RubiksCube.FLAG_FORWARD)

	def rotate_anticlockwise_entire(self):
		self.rotate_anticlockwise([i for i in range(self.num)])


	def rotate_anticlockwise(self,arg=None):
		"""按逆时针方向转动指定的列。列是左面上的列"""
		if arg==None:arg=self.num-1
		if type(arg)==list:
			for col in arg:self.rotate_anticlockwise(col)
			return

		self.__rotate_clock(arg,RubiksCube.FLAG_ROTATE_ANTICLOCKWISE)
		if arg==0:self.__update_side_clockwise(RubiksCube.SIDE_BACK)
		elif arg==self.num-1:self.__update_side_anticlockwise(RubiksCube.SIDE_FRONT)


	def rotate_clockwise_entire(self):
		self.rotate_clockwise([i for i in range(self.num)])


	def rotate_clockwise(self,arg=None):
		"""按顺时针方向转动指定的列。列是左面上的列
		:: param col 左面的哪一列
		"""

		if arg==None:arg=self.num-1
		if type(arg)==list:
			for col in arg:self.rotate_clockwise(col)
			return

		self.__rotate_clock(arg,RubiksCube.FLAG_ROTATE_CLOCKWISE)
		if arg==0:self.__update_side_anticlockwise(RubiksCube.SIDE_BACK)
		elif arg==self.num-1:self.__update_side_clockwise(RubiksCube.SIDE_FRONT)


	def __update_side_clock(self,side,flag):
		"""按顺时针逆时针更新指定的面"""
		#有多少环要转动
		count_ring=int(self.num/2)
		for ring in range(count_ring):
			list_srcs=[]
			# 当前环的一边上的方块数
			num=self.num-2*ring

			list_srcs.append([[side,ring,c+ring] for c in range(num-1)] )
			list_srcs.append([[side, r+ring,self.num-1-ring] for r in range(num-1)])
			list_srcs.append([[side, self.num-1-ring,self.num-1-c-ring] for c in range(num-1)])
			list_srcs.append([[side,self.num-1-r-ring, ring] for r in range(num-1)])

			if flag==RubiksCube.FLAG_ROTATE_CLOCKWISE:self.__update_by_srcslist(list_srcs,RubiksCube.FLAG_BACKWARD)
			elif flag==RubiksCube.FLAG_ROTATE_ANTICLOCKWISE:self.__update_by_srcslist(list_srcs,RubiksCube.FLAG_FORWARD)


	def __update_side_clockwise(self, side):
		"""按顺时针方向更新指定的面"""
		self.__update_side_clock(side, RubiksCube.FLAG_ROTATE_CLOCKWISE)


	def __update_side_anticlockwise(self,side):
		"""按逆时针方向更新指定的面"""
		self.__update_side_clock(side,RubiksCube.FLAG_ROTATE_ANTICLOCKWISE)


	def __update_by_srcslist(self,list_srcs,flag):
		"""根据指定的面行列索引列表更新数据。"""
		for s in range(len(list_srcs)-1):
			for j in range(len(list_srcs[0])):
				# 前进
				if flag==RubiksCube.FLAG_FORWARD:
					src=list_srcs[s][j]
					src1=list_srcs[s+1][j]
					# 后退
				elif flag==RubiksCube.FLAG_BACKWARD:
					src=list_srcs[0][j]
					src1=list_srcs[s+1][j]

				temp=self.list[src[0]][src[1]][src[2]]
				self.list[src[0]][src[1]][src[2]]=self.list[src1[0]][src1[1]][src1[2]]
				self.list[src1[0]][src1[1]][src1[2]]=temp



	def get_focus_block_information(self):
		return "%s, %s%s %s%s"%(self.list[self.side_focus][self.row_focus][self.col_focus], self.row_focus+1, _("row"), self.col_focus+1, _("column"))


	def check_successful(self):
		for ll in self.list:
			title=ll[0][0]
			for l in ll:
				for t in l:
					if t!=title:return False

		return True


	def adjust_order(self):
		self.side_focus,self.row_focus,self.col_focus=0,0,0
		# 重新生成魔方
		self.list=[[[self.titles[s] for c in range(self.num)] for r in range(self.num)] for s in range(6)]
