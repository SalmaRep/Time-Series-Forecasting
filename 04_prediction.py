######### Prédictions futures avec le modele entraîné ############

##################################################################
# Préparer les données pour les prédictions futures
last_date = train_df['date'].max()

# Générer les dates futures entre date_debut et date_fin, en excluant les week-ends
future_dates = pd.date_range(start=date_debut, end=date_fin, freq='D')
future_dates = future_dates[future_dates.dayofweek < 5]

future_df = pd.DataFrame({'date': future_dates})

# Liste des lags à créer
lags = [1, 2, 3, 4, 5]

# Définir les années à prendre en compte pour les jours fériés
annees = [annee_debut, annee_fin]
jours_feries = []

# Obtenir les jours fériés pour chaque année
for annee in annees:
    fr_holidays = holidays.France(years=annee)

for i in range(len(future_df)):
    # Extraire les caractéristiques temporelles de chaque date
    future_df.loc[i, 'dayofweek'] = future_df.loc[i, 'date'].dayofweek
    future_df.loc[i, 'dayofmonth'] = future_df.loc[i, 'date'].day
    future_df.loc[i, 'dayofyear'] = future_df.loc[i, 'date'].dayofyear
    future_df.loc[i, 'month'] = future_df.loc[i, 'date'].month
    future_df.loc[i, 'year'] = future_df.loc[i, 'date'].year
    future_df.loc[i, 'quarter'] = future_df.loc[i, 'date'].quarter

    # Ajouter les variables d'encodage pour les jours de la semaine (lundi à vendredi)
    future_df.loc[i, 'dayofweek_0'] = int(future_df.loc[i, 'date'].dayofweek == 0)
    future_df.loc[i, 'dayofweek_1'] = int(future_df.loc[i, 'date'].dayofweek == 1)
    future_df.loc[i, 'dayofweek_2'] = int(future_df.loc[i, 'date'].dayofweek == 2)
    future_df.loc[i, 'dayofweek_3'] = int(future_df.loc[i, 'date'].dayofweek == 3)
    future_df.loc[i, 'dayofweek_4'] = int(future_df.loc[i, 'date'].dayofweek == 4)

    # Ajouter les valeurs de décalage (lags)
    for lag in lags:
        if i - lag >= 0:  # Vérification de l'index ( si 'i' est suffisamment grand pour remettre l'accès aux valeurs précédantes)
            future_df.loc[i, f'lag{lag}'] = future_df.loc[i - lag, 'predictions']

    # Éviter les prédictions pour les week-ends
    if future_df.loc[i, 'dayofweek'] >= 5:
        future_df.loc[i, 'predictions'] = None
    else:
        # Initialiser les valeurs de lag pour les premières lignes à partir de la fin de train_df
        if i == 0: #La 1ère ligne de ma data frame future_df
            future_df.loc[i, 'lag1'] = train_df['Recus'].iloc[-1] # On utilise la dernière valeur de 'Recus' dans train_df comme lag1 pour la première ligne de future_df
            future_df.loc[i, 'lag2'] = train_df['Recus'].iloc[-2] # On utilise l'avant-dernière valeur de 'Recus' dans train_df comme lag2 pour la première ligne de future_df
            future_df.loc[i, 'lag3'] = train_df['Recus'].iloc[-3]
            future_df.loc[i, 'lag4'] = train_df['Recus'].iloc[-4]
            future_df.loc[i, 'lag5'] = train_df['Recus'].iloc[-5]
        elif i == 1:  #La 2ème ligne de ma data frame future_df
            future_df.loc[i, 'lag2'] = train_df['Recus'].iloc[-1] # On copie la dernière valeur de 'Recus' depuis train_df dans la colonne 'lag2' de future_df (ligne i)
            future_df.loc[i, 'lag3'] = train_df['Recus'].iloc[-2] # On copie l'avant-dernière valeur de 'Recus' depuis train_df dans la colonne 'lag3' de future_df (ligne i)
            future_df.loc[i, 'lag4'] = train_df['Recus'].iloc[-3]
            future_df.loc[i, 'lag5'] = train_df['Recus'].iloc[-4]
        elif i == 2: 
            future_df.loc[i, 'lag3'] = train_df['Recus'].iloc[-1]
            future_df.loc[i, 'lag4'] = train_df['Recus'].iloc[-2]
            future_df.loc[i, 'lag5'] = train_df['Recus'].iloc[-3]
        elif i == 3:
            future_df.loc[i, 'lag4'] = train_df['Recus'].iloc[-1]
            future_df.loc[i, 'lag5'] = train_df['Recus'].iloc[-2]
        elif i == 4:
            future_df.loc[i, 'lag5'] = train_df['Recus'].iloc[-1] # -1 correspond à la dernière ligne de ma base train_df (ici nous reprenons la dernière ligne de notre base train_df pour la coller sur la base future_df (colonne lag5 / 1ère ligne )
        else:
            future_df.loc[i, 'lag1'] = future_df.loc[i - 1, 'predictions'] 

        # Effectuer la prédiction pour la date actuelle
        future_predictions = model.predict(
            future_df.iloc[[i]][['quarter', 'dayofmonth', 'dayofyear', 'month',
                                 'dayofweek_0', 'dayofweek_1', 'dayofweek_2',
                                 'dayofweek_4', 'lag1', 'lag2', 'lag3', 'lag4', 'lag5']]
            .values.reshape(1, -1)
        )
        future_df.loc[i, 'predictions'] = future_predictions[0]
