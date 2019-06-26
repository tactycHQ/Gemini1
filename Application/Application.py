#Gets tags from contentbuilder
#Gets data from API and writes clean data to DB
#Runs predictions from data to generate pulse score
#Delivers all content and pulse scores
from APICalls.TMDBRequests import TMDBData


class Searcher






TMDBData = TMDBData()
popularMovies = TMDBData.getPopularMovies(pages=2)
topRatedMovies = TMDBData.getTopRatedMovies(pages=2)
upcomingMovies = TMDBData.getUpcomingMovies(pages=2)
nowPlayingMovies = TMDBData.getNowPlayingMovies(pages=2)

print(popularMovies)