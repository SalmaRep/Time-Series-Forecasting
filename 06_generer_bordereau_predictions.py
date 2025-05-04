################################## Bordereau ##################################

# Sélectionner les colonnes pertinentes 'date', 'flux_primaire', 'prediction_par_jour'
nouveau_df = merged_df[['date', 'flux_primaire', 'prediction_par_jour']]

# Utilisation de pivot_table pour transformer les modalités de 'flux_primaire' en colonnes
nouveau_df = pd.pivot_table(nouveau_df, index='date', columns='flux_primaire', values='prediction_par_jour')
nouveau_df = nouveau_df.reset_index()
nouveau_df = nouveau_df.rename(columns={'index': 'date'})

# Créer un DataFrame avec toutes les dates entre la première et la dernière date
toutes_dates = pd.date_range(start=nouveau_df['date'].min(), end=nouveau_df['date'].max())

# Filtrer pour obtenir uniquement les weekends (samedi et dimanche)
weekends = toutes_dates[toutes_dates.dayofweek.isin([5, 6])]

# Créer un DataFrame pour les weekends avec 'flux_primaire' et 'prediction_par_jour' égaux à 0
weekends_df = pd.DataFrame({'date': weekends, 'FLUX A': 0, 'FLUX B': 0, 'FLUX C': 0, 'FLUX D': 0, 'FLUX E': 0})

# Concaténer le DataFrame "nouveau_df" avec "weekends_df" pour ajouter les lignes des weekends
nouveau_df = pd.concat([nouveau_df, weekends_df])

# Trier les données par 'date' pour les organiser de manière chronologique
nouveau_df = nouveau_df.sort_values(by='date').reset_index(drop=True)

# Obtenir le mois de la première date
premier_mois = pd.to_datetime(nouveau_df['date'].iloc[0]).strftime('%Y-%m')

# Formater la colonne 'date' en format 'jour/mois/année'
nouveau_df['date'] = nouveau_df['date'].dt.strftime('%Y/%m/%d')

# Afficher le DataFrame résultant
print(nouveau_df)

# Enregistrer le DataFrame au format Excel avec le nom basé sur le mois
nom_fichier = f"bordereau_test_{premier_mois}.xlsx"
nouveau_df.to_excel(nom_fichier, index=False)
