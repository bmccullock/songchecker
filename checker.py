import urllib2
import sys
from bs4 import BeautifulSoup, SoupStrainer
from collections import Counter
from acora import AcoraBuilder

# ARTIST and Song Title passed in from CLI
ARTIST, SONG_TITLE = sys.argv[1], sys.argv[2]

def build_request_url(artist, song_title):
	"""Prepare user input and return a URL request"""
	base_api_url = 'http://lyrics.wikia.com/api.php?'
	response_format = 'html' # LyricsWikia API returns json, xml, html
	return '%sfunc=getSong&artist=%s&song=%s&fmt=%s' % (base_api_url, 
		ARTIST.replace(' ', '_').lower(), SONG_TITLE.replace(' ', '_').lower(),
		response_format)

def check_song_exists(soup_object):
	"""Check if song exists in LyricsWikia DB"""
	if (soup_object.pre.string) == 'Not found':
		print 'Song not found. Check your spelling. Restart...'
		quit()
	else:
		print 'Song found.'
		return

def remove_bad_tags(soup_object, tag_list):
	"""Remove given tags from soup_object"""
	for tag in tag_list:
		target = soup_object.find_all(tag)
		for tag in target:
			tag.decompose()

def make_lyrics_list(stripped_string_gen):
	"""Takes a generator and returns a list of unicode strings"""
	# Is this needed if already have stripped string gen?
	lyrics_list = []
	for i in lyrics_soup.stripped_strings:
		lyrics_list.append(i)
	return lyrics_list

def make_reference_list(word_list_file):
	"""Load a list of bad words from a txt file into a dictionary."""
	reference_list = []
	with open(word_list_file, 'r') as f:
		words_list = f.readlines()
		for item in words_list:
			s = str(item)[:-2] # should do with regex?
			reference_list.append(s)
	return reference_list

def save_lyrics(song_lyrics):
	"""Write the lyrics and a header to a txt file."""
	# Using global valuse right now
	file_name = '%s - %s.txt' % (ARTIST, SONG_TITLE)
	with open(file_name, 'w') as output_file:
		header = '%s - %s' % (ARTIST, SONG_TITLE)
		output_file.write(header)
		output_file.write('\n\n')
		for string in song_lyrics:
			output_file.write(string)
			output_file.write('\n')

def check_language(reference_list, song_lyrics):
	builder = AcoraBuilder(reference_list)
	acora_engine = builder.build()

	

# Check with the LyricsWikia API to confirm that the song exists and 
# grab URL to full lyrics since API only provides excerpts.
api_url = build_request_url(ARTIST, SONG_TITLE)
api_soup = BeautifulSoup(urllib2.urlopen(api_url).read())

# Confirm that the song actually exists before looking for the url
check_song_exists(api_soup)
lyrics_url = api_soup.find_all('a', title = 'url')[0].string # Grab URL to song

target_div = SoupStrainer(class_='lyricbox') # No need for extra HTML
lyrics_soup = BeautifulSoup(urllib2.urlopen(lyrics_url).read(), parse_only = target_div)

# Remove unwanted tags
tags_for_removal = ['script', 'br']	
remove_bad_tags(lyrics_soup, tags_for_removal)
# Save song lyrics to TXT file

# Create list of strings from lyrics
raw_lyrics = make_lyrics_list(lyrics_soup.stripped_strings)
print raw_lyrics

save_lyrics(raw_lyrics)

# Prepare refence dict of "bad words"
bad_word_reference = make_reference_list('banned_words.txt')
# print bad_word_reference
print check_language(bad_word_reference, raw_lyrics)
c = Counter()



