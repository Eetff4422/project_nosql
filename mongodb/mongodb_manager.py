# mongodb_manager.py
"""Ce fichier contient la classe MongoDBManager,
qui gère la connexion à une base de données MongoDB et
fournit des méthodes pour exécuter diverses requêtes sur les collections de données.
Les méthodes couvrent un large éventail de fonctionnalités,
de la récupération des nombres de base (utilisateurs, tweets, hashtags)
à des requêtes plus complexes pour analyser les données de tweet."""

from pymongo import MongoClient

class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        # Établissement de la connexion à la base de données MongoDB.
        self.client = MongoClient("mongodb+srv://frangiessono1:ohADwBLcW5IIgQnl@cluster442.cadx49i.mongodb.net/")
        self.db = self.client.dbnowsql

    # Diverses méthodes pour interroger la base de données MongoDB.
    # Chaque méthode récupère des données spécifiques ou effectue un calcul basé sur la collection cible.

    def get_user_count(self):
        # Retourne le nombre total d'utilisateurs.
        return self.db.tw_user.count_documents({})

    def get_tweet_count(self):
        # Retourne le nombre total de tweets.
        return self.db.tweet.count_documents({})

    def get_hashtag_count(self):
        # Calcule le nombre total de hashtags uniques.
        return self.db.tweet_hashtag.aggregate([{"$unwind": "$hashtag"}, {"$count": "total_hashtags"}])

    # Les méthodes suivantes implémentent des requêtes plus complexes, telles que la récupération des tweets initiants une discussion, le calcul des hashtags les plus populaires, etc.
    
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

    def get_tweets_initiating_discussion(self):
        # Cette fonction retourne les tweets qui initient une discussion
        # On recherche tous les tweets qui ne sont pas des réponses mais qui ont des réponses
        initiating_tweets = list(self.db.tweet.find({"replyIdTweet": {"$exists": False}}))
        
        # Créer une liste pour stocker les informations des tweets initiateurs
        initiating_tweets_info = []
        for tweet in initiating_tweets:
            # Vérifier si le tweet a des réponses
            if self.db.tweet.count_documents({"replyIdTweet": tweet["idTweet"]}) > 0:
                # Ajouter les informations du tweet à la liste s'il initie une discussion
                initiating_tweets_info.append({
                    "tweetId": tweet["idTweet"],
                    "tweetText": tweet.get("text", "")
                })
        
        return initiating_tweets_info

    def get_user_info_by_id(self, user_id):
        # Cherchez l'utilisateur par son ID et retournez les informations nécessaires
        user = self.db.tw_user.find_one({"idUser": user_id}, {"_id": 0, "name": 1, "nbFollowers": 1, "description": 1})
        return user

    def get_users_with_over_10_followers(self):
        # Récupérer les utilisateurs ayant plus de 10 followers
        users = list(self.db.tw_user.find({"nbFollowers": {"$gt": 10}}))
        return users

    def get_users_following_more_than_5(self):
        # Récupérer les utilisateurs qui suivent plus de 5 utilisateurs
        users = list(self.db.tw_user.find({"nbFollowing": {"$gt": 5}}))
        return users

    def get_user_name_by_id(self, user_id):
        user = self.db.tw_user.find_one({"idUser": user_id})
        return user['name'] if user else None

    def get_tweet_text_by_id(self, tweet_id):
        tweet = self.db.tweet.find_one({"idTweet": tweet_id})
        return tweet['text'] if tweet else None
    
    def get_user_id_by_name(self, user_name):
        user = self.db.tw_user.find_one({"name": user_name})
        return user['idUser'] if user else None

    def get_longest_discussion(self):
        # Question 15
        # Cette fonction retourne la plus longue discussion en termes de nombre de réponses en chaîne.
        pipeline = [
            {"$match": {"replyIdTweet": {"$exists": True}}},  # Trouver tous les tweets qui sont des réponses
            {"$group": {
                "_id": "$replyIdTweet",  # Grouper par le tweet auquel ils répondent
                "count": {"$sum": 1}  # Compter le nombre de réponses
            }},
            {"$sort": {"count": -1}},  # Trier pour trouver le plus grand nombre de réponses
            {"$limit": 1},  # Prendre le sommet (le tweet avec le plus de réponses)
            {"$lookup": {  # Rejoindre avec la collection originale pour trouver le tweet initial
                "from": "tweet",
                "localField": "_id",
                "foreignField": "idTweet",
                "as": "initiatingTweet"
            }},
            {"$unwind": "$initiatingTweet"}  # Déballer le résultat du lookup
        ]
        result = list(self.db.tweet.aggregate(pipeline))
        if result:
            # Extraire le tweet initial et le nombre de réponses
            longest_discussion = result[0]
            return {
                "initiatingTweetId": longest_discussion["_id"],
                "initiatingTweetText": longest_discussion["initiatingTweet"].get("text", ""),
                "responseCount": longest_discussion["count"]
            }
        return None



    def get_discussions_start_end(self):
        # Question 16
        # Cette fonction trouve le début et la fin de chaque discussion basée sur les réponses directes
        pipeline = [
            {"$match": {"replyIdTweet": {"$exists": False}}},  # Sélectionner les tweets qui initient des discussions
            {"$lookup": {  # Rechercher toutes les réponses directes à ces tweets
                "from": "tweet",
                "localField": "idTweet",
                "foreignField": "replyIdTweet",
                "as": "replies"
            }},
            {"$project": {  # Projeter les informations nécessaires
                "startTweetId": "$idTweet",
                "startTweetText": "$text",
                "endTweetId": {"$arrayElemAt": ["$replies.idTweet", -1]},  # Assumer que le dernier dans la liste est la fin
                "numReplies": {"$size": "$replies"}  # Nombre de réponses directes
            }},
            {"$match": {"numReplies": {"$gt": 0}}}  # Filtrer pour ne garder que les discussions avec au moins une réponse
        ]
        discussions = list(self.db.tweet.aggregate(pipeline))

        # Pour chaque discussion, trouvez le texte du dernier tweet
        for discussion in discussions:
            if discussion["endTweetId"]:  # S'il y a une fin de discussion identifiée
                end_tweet = self.db.tweet.find_one({"idTweet": discussion["endTweetId"]})
                discussion["endTweetText"] = end_tweet.get("text", "") if end_tweet else ""

        return discussions

    def execute_queries(self):
        # Exécute toutes les requêtes définies et stocke leurs résultats dans un dictionnaire pour une récupération facile.
        query_results = {}

        # Appel de chaque fonction définie pour récupérer les données spécifiques et stockage des résultats.
        query_results['user_count'] = self.get_user_count()
        query_results['tweet_count'] = self.get_tweet_count()
        query_results['hashtag_count'] = next(self.get_hashtag_count(), {}).get('total_hashtags', 0)
        query_results['tweets_with_hashtag_actualite'] = self.get_tweets_with_hashtag('actualite')
        query_results['unique_users_for_hashtag_valls'] = self.get_unique_users_for_hashtag('valls')
        query_results['tweets_as_replies'] = self.get_tweets_as_replies()
        query_results['top_10_popular_tweets'] = self.get_top_10_popular_tweets()
        query_results['top_10_popular_hashtags'] = self.get_top_10_popular_hashtags()
        query_results['get_tweets_initiating_discussion'] = self.get_tweets_initiating_discussion()
        query_results['get_longest_discussion'] = self.get_longest_discussion()
        query_results['get_discussions_start_end'] = self.get_discussions_start_end()
        query_results['users_with_over_10_followers'] = self.get_users_with_over_10_followers()
        query_results['users_following_more_than_5'] = self.get_users_following_more_than_5()

        # Retourner les résultats de toutes les requêtes
        return query_results

    def close(self):
        # Ferme la connexion au client MongoDB.
        self.client.close()
