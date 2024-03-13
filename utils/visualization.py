import matplotlib.pyplot as plt

def visualize_mongodb_data(data):
    # Visualiser les données MongoDB
    # Exemple : afficher le nombre d'utilisateurs
    plt.bar(["Nombre d'utilisateurs"], [data["nombre_utilisateurs"]])
    plt.show()

def visualize_neo4j_data(data):
    # Visualiser les données Neo4j
    # Exemple : afficher le nombre de relations "SUIT"
    plt.bar(["Nombre de relations"], [data["nombre_relations"]])
    plt.show()