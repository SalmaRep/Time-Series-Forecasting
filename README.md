# Time-Series Forecasting  
## Modélisation de Séries Temporelles

Ce projet a pour objectif de modéliser et prédire l'évolution d'une variable métier à l'aide de techniques de machine learning, en particulier le modèle **XGBoost**. Il permet d’identifier les tendances, de détecter les comportements saisonniers et d’anticiper les volumes futurs, dans un cadre applicable à des cas industriels réels.

---

## Technologies utilisées

- Python
- XGBoost
- Pandas
- NumPy
- Matplotlib & Seaborn (visualisation)

---

## Fonctionnalités

- Prévisions sur des périodes définies à partir de séries temporelles.
- Analyse des tendances, variations saisonnières et anomalies.
- Développement de modèles prédictifs pour améliorer la prise de décision.
- Génération de tableaux de bord automatisés à partir des résultats de prévision.

---

## Spécificité du modèle

L’une des particularités de ce projet est qu'il permet d’entraîner **un modèle global de prédiction** pour plusieurs flux , sans nécessiter la construction d’un modèle distinct pour chaque flux. Cette approche permet :

- Une simplification de la gestion du processus de modélisation.
- Un gain de temps dans l’entraînement des modèles et une meilleure maintenance à long terme.
- Une plus grande scalabilité dans les environnements où de nouveaux flux peuvent apparaître.

Une fois le modèle global de prédiction créé, les prévisions sont **réparties entre les différents flux** à l’aide de **poids historiques** recalculés à chaque période (typiquement chaque mois). Ces poids sont basés sur la répartition historique des flux par **jour de la semaine**, en excluant les week-ends et jours fériés. Ils reflètent la contribution de chaque flux à la charge totale journalière observée récemment.

> **Important** : Les poids sont **toujours recalculés en fonction des derniers mois de données**, garantissant ainsi que la répartition des flux soit toujours mise à jour avec les données les plus récentes. Cela permet d’adapter la répartition aux évolutions récentes des flux tout en conservant une granularité pertinente dans les prévisions.

Cette méthode repose sur l’hypothèse de **stabilité temporelle** des répartitions des flux. Toute évolution majeure dans la structure des flux ou des comportements opérationnels peut nécessiter un recalibrage des poids, ce qui doit être vérifié régulièrement.

---

## Qualité des données et évaluation des performances

Pour garantir des prévisions fiables et cohérentes, il est essentiel de :

- Utiliser une base de données **propre et de qualité**, avec une couverture temporelle suffisante pour calculer des poids significatifs.
- Analyser régulièrement la **stabilité de la répartition des flux** afin de s’assurer que les poids calculés sont toujours représentatifs des tendances actuelles.
- Tester la performance du modèle pour chaque flux, même dans un cadre global. Des **métriques de précision** comme :
  - **MAPE (Mean Absolute Percentage Error)**
  - **RMSE (Root Mean Squared Error)**
  - **MAE (Mean Absolute Error)**

Ces métriques permettent d’évaluer la fiabilité des prévisions désagrégées et d’ajuster les modèles ou les poids si nécessaire.

---

## Adaptabilité du code

Le projet est conçu de manière modulaire, ce qui permet de l’adapter à divers cas d’usage :

- Il peut être utilisé pour **une seule série temporelle** (un seul flux) en désactivant la logique de répartition des poids.
- Le code est aussi facilement adaptable à d’autres **regroupements ou entités** comme des régions, des produits, ou des canaux de distribution.

La flexibilité du modèle permet de l’utiliser pour des prévisions centralisées ou pour des applications à plus grande échelle.

---

## Accès au code

Le code source de ce projet est actuellement **privé**.

Pour en faire la demande, veuillez me contacter par email :  
**atik.salma00@gmail.com**

Ou via une demande GitHub. L’accès est restreint aux utilisateurs autorisés.

---
