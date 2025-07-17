# Structure du projet InfoWatchdog

## Architecture des fichiers

```
info-watchdog/
├── src/
│   ├── main.py              # Gestionnaire principal
│   ├── collectors/          # Collecteurs de données
│   │   ├── base_collector.py
│   │   ├── reddit_collector.py
│   │   └── rss_collector.py
│   ├── storage/             # Systèmes de stockage
│   │   ├── base_storage.py
│   │   └── airtable_storage.py
│   └── utils/               # Utilitaires
├── config/
│   ├── config.yml           # Configuration principale
│   └── keywords.json        # Mots-clés environnementaux
├── requirements.txt         # Dépendances Python
├── run.py                   # Script de lancement
├── .env.example            # Template variables d'environnement
└── README.md               # Documentation
```

## Collecteurs de données

### Reddit Collector
- **Fonctionnalité** : Collecte des posts depuis les subreddits environnementaux
- **Configuration** : Client ID, Client Secret, User Agent Reddit
- **Données récupérées** : Titre, contenu, score, commentaires, auteur

### RSS Collector
- **Fonctionnalité** : Collecte depuis les flux RSS de sites d'actualités environnementales
- **Configuration** : Liste des URLs de flux RSS
- **Données récupérées** : Articles avec métadonnées complètes

## Système de stockage

### Airtable Storage
- **Fonctionnalité** : Stockage structuré dans une base Airtable
- **Avantages** : Interface utilisateur, collaboratif, API robuste
- **Configuration** : API Key, Base ID, Table Name

## Configuration des champs

Pour le bon fonctionnement du système, les champs doivent être créés manuellement dans Airtable avant l'utilisation de l'API.
