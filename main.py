"""Etablir la connexion, exécuter des requêtes,
    visualiser les résultats,
    générer un rapport,
    puis fermer la connexion."""


from mongodb.mongodb_manager import MongoDBManager
from neo4j_custom.neo4j_manager import Neo4jManager
from mongodb.init_mongodb import init_mongodb
from mongodb.update_documents_fields import main_update_document_fields
from neo4j_custom.init_neo4j import init_neo4j
from utils.visualization import Visualizer
from utils.data_analysis import generate_report
from utils.check_database import main_check_database

class App:
    def __init__(self):
        # Initialisation des gestionnaires pour MongoDB et Neo4j.
        self.mongodb_manager = MongoDBManager()
        self.neo4j_manager = Neo4jManager()

    def run(self):
        # Vérification de l'existence des base de données
        mongodb_exists, neo4j_exists = main_check_database()

        if not mongodb_exists:
            # Initialisation de la base de données mongodb
            init_mongodb()

        if not neo4j_exists:
            # Initialisation de la base de données neo4j
            init_neo4j()
        
        # Mise à jour des types de données et nettoyage des champs pour les collections MongoDB
        main_update_document_fields()

        # Établissement des connexions aux bases de données MongoDB et Neo4j.
        self.mongodb_manager.connect()
        self.neo4j_manager.connect()

        # Exécution des requêtes spécifiques à chaque base de données et stockage des résultats.
        mongo_data = self.mongodb_manager.execute_queries()
        neo4j_data = self.neo4j_manager.execute_queries()

        # Création d'un objet visualiseur pour la représentation graphique des données.
        visualizer = Visualizer(mongo_data, neo4j_data)

        # Visualisation des données récupérées de MongoDB et Neo4j.
        visualizer.visualize_mongodb_data()
        visualizer.visualize_neo4j_data()

        # Génération d'un rapport d'analyse basé sur les données récupérées.
        generate_report(mongo_data, neo4j_data)

        # Fermeture des connexions aux bases de données.
        self.mongodb_manager.close()
        self.neo4j_manager.close()

if __name__ == "__main__":
    app = App()
    app.run()