from pymongo import MongoClient
from neo4j import GraphDatabase

def check_if_mongodb_database_exists(db_uri, db_name):
    # Connexion au cluster MongoDB
    client = MongoClient(db_uri)

    # Vérifier si la base de données spécifiée existe
    if db_name in client.list_database_names():
        return True
    else:
        return False

class Neo4jDatabaseChecker:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        # Fermer la connexion au driver
        self.driver.close()
    
    def check_database_exists(self, db_name):
        with self.driver.session() as session:
            result = session.run("SHOW DATABASES")
            databases = [record["name"] for record in result]
            return db_name in databases

def main_check_database():
    # Paramètres MongoDB
    mongodb_uri = "mongodb+srv://frangiessono1:ohADwBLcW5IIgQnl@cluster442.cadx49i.mongodb.net/"
    mongodb_db_name = "dbnowsql"
    mongodb_exists = check_if_mongodb_database_exists(mongodb_uri, mongodb_db_name)
    print(f"La base de données MongoDB '{mongodb_db_name}' existe : {mongodb_exists}")
    
    # Paramètres Neo4j
    neo4j_uri = "neo4j+s://dc15bb96.databases.neo4j.io"
    neo4j_user = "neo4j"
    neo4j_password = "xZLEUi-SSuZkCSafSdxd7qtJJGHRDTmVRZNBzDAYc58"
    neo4j_db_name = "neo4j" # Remplacer par le nom réel de votre base de données Neo4j Aura
    
    checker = Neo4jDatabaseChecker(neo4j_uri, neo4j_user, neo4j_password)
    neo4j_exists = checker.check_database_exists(neo4j_db_name)
    
    print(f"La base de données Neo4j '{neo4j_db_name}' existe : {neo4j_exists}")
    
    checker.close()
    return mongodb_exists, neo4j_exists

