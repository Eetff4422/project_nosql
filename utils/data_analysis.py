def generate_report(mongo_data, neo4j_data):
    report_lines = []

    # Ajouter les analyses pour les données MongoDB
    top_hashtags = mongo_data['top_10_popular_hashtags']
    report_lines.append("Les 10 hashtags les plus populaires sont :\n")
    for hashtag in top_hashtags:
        report_lines.append(f"{hashtag['_id']}: {hashtag['count']} mentions\n")

    longest_discussion = mongo_data['get_longest_discussion']
    report_lines.append("\nLa plus longue discussion est initiée par le tweet :\n")
    if longest_discussion:
        report_lines.append(f"'{longest_discussion['initiatingTweetText']}' avec {longest_discussion['responseCount']} réponses.\n")
    else:
        report_lines.append("Aucune discussion longue n'a été trouvée.\n")

    # Ajouter les analyses pour les données Neo4j
    user_infos = mongo_data['users_with_over_10_followers']
    # S'assurer que user_infos contient les informations, puis les trier par le nombre de followers
    sorted_user_infos = sorted(user_infos, key=lambda x: x['nbFollowers'], reverse=True)[:5]

    report_lines.append("\nLes top influenceurs sont :\n")
    for influencer in sorted_user_infos:
        report_lines.append(f"- {influencer['name']} avec {influencer['nbFollowers']} followers. Description: {influencer.get('description', 'Pas de description')} \n")

    # Écrire le rapport dans un fichier
    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        f.writelines(report_lines)

    print("Rapport d'analyse généré dans analysis_report.txt.")
