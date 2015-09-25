import os
from setuptools import setup

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='media',
    version='1.0.0',
    description='A simple webpage generator for movies',
	long_description=read("README.rst"),
    url='https://github.com/walchko/media_html_page_generator',
    author='Kevin Walchko',
    author_email='kevin.walchko@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Environment :: MacOS X',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Topic :: Multimedia :: Video',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    keywords=['media','html','html5','tmdb','rotten tomatoes'],
    packages=['media'],
    install_requires=['rottentomatoes','tmdb3','requests'],
    entry_points={
        'console_scripts': [
            'media=media.media:main',
        ],
    },
)
