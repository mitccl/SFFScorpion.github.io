# -*- coding: utf-8 -*-
from resources.lib.modules import control, cleantitle, utils
import requests
import os,sys,re,json,urllib,urlparse
import xbmc, xbmcaddon, xbmcgui, xbmcvfs
import time
import json
import libThread


sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

addonInfo     = xbmcaddon.Addon().getAddonInfo
profilePath   = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
libraryPath   = xbmc.translatePath(control.setting('library.path'))
manualLibrary = xbmc.translatePath(control.setting('library.manual'))
libPathMeta   = control.setting('library.path')
addonPath = xbmcaddon.Addon().getAddonInfo('profile')
addonSettings = xbmcaddon.Addon().getSetting
rdSettings = xbmc.translatePath(os.path.join(addonPath, 'rdauth.json'))
cloudFile = xbmc.translatePath(os.path.join(addonPath, 'cloud.json'))
USER_AGENT = 'RealDebrid Addon for Kodi'
BOUNDARY = 'X-X-X'
data = {}
params = {}

VALID_EXT = ['mkv', 'avi', 'mp4' ,'divx', 'mpeg', 'mov', 'wmv', 'avc', 'mk3d', 'xvid', 'mpg', 'flv', 'aac', 'asf', 'm4a', 'm4v', 'mka', 'ogg' 'oga', 'ogv', 'ogx', '3gp', 'VIVO', 'PVA', 'NUV', 'NSV', 'NSA', 'FLI', 'FLC']

requestTimeout = 30
EXT_BLACKLIST = ['rar.html','.php','.txt','.iso','.zip', '.rar', '.jpeg', '.img', '.jpg', '.RAR', '.ZIP', '.png' , '.sub', '.srt']

data = {}

# ####################################################################################
# ################################ REAL DEBRID #######################################
# ####################################################################################

def transferList(page='1'):
	clearAll = '%s?action=%s' % (sysaddon, 'rdDeleteAll')
	item = control.item(label='[Delete All Downloads]')
	control.addItem(handle=syshandle, url=clearAll, listitem=item, isFolder=False)

	r = []
	
	try: r, isNext = realdebrid().transferList(page=int(page), info=True)
	except: pass
	
	try:
		for result in r:
			try:
				cm = []
				icon = result['host_icon']
				name = result['filename']
				name = normalize(name)
				id = result['id']
				link = result['link']
				ext = name.split('.')[-1].encode('utf-8')

				if ext in VALID_EXT: isPlayable = True	
				else: isPlayable = False
					
				label = ext.upper() + " | " + name
				
				item = control.item(label=label)
				item.setArt({'icon': icon, 'thumb': icon})
				item.setProperty('Fanart_Image', control.addonFanart())

				infolabel = {"Title": label}
				item.setInfo(type='Video', infoLabels = infolabel)
				item.setProperty('IsPlayable', 'true')
							
				url = result['download']
				cm.append(('Delete Download Item', 'RunPlugin(%s?action=rdDeleteItem&id=%s&type=downloads)' % (sysaddon, id)))
				if control.setting('downloads') == 'true': cm.append(('Download from Cloud', 'RunPlugin(%s?action=download&name=%s&url=%s&id=%s)' % (sysaddon, name, url, id)))
				item.addContextMenuItems(cm)
				control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
			except:pass
	except:pass

	
	try:
		if isNext == True:
			page = int(page) + 1
			item = control.item(label='NEXT >>>')
			item.setArt({'icon': control.addonIcon()})
			item.setProperty('Fanart_Image', control.addonFanart())
			x = '%s?action=%s&page=%s' % (sysaddon, 'rdTransfers', str(page))
			control.addItem(handle=syshandle, url=x, listitem=item, isFolder=True)
	except: pass
	
	control.content(syshandle, 'movies')
	control.directory(syshandle, cacheToDisc=True)
	

def torrentList(page='1'):
	r, isNext = realdebrid().torrentList(page=int(page), info=True)

	if control.setting('sort.torrents') == 'true':
		try: r = sorted(r, key=lambda k: utils.title_key(k['filename']))
		except: pass
		
	for item in r:
		cm = []
		status = item['status']
		id = item['id']
		name = item['filename']
		label = status.upper() + " | " + name
		item = control.item(label=label)
		item.setArt({'icon': control.addonIcon()})
		item.setProperty('Fanart_Image', control.addonFanart())
		infolabel = {"Title": label}
		cm.append(('Delete Torrent Item', 'RunPlugin(%s?action=rdDeleteItem&id=%s&type=torrents)' % (sysaddon, id)))
		url = '%s?action=%s&id=%s' % (sysaddon, 'rdTorrentInfo', id) 
		item.addContextMenuItems(cm)
		control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)

	try:
		if isNext == True:
			page = int(page) + 1
			item = control.item(label='NEXT >>>')
			item.setArt({'icon': control.addonIcon()})
			item.setProperty('Fanart_Image', control.addonFanart())
			x = '%s?action=%s&page=%s' % (sysaddon, 'rdTorrentList', str(page))
			control.addItem(handle=syshandle, url=x, listitem=item, isFolder=True)
	except: pass
				
	control.directory(syshandle, cacheToDisc=True)
	
def torrentInfo(id):
	r = realdebrid().torrentInfo(id)
	links = r['links']
	files = r['files']
	try: files = sorted(files, key=lambda k: utils.title_key(k['path']))
	except:pass
	count = 0
	for x in files:
		try:
			oriGinalName = x['path']
			if oriGinalName.startswith('/'):
				name = oriGinalName.split('/')[-1]

			ext = name.split('.')[-1].encode('utf-8')

			if ext in VALID_EXT: isPlayable = True	
			else: isPlayable = False
			
			if not ext.lower() in VALID_EXT: raise Exception()
			
			
			label = ext.upper() + " | " + name
			
			item = control.item(label=label)
			item.setArt({'icon': control.addonIcon()})
			item.setProperty('Fanart_Image', control.addonFanart())

			# itemID = x['id']
			# playlink = links[count]
			# count += 1
			
			infolabel = {"Title": label}
			item.setInfo(type='Video', infoLabels = infolabel)
			item.setProperty('IsPlayable', 'true')
					
			url = url = '%s?action=%s&name=%s&id=%s' % (sysaddon, 'playtorrentItem', name, id) 
			#item.addContextMenuItems(cm)
			control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
		except: pass
					
	control.content(syshandle, 'movies')
	control.directory(syshandle, cacheToDisc=True)
	
	
def playtorrentItem(name, id):
	torrInDownload = []
	try : name = name.split('/')[-1]
	except: name = name
	try:
		downloads = realdebrid().transferList()
		torrInDownload = [i for i in downloads if i['filename'].lower() == name.lower()][0]
	except:pass
	
	if len(torrInDownload) > 0:
		item = control.item(label=name)
		item.setArt({'icon': control.addonIcon()})
		item.setProperty('Fanart_Image', control.addonFanart())		
		infolabel = {"Title": name}
		item.setInfo(type='Video', infoLabels = infolabel)
		item.setProperty('IsPlayable', 'true')	
		item = control.item(path= torrInDownload['download'])
		
		control.resolve(int(sys.argv[1]), True, item)
		
	else:
		newTorr = []

		try:
			result = torrentItemToDownload(name, id)
			if result != None: newTorr.append(result)
		except:pass

		time.sleep(1)

		torrItem = newTorr[0]
		
		if len(torrItem) > 0:
			control.infoDialog('Playing Torrent Item', torrItem['filename'], time=3)
			item = control.item(label=name)
			item.setArt({'icon': control.addonIcon()})
			item.setProperty('Fanart_Image', control.addonFanart())		
			infolabel = {"Title": name}
			item.setInfo(type='Video', infoLabels = infolabel)
			item.setProperty('IsPlayable', 'true')	
			item = control.item(path= torrItem['download'])
			control.resolve(int(sys.argv[1]), True, item)
			
			
def torrentItemToDownload(name, id):
	torrInDownload = []
	torrItem = []
	FileMatch = False
	try:
		#print ("TORRENT ITEM TO DOWNLOAD", name, id)
		r = realdebrid().torrentInfo(id)
		links = r['links']
		files = r['files']
		newTorr = []
		
		#print ("TORRENT ITEM TO DOWNLOAD LEN", len(links), len(files))
		count = 0
		for x in files:
			try:
				itemID = x['id']
				itemName = x['path']
				
				ext = itemName.split('.')[-1].encode('utf-8')				
				if not ext.lower() in VALID_EXT: raise Exception()
		
				#print ("TORRENT ITEM TO DOWNLOAD 2", count, itemName)				

				playlink = links[count]
				count += 1	
				
				fileName = itemName
				try: fileName = fileName.split('/')[-1]
				except:pass
				
				origName = name
				try: origName = origName.split('/')[-1]
				except: pass
				
				#print ("TORRENT ITEM TO DOWNLOAD PASSED", count, itemName)
				if not cleantitle.get(fileName) == cleantitle.get(origName): raise Exception()
				result = realdebrid().resolve(playlink, full=True)
				if result != None: newTorr.append(result)
			except:pass
		
		time.sleep(1)
		torrItem = newTorr
		
		if len(torrItem) > 0: 
			for x in torrItem:
				fileName = x['filename']
				try: fileName = fileName.split('/')[-1]
				except:pass
				
				origName = name
				try: origName = origName.split('/')[-1]
				except: pass
				if cleantitle.get(fileName) == cleantitle.get(origName): 
					FileMatch = True
					return x
					
		if FileMatch == False:  #FALLBACK TO UNRESTRICT ALL PACK
			for y in links:
				try: 
					result_2 = realdebrid().resolve(y, full=True)
					newFileName = result_2['filename']
					try: newFileName = newFileName.split('/')[-1]
					except:pass
					origName = name
					try: origName = origName.split('/')[-1]	
					except: pass

					if cleantitle.get(newFileName) == cleantitle.get(origName): 
						FileMatch = True
						return result_2
						
					realdebrid().delete(result_2['id'])
				except:pass
			
				

	except: return []

	
def scrapecloud(title, year=None, season=None, episode=None):
	progress = control.progressDialogBG
	cachedSession = control.setting('cached.mode')
	playbackMode  = control.setting('playback.mode')
	matchTitle  = control.setting('match.mode')
		
		
	if cachedSession == 'true': # CACHE MODE	
			if control.setting('first.start') == 'true':
				progress.create('Caching Your Cloud','Please Wait...')
				progress.update(100,'Caching Your Cloud','Please Wait...')
				r = realdebrid().scraperList(cache = True)
			else:
				control.infoDialog('Using Cached Cloud List', time = 3)
				r = realdebrid().cloudJson(mode= 'get')
				control.setSetting(id='first.start', value='false')

	else:
		#print ("SCRAPING NORMAL")
		progress.create('Scraping Your Cloud','Please Wait...')
		progress.update(100,'Scraping Your Cloud','Please Wait...')
		r = realdebrid().scraperList()
		
	try: progress.close()
	except: pass
	try: progress.close()
	except: pass

	labels = []
	sources = []
	types = []
	IDs = []
	sourceNames = []	
	normalSources = []
	exactSources  = []
	
	# TITLE CHECK SCRAPE ROUTINE
	titleCheck = cleantitle.get(title)
	exactPlay = False
	if season != None:
		epcheck    = "s%02de%02d" % (int(season), int(episode))
		epcheck_2  = "%02dx%02d"  % (int(season), int(episode))
		
		dd_season  = "%02d" % int(season)
		dd_episode = "%02d" % int(episode)
		
		exactCheck_1 = titleCheck + epcheck
		exactCheck_2 = titleCheck + epcheck_2

	else:
		if year == '' or year == None or year == '0': year = ''
		exactCheck_1 = titleCheck + year
		exactCheck_2 = titleCheck + year
	
	downloadList = []
	torrentList  = []
	
	try: downloadList = [i for i in r if i['type'] == 'download']
	except: pass
	try: torrentList = [i for i in r if i['type'] == 'torrent']
	except: pass
		
	# SCRAPE DOWNLOADLIST FIRST
	for x in downloadList:
		try:
			id = x['id']
			name = x['name'].encode('utf-8')
			name = normalize(name)
			x.update({'type':'download'})

			if not titleCheck in cleantitle.get(name): raise Exception()

			normalSources.append(x)
			
			if exactCheck_1 in cleantitle.get(name) or exactCheck_2 in cleantitle.get(name):
				exactSources.append(x)
			else:
				epmixed = re.findall('[._ -]s?(\d+)[e|x](\d+)[._ -]', name.lower())[0]
				s = epmixed[0]
				e = epmixed[1]
				if s == dd_season or s == season:
					if e == dd_episode or e == episode: exactSources.append(x)
		except:pass
		
	content = []

	if len(exactSources) == 1:
		content = exactSources[0]
		exactPlay = True
		
	# FALLBACK TO TORRENTLIST SCRAPE
	try:
		for y in torrentList:
			try:
				id = y['id']
				name = y['name'].encode('utf-8')
				name = name.split('/')[-1]
		
				y.update({'type':'torrent'})
				if not titleCheck in cleantitle.get(name): raise Exception()

				normalSources.append(y)
				
				if exactCheck_1 in cleantitle.get(name) or exactCheck_2 in cleantitle.get(name):
					exactSources.append(y)
				else:
					epmixed = re.findall('[._ -]s?(\d+)[e|x](\d+)[._ -]', name.lower())[0]
					s = epmixed[0]
					e = epmixed[1]
					if s == dd_season or s == season:
						if e == dd_episode or e == episode: exactSources.append(y)
						
			except:pass

		if len(exactSources) == 1: 
			content = exactSources[0]
			exactPlay = True
	except:pass

	#print ("EXACT SOURCES", exactSources)
	#print ("NORMAL SOURCES", normalSources)
	# EXACT PLAY AND AUTO PLAY MODE
	if playbackMode == '0' and exactPlay == True: 
		if content['type'] == 'download': return content['link'], content['id']
		else: 
			torrName = content['name']
			torrFile = torrentItemToDownload(torrName, content['id'])
			control.infoDialog('Playing Torrent Item', torrFile['filename'], time=3)
			return torrFile['download'], torrFile['id']
		
	# NORMAL PLAY MODE	
	elif len(exactSources) > 1 and playbackMode == '0':	
		for result in exactSources:
			type = result['type']
			fileLabel = type
			id = result['id']
			name = result['name'].encode('utf-8')
			#name = normalize(name)
			sourceNames.append(name)
			
			playLink = result['link']
			try: labelName = name.split('/')[-1]
			except: labelName = name
			
			label = "[B]" + fileLabel.upper() + " |[/B] " + labelName

			labels.append(label)
			sources.append(playLink)
			types.append(type)
			IDs.append(id)
			
	elif len(exactSources) > 0 and matchTitle == 'true':	
		for result in exactSources:
			type = result['type']
			fileLabel = type
			id = result['id']
			name = result['name'].encode('utf-8')
			#name = normalize(name)
			sourceNames.append(name)
			
			playLink = result['link']
			try: labelName = name.split('/')[-1]
			except: labelName = name
			
			label = "[B]" + fileLabel.upper() + " |[/B] " + labelName

			labels.append(label)
			sources.append(playLink)
			types.append(type)
			IDs.append(id)
	else:
		
		for result in normalSources:
			type = result['type']
			fileLabel = type
			id = result['id']
			name = result['name'].encode('utf-8')
			#name = normalize(name)
			sourceNames.append(name)
			
			playLink = result['link']
			try: labelName = name.split('/')[-1]
			except: labelName = name
			
			label = "[B]" + fileLabel.upper() + " |[/B] " + labelName

			labels.append(label)
			sources.append(playLink)
			types.append(type)
			IDs.append(id)
	
	
	if len(sources) < 1: return '0', '0'
	select = control.selectDialog(labels)
	if select == -1: return '0', '0'
	selected_type = types[select]
	selected_url = sources[select]
	selected_id = IDs[select]
	selected_name = sourceNames[select]
	
	if selected_type != 'download': 
		torrName = selected_name
		torrFile = torrentItemToDownload(torrName, selected_id)
		control.infoDialog('Playing Torrent Item', torrFile['filename'], time=3)
		return torrFile['download'], torrFile['id']
		
	else: return selected_url, selected_id
	
	
def downloadItem(name, url, id):
	from resources.lib.modules import downloader
	downloader.downloader().download(name, url)
	
class realdebrid:
	def __init__(self):
		self.RealDebridApi = 'https://api.real-debrid.com/rest/1.0'
		self.RD_APINAME = 'Realizer'
		self.RD_CLIENTID = 'X245A4XAIBGVM'
		self.RD_OAUTH = 'https://api.real-debrid.com/oauth/v2/device/code?client_id=%s&new_credentials=yes' % self.RD_CLIENTID
		self.RD_TOKEN_AUTH = "https://api.real-debrid.com/oauth/v2/token"
		self.RD_CREDENTIALS_AUTH = "https://api.real-debrid.com/oauth/v2/device/credentials?client_id=%s&code=%s"
		self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
		self.transfers = []
		self.torrentFiles = []
		self.torrents = []	
	
	def auth(self):
		result = requests.get(self.RD_OAUTH, timeout=requestTimeout).json()
		line1 = "1) Visit:[B][COLOR skyblue] %s [/COLOR][/B]"
		line2 = "2) Input Code:[B][COLOR skyblue] %s [/COLOR][/B]"
		line3 = "Note: Your code has been copied to the clipboard"
		verification_url = (line1 % result['verification_url']).encode('utf-8')
		user_code = (line2 % result['user_code']).encode('utf-8')
		expires_in = result['expires_in']
		device_code = result['device_code']
		interval = result['interval']

		try:
			from resources.lib.modules import clipboard
			clipboard.Clipboard.copy(result['user_code'])
		except:pass
		
		progressDialog = control.progressDialog
		progressDialog.create('Real Debrid', verification_url, user_code, line3)

		for i in range(0, int(expires_in)):
			try:
				if progressDialog.iscanceled(): break
				time.sleep(1)
				if not float(i) % interval == 0: raise Exception()
				
				percent = (i * 100) / int(expires_in)
				progressDialog.update(percent, verification_url, user_code, line3)
				
				credentials = self.getCredentials(device_code)
				if not "client_secret" in str(credentials): raise Exception()
				
				client_secret = credentials['client_secret']
				client_id = credentials['client_id']
				r = self.getAuth(self.RD_TOKEN_AUTH , client_id, client_secret, device_code)

				if 'access_token' in str(r): 
					token = r['access_token']
					refresh_token = r['refresh_token']		
					self.saveJson(token=token, client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
					control.infoDialog('RealDebrid Authorized')
					
					try: progressDialog.close()
					except: pass 
					
					return token
					break
			except:
				pass
		try: progressDialog.close()
		except: pass
				
	def getCredentials(self, device_code): 
		url = self.RD_CREDENTIALS_AUTH % (self.RD_CLIENTID, device_code)
		result = requests.get(url, timeout=5).json()
		return result
					
	def getAuth(self, url, client_id, client_secret, device_code): 
		headers = {'User-Agent': self.USER_AGENT}
		data = {'client_id': client_id, 'client_secret': client_secret, 'code': device_code, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
		result = requests.post(url, data=data, headers=headers, timeout=requestTimeout).json()
		return result
		
	def saveJson(self, client_id=None, client_secret=None, token=None, refresh_token=None, expires_in=None):
		from datetime import datetime
		timeNow = datetime.now().strftime('%Y%m%d%H%M')
		dirCheck = xbmc.translatePath(addonPath)
		if not os.path.exists(dirCheck): os.makedirs(xbmc.translatePath(dirCheck))
		if token != None: data = {'client_id': client_id, 'client_secret': client_secret, 'token': token, 'refresh_token': refresh_token , 'added':timeNow}
		else: data = {'client_id': client_id, 'client_secret': client_secret, 'token':'0', 'refresh_token': '0' , 'added': timeNow}
		with open(rdSettings, 'w') as outfile: json.dump(data, outfile, indent=2)
		
		
	def refreshToken(self, refresh_token, client_secret, client_id): 
		headers = {'User-Agent': self.USER_AGENT}
		data = {'client_id': client_id, 'client_secret': client_secret, 'code': refresh_token, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
		result = requests.post(self.RD_TOKEN_AUTH, data=data, headers=headers, timeout=requestTimeout).json()
		if 'access_token' in str(result):
			# expires_in = result['expires_in']
			token = result['access_token']
			refresh_token = result['refresh_token']
			# print ("REFRESHING TOKEN", token)
			self.saveJson(token=token, client_secret=client_secret, client_id=client_id, refresh_token=refresh_token)
			return token
			
	# REAL DEBRID TOKEN #######################################		
	def getToken(self, refresh=False):
		token = '0'
		if not os.path.exists(rdSettings): 
			self.saveJson()
			return
		if refresh: 
			try:
				with open(rdSettings) as json_file:
					try:
						data = json.load(json_file)
						refresh_token = data['refresh_token']
						client_id = data['client_id']
						client_secret = data['client_secret']
						token = self.refreshToken(refresh_token, client_secret, client_id)
					except:	token = None
				if token == '' or token == None or token == '0': control.infoDialog('Real Debrid is not Authorized','Please authorize in the settings')
			except: pass
			
		else:
			try:
				with open(rdSettings) as json_file:
					try:
						data = json.load(json_file)
						token = data['token']
					except:	token = None
				if token == '' or token == None or token =='0': control.infoDialog('Real Debrid is not Authorized','Please authorize in the settings')
			except: pass
		if token == '' or token == None: token = '0'
		return token
		
	def accountInfo(self, refresh=False):
		token = '0'
		if not os.path.exists(rdSettings): self.saveJson()
		try:
			with open(rdSettings) as json_file:
				try:
					data = json.load(json_file)
					token = data['token']
				except:	token = None
		
		except: pass
		if token == '' or token == None or token == '0': return False
		else: return True
		
	def getUser(self, token):
		try:
			# --------------- DEBRID AUTH -----------------------------------------	
			headers = {'Authorization': 'Bearer %s' % token, 'User-Agent': self.USER_AGENT}
			# --------------- DEBRID AUTH -----------------------------------------	
			url = self.RealDebridApi + '/user'
			result = self.rdRequest(url).json()
			if 'error' in result: return ''
			user = result['username'].encode('utf-8')
			return user
		except:
			return ''
		
	def rdRequest(self, url, method='get', data=None, params=None, refresh=False):
		
		token = self.getToken(refresh=refresh)
		headers = {'Authorization': 'Bearer %s' % token, 'User-Agent': self.USER_AGENT}
		try:
			if method == 'get': result = requests.get(url, headers=headers, params=params, timeout=requestTimeout)
			elif method == 'post': result = requests.post(url, headers=headers, data=data, timeout=requestTimeout)
			elif method == 'delete': result = requests.delete(url, headers=headers, data=data, timeout=requestTimeout)
		except requests.Timeout as err: control.infoDialog('REALDEBRID TIMED OUT', time=3)
		if result.status_code == 401: 
			if not refresh: 
				result = self.rdRequest(url, method=method, data=data, refresh=True)
				return result
			else: return result
		else: 
			return result
	
	def transferList(self, page = 1, info=False):
		try:
			url = self.RealDebridApi + '/downloads'
			params = {'limit': 100, 'page': page}
			nextPage = False
			
			result = self.rdRequest(url, method='get', params=params)
			
			if result.json() != None: 
				heads = result.headers
				totalCounts = heads['X-Total-Count']
					
				pageCount = int(page) * 100	
				if int(totalCounts) > pageCount: nextPage = True
				self.transfers += result.json()
				
			else:
				if info == True:
					return self.transfers, nextPage
				else:
					return self.transfers	

			if info == True:
				return self.transfers, nextPage
			else:
				return self.transfers	
					
		except:
			return []
			
	def torrentList(self, page = 1, scraper = False, info = False):
		url = self.RealDebridApi + '/torrents'
		params = {'limit': 100, 'page': page}

		#print ("TORRENTLIST", params, scraper)
		nextPage = False
		
		result = self.rdRequest(url, method='get', params=params)
		
		if result.json() != None: 
			heads = result.headers
			totalCounts = heads['X-Total-Count']
				
			pageCount = int(page) * 100	
			if int(totalCounts) > pageCount: nextPage = True
			self.torrents += result.json()
			
		else:
			if info == True:
				return self.torrents, nextPage
			else:
				return self.torrents
			
		if info == True:
			#print ("RETURNING TORRENTS", len(self.torrents))
			return self.torrents, nextPage
		else:
			return self.torrents


	def torrentInfo(self, id):
		url = self.RealDebridApi + '/torrents/info/' + id
		result = self.rdRequest(url, method='get').json()
		return result

	def torrentselectFiles(self, torrentID, fileID):
		url = self.RealDebridApi + '/torrents/selectFiles/' + torrentID
		data = {'files': fileID}
		result = self.rdRequest(url, method='post', data=data).json()
		return result

		
	def addtorrent(self, torrent):
		url = self.RealDebridApi + '/torrents/addMagnet'
		data = {'magnet': torrent}
		result = self.rdRequest(url, method='post', data=data).json()
		return result

	def getTorrentFilesId(self, id):
		try:
			data = {'files': fileID}
			idTorrent = '/torrents/selectFiles/%s' % id
			url = self.RealDebridApi + idTorrent
			r = self.rdRequest(url, data=data, method='post')
			if r.status_code == 204: print "[REALDEBRID] >>> TORRENT CACHED"
		except:
			pass


	def selectTorrentList(self, id, fileIDs):
		try:
			files = ','.join(map(str, fileIDs))
			data = {'files': files}
			idTorrent = '/torrents/selectFiles/%s' % id
			url = self.RealDebridApi + idTorrent
			r = self.rdRequest(url, data=data, method='post')
			if r.status_code == 204: print "[REALDEBRID] >>> TORRENT CACHED"
			return r.json()
		except:
			pass		
		
		

	# #######  REALDEBRID SCRAPERS AND CLOUD CACHE ###############################################
	
	def torrentScrapePages(self):
		self.page = 1
		self.nextPage = False
		self.scrapedTorrents = []		
		results, self.nextPage = self.torrentList(page = self.page, info = True)
		if results != None: self.scrapedTorrents = results
		
		while self.nextPage == True:
			self.page += 1
			#print ("SCRAPING MULTIPLE PAGES", self.page)
			results, self.nextPage = self.torrentList(page = self.page, info = True)
			if results != None: self.scrapedTorrents = results
			
		#print ("TOTAL TORRENTS", len(self.scrapedTorrents))
		return self.scrapedTorrents

			
	def torrentScrape(self):
		try:
			threads = []
			torrents = self.torrentScrapePages()
			for item in torrents: 
				threads.append(libThread.Thread(self.torrentScrapeInfo, item['id']))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.torrentFiles
		except:
			pass

	def torrentScrapeInfo(self, id):
		try:
			torrentInfo = self.torrentInfo(id)
			files = torrentInfo['files']
			for item in files:
				ext = item['path'].split('.')[-1]
				if not ext.lower() in VALID_EXT: continue
				data = {'name': item['path'], 'id': id}
				self.torrentFiles.append(data)
		except:
			pass

	def scraperList(self, cache = False):
		self.sources = []
		try:
			downloads = self.transferList()
			#print ("SCRAPERLIST downloads", downloads)
			for down in downloads:
				data = {'type': 'download', 'name': down['filename'], 'link': down['download'], 'id': down['id']}
				self.sources.append(data)
		except:pass

		try:
			torrents = self.torrentScrape()
			#print ("SCRAPERLIST torrents", torrents)
			for torr in torrents:
				data = {'type': 'torrent', 'name': torr['name'], 'link': '0', 'id': torr['id']}
				self.sources.append(data)
		except: pass

		if cache == True: 
			if len(self.sources) > 0: self.cloudJson(self.sources)
			control.setSetting(id='first.start', value='false')
		return self.sources
		
        
	def cloudJson(self, data=None, mode='write'):
		control.makeFile(control.dataPath)
		from datetime import datetime
		timeNow = datetime.now().strftime('%Y%m%d%H%M')
		jsonList = {}
		if mode == 'write':
			jsonList['added'] = timeNow
			jsonList['files'] = data
			with open(cloudFile, 'w') as outfile: json.dump(jsonList, outfile, indent=2)
		elif mode == 'get':
			try:
				with open(cloudFile, 'r') as file:	
					data = json.load(file)
					items = data['files']
					return items
			except:
				return []



	def delete(self, id, type = 'downloads', deleteAll = False):
	
		try:  # DOWNLOADS
			if type != 'downloads': raise Exception()
			if deleteAll == False:
				d = '/downloads/delete/%s' % id
				delete = self.RealDebridApi + d
				result = self.rdRequest(delete, method='delete').json()
			else:
				downloads = self.RealDebridApi + '/downloads'
				r = self.rdRequest(downloads).json()
				for item in r:
					id = item['id'].encode('utf-8')
					d = '/downloads/delete/%s' % id
					delete = self.RealDebridApi + d
					result = self.rdRequest(delete, method='delete').json()		
		except:
			pass
			
		try: # TORRENTS
			if type != 'torrents': raise Exception()
			if deleteAll == False:
				d = '/torrents/delete/%s' % id
				delete = self.RealDebridApi + d
				result = self.rdRequest(delete, method='delete').json()
			else:
				url = self.RealDebridApi + '/torrents'
				r = self.rdRequest(url).json()
				for item in r:
					id = item['id']
					d = '/torrents/delete/%s' % id
					delete = self.RealDebridApi + d
					result = self.rdRequest(delete, method='delete').json()					
		except:
			pass


	def check(self, url, type = 'downloads'):
		try:
			if type != 'torrents': raise Exception()
			hash = torrentHashMagnet(url)
			if hash == None: hash = torrentHashFile(url)
			if hash == '' or hash == None or hash == '0': return '0'
			url = self.RealDebridApi + '/torrents/instantAvailability/' + str(hash)
			r = self.rdRequest(url, method='get').json()
			if 'filename' in str(r): return True
			else: return False
		except: pass
	
	
		try:
			if type != 'downloads': raise Exception()
			if url.startswith("//"): url = 'http:' + url
			u = url
			u = u.replace('filefactory.com/stream/', 'filefactory.com/file/')
			try:
				post = {'link': u}		
				url = self.RealDebridApi + '/unrestrict/check'
				try: result = self.rdRequest(url, data=post, method='post').json()
				except: return False

				if 'error_code' in str(result): return False
				r = ''
				try: r = result.get('supported')
				except: return False
				
				if r == '' or r == None:  return False
				if int(r) > 0: 
					try:
						filename = result['filename'].lower()
						if filename.endswith(tuple(EXT_BLACKLIST)): return False
					except:pass
					url = True
				
				else: url = False
				return url
			except:
				return False
		except: pass
			
	def resolve(self, url, full=False):
		if url.startswith("//"): url = 'http:' + url
		u = url
		try:
			post = {'link': u}		
			url = self.RealDebridApi + '/unrestrict/link'
			result = self.rdRequest(url, method='post', data=post).json()
			if 'error_code' in str(result): return None
			if full == True: return result
			try: url = result['download'].encode('utf-8')
			except: return None
			if url.startswith('//'): url = 'http:' + url
			return url
		except:
			pass

def cleantitle_get(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub(r'\<[^>]*\>','', title)
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\(|\)|\[|\]|\{|\}|\s', '', title)
    title = re.sub('[^A-z0-9]', '', title)
    return title	
	
	

def normalize(txt):
    txt = re.sub(r'[^\x00-\x7f]',r'', txt)
    return txt