Movie Recommender System
This project is a movie recommendation system built with Django. It trains on movie data, and when a user searches for a movie, it recommends similar movies based on several attributes such as genres, keywords, cast, and crew.

Features
Movie Search: Users can search for a movie by its name.
Recommendation System: Based on the search, the system recommends five movies that are similar to the queried movie.
Data: The system uses the TMDB 5000 movies and credits datasets.
Machine Learning: The system uses vectorization (CountVectorizer) and cosine similarity to find the most relevant recommendations.

Data Preprocessing
The dataset used includes the following columns:

movie_id
title
overview
genres
keywords
cast
crew
We clean and transform the data to make it suitable for training the model. This includes:

Extracting relevant fields like genres, keywords, cast, and crew into lists of names.
Collapsing these fields into a single tags column to represent a movie’s key characteristics.
Vectorizing the tags using CountVectorizer.
Recommendation Algorithm
The recommendation engine is based on cosine similarity, which computes the similarity between the tag vectors of two movies. When a user searches for a movie, the system:

Finds the index of the searched movie.
Calculates the similarity between the searched movie and all other movies.
Returns the top 5 most similar movies.
Example Code for Movie Recommendation
python
Copy code
def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)
Model Saving
The processed data and the similarity matrix are saved using Python's pickle module, making it easier to load the model for future use without reprocessing the data.

python
Copy code
import pickle
pickle.dump(new, open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
Requirements
Django
Pandas
Scikit-learn
Numpy
How to Use
Enter the movie title in the search bar on the app’s homepage.
The app will display the top 5 recommended movies similar to the one you searched for.
Future Enhancements
Add user ratings to refine recommendations.
Allow filtering recommendations based on user preferences (e.g., genre).
Improve the search functionality to handle variations in movie titles.






# view 



Imports:
os: Provides functions to interact with the file system.
settings: Django's settings module, used to get the base directory path.
pickle: Used to load pre-trained models (movie data and similarity matrix).
requests: Used for making HTTP requests to external APIs (in this case, TMDB API).
render: Django function that renders templates with a given context.


@@@@@
1. fetch_poster(movie_id):
This function takes a movie ID as input and fetches the corresponding movie poster from the TMDB API.

url: It constructs the URL by using the movie's ID and appending the TMDB API key.
data = requests.get(url): Sends a GET request to the TMDB API.
poster_path: Extracts the poster path from the JSON response.
full_path: Concatenates the base image URL with the poster path to generate the full URL for the movie poster.
return full_path: Returns the full URL of the movie poster.
2. recommend(movie, movies, similarity):
This function generates movie recommendations based on the selected movie using a pre-trained similarity matrix.


@@
index = movies[movies['title'] == movie].index[0]:
 Finds the index of the movie that matches the input movie title.



distances: Calculates cosine similarity between the input movie and all other movies. It sorts the movies in descending order of similarity.
recommended_movie_names: Initializes an empty list to store the names of recommended movies.
recommended_movie_posters: Initializes an empty list to store the URLs of the recommended movie posters.
for i in distances[1:6]: Iterates over the top 5 similar movies (skipping the first one, which is the movie itself).
movie_id = movies.iloc[i[0]].movie_id: Retrieves the movie_id for each recommended movie.
recommended_movie_posters.append(fetch_poster(movie_id)): Fetches the movie poster for each recommended movie and appends it to the list.
recommended_movie_names.append(movies.iloc[i[0]].title): Appends the recommended movie title to the list.
return recommended_movie_names, recommended_movie_posters: Returns the recommended movie titles and poster URLs.


@@@@@@@@@@

3. movie_recommender(request) (View Function):
This is the main view function responsible for handling the user request and rendering the movie recommendations.



movie_list_path and similarity_path:      Define paths to the pre-trained movie data (movie_list.pkl) and similarity matrix (similarity.pkl) using os.path.join to ensure correct paths.
with open(movie_list_path, 'rb') as f:   Loads the movie data (which contains titles, IDs, and other metadata) using pickle.
with open(similarity_path, 'rb') as f:    Loads the similarity matrix using pickle.
movie_list = movies['title'].values:   Extracts all movie titles from the movie DataFrame to display in the frontend (for selection by the user).
if request.method == 'POST':       If the request is a POST (submitted form):
selected_movie = request.POST.get('selected_movie'):    Retrieves the movie title selected by the user from the POST request.
recommend():   Cal ls the recommend() function to get the recommended movie names and posters based on the selected movie.
recommendations =    zip(recommended_movie_names, recommended_movie_posters): Zips together the movie names and posters to pass them to the template.
context:    Creates a context dictionary to send data to the template.
'movie_list':    Contains the list of all movie titles.
'selected_movie':    Contains the movie title selected by the user.
'recommendations'  : Contains the recommended movie names and their posters.
return render(request,    'recommendation.html', context): Renders the recommendation.html template with the provided context, displaying the movie recommendations and posters.



Explanation of Workflow:
User selects a movie: The user selects a movie from a list (sent to the frontend from movie_list).
Form submission: When the form is submitted, the view captures the selected movie via a POST request.
Recommendations: The view then calls the recommend() function, which:
Fetches the top 5 most similar movies.
Fetches the posters for those movies from the TMDB API.
Rendering: Finally, the recommended movie titles and posters are passed to the recommendation.html template and displayed.# moviesecommendersystem
