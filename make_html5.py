#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# copyright kevin j. walchko 17 Jan 2015
#------------------
# 17 Jan 2015 Created
#

import sys # cmd line
import os  # dir list
import re  # clean up movie names
import pprint as pp
import time # sleep
import yaml # api keys

def makeAscii(data):
	new_list = []
	for m in data:
		ascii = {}
		for k,v in m.items():
			#print type(v)
			if type(v) is unicode: ascii[k]=v.encode('ascii', 'ignore')
			elif type(v) is dict: 
				sub = {}
				for a,b in v.items():
					sub[a] = b.encode('ascii', 'ignore')
				ascii[k] = sub
			else: ascii[k] = v
		new_list.append(ascii)
	return new_list

def readYaml(fname):
		f = open( fname )
		dict = yaml.safe_load(f)
		f.close()
		return dict
		
def writeYaml(filename,data):
		f = open(filename,'w')
		yaml.dump(data,f)
		f.close()
		
class WebPage:
	def __init__(self):
		self.page = []
		
	def create(self,html_body):
		html_start = """
<!DOCTYPE html>
<html>
  <head>
	<!--link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet"-->
	<link rel="stylesheet" type="text/css" href="mystyle.css">
	
	<meta charset="utf-8">
	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">

	<!-- Optional theme -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap-theme.min.css">

	<!-- Latest compiled and minified JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
  </head>
  <body>"""
		
		html_end = '</body></html>'
		
		page = []
		page.append(html_start)
		page.append(html_body)
		page.append(html_end)
		#page = ''.join(page)
		
		self.page = page
	
	def savePage(self,filename):
		f = open(filename,'w')
		for i in self.page:
			f.write(i)
		f.close()
		
	# Expect a list containing lines of html which will create a Google Map	
	def printPage(self):
		for i in self.page:
			print i

# Creates modal pop-up window
# in: movie dict(), info for window [string]
# out: string
def modal(movie,info):
	id = movie['imdb']
	link = movie['hd_link']
	win=[u'<div class="modal fade" id="%s" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"><div class="modal-dialog  modal-sm"><div class="modal-content"><div class="modal-body">'%id]
	win.append(info)
	win.append(u'</div></div></div></div>')
	win.append(u'\n')
	ans=[line.decode('utf-8') for line in win]
	return u' '.join(ans)

# Info for modal window
# in: movie dict()
# out: string
def subTable(movie):
	row = [u'<table>']
	
	row.append(u'<tr><td><a href="%s"><img src="%s" alt="poster" width="270" height="400"></a><tr><td>'%(movie['hd_link'],movie['poster']) )
	row.append(u'<tr><td><div class="tagline">  %s </div><tr><td> '%(movie['tagline']))
	
	row.append(u'<tr><td> <div>')
	row.append(u'<div class="left"> <i class="mpaa_rating">%s</i> </div>'%movie['rating'])
	
	# critic score
	tom = ''
	if int(movie['score']['critic']) > 60:
		tom = u'./images/tomato.png'
	else:
		tom = u'./images/splat.png'
	row.append('<div class="right"><div class="rt_rating"><img src="%s" height="40"><i class="rating">%s</i></div></div>'%(tom,movie['score']['critic']))
	
	# audience score
	tom = ''
	if int(movie['score']['audience']) > 60:
		tom = u'./images/popcorn_full.png'
	else:
		tom = u'./images/popcorn_empty.png'
		
	row.append(u'<div class="right"><div class="rt_rating"><img src="%s" height="40"><i class="rating">%s</i></div></div>'%(tom,movie['score']['audience']))		
	row.append(u'<div class="center"> <a href="%s"><span class="glyphicon glyphicon-film" aria-hidden="true"></span></a> %s mins </div>'%(movie['trailer'],movie['runtime']))
	row.append(u'</div><tr><td>')
	
	row.append(u'</table>')
	ans = u''.join(row)
	return ans

# Creates each individual frame
# in: movie dict()
# out: single movie info [string] 
def makeFrame(movie):
	poster = movie['poster']
	frame=[u'<div class="img">']
	frame.append(u'<a data-toggle="modal"  data-target="#%s"><img src="%s" alt="poster" width="135" height="200"></a>'%(str(movie['imdb']),poster) )
	frame.append(u'</div>')
	frame.append(u'\n')
	frame.append( modal(movie, subTable(movie)) )
	frame.append(u'\n')
	return u''.join(frame)

	
#
# in: movies dict(tomatoes/tmdb info and filenames)
# out: webpage [string]
def makeTable(movies):
	table = ['']
	for mov in movies:
		table.append(makeFrame(mov))
		table.append('\n')
	return ''.join(table)



from rottentomatoes import RT as rt	
from tmdb3 import set_key
from tmdb3 import set_cache
from tmdb3 import searchMovie, Movie

class MovieWrapper:
	def __init__(self):
		# get api keys
		#keys = readYaml('/home/pi/accounts.yaml')
		keys = readYaml('/Users/kevin/Dropbox/accounts.yaml')
		tmdb_key = keys['TMDB']
		self.rt_api = keys['ROTTENTOMATOES']
		set_key(tmdb_key)
		set_cache(filename='tmdb3.cache')	
	
	def get_rt(self,mov):
		ret=rt(self.rt_api).search( mov['title'] )
		for m in ret:
			if 'alternate_ids' in m:
				if 'imdb' in m['alternate_ids']:
					if m['alternate_ids']['imdb'] == mov['imdb'].lstrip('tt'):
						mov['rating'] = unicode(m['mpaa_rating'])
						mov['year'] = unicode(m['year'])
						mov['score'] = {'critic':0,'audience':0}
						mov['score']['critic'] = unicode(m['ratings']['critics_score'])
						mov['score']['audience'] = unicode(m['ratings']['audience_score'])
						return mov
		# couldn't match the exact movie ... fill w/ dummy values
		mov['rating'] = u'u'
		mov['year'] = u'u'
		mov['score']={'critic': u'0','audience': u'0'}
		print '[-] Error: could not match IMDB for',mov['title']
		return mov
		
	# in: movie name [string]
	# out: movie info [dict]
	def get(self,movie):
		try:
			ret = searchMovie(movie)
			if len(ret) == 0:
				print '[-] Error: could not find',movie
				return False
			else:
				ans = ret[0]
			mov = {}
			mov['title'] = unicode(ans.title.decode('unicode-escape'))
			mov['tagline'] = unicode(ans.tagline.decode('unicode-escape'))
			mov['runtime'] = unicode(ans.runtime)
			t = ans.youtube_trailers
			if not t:
				mov['trailer'] = ' '
			else:
				mov['trailer'] = unicode(t[0].geturl())
			p = ans.poster
			if 'w342' in p.sizes():
				mov['poster'] = unicode(p.geturl('w342'))
			else:
				print '[.] Ops ... getting larger poster for',mov['title'],p.sizes()
				mov['poster'] = unicode(p.geturl())
			mov['imdb'] = unicode(ans.imdb)
		
			mov = self.get_rt(mov)
			
			pp.pprint(mov)
			
			return mov
		except Exception as e:
			print '[-] Error: fucking tmdb3 could not get movie info for:',movie
			print '\t[-] Error Msg:',e
			return False

def main(webpage_name,hd_path):
	# get movies
	movie_list = os.listdir(hd_path)
	
	# remove some misc stuff
	if '.DS_Store' in movie_list: movie_list.remove('.DS_Store')
	if '.sync' in movie_list: movie_list.remove('.sync')
	if '.git' in movie_list: movie_list.remove('.git')
	if '.AppleDouble' in movie_list: movie_list.remove('.AppleDouble')
	
	movie_list.extend(['matrix.m4v','lord of the flies.m4v','harry potter and the chamber of secrets.m4v','evolution.m4v','UNDERCOVER_BROTHER.m4v','tron.m4v','EURO_TRIP.m4v','how to train your dragon.m4v','batman.m4v','alien.m4v','aliens.m4v','raiders of the lost ark.m4v','hellboy.m4v','hellboy_2.m4v','james bond: skyfall.m4v','lord of the rings: return of the king.m4v','star wars: a new hope.m4v','star wars: the empire strikes back.m4v','revenge of the sith.m4v'])
	#movie_list=['matrix.m4v']
	
	#y = readYaml('./movies.yaml')
	
	print '[+] Found',len(movie_list),'movies at',hd_path
	
	# get tomatoes info
	mw = MovieWrapper()
	movie_info = []
	for m in movie_list:
		m_name = m.rstrip('mov')
		m_name = m_name.rstrip('m4v')
		m_name = m_name.rstrip('mp4')
		m_name = re.sub('[_-]',' ',m_name)
		m_name = m_name.lower()
		ans = mw.get(m_name)
		if ans == False:
			print '[-] Error: could not get info for',m
			pass
		else:
			ans['hd_link']=hd_path + '/' + m
			ans['fname'] = m
			movie_info.append(ans)
			#time.sleep(0.3)
			print '[+] Got:',m
	
	#pp.pprint(movies)
	
	movie_info = makeAscii(movie_info)
	
	writeYaml('./movies.yaml',movie_info)
	
	print '*'*60
	print '\t Found',len(movie_info),'movies and now making webpage'
	print '*'*60
	
	table = makeTable(movie_info)
	
	page = WebPage()
	page.create(table)
	page.savePage(webpage_name)
	

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print 'Usage: make_html.py <webpage name> <path_to_movies>'
		exit(1)
	else:
		page = str(sys.argv[1])
		path = str(sys.argv[2])
		
	main( page, path)
