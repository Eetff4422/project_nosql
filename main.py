"""Etablir la connexion, exécuter des requêtes,
    visualiser les résultats,
    générer un rapport,
    puis fermer la connexion."""


from mongodb.mongodb_manager import MongoDBManager
from neo4j_custom.neo4j_manager import Neo4jManager
from utils.visualization import Visualizer
from utils.data_analysis import generate_report

class App:
    def __init__(self):
        # Initialisation des gestionnaires pour MongoDB et Neo4j.
        self.mongodb_manager = MongoDBManager()
        self.neo4j_manager = Neo4jManager()

    def run(self):
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