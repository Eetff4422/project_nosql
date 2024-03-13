from neo4j import GraphDatabase

class Neo4jManager:
    def __init__(self):
        self.driver = None

    def connect(self):
        # Établir la connexion à Neo4j
        uri = "neo4j+s://<username>:<password>@<neo4j-url>"
        self.driver = GraphDatabase.driver(uri)

    def execute_queries(self):
        # Implémenter les requêtes Neo4j ici
        # Exemple : récupérer le nombre de relations "SUIT"
        with self.driver.session() as session:
            result = session.run("MATCH ()-[r:SUIT]->() RETURN count(r)")
            nombre_relations = result.single().value()

        # Retourner les données résultantes
        return {"nombre_relations": nombre_relations}

    def close(self):
        # Fermer la connexion à Neo4j
        self.driver.close()