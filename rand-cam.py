# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
import cv2
import time
import tkinter as tk
from tkinter import *

import requests
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
from skimage import io

sources = []
ix = 0
root, panel, canvas = None,None,None

def update_v():
	# root,canvas,panel=rootcanvaspanel
	global root
	global ix
	global sources
	global canvas
	try:
		url = sources[ix]
		if url.endswith('.cgi'):
			print('!!!')

		else:
			print('Getting image ' + url)
			raw_img = io.imread(url)
			img = ImageTk.PhotoImage(Image.fromarray(raw_img, 'RGB'))
			panel.img = img
			panel.configure(image=img)
			canvas.update_idletasks()
	except Exception as ex:
		print(ex)
		print(sources.pop(ix))
	root.after(1, update_v)

def decr_ix(e=None):
	global ix
	ix-=1
def incr_ix(e=None):
	global ix
	ix+=1
def exit_safely(e):
	sys.exit(0)

def keep_updating_image():
	global root
	global ix
	global panel
	global sources
	global canvas
	root = Tk()
	# root.bind_all('w', keydown)
	# root.bind_all('<w>', keydown)
	# root.bind_all('<KeyPress-w>', keydown)
	# root.bind_all('<KeyPress>', keydown)
	# root.bind('w', keydown)
	# root.bind('<w>', keydown)
	# root.bind('<KeyPress-w>', keydown)
	# root.bind('<KeyPress>', keydown)
	# root.bind('<Escape>', keydown)
	# root.bind('KeyRelease', keydown)
	# root.bind('<KeyRelease>', keydown)
	# canvas = tk.Frame(master=root)
	# canvas.bind_all('w', keydown)
	# canvas.bind_all('<w>', keydown)
	# canvas.bind_all('<KeyPress-w>', keydown)
	# canvas.bind_all('w', keydown)
	# canvas.bind('<w>', keydown)
	# canvas.bind('<KeyPress-w>', keydown)
	canvas = tk.Frame(master=root)
	root.bind('<Escape>', exit_safely)
	root.bind('<Left>', decr_ix)
	root.bind('<Right>', incr_ix)
	canvas.pack(side='bottom', fill='both', expand='yes')
	panel = tk.Label(master=canvas)
	# panel.ix = ix
	panel.pack(side='bottom', fill='both', expand='yes')
	root.after(10, update_v)
	# Thread(target=root.after, args=[100, update_v, root, canvas, panel,]).start()
	# ent = tk.Entry(root)
	# ent.bind('w', keydown)
	# ent.bind('<w>', keydown)
	# ent.bind('<KeyPress-w>', keydown)
	# ent.bind('<KeyRelease-w>', keydown)
	# ent.bind_all('w', keydown)
	# ent.bind_all('<w>', keydown)
	# ent.bind_all('<KeyPress-w>', keydown)
	# ent.bind_all('<KeyRelease-w>', keydown)
	# ent.bind_all('<Escape>', keydown)
	# root.focus_set()
	#Thread(target=root.after, args=[50, update_v, panel,]).start()
	print('Mainlooping')
	root.mainloop()


def main(v=True):
	session = requests.session()
	s = time.time()
	headers = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Host':'www.insecam.org',
		'DNT':1,
		'Accept-Language':'en-US,en;q=0.5',
		'Upgrade-Insecure-Requests':1
	}
	ps = session.get('https://www.insecam.org/en/bynew/', headers=headers, timeout=5).text
	bs = BeautifulSoup(ps, 'lxml')
	imgs = bs.find_all('img')
	if v: print('Retrieving...')
	ix = 0
	for img in imgs:
		src = img.get('src')
		try:
			if 'google' not in src:# and session.get(src, timeout=5).text:
				sources.append(src)
		except:pass
	print(sources)
	keep_updating_image()
main()
