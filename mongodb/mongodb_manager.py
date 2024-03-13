from pymongo import MongoClient

class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        # Établir la connexion à MongoDB
        self.client = MongoClient("mongodb+srv://frangiessono1:ohADwBLcW5IIgQnl@cluster442.cadx49i.mongodb.net/")
        self.db = self.client.dbnowsql

    def get_user_count(self):
        return self.db.tw_user.count_documents({})

    def get_tweet_count(self):
        return self.db.tweet.count_documents({})

    def get_hashtag_count(self):
        return self.db.tweet_hashtag.aggregate([{"$unwind": "$hashtag"}, {"$count": "total_hashtags"}])

    def get_tweets_with_hashtag(self, hashtag):
        return self.db.tweet_hashtag.count_documents({"hashtag": hashtag})

    def get_unique_users_for_hashtag(self, hashtag):
        return len(self.db.tweet_hashtag.distinct("idTweet", {"hashtag": hashtag}))

    def get_tweets_as_replies(self):
        # 6. Tweets qui sont des réponses à un autre tweet
        return list(self.db.tweet.find({"replyIdTweet": {"$exists": True, "$ne": ""}}))

    def get_top_10_popular_tweets(self):
        # 12. Les 10 tweets les plus populaires
        return list(self.db.tweet.find().sort("nbFavorites", -1).limit(10))

    def get_top_10_popular_hashtags(self):
        # 13. Les 10 hashtags les plus populaires
        return list(self.db.tweet_hashtag.aggregate([
            {"$unwind": "$hashtag"},
            {"$group": {"_id": "$hashtag", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]))

    def execute_queries(self):
        # Initialiser un dictionnaire pour stocker les résultats des requêtes
        query_results = {}

        # Exécuter chaque fonction de requête et stocker les résultats
        query_results['user_count'] = self.get_user_count()
        query_results['tweet_count'] = self.get_tweet_count()
        query_results['hashtag_count'] = next(self.get_hashtag_count(), {}).get('total_hashtags', 0)
        query_results['tweets_with_hashtag_actualite'] = self.get_tweets_with_hashtag('actualite')
        query_results['unique_users_for_hashtag_valls'] = self.get_unique_users_for_hashtag('valls')
        query_results['tweets_as_replies'] = self.get_tweets_as_replies()
        query_results['top_10_popular_tweets'] = self.get_top_10_popular_tweets()
        query_results['top_10_popular_hashtags'] = self.get_top_10_popular_hashtags()

        # Retourner les résultats de toutes les requêtes
        return query_results

    def close(self):
        self.client.close()
