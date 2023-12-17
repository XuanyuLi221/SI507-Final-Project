# SI507-Final-Project
# Movie Recommendation System

## Introduction
The Movie Recommendation System is an interactive Python application designed to guide users through a vast array of movies organized in a hierarchical structure. This tool simplifies the movie selection process based on categories and enhances the user experience by providing detailed information, including summaries from Wikipedia for each selected movie.

## Data Structure

### Construction Method
The core of this system is its hierarchical data structure, implemented using a JSON file (`movies_tree.json`). This structure organizes movies in a multi-level tree format, allowing efficient storage and retrieval based on various movie attributes.

#### Hierarchical Levels:
- **Language Level**: The topmost level categorizing movies by the language they are in.
- **Country Level**: Under each language, movies are further categorized based on the country of their origin or popularity.
- **Genre Level**: Each country category branches into genres, grouping movies by their style or thematic content.
- **Awards Level**: Within each genre, movies are sorted based on their recognition status - whether they have received awards or not.
- **Movie Detail Level**: The leaf nodes of the structure, containing detailed attributes of each movie (title, year, director, etc.).

### JSON Example:
```json
{
    "English": {
        "United States": {
            "Comedy": {
                "No Awards": [
                    {
                        "Title": "Movie Title",
                        "Year": "Release Year",
                        ...
                    },
                    ...
                ],
                ...
            },
            ...
        },
        ...
    },
    ...
}
```

### Interaction 
#### User Interaction Method 
Interacting with the system is designed to be intuitive and user-friendly, following these steps:  

- Starting the Application: Run the Python script (recommend_movie.py) to initiate the program.  

- Category Navigation: Users are first prompted to select a movie category based on language, followed by country, genre, and awards status.  

- Movie Selection: After navigating through categories, a list of movies is presented. Users can select a movie to view more details.  

- Sorting and Filtering: Users have the option to sort movies based on attributes like IMDb rating or popularity.  

- Fetching Summaries: For a selected movie, the system can retrieve a brief summary from Wikipedia.  

- Exiting the System: At any point, users can choose to exit the system by following the on-screen prompt.

Select a movie category: English
Select a country: United States
Select a genre: Comedy
List all movies in this category? Yes
Sort movies by (imdbRating/popularity/Year): imdbRating
Sort order (ascending/descending): descending
...


This README, formatted in Markdown, provides a clear and structured overview of the Movie Recommendation System, its data structure, and the method of interaction, guiding users to effectively understand and use the system.
