"""
############################## Final Projec: Date Processing ############################

% Student Name: Xuanyu Li

% Student Unique Name: xuanyuli

% Lab Section 00X:  103

% I worked with the following classmates: none

"""

import json
import requests

def id_popularity_dict(fileName):
    """
    Read a JSON file and create a dictionary mapping movie IDs to their popularity.

    Parameters
    ----------
    filename : str
        The name of the file to be read. The file should be in JSON format,
        with each line containing a JSON object that includes 'id' and 'popularity' keys.

    Returns
    -------
    dict
        A dictionary where each key is a movie ID and each value is the popularity of that movie.
    """
    id_popularity_dict = {}
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        for line in file:
            parts = json.loads(line)
            id_value = parts["id"]
            popularity_value = parts["popularity"]
            id_popularity_dict[id_value] = popularity_value

    return id_popularity_dict

def get_imdb_id_from_tmdb(tmdb_id, tmdb_api_key):
    """
    Retrieve the IMDb ID corresponding to a given TMDb ID using the TMDb API.

    Parameters
    ----------
    tmdb_id : int or str
        The Movie Database (TMDb) ID for the movie.
    tmdb_api_key : str
        Your personal API key for accessing the TMDb API.

    Returns
    -------
    str
        The corresponding IMDb ID for the given TMDb ID. Returns an error message string if the request fails.
    """
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('imdb_id')
    else:
        return f"Error: {response.status_code}"

def writeFile(filename, dict):
    """
    Write the contents of data to a JSON file.

    This function takes a filename and writes the contents of a dict
    to a JSON file with that name. The JSON file is encoded in UTF-8 and 
    the data is written in a formatted way with an indentation of 4 spaces.

    Parameters
    ----------
    filename : str
        The name of the file to which the data will be written. If the file
        already exists, it will be overwritten.
    
    dict : dict
        The dictionary to be written
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(dict, file, ensure_ascii=False, indent=4)

def readFile(fileName,outputName):
    """
    Read and return the contents of a JSON file.

    This function opens a JSON file specified by `filename`, reads its contents, 
    and returns the data as a Python dictionary. The JSON file is assumed to be 
    encoded in UTF-8.

    Parameters
    ----------
    filename : str
        The name of the file from which the data will be read.
    Returns
    -------
    dict
        A dictionary containing the data read from the JSON file.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    json.JSONDecodeError
        If the file is not a valid JSON file.
    """
    with open(fileName, 'w', encoding='utf-8') as file:
        json.dump(outputName, file, ensure_ascii=False, indent=4)

def fetch_movies_info(OMDB_key, movie_ids):
    """
    Fetch and return movie information from the OMDB API for a given set of movie IDs.

    Parameters
    ----------
    OMDB_key : str
        The API key for accessing the OMDB API.
    movie_ids : list of str
        A list of movie IDs for which information will be fetched from the OMDB API.

    Returns
    -------
    dict
        A dictionary where each key is a movie ID and each value is the corresponding movie information. 
        The information is in the form of a dictionary of movie details as returned by the OMDB API.

    Raises
    ------
    requests.RequestException
        If an error occurs during the API requests.
    """
    movies_info = {}

    for movie_id in movie_ids:
        url = f"http://www.omdbapi.com/?apikey={OMDB_key}&i={movie_id}"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                movie_data = response.json()
                movies_info[movie_id] = movie_data
            else:
                print(f"Error fetching data for movie ID {movie_id}: {response.status_code}")

        except requests.RequestException as e:
            print(f"Request failed: {e}")

    return movies_info

class Movie:
    """
    A class to represent a movie with various attributes.

    Parameters
    ----------
    movie_data : dict
        A dictionary containing movie attributes.

    Attributes
    ----------
    Dynamically added based on the keys in movie_data.
    """

    def __init__(self, movie_data):
        for key, value in movie_data.items():
            setattr(self, key, value)

    def __str__(self):
        return f"Movie({', '.join(f'{k}: {v}' for k, v in self.__dict__.items())})"

def create_movie_objects(movie_data_dict):
    """
    Create Movie objects from a dictionary of movie data.

    Parameters
    ----------
    movie_data_dict : dict
        A dictionary where each key is a movie ID and the value is a dictionary of movie attributes.

    Returns
    -------
    dict
        A dictionary of Movie objects with keys formatted as 'movie_{movie_id}'.

    """
    movies = {}
    for key, value in movie_data_dict.items():
        movie_name = f"movie_{key}"
        movies[movie_name] = Movie(value)
    return movies

def add_popularity_to_movies(imdbPopularity_dict, movies_info):
    """
    Adds IMDb popularity information to the movies_info dictionary.

    Args:
    imdbPopularity_dict (dict): Dictionary containing IMDb popularity scores.
    movies_info (dict): Dictionary containing information about movies.

    Returns:
    dict: The updated movies_info dictionary with tmdb_popularity added.
    """
    for imdb_id in imdbPopularity_dict:
        if imdb_id in movies_info:
            # Add 'tmdb_popularity' key with the value from imdbPopularity_dict
            movies_info[imdb_id]['tmdb_popularity'] = imdbPopularity_dict[imdb_id]

    return movies_info

id_popularity_dict = id_popularity_dict('movie_ids_12_12_2023.json')
movie_ids = list(id_popularity_dict.keys())
movie_ids = movie_ids[:500] #sample 500 movies

tmdb_api_key = '7091325f03a84189b351cfc2a22417e0'
IMDB_popularity_dict = {}
for i in movie_ids:
    IMDB_id = get_imdb_id_from_tmdb(i, tmdb_api_key)
    if IMDB_id not in ['Error', None, '']:  # Check if a valid IMDb ID was returned
        IMDB_popularity_dict[IMDB_id] = id_popularity_dict[i]

writeFile('IMDB_popularity_dict.json',IMDB_popularity_dict)

IMDB_ids = list(IMDB_popularity_dict.keys())
OMDB_key = 'abed733b'
movies_info = fetch_movies_info(OMDB_key, IMDB_ids)
writeFile('movies_info.json',movies_info)

movies = create_movie_objects(movies_info)
movies_info_updated = add_popularity_to_movies(IMDB_popularity_dict, movies_info)
writeFile('movies_info_updated.json',movies_info_updated)