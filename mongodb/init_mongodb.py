import requests
import csv
from pymongo import MongoClient

def init_mongodb():
    # Connexion à MongoDB
    client = MongoClient("mongodb+srv://frangiessono1:ohADwBLcW5IIgQnl@cluster442.cadx49i.mongodb.net/")
    db = client.dbnowsql  # Nom de votre base de données

    # URLs des fichiers CSV sur GitHub
    files_urls = [
        "https://raw.githubusercontent.com/Eetff4422/project_nosql/main/mongodb/docs/tw_user.csv",
        "https://raw.githubusercontent.com/Eetff4422/project_nosql/main/mongodb/docs/tweet.csv",
        "https://raw.githubusercontent.com/Eetff4422/project_nosql/main/mongodb/docs/tweet_hashtag.csv"
    ]

    # Noms des collections à créer pour chaque fichier CSV
    collections_names = ["tw_user", "tweet", "tweet_hashtag"]

    def download_and_import_csv(url, collection_name):
        response = requests.get(url)
        decoded_content = response.content.decode('utf-8')
        if collection_name == 'tw_user':
            cr = csv.reader(decoded_content.splitlines(), delimiter='\t')
        else:
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        header = next(cr)
        data = [dict(zip(header, row)) for row in cr]

        collection = db[collection_name]
        collection.insert_many(data)
        print(f"Imported {len(data)} records into {collection_name}.")

    for url, name in zip(files_urls, collections_names):
        download_and_import_csv(url, name)
