from neo4j import GraphDatabase

class Neo4jManager:
    def __init__(self):
        self.driver = None

    def connect(self):
        uri = "neo4j+s://dc15bb96.databases.neo4j.io"
        user = "neo4j"
        password = "xZLEUi-SSuZkCSafSdxd7qtJJGHRDTmVRZNBzDAYc58"
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_followers_count(self, user_name):
        with self.driver.session() as session:
            result = session.run("MATCH (user:User {name: $user_name})<-[:FOLLOWS]-(follower) RETURN count(follower)", user_name=user_name)
            return result.single()[0]

    def get_following_count(self, user_name):
        with self.driver.session() as session:
            result = session.run("MATCH (user:User {name: $user_name})-[:FOLLOWS]->(following) RETURN count(following)", user_name=user_name)
            return result.single()[0]

    def get_followers_of_spinomade(self):
        # 7. Nom des followers de Spinomade
        with self.driver.session() as session:
            result = session.run("MATCH (user:User)-[:FOLLOWS]->(spinomade:User {name: 'Spinomade'}) RETURN user.name")
            return [record["user.name"] for record in result]

    def get_followed_by_spinomade(self):
        # 8. Nom des utilisateurs suivis par Spinomade
        with self.driver.session() as session:
            result = session.run("MATCH (spinomade:User {name: 'Spinomade'})-[:FOLLOWS]->(user:User) RETURN user.name")
            return [record["user.name"] for record in result]

    def get_mutual_followers_of_spinomade(self):
        # 9. Utilisateurs qui sont à la fois followers et followees de Spinomade
        with self.driver.session() as session:
            result = session.run("""
            MATCH (user:User)-[:FOLLOWS]->(spinomade:User {name: 'Spinomade'})-[:FOLLOWS]->(user)
            RETURN user.name
            """)
            return [record["user.name"] for record in result]

    def get_users_with_over_10_followers(self):
        # 10. Utilisateurs ayant plus de 10 followers
        with self.driver.session() as session:
            result = session.run("MATCH (user:User)<-[:FOLLOWS]-(followers) WITH user, count(followers) AS numFollowers WHERE numFollowers > 10 RETURN user.name")
            return [record["user.name"] for record in result]

    def get_users_following_more_than_5(self):
        # 11. Utilisateurs qui suivent plus de 5 utilisateurs
        with self.driver.session() as session:
            result = session.run("MATCH (user:User)-[:FOLLOWS]->(following) WITH user, count(following) AS numFollowing WHERE numFollowing > 5 RETURN user.name")
            return [record["user.name"] for record in result]

    def get_tweets_initiating_discussion(self):
        # 14. Tweets qui initient une discussion
        with self.driver.session() as session:
            result = session.run("""
            MATCH (tweet:Tweet)-[:REPLY_TO]->(originalTweet:Tweet)
            WHERE NOT ((originalTweet)-[:REPLY_TO]->())
            RETURN originalTweet.id AS initiatingTweetId
            """)
            return [record["initiatingTweetId"] for record in result]

    def get_longest_discussion(self):
        # 15. La plus longue discussion
        with self.driver.session() as session:
            result = session.run("""
            MATCH (start:Tweet)-[:REPLY_TO*]->(end:Tweet)
            WITH start, end, LENGTH(SHORTEST_PATH((start)-[:REPLY_TO*]->(end))) AS length
            ORDER BY length DESC
            LIMIT 1
            RETURN start.id AS startTweetId, end.id AS endTweetId, length
            """)
            return result.single()

    def get_discussions_start_end(self):
        # 16. Pour chaque conversation, donnez-en le début et la fin
        with self.driver.session() as session:
            result = session.run("""
            MATCH p=(start:Tweet)-[:REPLY_TO*]->(end:Tweet)
            WHERE NOT ((start)-[:REPLY_TO]->()) AND NOT ((end)<-[:REPLY_TO]-())
            RETURN start.id AS startTweetId, end.id AS endTweetId, LENGTH(p) as length
            ORDER BY length DESC
            """)
            return [record.data() for record in result]

    def close(self):
        self.driver.close()
