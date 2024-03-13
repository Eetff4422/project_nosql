# Application de Suivi de Tweets et d'Analyse des Réseaux Sociaux

Cette application permet d'interagir avec et d'analyser des données issues de Twitter, en se concentrant sur les relations d'abonnement entre utilisateurs et les interactions via les tweets et retweets. L'application utilise MongoDB pour stocker les données des utilisateurs et des tweets, et Neo4j pour analyser les relations entre les utilisateurs et les discussions de tweets.

## Configuration des Bases de Données

### Neo4j

1. **Initialisation de la Base de Données Neo4j** : Avant de lancer l'application, assurez-vous que votre base de données Neo4j est initialisée avec les données nécessaires. Utilisez le script `init_neo4j.py` pour importer les relations entre utilisateurs (suivis et abonnements) ainsi que les informations relatives aux tweets et retweets. Ce script doit être exécuté après avoir démarré votre instance Neo4j et configuré avec les bons identifiants de connexion.



    Assurez-vous que les fichiers CSV référencés dans `init_neo4j.py` sont accessibles et correctement formatés avant d'exécuter le script.

### MongoDB

1. **Configuration de MongoDB** : Connectez-vous à votre cluster MongoDB via MongoDB Compass. Créez une base de données nommée, par exemple, `dbnowsql` et importez les fichiers CSV correspondant à chaque collection :

    - Utilisateurs (`tw_user.csv`)
    - Tweets (`tweet.csv`)
    - Hashtags (`tweet_hashtag.csv`)

    Chaque fichier CSV correspondra à une collection spécifique dans MongoDB.

## Démarrage de l'Application

Après avoir configuré les bases de données, vous pouvez lancer l'application. Assurez-vous que toutes les dépendances sont installées :

```bash
pip install -r requirements.txt
```

Exécutez ensuite le script principal pour démarrer l'application :

```bash
python main.py
```

L'application exécutera des requêtes sur les bases de données MongoDB et Neo4j pour extraire et analyser les données, puis affichera les résultats sous forme de graphiques.

## Fonctionnalités

- **Analyse des Relations d'Abonnement** : Visualisez comment les utilisateurs suivent d'autres utilisateurs et comment ces relations structurent le réseau social.
- **Analyse des Interactions de Tweets** : Examinez les discussions générées par les tweets et identifiez les discussions les plus longues et les plus engagées.
- **Analyse des Hashtags** : Découvrez les hashtags les plus populaires et comment ils sont utilisés par différents utilisateurs.

## Notes Importantes

- Assurez-vous que votre instance Neo4j est en cours d'exécution et que votre cluster MongoDB est accessible avant de lancer l'application.
- Les scripts d'initialisation et les fichiers CSV doivent être correctement configurés et formatés pour assurer une initialisation réussie des bases de données.
