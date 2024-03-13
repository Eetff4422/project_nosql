import matplotlib.pyplot as plt
import seaborn as sns

def visualize_mongodb_data(data):
    plt.figure(figsize=(15, 10))
    plt.suptitle('Visualisations des Données MongoDB')

    # Nombre d'utilisateurs et de tweets
    plt.subplot(2, 3, 1)
    categories = ['user_count', 'tweet_count']
    counts = [data.get('user_count', 0), data.get('tweet_count', 0)]
    sns.barplot(x=categories, y=counts)

    plt.title("Nombre d'Utilisateurs et de Tweets")
    plt.ylabel('Nombre')

    # Nombre total d'hashtags
    plt.subplot(2, 3, 2)
    plt.bar(['Total Hashtags'], [data.get('hashtag_count', 0)])
    plt.title("Nombre Total d'Hashtags")
    plt.ylabel('Nombre')

    # Tweets avec des hashtags spécifiques
    plt.subplot(2, 3, 3)
    hashtags = ['actualite', 'valls']
    hashtag_counts = [data.get('tweets_with_hashtag_actualite', 0), data.get('unique_users_for_hashtag_valls', 0)]
    sns.barplot(x=hashtags, y=hashtag_counts)
    plt.title("Nombre de Tweets par Hashtag Spécifique")
    plt.ylabel('Nombre')

    # Les 10 tweets les plus populaires (basés sur les favoris)
    if 'top_10_popular_tweets' in data:
        tweets_data = data['top_10_popular_tweets']
        tweet_labels = [tweet['text'][:10] + '...' if 'text' in tweet else 'NoText' for tweet in tweets_data]
        favorite_counts = [tweet['nbFavorites'] if 'nbFavorites' in tweet else 0 for tweet in tweets_data]

        plt.subplot(2, 3, 4)  # Ajustez selon la disposition souhaitée
        sns.barplot(x=tweet_labels, y=favorite_counts)
        plt.title('Top 10 Tweets Populaires')
        plt.xlabel('Tweets')
        plt.ylabel('Nombre de Favoris')
        plt.xticks(rotation=45)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def visualize_neo4j_data(data):
    plt.figure(figsize=(15, 10))
    plt.suptitle('Visualisations des Données Neo4j')

    # Nombre de followers et following pour un utilisateur spécifique
    plt.subplot(2, 3, 1)
    categories = ['followers_count', 'following_count']
    values = [data.get('followers_count', 0), data.get('following_count', 0)]
    sns.barplot(x=categories, y=values)
    plt.title("Followers et Following de " + data.get('user_name', 'Utilisateur'))
    plt.ylabel('Nombre')
    
    # Utilisateurs ayant plus de 10 followers
    plt.subplot(2, 3, 2)
    sns.barplot(x=list(range(len(data['users_with_over_10_followers']))), y=data['users_with_over_10_followers'])
    plt.title('Utilisateurs avec plus de 10 Followers')
    plt.xlabel('Utilisateurs')
    plt.ylabel('Nombre de Followers')
    plt.xticks([])

    # Utilisateurs suivis par plus de 5 utilisateurs
    plt.subplot(2, 3, 3)
    sns.barplot(x=list(range(len(data['users_following_more_than_5']))), y=data['users_following_more_than_5'])
    plt.title('Utilisateurs suivant plus de 5 personnes')
    plt.xlabel('Utilisateurs')
    plt.ylabel('Nombre suivis')
    plt.xticks([])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()