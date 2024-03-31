# Application de Suivi de Tweets et d'Analyse des Réseaux Sociaux

Notre application est un outil puissant qui permet d'analyser les tendances sur Twitter. Elle est parfaite pour voir comment les gens interagissent et se suivent entre eux, ainsi que pour observer l'influence et la popularité des tweets et des retweets. On utilise MongoDB pour gérer toutes les infos sur les utilisateurs et leurs tweets sans souci. Et avec Neo4j, on peut visualiser les liens entre les abonnements et suivre les conversations. En gros, l'application est super pour comprendre ce qui se passe sur Twitter et découvrir qui sont les utilisateurs les plus influents.

## Configuration des Bases de Données

### Neo4j

**Initialisation de la Base de Données Neo4j** : Avant de démarrer l'application, assurez-vous que votre base de données Neo4j soit en cours d'exécution.
1. **Identifiants de Connexion** : Ouvrez le script `init_neo4j.py` et renseignez vos identifiants de connexion à votre instance Neo4j dans les variables appropriées.
2. **Importation des Données** : Utilisez le script `init_neo4j.py` pour importer les données sur les relations d'abonnement entre utilisateurs, ainsi que les tweets et retweets.

### MongoDB

1. **Connexion Automatisée** : Le script se connecte à votre cluster MongoDB en utilisant l'URI que vous aurez fourni.
2. **Création de la Base de Données** : Si elle n'existe pas déjà, une base de données nommée dbnowsql sera créée.
3. **Importation des Collections** : Les données sont importées dans les collections MongoDB depuis les fichiers CSV stockés sur GitHub, via les URLs suivantes :
- **Utilisateurs** : Les données des utilisateurs sont importées depuis tw_user.csv dans la collection tw_user.
- **Tweets** : Les données des tweets sont importées depuis tweet.csv dans la collection tweet.
- **Hashtags** : Les données des hashtags sont importées depuis tweet_hashtag.csv dans la collection tweet_hashtag.
**Note** : Le script détecte et utilise automatiquement le bon délimiteur pour chaque fichier CSV pendant l'importation.

Pour lancer le processus d'initialisation, assurez-vous de renseigner vos identifiants de connexion MongoDB dans le script init_mongodb.py et exécutez-le. Une fois terminé, vous recevrez une confirmation dans la console pour chaque collection importée avec succès.

Cette automatisation élimine la nécessité de manipulations manuelles via MongoDB Compass, garantissant une configuration cohérente et reproductible de votre base de données.

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

- **Initialisation et Vérification des Bases de Données** : Les scripts intégrés vérifient l'existence et initialisent les bases de données MongoDB et Neo4j si nécessaire, assurant une préparation adéquate de l'environnement de données.
- **Normalisation des Données** : Les champs de données sont mis à jour et normalisés pour garantir la cohérence des types de données, ce qui facilite les analyses précises et les visualisations pertinentes.
- **Analyse de Réseau Social avec Neo4j** : Utilisez Neo4j pour explorer les relations d'abonnement entre les utilisateurs et dévoiler la complexité des structures de réseau social.
- **Analyse des Données de Tweet avec MongoDB** : Plongez dans les interactions des tweets, analysez les discussions initiées par les tweets et mesurez l'engagement autour des discussions.
- **Visualisation des Données** : Avec l'outil de visualisation intégré, transformez les données brutes en graphiques et visualisations significatives, révélant des insights cachés dans les modèles de données.
- **Rapport d'Analyse** : Générez des rapports d'analyse détaillés pour résumer les découvertes et soutenir les décisions basées sur les données.
- **Fermeture Propre des Connexions** : Après les analyses, les connexions aux bases de données sont fermées proprement, assurant l'intégrité des données et la stabilité du système.

## Notes Importantes

- Vérifiez que votre instance Neo4j est active et que votre cluster MongoDB est accessible avant de lancer l'application.
