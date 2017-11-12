from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from skimage import io
import urllib3
import random
from threading import Thread
from time import sleep
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections import deque
from skimage import data
from skimage.viewer import ImageViewer

deq = deque() # ? this threadsafe but normal var isnt? what the fuck

def update_v(v, src):
	while True:
		v.update_image(io.imread(src))

def keep_updating_image(src, ix):
	#while True:
	v = ImageViewer(io.imread(src))
	Thread(target=update_v, args=[v,src]).start()
	v.show()
	

def in_thread(v=False):
	if v: print('Warming up')
	d = webdriver.Firefox(firefox_binary=FirefoxBinary('/usr/lib/firefox/firefox'))
	#cam_no = str(random.randint(1,512000)) this didnt work well
	if v: print('Requesting new cams...')
	d.get('https://www.insecam.org/en/bynew/')
	deq.append(d.page_source)
	if v: print('Processing insecam source...')
	bs = BeautifulSoup(d.page_source, 'lxml')
	imgs = bs.find_all('img')
	if v: print('Retrieving...')
	ix = 0
	for img in imgs:
		src = img.get('src')
		if 'google' not in src and ix == 1:
			Thread(target=keep_updating_image, args=[src, ix]).start()
		ix+=1
	d.close()
Thread(target=in_thread).start()
