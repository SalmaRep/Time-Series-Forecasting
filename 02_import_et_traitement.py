################### Importation et Prétraitement des Données ##########################

# A) Importation des données
# Sélection des colonnes nécessaires dans le fichier CSV
selected_columns = ['Date', 'recus', 'flux_primaire']
df = pd.read_csv(r"data/donnees.csv",  
                 encoding="latin1", delimiter=";", usecols=selected_columns)

# Renommer les colonnes pour une meilleure lisibilité
df = df.rename(columns={'Date': 'date', 'recus': 'Recus''})

# B) Prétraitement des données
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')  # Convertir 'date' en format datetime
df = df[df['date'] >= date_deb_histo]  # Filtrer les données à partir de la date de début
df = df[df['flux_primaire'].isin(flux_primaires)]  # Filtrer sur les flux primaires d'intérêt

# Créer une copie de df pour les poids par jour
df_poids = df.copy()

# Agrégation des données par date pour obtenir la table des réceptions
df = df.groupby('date', as_index=False)['Recus'].sum()

# Agrégation des données pour les poids par flux primaire
df_poids = df_poids.groupby(['date', 'flux_primaire'])['Recus'].sum().reset_index()

# C) Filtrage sur les jours de la semaine (lundi à vendredi)
df['dayofweek'] = df['date'].dt.dayofweek  # Ajouter la colonne 'dayofweek' pour les jours de la semaine
df = df[df['dayofweek'] < 5]  # Supprimer les samedis et dimanches

# D) Vérification de la date de début
# Message dans le cas où l'utilisateur a choisi une date debut supérieur à la date fin du fichier plus 1
if date_debut > df['date'].max() + pd.Timedelta(days=1):  
    print("\033[1mAVERTISSEMENT\033[0m")
    print("La date de début sélectionnée est supérieure strictement à la dernière date disponible dans la base de données plus 1 jour.")
    print("Veuillez choisir une date de début valide.")
    date_debut = df['date'].max() + pd.Timedelta(days=1)

# Condition qui nous permet d'éviter les erreurs par rapport à notre boucle de prédictions(lags) dans le cas où l'utilisateur choisi une date_debut inférieure à la date max de notre base df +1 (debut de préd)
if date_debut < df['date'].max() + pd.Timedelta(days=1):   
    df = df[df['date'] < date_debut]  # Filtrer les données jusqu'à la date de début

# E) Traitement des valeurs atypiques avec Isolation Forest
df = df.set_index('date')
# Utilisation de l'Isolation Forest (forêt d'isolation) est un algorithme d'apprentissage non supervisé de Machine Learning qui permet la détection d'anomalies dans un jeu de données (Data Set). Il isole les données atypiques, autrement dit celles qui sont trop différentes de la plupart des autres données calcule un score d'anomalie pour chaque observation du dataset.
# (5% des données sont considérées comme anormales)
isolation_forest_model = IsolationForest(contamination=0.05)
isolation_forest_model.fit(df)
df['anomaly'] = isolation_forest_model.predict(df)

# Suppression des anomalies et création d'une nouvelle colonne pour les réceptions "nettoyées"
df['new_Recus'] = df.apply(lambda row: row.Recus if row.anomaly == 1 else None, axis='columns')

# F) Remplissage des données manquantes par moyenne mobile (sur 30 jours)
df = df.assign(rolling_mean=df.new_Recus.fillna(df.new_Recus.rolling(31, min_periods=1).mean()))
df = df.dropna()  # Supprimer les valeurs manquantes
df = df.drop(columns=['Recus', 'anomaly', 'dayofweek', 'new_Recus']).rename(columns={'rolling_mean': 'Recus'})
