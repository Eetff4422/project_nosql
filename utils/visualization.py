import matplotlib.pyplot as plt
import seaborn as sns

def visualize_mongodb_data(data):
    # Exemple de visualisation: nombre de tweets par hashtag
    hashtags, counts = zip(*data.items())  # Suppose que 'data' est un dictionnaire {hashtag: count}
    plt.figure(figsize=(10, 6))
    sns.barplot(list(hashtags), list(counts))
    plt.title('Nombre de Tweets par Hashtag')
    plt.xlabel('Hashtags')
    plt.ylabel('Nombre de Tweets')
    plt.xticks(rotation=45)
    plt.show()

def visualize_neo4j_data(data):
    # Exemple basique de visualisation pour Neo4j: nombre de followers par utilisateur
    users, follower_counts = zip(*data.items())  # Suppose que 'data' est un dictionnaire {user: follower_count}
    plt.figure(figsize=(10, 6))
    sns.barplot(list(users), list(follower_counts))
    plt.title('Nombre de Followers par Utilisateur')
    plt.xlabel('Utilisateurs')
    plt.ylabel('Nombre de Followers')
    plt.xticks(rotation=45)
    plt.show()