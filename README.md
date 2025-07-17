# InfoWatchdog - Agent de Veille Environnementale

Agent automatique de collecte et de veille d'actualités environnementales depuis multiple sources (Reddit, RSS) avec stockage structuré dans Airtable.

## 🎯 Objectif

InfoWatchdog surveille automatiquement l'actualité environnementale en collectant des contenus récents depuis diverses sources et les stocke de manière structurée pour faciliter l'analyse et le suivi des tendances.

## 📖 Documentation

- **[Configuration Airtable](docs/airtable_setup.md)** - Guide complet pour configurer Airtable
- **[Structure du projet](docs/structure.md)** - Architecture et organisation des fichiers

## 🌱 Sources de Données

### Reddit
- **Subreddits surveillés** : `environment`, `climate`, `sustainability`, `renewableenergy`, `ClimateChange`, `solar`, `wind`
- **Collecte** : Posts les plus populaires et récents
- **Filtrage** : Pertinence environnementale automatique

### RSS Feeds
- **CleanTechnica** - Actualités cleantech et énergies renouvelables
- **TreeHugger** - Environnement et développement durable
- **GreenTech Media** - Technologies vertes
- **Yale Environment 360** - Analyses environnementales
- **Environmental Leader** - Business et environnement
- **Carbon Brief** - Changement climatique et énergie

## 📊 Format des Données

Chaque article collecté contient :
- **Titre** et **URL** source
- **Contenu/Résumé** (extrait)
- **Source** et **Auteur**
- **Date de publication** et **Date de collecte**
- **Tags/Mots-clés** automatiques
- **Métadonnées** spécifiques (score Reddit, catégories RSS, etc.)
- **Hash unique** pour éviter les doublons

## 🛠 Installation

### Prérequis
- Python 3.8+
- Compte Reddit (pour API)
- Compte Airtable

### 1. Cloner le projet
```bash
git clone https://github.com/yemal22/info-watchdog.git
cd info-watchdog
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration des APIs

#### Reddit API
1. Allez sur [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Créez une nouvelle application (type "script")
3. Notez le `client_id` et `client_secret`

#### Airtable
⚠️ **Important** : Les champs Airtable doivent être créés manuellement avant utilisation.

**Configuration rapide :**
1. Créez une base Airtable avec une table "Environmental_News"
2. Ajoutez les champs requis (voir [guide détaillé](docs/airtable_setup.md))
3. Récupérez votre API key et Base ID

**Champs obligatoires :**
- `Title` (Single line text)
- `URL` (URL) 
- `Source` (Single line text)
- `Content` (Long text)
- `Author` (Single line text)
- `Published_Date` (Date)
- `Collected_Date` (Date)
- `Collector` (Single line text)
- `Hash` (Single line text)
- `Tags` (Single line text)

**Champs optionnels (Reddit) :**
- `Reddit_Score` (Number)
- `Reddit_Comments` (Number)
- `Subreddit` (Single line text)

➡️ **[Guide complet de configuration Airtable](docs/airtable_setup.md)**

### 4. Variables d'environnement
```bash
cp .env.example .env
```

Éditez le fichier `.env` :
```bash
# Reddit API
REDDIT_CLIENT_ID=votre_client_id
REDDIT_CLIENT_SECRET=votre_client_secret
REDDIT_USER_AGENT=InfoWatchdog/1.0

# Airtable
AIRTABLE_API_KEY=votre_api_key
AIRTABLE_BASE_ID=votre_base_id
AIRTABLE_TABLE_NAME=Environmental_News
```

## 🚀 Utilisation

### Test de configuration
```bash
python run.py --test-only
```

### Collecte unique
```bash
python run.py
```

### Afficher les statistiques
```bash
python run.py --stats
```

### Configuration personnalisée
```bash
python run.py --config config/custom.yaml
```

## ⚙️ Configuration

Le fichier `config/config.yml` permet de personnaliser :

### Collecteurs Reddit
```yaml
collectors:
  reddit:
    enabled: true
    subreddits: ["environment", "climate", "sustainability"]
    limit: 50
    sort_type: "hot"  # hot, new, top, rising
```

### Flux RSS
```yaml
collectors:
  rss:
    enabled: true
    feeds:
      - url: "https://example.com/feed/"
        name: "Example News"
```

### Planification
```yaml
schedule:
  interval: 3600  # Collecte toutes les heures
```

## 🔄 Automatisation

### Avec cron (Linux/macOS)
```bash
# Collecte toutes les heures
0 * * * * cd /path/to/info-watchdog && python run.py

# Logs
0 * * * * cd /path/to/info-watchdog && python run.py >> logs/cron.log 2>&1
```

### Avec Task Scheduler (Windows)
1. Ouvrez le Planificateur de tâches
2. Créez une tâche de base
3. Déclencheur : Quotidien/Horaire
4. Action : `python.exe /path/to/InfoWatchdog/run.py`

## 📋 Structure du Projet

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

## 🎛 Choix Techniques

### Architecture Modulaire
- **Collecteurs** : Facilement extensibles pour nouvelles sources
- **Stockage** : Interface abstraite (Airtable, Google Sheets, etc.)
- **Configuration** : YAML pour simplicité et lisibilité

### Gestion des Doublons
- Hash MD5 basé sur titre + URL
- Cache en mémoire pour performances
- Vérification avant stockage

### Filtrage Intelligent
- Mots-clés environnementaux prédéfinis
- Exclusion des contenus non-pertinents
- Métadonnées spécifiques par source

### Robustesse
- Gestion d'erreur par collecteur
- Logs détaillés
- Tests de connexion
- Traitement par lots

## 📈 Métriques et Monitoring

Le système fournit :
- Nombre d'articles collectés par cycle
- Répartition par source
- Taux de réussite du stockage
- Durée des cycles de collecte
- Statistiques de doublons

## 🔧 Développement

### Ajouter un nouveau collecteur
1. Hériter de `BaseCollector`
2. Implémenter la méthode `collect()`
3. Ajouter la configuration dans `config.yml`
4. Enregistrer dans `main.py`

### Ajouter un nouveau système de stockage
1. Hériter de `BaseStorage`
2. Implémenter les méthodes abstraites
3. Ajouter la configuration

## 📝 Logs

Les logs sont sauvegardés dans `infowatchdog.log` avec :
- Horodatage
- Niveau (INFO, ERROR, WARNING)
- Source (collector, storage)
- Message détaillé

## 🐛 Dépannage

### Erreur Reddit API
- Vérifiez vos credentials dans `.env`
- Respectez les limites de taux Reddit

### Erreur Airtable
- Vérifiez votre API key et Base ID
- Assurez-vous que la table a tous les champs requis

### Aucun article collecté
- Vérifiez la connectivité internet
- Testez avec `--test-only`
- Consultez les logs

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add amazing feature'`)
4. Push sur la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request