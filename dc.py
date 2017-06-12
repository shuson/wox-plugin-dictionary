# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup
from dc import requests

URL = 'http://www.dictionary.com/browse/'

def full2half(uc):
	"""Convert full-width characters to half-width characters.
	"""
	return unicodedata.normalize('NFKC', uc)

class Main(Wox):
  
	def request(self,url):
		#get system proxy if exists
		if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
			proxies = {
			"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
			"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
			}
			return requests.get(url,proxies = proxies)
		else:
			return requests.get(url)
			
	def query(self, param):
		r = self.request(URL + param)
		bs = BeautifulSoup(r.content, 'html.parser')
		wordType = ""
		means = []
		if bs.find('header', 'luna-data-header'):
				wordType = bs.find('header', 'luna-data-header').get_text(strip=True)
		if bs.find('section', 'def-pbk ce-spot'):
				means = bs.find('section', 'def-pbk ce-spot').find_all('div', 'def-set')

		result = []
		index = 0
		for m in means:
				title = m.find('div', 'def-content').get_text(strip=True)
				item = {
					'Title': full2half(str(index + 1) + ": " + title),
					'Subtitle': wordType,
					'IcoPath': os.path.join('img', 'dc.png')
				}
				result.append(item)
				index+=1
			
		return result
	
	def open_url(self, url):
		webbrowser.open(url) #use default browser

if __name__ == '__main__':
	Main()
