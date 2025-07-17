# Configuration Airtable pour InfoWatchdog

## Vue d'ensemble

InfoWatchdog utilise Airtable comme système de stockage principal pour les articles environnementaux collectés. **Important** : L'API Airtable ne peut pas créer automatiquement les champs - ils doivent être configurés manuellement depuis l'interface web d'Airtable.

## Prérequis

1. Compte Airtable (gratuit ou payant)
2. Clé API Airtable
3. Base Airtable configurée avec la structure de champs requise

## Configuration des champs requis

### Étapes de configuration

1. **Créer une nouvelle base** ou utiliser une base existante sur airtable.com
2. **Créer une table** nommée `Environmental_News` (ou le nom défini dans `AIRTABLE_TABLE_NAME`)
3. **Ajouter manuellement chaque champ** avec le type spécifié ci-dessous

### Structure des champs obligatoires

| Nom du champ | Type Airtable | Description | Exemple |
|--------------|---------------|-------------|---------|
| `Title` | Single line text | Titre de l'article | "Climate Change Impacts..." |
| `URL` | URL | Lien vers l'article | https://example.com/article |
| `Source` | Single line text | Source de l'article | "r/environment", "CleanTechnica" |
| `Content` | Long text | Contenu/résumé de l'article | "Article content here..." |
| `Author` | Single line text | Auteur de l'article | "John Doe" |
| `Published_Date` | Date | Date de publication | 2025-01-15 |
| `Collected_Date` | Date | Date de collecte par le système | 2025-01-15 |
| `Collector` | Single line text | Type de collecteur utilisé | "reddit", "rss" |
| `Hash` | Single line text | Identifiant unique (évite doublons) | "a1b2c3d4e5f6..." |
| `Tags` | Single line text | Mots-clés séparés par virgules | "climate, renewable, solar" |

### Champs optionnels (spécifiques Reddit)

| Nom du champ | Type Airtable | Description |
|--------------|---------------|-------------|
| `Reddit_Score` | Number | Score du post Reddit |
| `Reddit_Comments` | Number | Nombre de commentaires |
| `Subreddit` | Single line text | Nom du subreddit source |

### Champs optionnels (spécifiques RSS)

| Nom du champ | Type Airtable | Description |
|--------------|---------------|-------------|
| `Feed_URL` | URL | URL du flux RSS source |

## Configuration de l'API

### 1. Récupérer la clé API

1. Connectez-vous à votre compte Airtable
2. Allez dans **Account** → **Developer Hub** → **Personal Access Tokens**
3. Créez un nouveau token avec les permissions :
   - `data.records:read`
   - `data.records:write`
   - `schema.bases:read`

### 2. Récupérer l'ID de la base

1. Ouvrez votre base Airtable
2. L'ID de la base se trouve dans l'URL : `https://airtable.com/appXXXXXXXXXXXXXX/...`
3. Copiez la partie `appXXXXXXXXXXXXXX`

### 3. Configuration des variables d'environnement

Ajoutez ces variables dans votre fichier `.env` :

```env
# Configuration Airtable
AIRTABLE_API_KEY=your_api_key_here
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_TABLE_NAME=Environmental_News
```

## Format des données

### Exemple d'enregistrement dans Airtable

```json
{
  "Title": "Solar Energy Breakthrough in 2025",
  "URL": "https://cleantechnica.com/solar-breakthrough-2025",
  "Source": "CleanTechnica",
  "Content": "Scientists have developed a new solar panel technology...",
  "Author": "Clean Energy Team",
  "Published_Date": "2025-01-15",
  "Collected_Date": "2025-01-15",
  "Collector": "rss",
  "Hash": "a1b2c3d4e5f67890abcdef1234567890",
  "Tags": "solar, energy, breakthrough, technology",
  "Reddit_Score": null,
  "Reddit_Comments": null,
  "Subreddit": null
}
```

## Limitations importantes

### Ce que l'API peut faire
- ✅ Lire les données existantes
- ✅ Créer de nouveaux enregistrements
- ✅ Modifier des enregistrements existants
- ✅ Supprimer des enregistrements

### Ce que l'API ne peut PAS faire
- ❌ Créer automatiquement des champs
- ❌ Modifier la structure de la table
- ❌ Changer les types de champs

## Validation de la configuration

### Script de test

Utilisez le script `test_airtable.py` pour vérifier votre configuration :

```bash
python test_airtable.py
```

### Vérifications manuelles

1. **Test de connexion** : Le système peut-il se connecter à votre base ?
2. **Test d'insertion** : Un enregistrement test peut-il être créé ?
3. **Vérification des champs** : Tous les champs requis existent-ils ?

## Dépannage courant

### Erreur "Unknown field name"
- **Cause** : Le champ n'existe pas dans votre table Airtable
- **Solution** : Créer manuellement le champ manquant dans l'interface Airtable

### Erreur "Invalid value for column"
- **Cause** : Le type de données ne correspond pas au type de champ Airtable
- **Solution** : Vérifier que le type de champ Airtable correspond aux spécifications

### Erreur de permissions
- **Cause** : Clé API sans permissions suffisantes
- **Solution** : Recréer la clé API avec les bonnes permissions

## Bonnes pratiques

1. **Sauvegarde** : Exportez régulièrement vos données Airtable
2. **Permissions** : Utilisez des clés API avec permissions minimales nécessaires
3. **Monitoring** : Surveillez les logs pour détecter les erreurs de stockage
4. **Limite de taux** : Respectez les limites de l'API Airtable (5 req/sec)

## Évolutions futures

- Support pour d'autres systèmes de stockage (Google Sheets, bases de données)
- Configuration automatique des champs via templates
- Interface de gestion des données intégrée