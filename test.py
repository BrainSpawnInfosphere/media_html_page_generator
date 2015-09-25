#!/usr/bin/env python

import os
import media.media as med
import json

directory = './tmp'
if not os.path.exists(directory):
    os.makedirs(directory)

def test_movie_list():
	ml = med.getMovieList('./test')
	ans = ['9.m4v', 'alien (1979).m4v', 'aliens.m4v', 'captain america.m4v', 'eurotrip.mov', 'hellboy 2.m4v', 'hellboy.mp4', 'james bond: skyfall.m4v', 'star wars: the empire strikes back.m4v', 'the matrix.m4v', 'tron.m4v', 'undercover brother.m4v']
	assert len(ml) == len(ans) and ml == ans

def test_tmdb_rt():
	"""
	Test tmdb and rt api
	"""
	mw = med.MovieWrapper()
	m = mw.getMovieInfo(['alien (1979)'],'./here')[0]
	assert m['title'] == 'Alien' and m['year'] == '1979' and m['imdb'] == 'tt0078748' 

def main():
	movie_list = med.getMovieList('./test')
	print movie_list
	mw = med.MovieWrapper()
	movie_info = mw.getMovieInfo(movie_list,'/here')

	# j = json.dumps(movie_info)
	with open('./tmp/movie.json', 'w') as outfile:
		 json.dump(movie_info, outfile, sort_keys = True, indent = 2, ensure_ascii=True)

	med.css.write_css('./tmp/mystyle.css')

	table = med.makeTable(movie_info)

	page = med.WebPage()
	page.create(table)
	page.savePage('./tmp/test.html')


if __name__ == "__main__":
	main()
