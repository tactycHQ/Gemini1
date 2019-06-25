from tmdbv3api import TMDb
from tmdbv3api import Movie
from dotmap import DotMap
import

class TMDBData():

    def __init__(self):
        self.tmdb = TMDb()
        self.tmdb.api_key = '2555845ba9ed9bbc618e7d09abbb5069'
        self.tmdb.language = 'en'
        self.tmdb.debug = True

    def getPopularMovies(self):
        movie = Movie()
        popular = movie.popular()
        popular = DotMap(json.lo)
        return popular

if __name__ == '__main__':
    TMDBData = TMDBData()
    TMDBData.getPopularMovies()