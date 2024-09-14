from django.urls import path
from .views import *
urlpatterns =[
    path('', movie_recommender, name='movie_recommender'),  # The home page will show the recommender system
]