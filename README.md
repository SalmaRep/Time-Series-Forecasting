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

- **Prévisions sur des périodes définies** à partir de séries temporelles : le modèle permet à l'utilisateur de **choisir** la période qu'il souhaite prédire, offrant ainsi une flexibilité dans la planification des prévisions (ex. : prévisions sur les 30 prochains jours, sur les 3 prochains mois, etc.).
- Analyse des tendances, variations saisonnières et anomalies.
- Développement de modèles prédictifs pour améliorer la prise de décision.
- Génération de tableaux de bord automatisés à partir des résultats de prévision.

---

## Spécificité du modèle

Ce projet permet d’entraîner **un seul modèle global de prédiction** pour l’ensemble des flux. Cela permet de simplifier la gestion du processus de modélisation dans les environnements multi-flux.

### **Recalcul dynamique des poids**

Les prévisions obtenues par le modèle global sont **désagrégées** entre les différents flux en utilisant des **poids historiques recalculés à chaque période de prédiction**. Ces poids sont basés sur la répartition des flux observée **par jour de la semaine**, en excluant les week-ends et jours fériés. Chaque poids représente la contribution moyenne de chaque flux à la charge totale journalière. 

Il est essentiel de souligner que ces poids sont **calculés sur les derniers mois de données** et sont régulièrement **réajustés** pour tenir compte des évolutions récentes. Cela garantit que les prévisions restent adaptées aux tendances actuelles des flux.

### **Étude préalable de chaque flux**

Avant de recourir à un modèle global, il est primordial de procéder à une **analyse approfondie** de chaque flux de manière **indépendante**, en étudiant leur comportement sur plusieurs périodes (mois, semaines, jours). Cela permet de comprendre les dynamiques spécifiques de chaque flux et de vérifier que l’hypothèse de **stabilité** de leur répartition dans le temps est valide.

L’utilisation d’un modèle global pour répartir les prévisions entre les flux ne sera efficace que si cette structure de répartition entre les flux reste relativement stable au fil du temps. Il est donc crucial de vérifier que chaque flux présente des caractéristiques similaires en termes de saisonnalité et de comportement avant de procéder à l’entraînement du modèle global.

### **Réévaluation continue de la logique**

Même avec des poids recalculés régulièrement, il est important de **réévaluer périodiquement** la logique d’utilisation d’un modèle global. En fonction des résultats obtenus et des nouvelles données, il peut être nécessaire d’ajuster la méthode de répartition ou de passer à des modèles plus spécifiques si la structure des flux change de manière significative.

---

## Qualité des données et évaluation des performances

Pour garantir la fiabilité des prévisions, il est essentiel de :

- Utiliser une **base de données propre et complète** pour calculer des poids de manière robuste.
- Vérifier que la **répartition des flux** reste stable dans le temps avant d’appliquer les poids recalculés.
- Tester la performance du modèle pour chaque flux, même si le modèle est global. Des **métriques de précision** telles que :
  - **MAPE (Mean Absolute Percentage Error)**
  - **RMSE (Root Mean Squared Error)**
  - **MAE (Mean Absolute Error)**

Ces métriques permettent d’évaluer la qualité des prévisions désagrégées et de garantir que le modèle répond aux objectifs de performance.

---
## Adaptabilité du code

Le projet est conçu de manière modulaire et peut être facilement adapté à différents cas d’usage :

- Il peut être utilisé pour **une seule série temporelle** (un seul flux) en désactivant la logique de répartition des poids.
- Le code est également flexible pour s’adapter à des configurations plus complexes avec **plusieurs flux** ou entités (produits, canaux, régions, etc.).

Le modèle peut ainsi être utilisé pour des prévisions simples ou pour des pipelines de prévision à plus grande échelle, selon les besoins du projet.

---

## Étapes préliminaires : Tests statistiques à réaliser

Avant de procéder à la modélisation des séries temporelles, il est essentiel de vérifier les propriétés des données à l’aide de tests statistiques. Ces tests permettent de valider les hypothèses nécessaires à la modélisation.

### Stationnarité

La stationnarité est une condition clé pour de nombreux modèles de séries temporelles. Les tests suivants sont utilisés pour évaluer la stationnarité :

- **Test ADF (Augmented Dickey-Fuller)**  
  - **Hypothèse nulle (H0)** : La série est non stationnaire.  
  - Si la **p-value** < 0.05 → Rejet de H0 → La série est **stationnaire**.

- **Test KPSS (Kwiatkowski-Phillips-Schmidt-Shin)**  
  - **Hypothèse nulle (H0)** : La série est stationnaire.  
  - Si la **p-value** < 0.05 → Rejet de H0 → La série est **non stationnaire**.

> **Conseil** : Utiliser ces deux tests permet de confirmer la stationnarité de la série avec plus de fiabilité.

### Autocorrélation

Les tests suivants permettent d’analyser la dépendance temporelle dans les données :

- **ACF (Autocorrelation Function)** : Évalue la corrélation entre la série et ses lags (retards).
- **PACF (Partial Autocorrelation Function)** : Permet de visualiser les lags significatifs après ajustement.

Ces outils aident à identifier la présence de composantes saisonnières ou de dépendances à court terme.

### Normalité des résidus

Une fois le modèle entraîné, il est important de tester la normalité des résidus, car cela affecte la précision des prévisions et des intervalles de confiance. Pour ce faire, on peut utiliser le test suivant :

- **Kolmogorov-Smirnov (KS test)**  
  - Hypothèse nulle (H0) : les résidus suivent une distribution normale.  
  - Si la *p-value* < 0.05 → on rejette H0 → les résidus ne sont pas normalement distribués.

> Des résidus normalement distribués améliorent la fiabilité des intervalles de confiance pour les prévisions.

### Hétéroscédasticité

- L’hétéroscédasticité désigne une variance non constante des résidus dans le temps. Elle peut affecter la qualité des prévisions et fausser les intervalles de confiance, car les modèles supposent souvent une variance homogène (homoscédasticité).

Pour détecter l’hétéroscédasticité, on peut utiliser le test suivant :

- **Test de Breusch-Pagan**  
  - Il évalue si la variance des résidus dépend de certaines variables explicatives.  
  - Hypothèse nulle (H0) : les résidus sont homoscédastiques (variance constante).  
  - Si la *p-value* < 0.05 → on rejette H0 → il existe une hétéroscédasticité.

### Transformation des données en cas d’hétéroscédasticité

Si l'hétéroscédasticité est détectée, une transformation des données peut être nécessaire pour stabiliser la variance des erreurs. Parmi les solutions couramment utilisées, on peut envisager :

- **Transformation logarithmique** : Prendre le logarithme des valeurs de la série peut réduire l'impact des valeurs extrêmes et stabiliser la variance.

Cette transformation peut améliorer la performance du modèle en éliminant les effets de l’hétéroscédasticité et en rendant les données plus adaptées aux techniques de modélisation classiques.

---

