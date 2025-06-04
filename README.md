# 🎬 Movie Recommender System (Django + ML)

A content-based movie recommendation system built using Django and machine learning. This app recommends similar movies based on attributes such as genres, keywords, cast, and crew, using the TMDB 5000 dataset.

---

## 🚀 Features

- 🔍 **Movie Search**: Users can search for a movie by its title.
- 🎯 **Smart Recommendations**: Returns 5 similar movies using content-based filtering.
- 🖼️ **Movie Posters**: Displays recommended movie posters using the TMDB API.
- 🧠 **ML Powered**: Uses NLP techniques and cosine similarity to find relevant results.
- 📦 **Model Caching**: Saves preprocessed data and similarity matrix with Pickle for performance.

---

## 🧰 Technologies Used

- **Backend**: Django
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **API**: TMDB (The Movie Database) API for fetching movie posters
- **Storage**: Pickle for saving ML model artifacts

---

## 📚 Dataset

This system uses the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata), including:

- `movies.csv`
- `credits.csv`

Merged and preprocessed to form a clean dataset with:

- `movie_id`
- `title`
- `overview`
- `genres`
- `keywords`
- `cast`
- `crew`

---

## 🧪 How It Works

### 1. **Data Preprocessing**

- Extracts and cleans data from columns like genres, keywords, cast, and crew.
- Merges relevant information into a `tags` column.
- Vectorizes `tags` using `CountVectorizer`.

### 2. **Recommendation Logic**

- Calculates cosine similarity on vectorized tags.
- When a movie is searched:
  - Finds the most similar movies using the similarity matrix.
  - Fetches and displays their titles and posters.

```python
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


###Django View Logic
-Handles GET & POST requests.

-On form submission, recommends movies using the saved model.

```python 
  def movie_recommender(request):
      with open('movie_list.pkl', 'rb') as f:
          movies = pickle.load(f)
      with open('similarity.pkl', 'rb') as f:
          similarity = pickle.load(f)
      
      movie_list = movies['title'].values
      if request.method == 'POST':
          selected_movie = request.POST.get('selected_movie')
          recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
          recommendations = zip(recommended_movie_names, recommended_movie_posters)
          context = {
              'movie_list': movie_list,
              'selected_movie': selected_movie,
              'recommendations': recommendations,
          }
          return render(request, 'recommendation.html', context)
  
      return render(request, 'recommendation.html', {'movie_list': movie_list})
