from pymongo import MongoClient

class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        # Établir la connexion à MongoDB
        self.client = MongoClient("mongodb+srv://frangiessono1:eje3pqgSSkBfMesJ@clustereetff.hglyegz.mongodb.net/")
        self.db = self.client.nom_base_donnees

    def execute_queries(self):
        # Implémenter les requêtes MongoDB ici
        # Exemple : récupérer le nombre d'utilisateurs
        utilisateurs = self.db.utilisateurs.count_documents({})

        # Retourner les données résultantes
        return {"nombre_utilisateurs": utilisateurs}

    def close(self):
        # Fermer la connexion à MongoDB
        self.client.close()