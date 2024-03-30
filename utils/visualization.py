"""Dans visualization.py, la classe Visualizer est définie pour créer
des visualisations des données récupérées à partir de MongoDB et Neo4j.
La bibliothèque matplotlib est utilisée pour des visualisations de base,
tandis que plotly est employée pour des graphiques interactifs plus avancés."""


import matplotlib.pyplot as plt
from mongodb.mongodb_manager import MongoDBManager
import plotly.graph_objects as go

class Visualizer:
    def __init__(self, mongo_data, neo4j_data):
        # Stocke les données récupérées pour une utilisation dans les méthodes de visualisation.
        self.mongo_data = mongo_data
        self.neo4j_data = neo4j_data
        self.mongodb_manager = MongoDBManager()


    def visualize_mongodb_data(self):
        # Visualisation des statistiques générales récupérées de MongoDB.
        data = [
            self.mongo_data['user_count'],
            self.mongo_data['tweet_count'],
            self.mongo_data['hashtag_count']
        ]
        labels = ['Utilisateurs', 'Tweets', 'Hashtags']
        plt.figure(figsize=(8, 6))
        plt.bar(labels, data)
        plt.title("Questions 1,2 et 3")
        plt.show()

        data = [
            len(self.mongo_data['users_with_over_10_followers']),
            len(self.mongo_data['users_following_more_than_5'])
        ]
        labels = ['users with over 10 followers', 'users following more than 5']
        plt.figure(figsize=(8, 6))
        plt.bar(labels, data)
        plt.title("Questions 10 et 11")
        plt.show()

        data = [
            self.mongo_data['tweets_with_hashtag_actualite'],
            self.mongo_data['unique_users_for_hashtag_valls']
        ]
        labels = ['tweets with hashtag actualite', 'unique users for hashtag valls']
        plt.figure(figsize=(8, 6))
        plt.bar(labels, data)
        plt.title("Questions 4 et 5")
        plt.show()

        # Visualisation des 10 hashtags les plus populaires.
        top_hashtags = self.mongo_data['top_10_popular_hashtags']
        hashtags = [hashtag['_id'] for hashtag in top_hashtags]
        counts = [hashtag['count'] for hashtag in top_hashtags]
        plt.figure(figsize=(10, 6))
        plt.bar(hashtags, counts)
        plt.title("Question 13 : Les 10 hashtags les plus populaires")
        plt.xticks(rotation=45)
        plt.show()

        # Utilisation de Plotly pour une visualisation plus interactive des tweets populaires.
        top_tweets = self.mongo_data['top_10_popular_tweets']
        tweet_texts = [tweet['text'][:50] + '...' if len(tweet['text']) > 50 else tweet['text'] for tweet in top_tweets]  # Tronquer les textes de tweets longs
        favorites_counts = [tweet['nbFavorites'] for tweet in top_tweets]
        # Création du graphique
        fig = go.Figure([
            go.Bar(
                x=tweet_texts,  # Les textes des tweets servent d'axe des x
                y=favorites_counts,  # Les nombres de favoris servent d'axe des y
                marker=dict(color='rgba(50, 171, 96, 0.6)',
                            line=dict(color='rgba(50, 171, 96, 1.0)', width=1))
            )
        ])
        # Mise en page du graphique
        fig.update_layout(
            title='Question 12: Les 10 tweets les plus populaires',
            xaxis_tickangle=-45,
            xaxis_title='Tweets',
            yaxis_title='Nombre de Favoris',
            plot_bgcolor='rgba(245, 246, 249, 1)',
            showlegend=False
        )
        # Afficher le graphique
        fig.show()

    def visualize_neo4j_data(self):
        # Visualisation des relations autour de l'utilisateur 'Spinomade' dans Neo4j.
        followers_names = self.neo4j_data['followers_of_spinomade']
        following_names = self.neo4j_data['followed_by_spinomade']
        mutual_names = self.neo4j_data['mutual_followers_of_spinomade']

        # Créer des ensembles pour faciliter la création du diagramme de Venn
        followers_set = set(followers_names)
        following_set = set(following_names)

        # Utilisation de Plotly pour créer un diagramme de barres illustrant les followers, followings et mutual followers.
        trace_followers = go.Bar(x=list(followers_set), y=[1] * len(followers_set), name='Followers', marker_color='blue')
        trace_following = go.Bar(x=list(following_set), y=[1] * len(following_set), name='Following', marker_color='red')
        trace_mutual = go.Bar(x=list(mutual_names), y=[2] * len(mutual_names), name='Mutual Followers', marker_color='green')
        layout = go.Layout(
            title='Questions 7, 8 et 9: Relations de Spinomade',
            yaxis=dict(title='Count', tickvals=[1, 2]),
            xaxis=dict(title='Users')
        )
        fig = go.Figure(data=[trace_followers, trace_following, trace_mutual], layout=layout)
        fig.show()