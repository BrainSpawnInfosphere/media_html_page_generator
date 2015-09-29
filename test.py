#!/usr/bin/env python

import os
import media.media as med
import json

def test_movie_list():
	ml = med.getMovieList('./test')
	print ml
	ans = ['9.m4v', 'Alien (1979).m4v', 'Aliens.m4v', 'CAPTAIN_AMERICA.m4v', 'EUROTRIP.mov', 'HELLBOY-2.m4v', 'HELLBOY.mp4', 'THE_MATRIX.m4v', 'TRON.m4v', 'UNDERCOVER_BROTHER.m4v', 'james bond: skyfall.m4v', 'star wars: the empire strikes back.m4v']
	assert len(ml) == len(ans) and ml == ans

def test_tmdb_rt():
	"""
	Test tmdb and rt api
	"""
	mw = med.MovieWrapper()
	m = mw.getMovieInfo(['alien (1979)'],'./here')[0]
	assert m['title'] == 'Alien' and m['year'] == '1979' and m['imdb'] == 'tt0078748' 

def main():
	directory = './tmp'
	if not os.path.exists(directory):
		os.makedirs(directory)
	med.run('./tmp','/Users/kevin/Google Drive/github/media_server/test','/Users/kevin/Dropbox/accounts.json')

if __name__ == "__main__":
	main()
# 	test_movie_list()
# 	test_tmdb_rt()
