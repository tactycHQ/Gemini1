#Gets tags from contentbuilder
#Gets data from API and writes clean data to DB
#Runs predictions from data to generate pulse score
#Delivers all content and pulse scores
from APICalls.TMDBRequests import TMDBRequests
from APICalls.GetTwitter import GetTwitter
import pandas as pd
import numpy as np
from itertools import islice
from dotmap import DotMap
import logging
logging.basicConfig(level=logging.INFO)

class Application():

    def __init__(self):
        pass

    def getTMDBContent(self):
        TMDBData = TMDBRequests()
        self.popularMovies = TMDBData.getPopularMovies(pages=2)
        self.topRatedMovies = TMDBData.getTopRatedMovies(pages=2)
        self.upcomingMovies = TMDBData.getUpcomingMovies(pages=2)
        self.nowPlayingMovies = TMDBData.getNowPlayingMovies(pages=2)
        logging.info("API data recieved from TMDB")

    def writeTMDBtoDB(self):
        allTitles = pd.DataFrame()
        self.allTitles = allTitles.append([self.popularMovies, self.topRatedMovies, self.upcomingMovies, self.nowPlayingMovies], ignore_index=True)
        self.allTitles['content_type'] = "movie"
        self.allTitles.to_csv("..//Database//all_tmdb_movies.csv")
        logging.info("API data saved to file")
        logging.info("{} movies extracted from TMDB".format(self.allTitles.shape[0]))

    def getTMDBfromDB(self):
        self.allTitles = pd.read_csv("..//Database/all_tmdb_movies.csv")

    def getUniqueTitles(self):
        allTitleNames = self.allTitles['title']
        unique_titles = np.unique(allTitleNames)
        return unique_titles

    def cleanTitle(self, title):
        # cleanTitle = title.replace(" ", "").lower()
        cleanTitle = title.replace(",", "")
        cleanTitle = cleanTitle.replace(".", "")
        cleanTitle = cleanTitle.replace("-", "")
        cleanTitle = cleanTitle.replace("'", "")
        cleanTitle = cleanTitle.replace(":","")
        return cleanTitle

    def removeSpaces(self, title):
        spacesRemoved = title.replace(" ", "").lower()
        spacesRemoved = spacesRemoved.replace(",", "")
        spacesRemoved = spacesRemoved.replace(".", "")
        spacesRemoved = spacesRemoved.replace("-", "")
        spacesRemoved = spacesRemoved.replace("'", "")
        spacesRemoved = spacesRemoved.replace(":","")
        return spacesRemoved

    def quotesTitle(self, title):
        return '"{}"'.format(title)

    def queryCombinations(self, title):
        filter_String = "-filter:retweets -filter:links -filter:replies"
        #note can also add -filter:media if needed but that seems to remove most tweets
        content_string = "AND (release OR film OR movie OR watched)"
        combination = '({} OR {} OR {} OR {} {} {})'.format(title, self.cleanTitle(title),self.removeSpaces(title),self.quotesTitle(title),content_string, filter_String)

        return combination

    def createTwitterQueries(self,titles):
        query_dict = dict()
        logging.info("Creating queries")

        for title in titles:
            query_dict.update({title:self.queryCombinations(title)})
        query_df = pd.DataFrame(list(query_dict.values()), index = query_dict.keys()).reset_index()
        query_df.columns = ['title','queryString']
        query_df.to_csv("..//Database//queries_sent.csv")
        logging.info("Queries created")
        return query_df

    def getTweets(self,query_df, batch_size):
        getTwitter = GetTwitter()
        max_tweets = 100
        date_since = "2019-06-01"
        logging.info("Getting Tweets from Twitter API")

        rawTweets = []
        cleanTweets = []
        titleTracker = []
        counter=0

        for index, row in query_df.iterrows():
            if counter < batch_size:
                try:
                    tweets_text, tweet_location, tweet_time = getTwitter.getTweetsbyQuery(row['queryString'], max_tweets, date_since)
                    clean_tweets = getTwitter.clean_tweets(tweets_text)
                    rawTweets.append(tweets_text)
                    cleanTweets.append(clean_tweets)
                    titleTracker.append(row['title'])
                    counter+=1
                    print(DotMap(getTwitter.api.rate_limit_status()).resources.search)
                except Exception as ex:
                    print(ex)

        logging.info("Recieved tweets for {} titles".format(counter))

        queryResults = pd.DataFrame({'title':titleTracker,
                                     'rawTweets':rawTweets,
                                     'cleanTweets':cleanTweets}).astype('object')
        queryResults.to_pickle("..//Database//query_results.pkl")
        queryResults.to_csv("..//Database//query_results.csv")
        logging.info("Tweets saved to file")

        return queryResults

if __name__ == '__main__':
    app = Application()
    app.getTMDBContent()
    app.writeTMDBtoDB()
    app.getTMDBfromDB()
    uniques = app.getUniqueTitles()
    query_df = app.createTwitterQueries(uniques)
    results = app.getTweets(query_df, batch_size=300)













