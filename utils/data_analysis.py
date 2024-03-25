"""Ce script est responsable de la génération d'un rapport basé sur
    les données récupérées de MongoDB et Neo4j.
    Il traite et formate ces données en un rapport textuel,
    illustrant des analyses spécifiques comme les hashtags les plus populaires
    et les utilisateurs influents."""

def generate_report(mongo_data, neo4j_data):
    report_lines = []

    # Ajoute une section au rapport pour les analyses des données MongoDB.
    top_hashtags = mongo_data['top_10_popular_hashtags']
    report_lines.append("Les 10 hashtags les plus populaires sont :\n")
    for hashtag in top_hashtags:
        # Ajoute chaque hashtag et son nombre de mentions au rapport.
        report_lines.append(f"{hashtag['_id']}: {hashtag['count']} mentions\n")

    longest_discussion = mongo_data['get_longest_discussion']
    report_lines.append("\nLa plus longue discussion est initiée par le tweet :\n")
    if longest_discussion:
        # Si une discussion existe, ajoute son texte et le nombre de réponses au rapport.
        report_lines.append(f"'{longest_discussion['initiatingTweetText']}' avec {longest_discussion['responseCount']} réponses.\n")
    else:
        report_lines.append("Aucune discussion longue n'a été trouvée.\n")

    # Ajoute une section au rapport pour les analyses des données Neo4j.
    user_infos = mongo_data['users_with_over_10_followers']
    # S'assurer que user_infos contient les informations, puis les trier par le nombre de followers
    sorted_user_infos = sorted(user_infos, key=lambda x: x['nbFollowers'], reverse=True)[:5]

    report_lines.append("\nLes top influenceurs sont :\n")
    for influencer in sorted_user_infos:
        # Ajoute le nom, le nombre de followers et la description de chaque influenceur au rapport.
        report_lines.append(f"- {influencer['name']} avec {influencer['nbFollowers']} followers. Description: {influencer.get('description', 'Pas de description')} \n")

    # Écrit le rapport complet dans un fichier texte.
    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        f.writelines(report_lines)

    print("Rapport d'analyse généré dans analysis_report.txt.")
