"""
############################## Final Projec: Build Trees ############################

% Student Name: Xuanyu Li

% Student Unique Name: xuanyuli

% Lab Section 00X:  103

% I worked with the following classmates: none

"""

import json

def get_categories_by_attribute(movies_info, attribute):
    """
    Get unique categories for a specified attribute in a dictionary of movie information.

    Parameters:
    - movies_info (dict): A dictionary where keys are movie IDs and values are dictionaries containing movie information.
    - attribute (str): The attribute for which to extract categories.

    Returns:
    list of str: A list of unique categories for the specified attribute, sorted in alphabetical order.
    """
    # Create a set to store categories, using a set ensures uniqueness
    categories = set()
    
    # Iterate through the movie information dictionary
    for movie_id, movie in movies_info.items():
        # Check if the attribute exists in the movie information
        if attribute in movie:
            # Split the attribute value by comma if it contains a comma
            values = movie[attribute].split(', ')
            # Add each value to the categories set
            categories.update(values)
    
    # Convert the set to a sorted list
    sorted_categories = sorted(list(categories))
    
    return sorted_categories

def organize_movies_info_into_tree(movies_info):
    '''
    Organize movies information into a tree structure based on attributes.
    
    Parameters:
        movies_info (dict): A dictionary of movies information.
        
    Returns:
        dict: A dictionary of movies organized by attributes.
    '''
    tree = {}
    for movie_id, movie_details in movies_info.items():
        # Extract movie attributes
        languages = movie_details.get('Language', 'Unknown Language').split(', ')
        countries = movie_details.get('Country', 'Unknown Country').split(', ')
        genres = movie_details.get('Genre', 'Unknown Genre').split(', ')
        awards_value = movie_details.get('Awards', 'Unknown Awards')
        
        # Determine the awards category
        awards_category = 'Awards' if awards_value != 'N/A' else 'No Awards'
        
        # Create a dictionary with movie details
        movie_info = {
            'Title': movie_details['Title'],
            'Year': movie_details['Year'],
            'Director': movie_details['Director'],
            'Actors': movie_details['Actors'],
            'Plot': movie_details['Plot'],
            'imdbRating': movie_details['imdbRating'],
            'popularity': movie_details['tmdb_popularity'],
            'imdbVotes': movie_details['imdbVotes'],
            'Poster': movie_details['Poster'],
        }
        
        # Create nested dictionaries based on attributes and awards category
        for language in languages:
            for country in countries:
                for genre in genres:
                    tree.setdefault(language, {}).setdefault(country, {}).setdefault(genre, {}).setdefault(awards_category, []).append(movie_info)
    
    return tree

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

fileName = 'movies_info_updated.json'
with open(fileName, 'r', encoding='utf-8') as file:
    movies_info_updated = json.load(file)
movies_tree = organize_movies_info_into_tree(movies_info_updated)
writeFile('movies_tree.json',movies_tree)
