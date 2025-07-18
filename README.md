# InfoWatchdog - Agent de Veille Environnementale

<div align="center">
  <p>
  <a href="https://github.com/yemal22/info-watchdog">
    <img src="https://img.shields.io/badge/status-active-green.svg" alt="Status">
  </a>
  <a href="https://github.com/yemal22/info-watchdog/releases">
    <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style">
  </a>
  <img src="https://img.shields.io/badge/platform-linux%20|%20macos%20|%20windows-lightgrey.svg" alt="Platform">
  <a href="https://www.reddit.com/dev/api/">
    <img src="https://img.shields.io/badge/API-Reddit-FF4500.svg" alt="Reddit API">
  </a>
  <img src="https://img.shields.io/badge/Feeds-RSS-FFA500.svg" alt="RSS Feeds">
  <a href="https://airtable.com/">
    <img src="https://img.shields.io/badge/Database-Airtable-18BFFF.svg" alt="Airtable">
  </a>
  <img src="https://img.shields.io/badge/automation-cron%20|%20systemd%20|%20windows-green.svg" alt="Automation">
  <img src="https://img.shields.io/badge/focus-environmental%20news-32CD32.svg" alt="Environmental Focus">
  <img src="https://img.shields.io/badge/collection-automated-brightgreen.svg" alt="Automated Collection">
  <img src="https://img.shields.io/badge/duplicates-protected-orange.svg" alt="Duplicate Guard">
  <img src="https://img.shields.io/badge/monitoring-24%2F7-red.svg" alt="24/7 Monitoring">
  <img src="https://img.shields.io/badge/sources-reddit%20%2B%20rss-blue.svg" alt="Multi Source">
  <a href="https://streamlit.io/">
    <img src="https://img.shields.io/badge/dashboard-streamlit-FF4B4B.svg" alt="Streamlit Dashboard">
  </a>
</p>
  
  <br><br>
  <img src="assets/logo-static.svg" alt="InfoWatchdog Logo" width="400"/>
</div>

**InfoWatchdog** est un agent automatique de collecte et de veille d'actualités environnementales depuis multiples sources (Reddit, RSS) avec stockage structuré dans Airtable.

---

## 🎯 Objectif

InfoWatchdog surveille automatiquement l'actualité environnementale en collectant des contenus récents depuis diverses sources et les stocke de manière structurée pour faciliter l'analyse et le suivi des tendances.

## 📊 Dashboard Temps Réel

InfoWatchdog inclut un **dashboard Streamlit interactif** pour surveiller vos données en temps réel !

### 🚀 Lancement rapide du dashboard
```bash
# Méthode simple
python run_dashboard.py

# Ou directement avec Streamlit
streamlit run dashboard_streamlit.py
```

### 🎨 Fonctionnalités du dashboard

#### 📈 Visualisations en temps réel
- **Métriques principales** : Articles collectés, répartition par source, activité récente
- **Graphiques temporels** : Evolution quotidienne des collectes
- **Graphiques en secteurs** : Répartition par sources RSS et subreddits Reddit
- **Heatmap d'activité** : Patterns de collecte par heure et jour de la semaine

#### 🔍 Analyse des données
- **Articles récents** : Liste des dernières collectes avec scores Reddit
- **Sources tendances** : Top sources sur 7 jours
- **Top subreddits** : Subreddits les plus actifs
- **Statistiques détaillées** : Performance par collecteur, scores moyens

#### ⚙️ Contrôles interactifs
- **Filtrage par période** : 7j, 30j, 90j ou toutes les données
- **Actualisation automatique** : Mise à jour toutes les 30 secondes
- **Cache intelligent** : Données mises en cache 5 minutes pour de meilleures performances
- **Interface responsive** : Compatible mobile et desktop

#### 🎯 Accès direct
- **URL locale** : http://localhost:8501
- **Thème InfoWatchdog** : Design cohérent avec logos ASCII
- **Sidebar de contrôle** : Paramètres et informations de statut

### 📦 Installation dashboard
```bash
# Installation des dépendances
pip install streamlit plotly pandas numpy

# Ou mise à jour complète
pip install -r requirements.txt
```

### 🖥️ Captures d'écran
Le dashboard affiche :
- 🐕‍🦺 **En-tête stylisé** avec logo ASCII InfoWatchdog
- 📊 **Métriques temps réel** : Total articles, Reddit vs RSS, sources actives
- 📈 **Graphiques interactifs** : Plotly pour visualisations dynamiques
- 📰 **Feed articles récents** : Liens directs, scores Reddit, métadonnées
- 🔥 **Analyse tendances** : Sources populaires, subreddits actifs

---

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

## 🕐 Automatisation et Planification

InfoWatchdog inclut des scripts pour configurer automatiquement la collecte périodique selon votre système d'exploitation.

### Script de configuration automatique

```bash
python setup_scheduler.py
```

**Fonctionnalités :**
- ✅ Détection automatique du système d'exploitation
- ✅ Configuration de tâches cron (Linux/macOS)
- ✅ Configuration de services systemd (Linux)
- ✅ Configuration du Planificateur de tâches (Windows)
- ✅ Détection automatique de l'environnement virtuel Python
- ✅ Génération automatique des chemins et logs

### Vérification et gestion

```bash
python check_scheduler.py
```

**Fonctionnalités :**
- 🔍 Vérification des tâches planifiées existantes
- 📄 Consultation des logs d'exécution
- 🧪 Test d'exécution manuelle
- 🗑️ Suppression des tâches planifiées

### Intervalles de collecte disponibles

- **Hourly** : Toutes les heures (recommandé)
- **Daily** : Une fois par jour (8h du matin)
- **Twice daily** : Deux fois par jour (8h et 20h)
- **Every 6h** : Toutes les 6 heures

### Configuration manuelle alternative

#### Linux/macOS (cron)
```bash
# Édite le crontab
crontab -e

# Ajoute cette ligne pour une collecte horaire
0 * * * * cd /path/to/InfoWatchdog && python run.py >> logs/cron.log 2>&1
```

#### Linux (systemd)
Créez les fichiers de service avec `setup_scheduler.py` ou manuellement :

```bash
sudo systemctl enable infowatchdog.timer
sudo systemctl start infowatchdog.timer
```

#### Windows (PowerShell)
Le script génère automatiquement un fichier `setup_windows_task.ps1` :

```powershell
# Exécuter en tant qu'Administrateur
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_windows_task.ps1
```

### Logs et monitoring

Les logs d'exécution automatique sont sauvegardés dans :
- `logs/cron.log` - Logs des exécutions planifiées
- `logs/wrapper.log` - Logs du script wrapper
- `logs/infowatchdog.log` - Logs détaillés de l'application

```bash
# Voir les logs récents
tail -f logs/cron.log

# Vérifier le statut
python check_scheduler.py
```

## 📋 Structure du Projet

```
InfoWatchdog/
├── 📄 run.py                      # Script de lancement principal
├── 📄 run_dashboard.py            # Lanceur du dashboard Streamlit
├── 📊 dashboard_streamlit.py      # Dashboard interactif Streamlit
├── 📄 setup_scheduler.py          # Configuration automatique des tâches
├── 📄 check_scheduler.py          # Vérification et gestion des tâches
├── 🧪 test_airtable.py           # Tests de connexion Airtable
├── 📄 requirements.txt            # Dépendances Python
├── 📄 LICENSE                     # Licence MIT
├── 📄 README.md                   # Documentation principale
├── 📄 .env.example               # Template variables d'environnement
├── 📄 infowatchdog.log           # Logs principaux
│
├── 📁 src/                       # Code source principal
│   ├── 📄 __init__.py
│   ├── 📄 main.py                # Gestionnaire principal
│   │
│   ├── 📁 collectors/            # Collecteurs de données
│   │   ├── 📄 __init__.py
│   │   ├── 📄 base_collector.py  # Classe abstraite collecteur
│   │   ├── 📄 reddit_collector.py # Collecteur Reddit
│   │   └── 📄 rss_collector.py   # Collecteur RSS
│   │
│   ├── 📁 processors/            # Traitement des données
│   │   └── 📄 __init__.py
│   │
│   ├── 📁 storage/               # Systèmes de stockage
│   │   ├── 📄 __init__.py
│   │   ├── 📄 base_storage.py    # Interface abstraite stockage
│   │   └── 📄 airtable_storage.py # Stockage Airtable
│   │
│   └── 📁 utils/                 # Utilitaires
│       ├── 📄 __init__.py
│       └── 📄 logo.py            # Générateur de logos ASCII
│
├── 📁 config/                    # Configuration
│   ├── 📄 config.yml             # Configuration principale
│   └── 📄 keywords.json          # Mots-clés environnementaux
│
├── 📁 docs/                      # Documentation
│   ├── 📄 airtable_setup.md      # Guide configuration Airtable
│   ├── 📄 sources.md             # Documentation Reddit & RSS
│   └── 📄 structure.md           # Architecture du projet
│
├── 📁 assets/                    # Ressources
│   ├── 🖼️ logo.svg              # Logo animé InfoWatchdog
│   └── 🖼️ logo-static.svg       # Logo statique
│
└── 📁 logs/                      # Journaux d'exécution
    └── 📄 cron.log               # Logs des tâches planifiées
```

### 🏗️ Architecture modulaire

#### 🔧 **Scripts principaux**
- `run.py` : Point d'entrée principal pour collecte
- `run_dashboard.py` : Lancement automatique du dashboard
- `dashboard_streamlit.py` : Interface web interactive
- `setup_scheduler.py` : Configuration automatique des tâches
- `check_scheduler.py` : Monitoring et gestion

#### 📊 **Code source (`src/`)**
- **Collecteurs** : Modules spécialisés par source (Reddit, RSS)
- **Stockage** : Interface abstraite extensible (Airtable, futur Google Sheets)
- **Processors** : Traitement et transformation des données
- **Utils** : Outils transversaux (logos, helpers)

#### ⚙️ **Configuration (`config/`)**
- `config.yml` : Paramètres principaux (subreddits, flux RSS, intervalles)
- `keywords.json` : Dictionnaire de mots-clés environnementaux

#### 📚 **Documentation (`docs/`)**
- `airtable_setup.md` : Guide détaillé de configuration Airtable
- `sources.md` : Explications Reddit & RSS, justifications techniques
- `structure.md` : Architecture détaillée du système

#### 🎨 **Assets (`assets/`)**
- Logos SVG pour interface et documentation
- Ressources graphiques du projet

#### 📝 **Logs (`logs/`)**
- `cron.log` : Logs des exécutions automatiques
- `infowatchdog.log` : Logs détaillés de l'application

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