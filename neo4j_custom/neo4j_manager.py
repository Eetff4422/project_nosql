# neo4j_manager.py

from neo4j import GraphDatabase
from mongodb.mongodb_manager import MongoDBManager

class Neo4jManager:
    def __init__(self):
        self.driver = None
        self.mongodb_manager = MongoDBManager()

    def connect(self):
        uri = "neo4j+s://dc15bb96.databases.neo4j.io"
        user = "neo4j"
        password = "xZLEUi-SSuZkCSafSdxd7qtJJGHRDTmVRZNBzDAYc58"
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.mongodb_manager.connect()

    def get_followers_count(self, user_name):
        user_id = str(self.mongodb_manager.get_user_id_by_name(user_name))
        
        with self.driver.session() as session:
            result = session.run("MATCH (user:User {id: $user_id})<-[:FOLLOWS]-(follower) RETURN count(follower)", user_id=user_id)
            return result.single()[0]


    def get_following_count(self, user_name):
        user_id = str(self.mongodb_manager.get_user_id_by_name(user_name))
        if user_name:
            with self.driver.session() as session:
                result = session.run("MATCH (user:User {id: $user_id})-[:FOLLOWS]->(following) RETURN count(following)", user_id=user_id)
                return result.single()[0]
        return 0  # Retournez 0 si aucun nom d'utilisateur n'est trouvé

    def get_followers_of_spinomade(self):
        spinomade_id = '129479601'  # ID de Spinomade
        with self.driver.session() as session:
            result = session.run("""
                MATCH (user:User)-[:FOLLOWS]->(spinomade:User {id: $spinomade_id})
                RETURN user.id AS userId
            """, spinomade_id=spinomade_id)
            followers_ids = [record["userId"] for record in result]
        
        # Convertir les ID Neo4j en noms MongoDB
        followers_names = [self.mongodb_manager.get_user_name_by_id(int(user_id)) for user_id in followers_ids]
        return followers_names  # Liste des noms des followers

    def get_followed_by_spinomade(self):
        spinomade_id = '129479601'  # ID de Spinomade
        with self.driver.session() as session:
            result = session.run("""
                MATCH (spinomade:User {id: $spinomade_id})-[:FOLLOWS]->(user:User)
                RETURN user.id AS userId
            """, spinomade_id=spinomade_id)
            following_ids = [record["userId"] for record in result]
        
        # Convertir les ID Neo4j en noms MongoDB
        following_names = [self.mongodb_manager.get_user_name_by_id(int(user_id)) for user_id in following_ids]
        return following_names  # Liste des noms des utilisateurs suivis par Spinomade

    def get_mutual_followers_of_spinomade(self):
        spinomade_id = '129479601'  # ID de Spinomade
        with self.driver.session() as session:
            result = session.run("""
                MATCH (user:User)-[:FOLLOWS]->(spinomade:User {id: $spinomade_id})-[:FOLLOWS]->(user)
                RETURN user.id AS userId
            """, spinomade_id=spinomade_id)
            mutual_ids = [record["userId"] for record in result]
        
        # Convertir les ID Neo4j en noms MongoDB
        mutual_names = [self.mongodb_manager.get_user_name_by_id(int(user_id)) for user_id in mutual_ids]
        return mutual_names  # Liste des noms des utilisateurs qui sont à la fois followers et followees de Spinomade

    def execute_queries(self):
        # Initialiser un dictionnaire pour stocker les résultats des requêtes
        query_results = {}

        #user_id = '129479601'
        user_name = 'Spinomade'
        
        # Exécuter chaque fonction de requête et stocker les résultats
        query_results['followers_count'] = self.get_followers_count(user_name)
        query_results['following_count'] = self.get_following_count(user_name)
        query_results['followers_of_spinomade'] = self.get_followers_of_spinomade()
        query_results['followed_by_spinomade'] = self.get_followed_by_spinomade()
        query_results['mutual_followers_of_spinomade'] = self.get_mutual_followers_of_spinomade()

        # Retourner les résultats de toutes les requêtes
        return query_results

    def close(self):
        self.driver.close()
