#光学観測の流星が見えたタイミングを電波観測の結果に追加する。
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import pandas as pd
import datetime
import os

#電波観測した画像を取り込む
#対応した時刻の光学観測データを取り込む
#光学観測されたタイミングを画像に追記する

#光学観測された時間が電波観測のマークの座標に変換
def time2pix(dt1):
#start pixcel 19,81
#end pixcel 619,81
#600p = 600sec
	base=19
	time=(dt1.minute%10)*60+dt1.second
	px=time+base
	tri=((px-5, 70), (px+5, 70), (px, 80))
	return tri

def MakeTriList(filename):
	tri_list=[]
	for i in range(0,mfile.shape[0]-1):
		s1=mfile.at[i,'day(UT)']
		s1=s1.replace('/','')
		s2=mfile.at[i,'time(UT)']
		s2=s2.replace(':','')[1:]
		dt1 = datetime.datetime(int(s1[:4]), int(s1[4:6]), int(s1[7:]), int(s2[:2]), int(s2[2:4]), int(s2[4:]))
		dt1=dt1+datetime.timedelta(hours=9)	
		filename_opt='{}{:02d}{:02d}{:02d}{:02d}'.format(dt1.year,dt1.month,dt1.day,dt1.hour,dt1.minute)
		filename_opt=filename_opt[:11]+'0.png'
#		print(filename_opt)
		if filename==filename_opt:
			tri=time2pix(dt1)
			tri_list.append(tri)
	return tri_list

# 画像フォルダのパスを指定（適宜変更してください）
image_folder = "./radio/89.4MHz/20231003/"
# 画像フォルダ内のファイル名のリストを取得
image_files = os.listdir(image_folder)
# 画像ファイル名のリストをアルファベット順にソート
image_files.sort()
#画像リストの作成
image_file_list=[]
for file in image_files:
	base, ext = os.path.splitext(file)
	if ext == '.png':
#		print('file:{},ext:{}'.format(file,ext))
		image_file_list.append(file)
#print(image_file_list)

# 画像フォルダのパスを指定（適宜変更してください）
image_folder2 = "./radio/97MHz/20231003/"
# 画像フォルダ内のファイル名のリストを取得
image_files2 = os.listdir(image_folder2)
# 画像ファイル名のリストをアルファベット順にソート
image_files2.sort()
#画像リストの作成
image_file_list2=[]
for file in image_files2:
	base, ext = os.path.splitext(file)
	if ext == '.png':
#		print('file:{},ext:{}'.format(file,ext))
		image_file_list2.append(file)
#print(image_file_list)

#光学観測データの取り込み
mfile = pd.read_csv("_U2_20230901_S.csv", delimiter=',') # データ
print(mfile)
#print(mfile.shape[0]-1)

#各画像に対応するトリアングルのリストを作成する。
fill_tri_list=[]
for filename in image_file_list:
	tri_list=MakeTriList(filename)
	fill_tri_list.append(tri_list)
print(fill_tri_list)

#filename_old=""

##	dt1 = datetime.datetime(2020, 7, 21, 6, 12, 30, 551)
##	dt2 = dt1 + datetime.timedelta(days=1)
#	
#	is_file = os.path.isfile(filename)
#	if is_file:
#		if filename!=filename_old:
##			if filename_old!="":
#			img = Image.open(filename)
#			draw = ImageDraw.Draw(img)
##			triangle=((0, 0), (10, 0), (5, 10))
#			draw.polygon(tri, fill=(0, 255, 0), outline=(0, 0, 0))
##			img.show()
##			input()
#			filename_old=filename
#			print("new")
#		else:
#			draw.polygon(tri, fill=(0, 255, 0), outline=(0, 0, 0))
##			draw.polygon(((0, 0), (10, 0), (5, 10)), fill=(255, 255, 0), outline=(0, 0, 0))
##			img.show()
##			input()
#			print("old")
#	else:
#	    pass # パスが存在しないかファイルではない


#img = Image.open('202306010010.png')
#draw = ImageDraw.Draw(img)
#draw.polygon(((0, 0), (10, 0), (5, 10)), fill=(255, 255, 0), outline=(0, 0, 0))
#img.show()

#####################
# tkinterのウィンドウを作成
window = tk.Tk()

# ウィンドウのタイトルを設定
window.title("Image Viewer")

# ウィンドウのサイズを設定
window.geometry("829x800")

# 画像リストを表示するリストボックスを作成
listbox = tk.Listbox(window, width=20, height=60)
#listbox = tk.Listbox(window, width=200, height=600)
# リストボックスをウィンドウに配置
listbox.pack(side=tk.RIGHT)
# リストボックスに画像ファイル名と光学観測数を追加
#print(len(image_file_list))
for i in range(len(image_file_list)):
	image_file_add=image_file_list[i]+"   "+str(len(fill_tri_list[i]))
	listbox.insert(tk.END, image_file_add)
#    listbox.insert(tk.END, image_file)

# 画像を表示するキャンバスを作成
#canvas = tk.Canvas(window, width=600, height=600)
canvas = tk.Canvas(window, width=629, height=400)
# キャンバスをウィンドウに配置
#canvas.pack(side=tk.LEFT)
canvas.pack(side=tk.TOP)

# 画像を表示するキャンバスを作成
canvas2 = tk.Canvas(window, width=629, height=400)
# キャンバスをウィンドウに配置
canvas2.pack(side=tk.BOTTOM)


# リストボックスで選択された画像ファイル名を取得する関数
def get_selected_image(event):
	# リストボックスで選択されたインデックスを取得
	index = listbox.curselection()[0]
	
	# 画像ファイル名を取得
	image_file = image_file_list[index]
	
	# 画像ファイルのパスを作成
	image_path = os.path.join(image_folder, image_file)
	image_path2 = os.path.join(image_folder2, image_file)
#	print(image_path2)
	
	# 画像ファイルを開く
	image = Image.open(image_path)
	image2 = Image.open(image_path2)
	
#	#画像に光学観測時刻のマーカーを追加
#	draw = ImageDraw.Draw(image)
#	print(image_file)
#	print(index)
##	tri=((571, 70), (581, 70), (576, 80))
#	tri_list=fill_tri_list[index]
#	print(len(tri_list))
##	print(tri[0])
#	if len(tri_list)!=0:
#		for tri in tri_list:
#			print(tri)
#			draw.polygon(tri, fill=(0, 255, 0), outline=(0, 0, 0))
	
	# 画像をtkinter用に変換
	photo = ImageTk.PhotoImage(image)
	photo2 = ImageTk.PhotoImage(image2)
	
	# キャンバスに表示されている画像を削除
	canvas.delete("all")
	canvas2.delete("all")
	
	# キャンバスに新しい画像を表示
	canvas.create_image(0, 0, anchor=tk.NW, image=photo)
	canvas2.create_image(0, 0, anchor=tk.NW, image=photo2)
	
	# 画像オブジェクトをグローバル変数に保存（しないとガベージコレクションで消える）
	global current_image
	current_image = photo
	global current_image2
	current_image2 = photo2

# リストボックスで選択が変更されたときにget_selected_image関数を呼び出すように設定
listbox.bind("<<ListboxSelect>>", get_selected_image)

# CSVファイルのパスを指定（適宜変更してください）
csv_file = "U2_test.csv"

# CSVファイルを読み込んでデータフレームに変換
df = pd.read_csv(csv_file)

# データフレームの行数と列数を取得
rows, cols = df.shape
print(df.shape)

## tkinterのウィンドウを作成
#window = tk.Tk()
#Optlistbox = tk.Listbox(window, width=629, height=60)
Optlistbox = tk.Listbox(width=629,height=60)
Optlistbox.pack(side=tk.BOTTOM)
#
## ウィンドウのタイトルを設定
#window.title("CSV Viewer")
#
## ウィンドウのサイズを設定
#window.geometry("800x600")

# データフレームを表示する表を作成
#table = tk.Frame(window)
table = tk.Frame(Optlistbox)
#print(table)

# 表のヘッダーに列名を表示
label = tk.Label(table, text="selct")
label.grid(row=0, column=0)
label = tk.Label(table, text="No.")
label.grid(row=0, column=1)
for col in range(cols):
	print(df.columns[col])
	label = tk.Label(table, text=df.columns[col])
	label.grid(row=0, column=col+2)

# 表の各セルにデータとチェックボックスを表示
checkboxes = [] # チェックボックスのリスト
chk_bln_list=[]
for row in range(1, rows + 1):

	# 行の頭にチェックボックスを作成
	chk_bln=tk.BooleanVar(value=False) #add
	checkbox = tk.Checkbutton(table,variable=chk_bln)
	checkbox.grid(row=row, column=0, sticky="w")
	chk_bln_list.append(chk_bln)

	label = tk.Label(table, text=str(row-1))
	label.grid(row=row, column=1)
	for col in range(cols):
		# データを表示するラベルを作成
		label = tk.Label(table, text=df.iloc[row - 1, col])
		label.grid(row=row, column=col+2)

# tkinterのメインループを開始
window.mainloop()
