# 📊 Projet Scrapy - Extraction d’informations sur les entreprises belges

## 📝 Description

Ce projet Scrapy extrait des informations de trois sources publiques belges :

* **KBO** : Informations générales sur les entreprises.
* **eJustice** : Publications légales des entreprises.
* **NBB** : \[spider non terminé].

Les données sont stockées dans une base MongoDB Atlas.

## 🕸️ Structure du projet

```bash
scrapy_kbo_tp/
├── scrapy_kbo_tp/
│   ├── middlewares.py
│   ├── utils.py
│   ├── items.py
│   ├── pipelines.py  # MongoDB
│   ├── settings.py
│   ├── enterprises.csv 
│   ├── spiders/
│   │   ├── kbo_spider.py         # Spider 1
│   │   ├── ejustice_spider.py    # Spider 2
│   │   └── nbb_spider.py         # Spider 3 (non fonctionnel)
└── README.md
```
## ✅ Fonctionnalités

- **KBO Spider** :
  - Scrape les informations générales des entreprises : nom, statut, forme juridique, date de début, adresse du siège, etc.
  - Récupère également des informations dynamiques sur les entreprises comme les "qualités".
  - Données stockées dans la collection `kbo_spider` de MongoDB.

- **eJustice Spider** :
  - Récupère les publications légales des entreprises en français uniquement (titre, adresse, numéro BCE, type, date, lien PDF).
  - Données stockées dans la collection `ejustice_spider` de MongoDB.

- **NBB Spider** :
  - Le développement n’a pas pu être finalisé.
  - Objectif : récupérer les comptes annuels des entreprises à partir de la Banque Nationale de Belgique.
