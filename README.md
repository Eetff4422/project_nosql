# Application de Suivi de Tweets et d'Analyse des Réseaux Sociaux

Cette application offre une interface pour interagir avec et analyser des données Twitter, en se concentrant sur les relations d'abonnement entre utilisateurs et les interactions via tweets et retweets. Elle utilise MongoDB pour le stockage des données relatives aux utilisateurs et tweets, et Neo4j pour analyser les réseaux d'abonnement et les discussions de tweets.

## Configuration des Bases de Données

### Neo4j

**Initialisation de la Base de Données Neo4j** : Avant de démarrer l'application, assurez-vous que votre base de données Neo4j est prête et contient les données nécessaires.

1. **Identifiants de Connexion** : Ouvrez le script `init_neo4j.py` et renseignez vos identifiants de connexion à votre instance Neo4j dans les variables appropriées.
2. **Importation des Données** : Utilisez le script `init_neo4j.py` pour importer les données sur les relations d'abonnement entre utilisateurs, ainsi que les tweets et retweets. Veillez à ce que les fichiers CSV mentionnés dans le script soient accessibles et correctement formatés.

### MongoDB

**Configuration de MongoDB** : Pour configurer votre cluster MongoDB, suivez les étapes suivantes :

1. **Connexion** : Connectez-vous à MongoDB Compass et accédez à votre cluster MongoDB.
2. **Création de la Base de Données** : Créez une nouvelle base de données nommée `dbnowsql`.
3. **Importation des Collections** : Importez les données à partir des fichiers CSV suivants dans les collections correspondantes :
    - Utilisateurs : `tw_user.csv` pour la collection `tw_user`.
    - Tweets : `tweet.csv` pour la collection `tweet`.
    - Hashtags : `tweet_hashtag.csv` pour la collection `tweet_hashtag`.

Assurez-vous d'entrer vos identifiants de connexion MongoDB dans le script approprié de l'application pour permettre une connexion réussie.

## Démarrage de l'Application

1. **Installation des Dépendances** : Installez toutes les dépendances nécessaires à l'aide de la commande suivante :
    ```bash
    pip install -r requirements.txt
    ```
2. **Lancement de l'Application** : Exécutez le script principal avec la commande suivante pour démarrer l'application :
    ```bash
    python main.py
    ```

## Fonctionnalités Principales

- **Analyse des Relations d'Abonnement** : Explorez les relations d'abonnement entre les utilisateurs et la structure du réseau social.
- **Analyse des Interactions de Tweets** : Analysez les discussions initiées par les tweets pour identifier les plus engagées.
- **Analyse des Hashtags** : Identifiez les hashtags les plus populaires et leur usage parmi les utilisateurs.

## Notes Importantes

- Vérifiez que votre instance Neo4j est active et que votre cluster MongoDB est accessible avant de lancer l'application.
- Assurez-vous que les scripts d'initialisation et les fichiers CSV sont bien configurés pour une intégration réussie des données dans les bases de données.
