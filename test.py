#!/usr/bin/env python

import os
import media.media as med
import json

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
	directory = './tmp'
	if not os.path.exists(directory):
		os.makedirs(directory)
	med.main('./tmp','./test','/Users/kevin/Dropbox/accounts.json')

if __name__ == "__main__":
	main()
