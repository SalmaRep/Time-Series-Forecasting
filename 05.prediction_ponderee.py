################################## Calcul du Poids par Flux et Prévision par Jour (Hors Week-End et Jours Fériés) #################

# Définir la date actuelle et calculer la date deux mois avant
date_actuelle = date_debut
Deux_mois_avant = date_actuelle - relativedelta(months=2)

# Filtrage des données sur les deux derniers mois
df_filtre = df_poids[(df_poids['date'] >= Deux_mois_avant)]

# Condition pour éviter les erreurs dans le cas où la date_debut est inférieure à la date maximale de la base de données
if date_debut < df_filtre['date'].max() + pd.Timedelta(days=1):   
    df_filtre = df_filtre[df_filtre['date'] < date_debut]

# Copie des données filtrées et création d'une nouvelle colonne "Jour" pour le jour de la semaine
df_poids = pd.DataFrame(df_filtre.copy())
df_poids['Jour'] = df_poids['date'].dt.day_name()

# Regroupement des données par date, jour et flux primaire pour obtenir la somme des reçus
df_poids = df_poids.groupby(['date','Jour', 'flux_primaire'])['Recus'].sum().reset_index()

# Filtrer les jours de semaine (exclure les week-ends)
df_poids = df_poids.loc[df_poids['Jour'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]

# Calculer si le jour est férié et exclure les jours fériés
df_poids = df_poids.set_index('date')
fr_holidays = holidays.France()
df_poids["jour_ferie"] = df_poids.index.map(lambda x: 1 if x in fr_holidays else 0)
df_poids = df_poids.loc[df_poids['jour_ferie'] == 0]  # Exclure les jours fériés

# Regroupement des données par flux primaire et jour, puis somme des reçus
df_poids = df_poids.groupby(['Jour','flux_primaire'])['Recus'].sum().reset_index()

# Calcul du poids de chaque flux primaire par jour
df_poids['Poids'] = df_poids.groupby(['Jour'])['Recus'].transform(lambda x: x / x.sum())

# Préparation des données pour la prédiction par flux primaire et jour
future_df['Jour'] = future_df['date'].dt.day_name()
merged_df = future_df.merge(df_poids, on='Jour')

# Calcul des prédictions par jour en tenant compte du poids de chaque flux primaire
merged_df['prediction_par_jour'] = merged_df['predictions'] * merged_df['Poids']

# Gestion des jours fériés dans les prédictions (mettre à 0 pour les jours fériés)
merged_df = merged_df.set_index('date')
merged_df["jour_ferie"] = merged_df.index.map(lambda x: 1 if x in fr_holidays else 0)
merged_df["prediction_par_jour"] = merged_df.apply(lambda row: 0 if row["jour_ferie"] == 1 else row["prediction_par_jour"], axis=1)

# Réinitialiser l'index et renommer la colonne de la date
merged_df = merged_df.reset_index()
merged_df = merged_df.rename(columns={'index':'date'})
