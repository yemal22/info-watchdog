# Sources de Données : Reddit et RSS

InfoWatchdog utilise deux types de sources principales pour collecter l'actualité environnementale : **Reddit** et les **flux RSS**. Ce document explique les raisons de ces choix et leurs spécificités.

---

## 🔴 Reddit : La communauté environnementale

### Pourquoi Reddit ?

Reddit représente l'une des plus grandes communautés de discussion en ligne avec des communautés (subreddits) dédiées spécifiquement aux enjeux environnementaux. Cette plateforme offre plusieurs avantages uniques :

#### 📈 **Contenu démocratique et filtré**
- **Système de votes** : Les articles les plus pertinents remontent naturellement
- **Modération communautaire** : Qualité du contenu assurée par les utilisateurs
- **Discussions riches** : Commentaires et débats approfondis sur chaque sujet

#### 🌍 **Couverture thématique spécialisée**
- **Subreddits ciblés** : Communautés dédiées à des aspects spécifiques
- **Actualité mondiale** : Sources internationales et locales
- **Diversité des perspectives** : Opinions variées et débats constructifs

#### ⚡ **Réactivité et fraîcheur**
- **Temps réel** : Actualités publiées et discutées immédiatement
- **Tendances émergentes** : Détection précoce des sujets d'intérêt
- **Signal/bruit optimisé** : Algorithme de pertinence via les votes

### Subreddits surveillés

InfoWatchdog monitore les communautés les plus actives et pertinentes :

| Subreddit | Focus | Abonnés | Activité |
|-----------|-------|---------|----------|
| `r/environment` | Actualité environnementale générale | 1M+ | 🔥🔥🔥 |
| `r/climate` | Changement climatique | 200K+ | 🔥🔥🔥 |
| `r/sustainability` | Développement durable | 300K+ | 🔥🔥 |
| `r/renewableenergy` | Énergies renouvelables | 150K+ | 🔥🔥 |
| `r/ClimateChange` | Science du climat | 400K+ | 🔥🔥🔥 |
| `r/solar` | Énergie solaire | 200K+ | 🔥🔥 |
| `r/wind` | Énergie éolienne | 50K+ | 🔥 |

### Métadonnées collectées

Pour chaque post Reddit, InfoWatchdog capture :

```json
{
  "title": "Titre du post",
  "url": "URL de l'article source",
  "source": "Nom du site web",
  "content": "Extrait ou description",
  "author": "Utilisateur Reddit",
  "reddit_score": 1234,
  "reddit_comments": 56,
  "subreddit": "environment",
  "published_date": "2025-07-18T10:30:00",
  "collected_date": "2025-07-18T11:00:00"
}
```

### Filtrage intelligent

- **Scores minimums** : Seuls les posts avec un score significatif sont collectés
- **Mots-clés environnementaux** : Filtrage basé sur le vocabulaire spécialisé
- **Exclusions automatiques** : Élimination des memes, discussions non-constructives
- **Déduplication** : Évite les reposts et contenus similaires

---

## 🟠 RSS : Sources officielles et médias

### Pourquoi les flux RSS ?

Les flux RSS complètent parfaitement Reddit en apportant des sources officielles, journalistiques et institutionnelles. Ils offrent :

#### 📰 **Contenu éditorial professionnel**
- **Journalisme spécialisé** : Articles rédigés par des experts
- **Sources officielles** : Organismes gouvernementaux et ONG
- **Fact-checking** : Information vérifiée et sourcée

#### 🎯 **Couverture exhaustive**
- **Médias spécialisés** : Publications dédiées à l'environnement
- **Actualité économique** : Impact business et financier
- **Recherche scientifique** : Publications académiques et études

#### ⏰ **Publication structurée**
- **Calendrier éditorial** : Contenu planifié et régulier
- **Formats standardisés** : Métadonnées riches et structurées
- **Archives organisées** : Historique complet et accessible

### Sources RSS surveillées

InfoWatchdog collecte depuis des médias reconnus :

#### 🌿 **Médias environnementaux spécialisés**

**CleanTechnica**
- 🔗 Focus : Technologies propres et énergies renouvelables
- 📊 Volume : ~15 articles/jour
- 🎯 Public : Professionnels et passionnés de cleantech

**TreeHugger**
- 🔗 Focus : Écologie, mode de vie durable, innovation verte
- 📊 Volume : ~10 articles/jour
- 🎯 Public : Grand public éco-conscient

**GreenTech Media**
- 🔗 Focus : Marché des technologies vertes, analyses financières
- 📊 Volume : ~8 articles/jour
- 🎯 Public : Investisseurs et professionnels de l'énergie

#### 🎓 **Sources académiques et institutionnelles**

**Yale Environment 360**
- 🔗 Focus : Analyses approfondies, recherche environnementale
- 📊 Volume : ~5 articles/jour
- 🎯 Public : Chercheurs, décideurs politiques

**Carbon Brief**
- 🔗 Focus : Science du climat, politiques énergétiques
- 📊 Volume : ~3 articles/jour
- 🎯 Public : Scientifiques, journalistes spécialisés

**Environmental Leader**
- 🔗 Focus : Stratégies d'entreprises, RSE, développement durable
- 📊 Volume : ~6 articles/jour
- 🎯 Public : Dirigeants d'entreprise, consultants

### Configuration des flux

```yaml
rss:
  feeds:
    - url: "https://cleantechnica.com/feed/"
      name: "CleanTechnica"
      category: "cleantech"
      language: "en"
      
    - url: "https://www.treehugger.com/feeds/all"
      name: "TreeHugger"
      category: "lifestyle"
      language: "en"
      
    - url: "https://www.greentechmedia.com/rss/all"
      name: "GreenTech Media"
      category: "business"
      language: "en"
```

### Métadonnées RSS collectées

```json
{
  "title": "Titre de l'article",
  "url": "URL complète",
  "source": "Nom du média",
  "content": "Résumé ou contenu complet",
  "author": "Journaliste ou rédacteur",
  "published_date": "2025-07-18T09:00:00",
  "collected_date": "2025-07-18T09:15:00",
  "category": "cleantech",
  "tags": ["solar", "renewable", "policy"]
}
```

---

## ⚖️ Complémentarité des sources

### Reddit + RSS = Vision complète

| Aspect | Reddit | RSS | Synergie |
|--------|--------|-----|----------|
| **Fraîcheur** | ⚡ Temps réel | 📅 Planifié | Couverture continue |
| **Qualité** | 👥 Communauté | 👨‍💼 Éditorial | Double validation |
| **Diversité** | 🌍 Mondiale | 🏢 Institutionnelle | Perspectives multiples |
| **Profondeur** | 💬 Discussions | 📄 Articles longs | Analyse complète |

### Avantages de cette approche

#### 🎯 **Détection précoce**
- Reddit identifie les tendances émergentes
- RSS confirme avec des analyses approfondies

#### 🔍 **Validation croisée**
- Sujets populaires sur Reddit = intérêt réel
- Couverture RSS = importance confirmée

#### 📊 **Richesse des données**
- Métriques d'engagement (Reddit scores)
- Métadonnées structurées (RSS)

#### 🌐 **Couverture géographique**
- Reddit : Perspectives internationales diverses
- RSS : Sources locales et spécialisées

---

## 🔧 Implémentation technique

### Collecte Reddit

```python
def collect_reddit_posts(subreddit, limit=50):
    """Collecte les posts populaires d'un subreddit"""
    posts = reddit.subreddit(subreddit).hot(limit=limit)
    
    for post in posts:
        if post.score >= MIN_SCORE:
            article = {
                'title': post.title,
                'url': post.url,
                'reddit_score': post.score,
                'reddit_comments': post.num_comments,
                'subreddit': subreddit
            }
            yield article
```

### Collecte RSS

```python
def collect_rss_feed(feed_url):
    """Parse un flux RSS et extrait les articles"""
    feed = feedparser.parse(feed_url)
    
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'url': entry.link,
            'content': entry.summary,
            'published_date': entry.published_parsed
        }
        yield article
```

### Déduplication inter-sources

```python
def generate_article_hash(title, url):
    """Génère un hash unique pour éviter les doublons"""
    content = f"{title.lower().strip()}{url.strip()}"
    return hashlib.md5(content.encode()).hexdigest()
```

---

## 📈 Métriques et performance

### Volumes typiques (par heure)
- **Reddit** : 20-50 nouveaux posts (selon activité)
- **RSS** : 10-30 nouveaux articles
- **Total** : 30-80 articles collectés
- **Après filtrage** : 15-40 articles stockés

### Taux de qualité
- **Reddit** : ~60% d'articles pertinents (après filtrage par score)
- **RSS** : ~85% d'articles pertinents (sources pré-qualifiées)
- **Global** : ~70% de contenu de qualité stocké

Cette approche bicéphale garantit une couverture exhaustive et équilibrée de l'actualité environnementale, alliant réactivité communautaire et expertise journalistique.