#!/usr/bin/env python3

"""
Python script for fetching information of movies from your directory,
 sorting them from best to worse using a Bayesian Estimate formular.

(C) Sochima Biereagu, 2019
"""

import os, sys, json, locale
from pathlib import Path
from difflib import SequenceMatcher

import PTN 			# pip install parse-torrent-name
import requests

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 


API_KEY = 'YOUR_OMDB_API_KEY'
# get yours at http://www.omdbapi.com/apikey.aspx


if len(sys.argv)<2 or (len(sys.argv)>1 and sys.argv[1]=='-h'): #{
	print('Usage: %s [DIRECTORY]' % sys.argv[0])
	print("""
Creates a movies.json file containing the user ratings and votes of the movies listed in DIRECTORY.

Movie data is fetched from OMDb

The movies.json is sorted from best to worse using a Bayesian Estimate formular""")
	exit()
#}


# get cmd arg
arg = sys.argv[1]
path = os.path.abspath(arg)

if not (os.path.exists(path) and os.path.isdir(path)): #{
	print("invalid path")
	exit()
#}

# get movie list from provided path
p = Path(path)
movie_list = [os.path.splitext(file.name)[0] for file in p.iterdir() if file.is_file()]


####################
# helper functions #
####################

# ensure strings similarity >= 40%
def similar(a, b): #{
	return SequenceMatcher(None, a, b).ratio() >= .4
#}

# Converts a string to an integer
def atoi(N): #{
	try: return locale.atoi(N)
	except: return 0
#}

# Parses a string as a float
def atof(N): #{
	try: return locale.atof(N)
	except: return 0
#}

# Weighted rating using Bayesian estimate
def WR(o):
	R = o['IMDb rating']
	v = o['IMDb votes']
	m = 7000
	C = RATINGS['avg']
	WR = R*(v/(v+m)) + C*(m/(v+m))
	o['WR'] = WR
	return WR

# Print iterations progress
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█', printEnd = "\r"): #{
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
#}


#############
# Movie API #
#############
RATINGS = {"sum":0, "avg":0}

class API: #{
	def __init__(self):
		self.url = "http://www.omdbapi.com/"
		self.params = {
			"v": "1",
			"type":	"movie",
			"apikey": API_KEY
		}

	def search(self, title): #{
		U = self.url+"?t="+title
		r = requests.get(U, params=self.params)

		res = r.json()

		# no result
		if res['Response'] == 'False': #{
			return None
		#}

		# movie title dont match with search result
		if not similar(title, res['Title']): #{
			return None
		#}

		# aggregate ratings for later WR sorting
		RATINGS['sum'] += atoi(res['imdbRating'])

		return {
			"Title": title,
			"Genre": res['Genre'],
			"Runtime": res['Runtime'],
			"IMDb rating": atof(res['imdbRating']),
			"IMDb votes": atoi(res['imdbVotes']),
			"Metascore": atoi(res['Metascore'])
		}
	#}
#}


##########################
# get movies information #
##########################

api = API()
seen, unseen = [], []

i, N = 1, len(movie_list)
for title in movie_list: #{
	title = PTN.parse(title)['title']

	movie = api.search(title)

	if movie: #{
		seen += [movie]
	#}
	else: #{
		unseen += [title]
	#}

	printProgressBar(i, N)
	i+=1
#}


########################
# store/display result #
########################

# no movie found
if not seen: #{
	print("No movies found in this directory")
	exit()
#}

if unseen: #{
	print("The following weren't found: ")
	print(", ".join(unseen), "\n")
#}

# sort movie (best to worse)
RATINGS['avg'] = RATINGS['sum'] / len(seen)
seen.sort(key=lambda o: -WR(o))


# save JSON data
JSON = 'movies.json'
with open(JSON, 'w+') as jf: #{
	s = str(seen).replace("\'", "\"")
	j = json.loads(s)
	jf.write(json.dumps(j, indent=4))
	
	print("Movies data saved in ./movies.json")
#}
jf.close()
