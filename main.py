from mongodb.mongodb_manager import MongoDBManager
from neo4j_custom.neo4j_manager import Neo4jManager
from utils.visualization import visualize_mongodb_data, visualize_neo4j_data

class App:
    def __init__(self):
        self.mongodb_manager = MongoDBManager()
        self.neo4j_manager = Neo4jManager()

    def run(self):
        # Connecter à MongoDB
        self.mongodb_manager.connect()

        # Connecter à Neo4j
        self.neo4j_manager.connect()

        # Exécuter les requêtes MongoDB
        mongo_data = self.mongodb_manager.execute_queries()

        # Exécuter les requêtes Neo4j
        neo4j_data = self.neo4j_manager.execute_queries()

        # Visualiser les données MongoDB
        visualize_mongodb_data(mongo_data)

        # Visualiser les données Neo4j
        visualize_neo4j_data(neo4j_data)

        # Fermer les connexions
        self.mongodb_manager.close()
        self.neo4j_manager.close()

if __name__ == "__main__":
    app = App()
    app.run()