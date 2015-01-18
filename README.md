# Movie Server

![webpage](./images/webpage.png)
![modal](./images/modal.png)

## Requirements

This uses both [tmdb.org](http:tmdb.org) and [rotten tomatoes](http://rottentomatoes.com)
to get information about movies and generate a webpage. The following libraries are needed:

	sudo pip install rottentomatoes requests tmdb3

You will also have to sign-up for free API keys at both locations in order to access their info.

## Page Generator

	make_html5.py webpage.html ./my_movies

## HTTP Server

The webserver is nodejs and uses http-server. To install:

	npm install http-server -g

Then start it running:90

	http-server ./ -p 8080


## Usage

Now navigate to `computer:8080/<webpage_name>` to access your movies. Mine is `tardis.local:8080/movies.html`.