import os
from django.conf import settings
import pickle
import requests
from django.shortcuts import render

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    #trellor
    return recommended_movie_names, recommended_movie_posters

def movie_recommender(request):
    # Define the paths for the pickle files
    movie_list_path = os.path.join(settings.BASE_DIR, 'home', 'movie_list.pkl')
    similarity_path = os.path.join(settings.BASE_DIR, 'home', 'similarity.pkl')

    # Load the pickle files
    with open(movie_list_path, 'rb') as f:
        movies = pickle.load(f)
    
    with open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)

    # Extract movie titles from the loaded movie DataFrame
    movie_list = movies['title'].values

    if request.method == 'POST':
        selected_movie = request.POST.get('selected_movie')
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)

        recommendations = zip(recommended_movie_names, recommended_movie_posters)
        
        context = {
            'movie_list': movie_list,
            'selected_movie': selected_movie,
            'recommendations': recommendations,
        }
    else:
        # Initialize context for GET request
        context = {
            'movie_list': movie_list,
            'selected_movie': None,
            'recommendations': None,
        }
    return render(request, 'recommendation.html',context)


        
        