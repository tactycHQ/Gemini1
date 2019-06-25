from Gemini1.APICalls import GetTwitter

class ContentSearch():

    def __init__(self):
        pass

    def getJustWatched(self):
        keywords = ["just watched","just watching"]
        separator = ' OR '
        query = separator.join(keywords)
        print(query)



if __name__ == '__main__':
    C = ContentSearch()
    C.getJustWatched()
    tweets = GetTwitter()
