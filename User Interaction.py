"""
############################## Final Projec: User Interaction ############################

% Student Name: Xuanyu Li

% Student Unique Name: xuanyuli

% Lab Section 00X:  103

% I worked with the following classmates: none

"""

import json
import requests

def get_wikipedia_summary(movie_title):
    """
    Fetches the Wikipedia summary for a given movie title.

    This function queries the Wikipedia API to retrieve the introductory
    extract of a Wikipedia page corresponding to the provided movie title.
    If the data is successfully fetched and a summary is available, it is returned.
    Otherwise, appropriate error messages are printed, and an empty string is returned.

    Parameters
    ----------
    movie_title : str
        The title of the movie for which the Wikipedia summary is to be fetched.

    Returns
    -------
    str
        The introductory extract of the Wikipedia page of the movie, if available.
        Returns an empty string if no extract is found or if there's an error in data fetching.

    Notes
    -----
    The function makes an HTTP GET request to the Wikipedia API. Ensure that the
    network connection is active while using this function. If the movie title does
    not correspond to a Wikipedia page, or if there is an issue with the API request,
    the function will print an error message and return an empty string.
    """
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": movie_title,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    # Check if the 'pages' field is in the response and if it contains data
    if "query" in data and "pages" in data["query"]:
        page = next(iter(data["query"]["pages"].values()))
        # Check if a page with a valid extract was found
        if "extract" in page:
            return page["extract"]
        else:
            print(f"No summary available for '{movie_title}'.")
    else:
        print(f"Failed to fetch data for '{movie_title}'.")

    return ""


def recommend_movie(movie_tree):
    """
    Interactively recommend movies based on a hierarchical movie tree structure.

    This function allows a user to navigate through a tree of movie categories,
    offering options to list, sort, and select movies for more information. The user
    can choose to exit the recommendation system at any point.

    Parameters
    ----------
    movie_tree : dict or list
        The hierarchical structure of movie categories. Each node in the tree
        is either a dictionary representing a category with subcategories or
        a list of movies.

    Returns
    -------
    None
    """
    def collect_movies(node):
        """
        Recursively collects movies from a subtree of the movie tree.

        Parameters
        ----------
        node : dict or list
            A subtree of the movie tree, either a dictionary of subcategories
            or a list of movies.

        Returns
        -------
        list
            A list of movies collected from the subtree.
        """
        if isinstance(node, list):
            return [movie for movie in node]
        else:
            movies = []
            for key in node:
                movies.extend(collect_movies(node[key]))
            return movies

    def sort_movies(movies, sort_key, ascending):
        """
        Sorts a list of movies based on a specified key and order.

        Parameters
        ----------
        movies : list
            The list of movies to be sorted.
        sort_key : str
            The key to sort the movies by (e.g., 'year', 'imdbrating').
        ascending : bool
            The order of sorting (True for ascending, False for descending).

        Returns
        -------
        list
            The sorted list of movies.
        """
        for movie in movies:
            if sort_key == 'year':
                movie[sort_key] = int(movie[sort_key])
            elif sort_key == 'imdbrating':
                movie[sort_key] = float(movie[sort_key])

        return sorted(movies, key=lambda x: x[sort_key], reverse=not ascending)

    def validate_input(prompt, valid_options):
        """
        Validates user input against a set of valid options.

        Parameters
        ----------
        prompt : str
            The input prompt to be displayed to the user.
        valid_options : list
            A list of valid input options.

        Returns
        -------
        str
            The user input that matches one of the valid options.
        """
        while True:
            user_input = input(prompt)#.lower()
            if user_input in valid_options:
                return user_input
            print("Invalid input. Please try again.")
    
    def deduplicate_movies(movies):
        """
        Removes duplicate movies from the list based on title and year.

        Parameters
        ----------
        movies : list
            The list of movies from which duplicates need to be removed.

        Returns
        -------
        list
            The list of unique movies.
        """
        unique_movies = []
        seen = set()
        for movie in movies:
            identifier = (movie['Title'], movie['Year'])
            if identifier not in seen:
                seen.add(identifier)
                unique_movies.append(movie)
        return unique_movies
    
    current_node = movie_tree

    while isinstance(current_node, dict):
        print_option = validate_input("\nDo you want to list all movies in this category? (yes/no): ", ['yes', 'no'])
        if print_option == 'yes':
            all_movies = collect_movies(current_node)
            all_movies = deduplicate_movies(all_movies)

            sort_key = validate_input("Sort movies by (imdbRating/popularity/Year): ", ['imdbRating', 'popularity', 'Year'])
            order = validate_input("Sort order (ascending/descending): ", ['ascending', 'descending'])
            ascending = order == 'ascending'

            sorted_movies = sort_movies(all_movies, sort_key, ascending)

            for movie in sorted_movies:
                print(f"Title: {movie['Title']}, Year: {movie['Year']}, Director: {movie['Director']}, Actors: {movie['Actors']}, IMDb Rating: {movie['imdbRating']}, Popularity: {movie['popularity']}")

            ifInterested = input("Are you interested in some movies that you want to explore more? Answer yes/no: ")
            if ifInterested.lower() == 'yes':
                movie_selected = input("Please enter the name of the movie: ")
                print("Please wait...")
                summary = get_wikipedia_summary(movie_selected)
                print(summary)
    
                decision = input("Have you decided the movie to watch? Answer yes/no: ")
                if decision.lower() == 'yes':
                    print("Great! You can look up the movie for more details.")
                    return
                else:
                    continue_option = input("Please select: \n 1. Continue the recommendation system \n 2. Exit \n ")
                    if continue_option == '2':
                        print("Exiting the recommendation system.")
                        print("Bye!")
                        return

        # Print the options at the current level
        options = list(current_node.keys())
        print("\nSelect an option:")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")

        # Get and process user input
        choice = input("Enter your choice (or type 'exit' to quit): ")
        if choice.lower() == 'exit':
            print("Exiting the recommendation system.")
            return

        try:
            choice_index = int(choice) - 1
            if choice_index in range(len(options)):
                current_node = current_node[options[choice_index]]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    # Display movie details at the leaf node
    if isinstance(current_node, list):
        print("\nAvailable movies:")
        for movie in current_node:
            print(f"Title: {movie['Title']}, Year: {movie['Year']}, Director: {movie['Director']}, Actors: {movie['Actors']}")
            ifInterested = input("Are you interested in some movies that you want to explore more? Answer yes/no: ")
            if ifInterested.lower() == 'yes':
                movie_selected = input("Please enter the name of the movie: ")
                print("Please wait...")
                summary = get_wikipedia_summary(movie_selected)
                print(summary)
    
                decision = input("Have you decided the movie to watch? Answer yes/no: ")
                if decision.lower() == 'yes':
                    print("Great! You can look up the movie for more details.")
                    return
                else:
                    print("Sorry for our failure to help you find an interesting movie.")
                    print("Bye!")
                    return

fileName = 'movies_tree.json'
with open(fileName, 'r', encoding='utf-8') as file:
    movies_tree = json.load(file)
    
print("Welcom to this movie recommendation system!")
recommend_movie(movies_tree)