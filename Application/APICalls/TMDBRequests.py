import json
import requests
from dotmap import DotMap

class TMDBData():

    def __init__(self):
        self.api_key = '2555845ba9ed9bbc618e7d09abbb5069'
        self.language = 'en'
        self.debug = True

    def getPopularMovies(self):
        path = "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en-US&page=1".format(self.api_key)
        response = requests.get(path)
        print(response.json())
        popularMovies = response.json()
        for movies in popularMovies['results']:
            print(movies['title'])
        # print (popularMovies['results'])
        return popularMovies

    # def getMovieGenres(self):
    #     path = "https://api.themoviedb.org/3/genre/movie/list?api_key={}&language=en-US".format(self.api_key)
    #     response = requests.get(path)
    #     movieGenres = DotMap(response.json())
    #     return movieGenres

if __name__ == '__main__':
    TMDBData = TMDBData()
    popularMovies = TMDBData.getPopularMovies()
    TMDBData.getMovieGenres()