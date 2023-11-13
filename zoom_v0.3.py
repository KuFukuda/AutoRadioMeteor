import tkinter as tk
import datetime
from PIL import Image, ImageTk
from tkinter import font

#各フレームの縦横のサイズを決めておく
_squarelength = 200
_framelength = 50

_initial_posi_x=39
_initial_posi_y=230

class MainApplication(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.master.geometry('1000x700')
		self.master.title("Image Viewer")

		self.loadimage()
		self.create_widget()

	def create_widget(self):
#		self.canvas = tk.Canvas(self.master, bg="#ffffff")
		self.frame = tk.Frame(self.master, background='gray', width=1500, height=700)
		self.frame.pack()

		self.canvas1 = tk.Canvas(self.frame, width=self.resize_image.width, height=self.resize_image.height)
		self.canvas1.place(x=50, y=100)
		self.canvas1.create_image(0, 0, image=self.main_image,anchor=tk.NW)

#		self.canvas1.create_rectangle(150, 100, 200, 150,outline="red", tag="rect")
		self.canvas1.create_rectangle(_initial_posi_x-_framelength/2, _initial_posi_y-_framelength/2, _initial_posi_x+_framelength/2, _initial_posi_y+_framelength/2,outline="red", tag="rect")

		self.canvas2 = tk.Canvas(self.frame, width=_squarelength, height=_squarelength)
		self.canvas2.place(x=758, y=100)
		self.canvas2.create_line(_squarelength/2, 0,_squarelength/2, _squarelength,tag="line1")
		self.canvas2.create_line(0, _squarelength/2,_squarelength, _squarelength/2,tag="line2")

		self.label1 = tk.Label(root, bg="white", width=20, height=3)
		self.label1.place(x=758, y=400)

		self.var = tk.BooleanVar()
		self.text = tk.StringVar()
		self.text.set("Original Text")
		self.che1 = tk.Checkbutton( variable = self.var,textvariable=self.text)
		self.che1.place(x=50, y=600)

		root.bind("<KeyPress>", self.key_event)

	def time_set(self,x):
		self.x_time=self.position2time(x)
		self.label1["text"] = str(self.x_time) 

	def loadimage(self):
		self.image = Image.open("../202306012330.png")
#		self.image = Image.open("./datasets/train/images/202309060000.png")
		self.resize_image = self.image.resize((629, 400))
		self.main_image = ImageTk.PhotoImage(self.resize_image)

	def key_event(self,event):
		key = event.keysym
#		print(key)
		shift_x, shift_y = 0, 0
		if key == "i":
			shift_y -= 1
		if key == "k":
			shift_y += 1
		if key == "j":
			shift_x -= 1
		if key == "l":
			shift_x += 1
		if key == "space":
			self.start_point_get()
		self.canvas1.move("rect", shift_x, shift_y)
		self.canvas_set()
		self.time_set()

#	def start_point_get(self,event):
	def start_point_get(self):
		self.text.set(str(self.x_time))
#		print(self.x_time)
		self.che1 = tk.Checkbutton( text = self.text, variable = self.var )

#	def time_set(self,x):
	def time_set(self):
		self.rect_position=self.canvas1.bbox("rect")
		self.x_time=self.position2time((self.rect_position[0]+self.rect_position[2])/2)
		self.label1["text"] = str(self.x_time) 

	def position2time(self,x):
		file_time="2023-09-06 00:00:00"
		file_time=datetime.datetime.strptime(file_time, '%Y-%m-%d %H:%M:%S')
		add_time=int(600*(x-19)/(618-19))
		label_time=file_time+datetime.timedelta(seconds=add_time)
		return label_time

	def canvas_set(self):
		# 枠線内をクロップし、ズームする
		zoom_mag = _squarelength / _framelength
		self.rect_position=self.canvas1.bbox("rect")
#		print(self.rect_position)
		croped = self.resize_image.crop(self.rect_position)
		zoom_image = croped.resize((int(croped.width*zoom_mag), int(croped.height*zoom_mag)))

		# ズームした画像を右側canvasに当てはめる
		self.canvas2.delete("cv1")
		self.sub_image1 = ImageTk.PhotoImage(zoom_image)

		self.sub_cv1 = self.canvas2.create_image(0, 0, image=self.sub_image1, anchor=tk.NW, tag='cv1')

		self.canvas2.create_line(_squarelength/2, 0,_squarelength/2, _squarelength,tag="line1")
		self.canvas2.create_line(0, _squarelength/2,_squarelength, _squarelength/2,tag="line2")

if __name__ == '__main__':
	root = tk.Tk()
	app = MainApplication(master = root)
	app.mainloop()
