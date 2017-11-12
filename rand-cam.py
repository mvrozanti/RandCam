# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
from bs4 import BeautifulSoup
from skimage import io
import requests
import random
from threading import Thread
from time import sleep
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections import deque
from skimage import data
from skimage.viewer import ImageViewer

def update_v(v, src):
	while True:
		v.update_image(io.imread(src))

def keep_updating_image(src, ix):
	#while True:
	v = ImageViewer(io.imread(src))
	Thread(target=update_v, args=[v,src]).start()
	v.show()
	

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
	print(len(ps) > 0)
	print(ps)
	print(time.time() - s)
	bs = BeautifulSoup(ps, 'lxml')
	imgs = bs.find_all('img')
	if v: print('Retrieving...')
	ix = 0
	for img in imgs:
		src = img.get('src')
		if 'google' not in src and ix == 1:
			Thread(target=keep_updating_image, args=[src, ix]).start()
		ix+=1
	# if v: print('Warming up')
	# d = webdriver.Firefox(firefox_binary=FirefoxBinary('/usr/lib/firefox/firefox'))
	# #cam_no = str(random.randint(1,512000)) this didnt work well
	# if v: print('Requesting new cams...')
	# d.get()
	# deq.append(d.page_source)
	# if v: print('Processing insecam source...')
	# bs = BeautifulSoup(d.page_source, 'lxml')

main()
