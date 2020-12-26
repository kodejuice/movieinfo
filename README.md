# movie info fetch script

A python script which scans your local directory for movies and fetches the IMDb information of those movies,
storing that info in a json file where they are sorted from best to worse using a bayesian estimate formular based on user rating and vote count.

if you have tons of unwatched movies and you're not sure which to watch first then you could use this script to decide the movie to watch first.

## Installing dependencies

```bash
$ pip install parse-torrent-name
```

You would also need to get an API key from OMDb, from [https://www.omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)

once gotten, set the API key in the `main.py` file

```python
...
API_KEY = 'YOUR_OMDB_API_KEY'
...
```

## Usage

```bash
python3 main.py [DIRECTORY]
```

Once complete, a `movies.json` file will be created containing information about the movies found in your local directory.

Heres a sample `movies.json` file

```json
[
    {
        "Title": "The Lion King",
        "Genre": "Animation, Adventure, Drama, Family, Musical",
        "Runtime": "88 min",
        "IMDb rating": 8.5,
        "IMDb votes": 875159,
        "Metascore": 88,
        "WR": 8.432551841561443
    },
    {
        "Title": "John Wick - Chapter 3 - Parabellum",
        "Genre": "Action, Crime, Thriller",
        "Runtime": "131 min",
        "IMDb rating": 7.6,
        "IMDb votes": 197479,
        "Metascore": 73,
        "WR": 7.339826583658958
    },
    {
        "Title": "Dumbo",
        "Genre": "Animation, Drama, Family, Musical",
        "Runtime": "64 min",
        "IMDb rating": 7.2,
        "IMDb votes": 111700,
        "Metascore": 96,
        "WR": 6.775400168491997
    },
    {
        "Title": "Warm Bodies",
        "Genre": "Comedy, Horror, Romance",
        "Runtime": "98 min",
        "IMDb rating": 6.9,
        "IMDb votes": 211703,
        "Metascore": 60,
        "WR": 6.679152549347746
    }
]
```

The movies are sorted based on a weighted rating (**WR**) caculated using the bayesian estimate formular, [Bayes estimator](https://en.wikipedia.org/wiki/Bayes_estimator#Practical_example_of_Bayes_estimators)

### make script global

```bash
$ chmod +x main.py
$ sudo cp ./main.py /usr/bin/movieinfo

$ movieinfo
```
