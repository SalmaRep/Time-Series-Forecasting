# ### Modélisation du modèle de prédiction des réceptions ###

# 1. Réinitialiser l'index du DataFrame et renommer la colonne 'index' en 'date'
df = df.reset_index()
df = df.rename(columns={'index': 'date'})

# 2. Créer des variables explicatives basées sur la date
df['dayofweek'] = df['date'].dt.dayofweek       # Jour de la semaine (0 = lundi, 6 = dimanche)
df['dayofmonth'] = df['date'].dt.day            # Jour du mois
df['dayofyear'] = df['date'].dt.dayofyear       # Jour de l'année
df['month'] = df['date'].dt.month               # Mois
df['quarter'] = df['date'].dt.quarter           # Trimestre
df['year'] = df['date'].dt.year                 # Année

# 3. Optionnel : Ajouter un indicateur pour les jours fériés
# fr_holidays = holidays.France(years=df['date'].dt.year.unique())
# df['is_holidays'] = df['date'].isin(fr_holidays.keys()).astype(int)

# 4. Filtrer les données pour exclure les samedis et dimanches
df = df[df['dayofweek'] < 5]  # Retirer les week-ends

# 5. Ajouter des décalages (lags) sur la variable cible (Recus) avec un intervalle de 6 pas
for i in range(1, 6):
    df[f"lag{i}"] = df['Recus'].shift(i)

# 6. Supprimer les lignes contenant des valeurs manquantes après l'ajout des décalages
df = df.dropna()

# 7. Variables catégorielles à encoder via One-Hot Encoding
categorical_vars = ['dayofweek']  # Jour de la semaine à encoder
df = pd.get_dummies(df, columns=categorical_vars, drop_first=False)

# 8. Diviser les données en ensembles d'entraînement et de test
train_df = df.copy()

# Variables explicatives (features) : Sélectionner les colonnes pertinentes
train_X = train_df[['quarter', 'dayofmonth', 'dayofyear', 'month', 
                    'dayofweek_0', 'dayofweek_1', 'dayofweek_2', 
                    'dayofweek_4', 'lag1', 'lag2', 'lag3', 'lag4', 'lag5']]

# Variable cible : La colonne 'Recus' (réceptions)
train_y = train_df['Recus']

# 9. Définir les hyperparamètres à optimiser pour XGBoost
param_grid = {
    'max_depth': [3, 5, 7],               # Profondeur maximale des arbres
    'learning_rate': [0.1, 0.01],         # Taux d'apprentissage
    'n_estimators': [100, 200],           # Nombre d'arbres
    'subsample': [0.8, 1.0],              # Fraction d'échantillons pour chaque arbre
    'colsample_bytree': [0.8, 1.0]        # Fraction de colonnes utilisées pour chaque arbre
}

# 10. Créer un modèle XGBoost
xgb_model = xgb.XGBRegressor()

# 11. Utiliser GridSearchCV pour rechercher les meilleurs paramètres avec validation croisée
tscv = TimeSeriesSplit(n_splits=3)  # Validation croisée avec division chronologique des données

grid_search = GridSearchCV(xgb_model, param_grid, cv=tscv)
grid_search.fit(train_X, train_y)

# 12. Afficher les meilleurs paramètres trouvés
print("Meilleurs paramètres : ", grid_search.best_params_)

# 13. Utiliser les meilleurs paramètres pour entraîner le modèle final
best_params = grid_search.best_params_
model = xgb.XGBRegressor(
    colsample_bytree=best_params['colsample_bytree'],
    learning_rate=best_params['learning_rate'],
    max_depth=best_params['max_depth'],
    n_estimators=best_params['n_estimators'],
    subsample=best_params['subsample']
)

# Entraîner le modèle avec les données d'entraînement
model.fit(train_X, train_y)

# 14. Optionnel : Affichage de l'importance des variables pour l'interprétation du modèle
# importance = pd.DataFrame({
#     'Feature': train_X.columns,
#     'Importance': model.feature_importances_
# })

# Trier l'importance des variables par ordre décroissant
# importance = importance.sort_values('Importance', ascending=False)
# Visualisation de l'importance des variables (optionnel)
# fig, ax = plt.subplots()
# ax.bar(importance['Feature'], importance['Importance'])
# ax.set_title("Importance des variables")
# ax.set_xlabel("Variables")
# ax.set_ylabel("Importance")
# plt.xticks(rotation=90)
# plt.show()
