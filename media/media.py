#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# copyright kevin j. walchko 17 Jan 2015
#------------------
# 17 Jan 2015 Created
# 13 Feb 2015 Made a python module and clean up
#

import sys      # cmd line
import os       # dir list
import re       # clean up movie names
import time     # sleep
import json     # save movie info
import argparse # command line args
import css      # create a css style sheet

# for getting movie posters, rating, etc
from rottentomatoes import RT as rt	
from tmdb3 import set_key
from tmdb3 import set_cache
from tmdb3 import searchMovie, Movie
from tmdb3 import searchMovieWithYear
from tmdb3 import get_locale, set_locale

import string # re giving issues, try cleanup movie names


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
					sub[a] = b.encode('ascii', 'ignore') # repr
				ascii[k] = sub
			else: ascii[k] = v
		new_list.append(ascii)
	return new_list
		
class WebPage:
	def __init__(self):
		self.page = []
		
	def create(self,html_body):
		html_start = """
<!DOCTYPE html>
<html>
  <head>
	<link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
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
	
	def savePage(self,path = './'):
		css.write_css(path)
		if not path[-1] == '/': path += '/'
		filename = path + 'movie.html'
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
		#tom = u'./images/tomato.png'
		tom = 'fa-thumbs-up'
	else:
		#tom = u'./images/splat.png'
		tom = 'fa-thumbs-down'
	#row.append('<div class="right"><div class="rt_rating"><img src="%s" height="40"><i class="rating">%s</i></div></div>'%(tom,movie['score']['critic']))
	row.append('<div class="right"><div class="rt_rating"> <i class="fa %s fa-1x fa-border"> %s </i> </div></div>'%(tom,movie['score']['critic']))
	
	# audience score
	tom = ''
	if int(movie['score']['audience']) > 60:
		#tom = u'./images/popcorn_full.png'
		tom = '<i class="fa fa-users fa-3x"></i>'
	else:
		#tom = u'./images/popcorn_empty.png'
		tom = '<i class="fa fa-users fa-3x"></i>'
	
	tom = 'fa-users'
		
	#row.append(u'<div class="right"><div class="rt_rating"><img src="%s" height="40"><i class="rating">%s</i></div></div>'%(tom,movie['score']['audience']))
	row.append(u'<div class="right"><div class="rt_rating"> <i class="fa %s fa-1x fa-border"> %s </i> </div></div>'%(tom,movie['score']['audience']))		
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

class MovieWrapper:
	"""
	Handles talking with movie websites via their APIs
	"""
	def __init__(self,key_file=''):
		try:
			if key_file:
				k=open(key_file).read()
				keys = json.loads(k)
				tmdb_key = keys['TMDB']
				self.rt_api = keys['ROTTENTOMATOES']
			else:
				tmdb_key = os.environ['TMDB']
				self.rt_api = os.environ['ROTTENTOMATOES']
		except:
			exit('Error getting API keys')
		
		set_key(tmdb_key)
		set_cache(filename='tmdb3.cache')	
		set_locale()
	
	def get_rt(self,mov):
		ret=rt(self.rt_api).search( mov['title'] )
		for m in ret:
			if 'alternate_ids' in m:
				if 'imdb' in m['alternate_ids']:
					if m['alternate_ids']['imdb'] == mov['imdb'] or int(m['alternate_ids']['imdb']) == int(mov['imdb'].lstrip('tt')):
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
		print '[-] Error: could not match IMDB for',mov['title'],mov['imdb']
		return mov
	
	def getMovieInfo(self,movie_list,hd_path):
		movie_info = []
		for m in movie_list:
			ans = self.get(m)
			if ans == False:
				print '[-] Error: tmdb returned nothing for',m
				pass
			else:
				if not hd_path[-1] == '/': hd_path += '/'
				ans['hd_link']=hd_path + m
				ans['fname'] = m
				movie_info.append(ans)
				time.sleep(0.3)
		return movie_info
				
	def get(self,movie):
		"""
		Gets the info for a single movie
	
		in: movie name [string]
		out: movie info [dict]
		"""
		movie = movie.replace('.mov','')
		movie = movie.replace('.m4v','')
		movie = movie.replace('.mp4','')
		movie = re.sub('[_-]',' ',movie)
		movie = movie.lower()
		
		try:
			ret = []
			# if there is a year in the title, the use it for the search
			if '(' in movie and ')' in movie:
				ret = list(searchMovieWithYear(movie))
			else:
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
			
			#pp.pprint(mov)
			
			return mov
		except Exception as e:
			print '[-] Error:',movie,'msg:',e
			return False

def getMovieList(path,prnt=False):
	movie_list = os.listdir(path)
	
	# remove some misc stuff
	for i in ['.DS_Store','.sync','.git','.AppleDouble']:
		if i in movie_list: movie_list.remove(i)
	
	# put them in order
	movie_list.sort()
	
	if prnt:
		print '*'*60
		print '\tFound',len(movie_list),'movies at',path
		print '*'*60
	
	return movie_list


def handleArgs():
	parser = argparse.ArgumentParser('A simple media html5 generator')
	parser.add_argument('-p', '--path', help='path to install webpages', default='./')
	parser.add_argument('-m', '--movies', help='absolute path to the movies', default='./')
	parser.add_argument('-k', '--keys', help='location of API keys', default='/Users/kevin/Dropbox/accounts.yaml')
	
	args = vars(parser.parse_args())
	return args	
	
def run(path,hd_path,key_file):
	# get movies
	movie_list = getMovieList(hd_path)
	
	# get tomatoes info
	mw = MovieWrapper(key_file)
	movie_info = mw.getMovieInfo(movie_list,hd_path)
	movie_info = makeAscii(movie_info)
	
	if not path[-1] == '/': path += '/'
	filename = path + 'movie.json'
	with open(filename, 'w') as outfile:
		 json.dump(movie_info, outfile, sort_keys = True, indent = 2, ensure_ascii=True)
	
	print '*'*60
	print '\t Found',len(movie_info),'movies and now making webpage'
	print '*'*60
	
	table = makeTable(movie_info)
	
	page = WebPage()
	page.create(table)
	page.savePage(path)


def main():
	args = handleArgs()
	
	path = args['path']
	hd_path = args['movies']
	key_file = args['keys']
	
	run(path,hd_path,key_file)

if __name__ == "__main__":
	main()
