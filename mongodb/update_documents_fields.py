from pymongo import MongoClient

def update_document_fields(db):
    # tweet_hashtag collection: Convertir en int et supprimer les chaînes vides
    db.tweet_hashtag.update_many(
        {},
        [
            {"$set": {
                #"idTweet": {"$convert": {"input": "$idTweet", "to": "int", "onError": 0}},
                "indiceStart": {"$convert": {"input": "$indiceStart", "to": "int", "onError": 0}},
                "indiceEnd": {"$convert": {"input": "$indiceEnd", "to": "int", "onError": 0}},
            }}
        ]
    )

    # tweet collection: Convertir en int et gérer les chaînes vides
    db.tweet.update_many(
        {},
        [
            {"$set": {
                "idTweet": {"$convert": {"input": "$idTweet", "to": "double", "onError": 0}},
                "idUser": {"$convert": {"input": "$idUser", "to": "int", "onError": 0}},
                "replyIdTweet": {"$convert": {"input": "$replyIdTweet", "to": "double", "onError": 0}},
                "replyIdUser": {"$convert": {"input": "$replyIdUser", "to": "double", "onError": 0}},
                "nbRetweet": {"$convert": {"input": "$nbRetweet", "to": "int", "onError": 0}},
                "nbFavorites": {"$convert": {"input": "$nbFavorites", "to": "int", "onError": 0}},
            }}
        ]
    )

    # tw_user collection: Convertir en int et supprimer les chaînes vides
    db.tw_user.update_many(
        {},
        [
            {"$set": {
                "idUser": {"$convert": {"input": "$idUser", "to": "int", "onError": 0}},
                "nbStatuses": {"$convert": {"input": "$nbStatuses", "to": "int", "onError": 0}},
                "nbFavorites": {"$convert": {"input": "$nbFavorites", "to": "int", "onError": 0}},
                "nbFollowers": {"$convert": {"input": "$nbFollowers", "to": "int", "onError": 0}},
                "nbFollowing": {"$convert": {"input": "$nbFollowing", "to": "int", "onError": 0}},
            }}
        ]
    )

def main_update_document_fields():
    client = MongoClient("mongodb+srv://frangiessono1:ohADwBLcW5IIgQnl@cluster442.cadx49i.mongodb.net/")
    db = client.dbnowsql
    update_document_fields(db)
