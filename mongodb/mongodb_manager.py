from pymongo import MongoClient

class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        # Établir la connexion à MongoDB
        self.client = MongoClient("mongodb+srv://frangiessono1:ohADwBLcW5IIgQnl@cluster442.cadx49i.mongodb.net/")
        self.db = self.client.nom_base_donnees

    def get_user_count(self):
        return self.db.users.count_documents({})

    def get_tweet_count(self):
        return self.db.tweets.count_documents({})

    def get_hashtag_count(self):
        return self.db.tweets.aggregate([{"$unwind": "$hashtags"}, {"$count": "total_hashtags"}])

    def get_tweets_with_hashtag(self, hashtag):
        return self.db.tweets.count_documents({"hashtags": hashtag})

    def get_unique_users_for_hashtag(self, hashtag):
        return len(self.db.tweets.distinct("user_id", {"hashtags": hashtag}))

    def get_tweets_as_replies(self):
        # 6. Tweets qui sont des réponses à un autre tweet
        return list(self.db.tweets.find({"replyIdTweet": {"$exists": True, "$ne": ""}}))

    def get_top_10_popular_tweets(self):
        # 12. Les 10 tweets les plus populaires
        return list(self.db.tweets.find().sort("nbFavorites", -1).limit(10))

    def get_top_10_popular_hashtags(self):
        # 13. Les 10 hashtags les plus populaires
        return list(self.db.tweets.aggregate([
            {"$unwind": "$hashtags"},
            {"$group": {"_id": "$hashtags", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]))

    def close(self):
        self.client.close()
