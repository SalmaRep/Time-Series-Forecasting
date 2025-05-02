# -*- coding: utf-8 -*-
"""
Auteur : Salma ATIK
Description : Prédiction de séries temporelles sur des flux
"""
# === Librairies et Paramètres de Configuration ===

# Importation des bibliothèques
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby
import datetime as dt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import holidays

from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, IsolationForest

from statsmodels.graphics import tsaplots
import xgboost as xgb

#################################### Paramètres ###########################################

# Flux d'intérêt
flux_primaires = ["FLUX A", "FLUX B", "FLUX C", "FLUX D", "FLUX E"]

# Dates de début et de fin de la période à prédire
# ! # La date_debut correspond au jour suivant la dernière date présente dans les données disponibles
date_debut_str = "(04/09/2024)"
date_fin_str = "(15/10/2024)"

# Conversion des dates en objets datetime
date_debut = datetime.strptime(date_debut_str, "(%d/%m/%Y)")
date_fin = datetime.strptime(date_fin_str, "(%d/%m/%Y)")
annee_debut = date_debut.year
annee_fin = date_fin.year

# Nombre de jours à prévoir
nombre_jours = (date_fin - date_debut).days + 1
print(f"Nombre de jours à prédire : {nombre_jours}")

# Date de début de l'historique
date_deb_histo_str = "(01/01/2021)"
date_deb_histo = datetime.strptime(date_deb_histo_str, "(%d/%m/%Y)")
