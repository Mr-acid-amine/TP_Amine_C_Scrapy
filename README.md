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
│   ├── items.py
│   ├── pipelines.py  # MongoDB
│   ├── settings.py
│   ├── spiders/
│   │   ├── kbo_spider.py         # Spider 1
│   │   ├── ejustice_spider.py    # Spider 2
│   │   └── nbb_spider.py         # Spider 3 (non fonctionnel)
├── numero_entreprises.csv       # Liste des numéros d’entreprise à scrapper
└── README.md
