import json
import requests
from dotmap import DotMap
from APICalls.config import get_config_from_json
import pandas as pd

class TMDBRequests():

    def __init__(self):
        self.keys = get_config_from_json('..//Keys//keys.json')
        self.api_key = self.keys.tmdb_key.api_key
        self.language = 'en'
        self.debug = True

    def getPopularMovies(self, pages):
        popularMovies=pd.DataFrame()

        for page in range (1,pages+1):
            path = "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US&page={}".format(self.api_key, page)
            response = requests.get(path)
            popularMovies_dict = response.json()
            popularMovies = popularMovies.append(popularMovies_dict['results'],ignore_index=True)
        popularMovies['tmdbCategory'] = 'popular'
        return popularMovies

    def getNowPlayingMovies(self, pages):
        nowPlayingMovies=pd.DataFrame()

        for page in range (1,pages+1):
            path = "https://api.themoviedb.org/3/movie/now_playing?api_key={}&language=en-US&page={}".format(self.api_key, page)
            response = requests.get(path)
            nowPlayingMovies_dict = response.json()
            nowPlayingMovies = nowPlayingMovies.append(nowPlayingMovies_dict['results'],ignore_index=True)
        nowPlayingMovies['tmdbCategory'] = 'nowPlaying'
        return nowPlayingMovies

    def getTopRatedMovies(self, pages):
        topRatedMovies = pd.DataFrame()

        for page in range(1, pages + 1):
            path = "https://api.themoviedb.org/3/movie/top_rated?api_key={}&language=en-US&page={}".format(self.api_key,
                                                                                                        page)
            response = requests.get(path)
            topRatedMovies_dict = response.json()
            topRatedMovies = topRatedMovies.append(topRatedMovies_dict['results'], ignore_index=True)
        topRatedMovies['tmdbCategory'] = 'topRated'
        return topRatedMovies

    def getUpcomingMovies(self, pages):
        upcomingMovies = pd.DataFrame()

        for page in range(1, pages + 1):
            path = "https://api.themoviedb.org/3/movie/upcoming?api_key={}&language=en-US&page={}".format(self.api_key,
                                                                                                        page)
            response = requests.get(path)
            upcomingMovies_dict = response.json()
            upcomingMovies = upcomingMovies.append(upcomingMovies_dict['results'], ignore_index=True)
        upcomingMovies['tmdbCategory'] = 'upcoming'
        return upcomingMovies

    def getMovieGenres(self):
        path = "https://api.themoviedb.org/3/genre/movie/list?api_key={}&language=en-US".format(self.api_key)

        response = requests.get(path)
        movieGenres_dict = response.json()
        movieGenres = pd.DataFrame(movieGenres_dict['genres'])
        return movieGenres

# if __name__ == '__main__':
#     TMDBData = TMDBData()
#     popularMovies = TMDBData.getPopularMovies(pages=2)
#     topRatedMovies = TMDBData.getTopRatedMovies(pages=2)
#     upcomingMovies = TMDBData.getUpcomingMovies(pages=2)
#     nowPlayingMovies = TMDBData.getNowPlayingMovies(pages=2)
#     # TMDBData.getMovieGenres()