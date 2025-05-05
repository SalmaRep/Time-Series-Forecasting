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

- Prévisions sur des horizons définis à partir de séries temporelles.
- Analyse des tendances, variations saisonnières et anomalies.
- Développement de modèles prédictifs pour améliorer la prise de décision.
- Génération de tableaux de bord automatisés à partir des résultats de prévision.

---

## Spécificité du modèle

Une caractéristique centrale de ce projet est la possibilité d’entraîner **un seul modèle global** sur l’ensemble des flux étudiés, plutôt que de développer un modèle distinct pour chaque flux primaire. Cette approche permet :

- Une réduction significative du temps de développement et de la complexité technique.
- Une meilleure maintenabilité du pipeline de modélisation.
- Une évolutivité plus simple dans un environnement multi-flux.

Les prévisions globales obtenues sont ensuite **désagrégées entre les flux** à l’aide de **poids historiques**, calculés par **jour de la semaine**, en excluant les week-ends et les jours fériés. Ces poids reflètent la contribution moyenne de chaque flux à la charge totale journalière observée historiquement.

> Cette méthode repose sur une **hypothèse forte** : la **stabilité temporelle de la répartition des flux**. Toute modification structurelle dans le comportement des flux (réorganisation, nouvelles affectations, changements opérationnels) peut rendre cette méthode inappropriée sans recalibrage.

---

## Qualité des données et évaluation des performances

Pour assurer la robustesse des résultats, il est impératif de :

- Utiliser une base de données propre, cohérente et suffisamment longue pour calculer des poids fiables.
- Vérifier la stabilité de la structure de répartition des flux dans le temps à l’aide d’analyses exploratoires.
- Évaluer la qualité des prévisions désagrégées pour chaque flux à l’aide de métriques standards telles que :

  - MAPE (Mean Absolute Percentage Error)
  - RMSE (Root Mean Squared Error)
  - MAE (Mean Absolute Error)

Ces analyses permettent de valider la pertinence du modèle global ainsi que la justesse de la désagrégation.

---

## Adaptabilité du code

Le code est conçu de manière modulaire pour s’adapter à différents cas d’usage. Il peut être utilisé :

- Pour un seul flux (série temporelle unique), en désactivant simplement la logique de pondération.
- Pour plusieurs entités (flux, canaux, produits, régions…), en adaptant la logique de regroupement.
- Dans des environnements métiers où la structure des flux est stable et prévisible.

Cette flexibilité rend le projet facilement réutilisable dans des contextes variés, tant pour des analyses ponctuelles que pour des pipelines de prévision en production.

---

## Accès au code

Le code source de ce projet est actuellement privé.

Pour en faire la demande, veuillez me contacter par email :  
**atik.salma00@gmail.com**

ou via une demande GitHub. L’accès est restreint aux utilisateurs autorisés.

---
