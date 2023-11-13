import tkinter as tk
import datetime
from PIL import Image, ImageTk
from tkinter import font

#各フレームの縦横のサイズを決めておく
_squarelength = 200
_framelength = 50

class MainApplication(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.master.geometry('1000x700')
		self.master.title("Image Viewer")

		self.image = Image.open("../202306012330.png")
#		self.resize_image = self.image.resize((608, 456))
		self.resize_image = self.image.resize((629, 400))
		self.main_image = ImageTk.PhotoImage(self.resize_image)

		self.create_widget()

	def create_widget(self):
		self.frame = tk.Frame(self.master, background='gray', width=1500, height=700)
		self.frame.propagate(False)
		self.frame.pack()

		self.canvas1 = tk.Canvas(self.frame, width=self.resize_image.width, height=self.resize_image.height)
		self.canvas2 = tk.Canvas(self.frame, width=_squarelength, height=_squarelength)
		self.label1 = tk.Label(root, bg="white", width=20, height=3)
		self.var = tk.BooleanVar()
		self.text = tk.StringVar()
		self.text.set("Original Text")
		self.che1 = tk.Checkbutton( variable = self.var,textvariable=self.text)

		self.canvas1.place(x=50, y=100)
		self.canvas2.place(x=758, y=100)
		self.label1.place(x=758, y=400)
		self.che1.place(x=50, y=600)

		self.canvas1.create_image(0, 0, image=self.main_image, anchor=tk.NW)

		self.canvas2.create_line(_squarelength/2, 0,_squarelength/2, _squarelength,tag="line1")
		self.canvas2.create_line(0, _squarelength/2,_squarelength, _squarelength/2,tag="line2")

		# canvas1にマウスが乗った場合、離れた場合のイベントをセット。
		self.canvas1.bind('<Motion>', self.mouse_motion)
		self.canvas1.bind('<Leave>', self.mouse_leave)
		self.canvas1.bind("<ButtonPress-1>", self.start_point_get)
		self.canvas1.bind('<KeyPress>',self.key_evnet)

		font = tk.font.Font(family='Arial', size=16, weight='bold')
		image_title = tk.Label(text='Original Image', bg = "gray", font=font)
		image_title2 = tk.Label(text='Enlarged Image', bg = "gray", font=font)

		image_title.place(x=50, y=60, anchor=tk.NW)
		image_title2.place(x=758, y=60, anchor=tk.NW)

	def key_evnet(self,event):
		key=evnet.keysym
		print(key)

	# ドラッグした時のイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
	def start_point_get(self,event):
		self.text.set(str(self.x_time))
		print(self.x_time)
		self.che1 = tk.Checkbutton( text = self.text, variable = self.var )

	def mouse_motion(self, event):
		# マウス位置の座標を取得, 写真から切り出す座標を定義
		x = event.x
		y = event.y
		self.frame_rect(x, y)
		self.canvas_set(x, y)
		self.time_set(x)

	def time_set(self,x):
		self.x_time=self.position2time(x)
		self.label1["text"] = str(self.x_time) 

	def position2time(self,x):
		file_time="2023-09-06 00:00:00"
		file_time=datetime.datetime.strptime(file_time, '%Y-%m-%d %H:%M:%S')
		add_time=int(600*(x-19)/(618-19))
		label_time=file_time+datetime.timedelta(seconds=add_time)
		return label_time

	def frame_rect(self, x, y):
		# 過去に枠線が描画されている場合はそれを削除し、メイン画像内マウス位置に枠線を描画
		self.frame_refresh()
		self.crop_frame = (x-_framelength/2, y-_framelength/2, x+_framelength/2, y+_framelength/2)	
		self.rectframe = self.canvas1.create_rectangle(self.crop_frame, outline='#AAA', width=2, tag='rect')

	def frame_refresh(self):
		try:
			self.canvas1.delete('rect')
		except:
			pass

	def canvas_set(self, x, y):
		# 枠線内をクロップし、ズームする
		zoom_mag = _squarelength / _framelength
		croped = self.resize_image.crop(self.crop_frame)
		zoom_image = croped.resize((int(croped.width*zoom_mag), int(croped.height*zoom_mag)))

		# ズームした画像を右側canvasに当てはめる
		self.image_refresh()
		self.sub_image1 = ImageTk.PhotoImage(zoom_image)

		self.sub_cv1 = self.canvas2.create_image(0, 0, image=self.sub_image1, anchor=tk.NW, tag='cv1')

		self.canvas1.delete("line1")  # すでに"rect1"タグの図形があれば削除
		self.canvas1.delete("line2")  # すでに"rect1"タグの図形があれば削除
		self.canvas2.create_line(_squarelength/2, 0,_squarelength/2, _squarelength,tag="line1")
		self.canvas2.create_line(0, _squarelength/2,_squarelength, _squarelength/2,tag="line2")

	def image_refresh(self):
		try:
			self.canvas2.delete('cv1')
		except:
			pass

	def mouse_leave(self, event):
		try:
			self.canvas2.delete('cv1')
			self.canvas1.delete('rect')
		except:
			pass

if __name__ == '__main__':
	root = tk.Tk()
	app = MainApplication(master = root)
	app.mainloop()
