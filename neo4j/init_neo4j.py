from py2neo import Graph

# Connexion à Neo4j
uri = "neo4j+s://dc15bb96.databases.neo4j.io"
user = "neo4j"
password = "xZLEUi-SSuZkCSafSdxd7qtJJGHRDTmVRZNBzDAYc58"
graph = Graph(uri, auth=(user, password))

# Import des données des utilisateurs et de leurs relations "follow"
query_follow = """
LOAD CSV WITH HEADERS FROM 'file:///path_to_your_csv/tw_user_follow.csv' AS row
MERGE (user1:User {id: row.sourceIdUser})
MERGE (user2:User {id: row.targetIdUser})
MERGE (user1)-[:FOLLOWS]->(user2);
"""
graph.run(query_follow)

# Import des données des tweets, des utilisateurs, et des relations "retweet"
query_retweet = """
LOAD CSV WITH HEADERS FROM 'file:///path_to_your_csv/tweet_retweet.csv' AS row
MERGE (tweet:Tweet {id: row.idTweet})
MERGE (user:User {id: row.idUser})
MERGE (originalTweet:Tweet {id: row.idRetweet})
MERGE (user)-[:POSTED]->(tweet)
MERGE (tweet)-[:RETWEET_OF]->(originalTweet);
"""
graph.run(query_retweet)

print("Les données ont été importées dans Neo4j avec succès.")
