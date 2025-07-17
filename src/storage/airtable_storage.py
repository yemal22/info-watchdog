from airtable import Airtable
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .base_storage import BaseStorage

class AirtableStorage(BaseStorage):
    """
    Système de stockage utilisant Airtable pour sauvegarder les articles environnementaux.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le stockage Airtable.
        
        Args:
            config: Configuration avec api_key, base_id, table_name
        """
        super().__init__("airtable", config)
        
        self.api_key = config.get("api_key")
        self.base_id = config.get("base_id")
        self.table_name = config.get("table_name", "Environmental_News")
        
        if not self.api_key or not self.base_id:
            raise ValueError("Airtable API key and base ID are required")
        
        self.airtable = Airtable(self.base_id, self.table_name, api_key=self.api_key)
        
        # Cache pour éviter les doublons
        self._hash_cache = set()
        self._last_cache_update = None
        self._cache_ttl = timedelta(hours=1)  # Cache valide 1 heure
    
    def store(self, articles: List[Dict[str, Any]]) -> bool:
        """
        Stocke les articles dans Airtable.
        
        Args:
            articles: Liste d'articles à stocker
            
        Returns:
            True si le stockage a réussi, False sinon
        """
        if not articles:
            return True
        
        try:
            # Filtre les nouveaux articles (réactivé)
            new_articles = self.filter_new_articles(articles)
            
            if not new_articles:
                self.logger.info("No new articles to store")
                return True
            
            self.logger.info(f"Filtered {len(articles)} articles to {len(new_articles)} new articles")
            
            # Stocke article par article pour éviter les problèmes de batch
            success_count = 0
            
            for article in new_articles:
                try:
                    record = self._convert_to_airtable_format(article)
                    result = self.airtable.insert(record)
                    if result:
                        success_count += 1
                        self._hash_cache.add(article.get("hash", ""))
                except Exception as e:
                    self.logger.error(f"Failed to insert article '{article.get('title', 'Unknown')}': {str(e)}")
                    continue
            
            self.logger.info(f"Successfully stored {success_count}/{len(new_articles)} articles")
            return success_count > 0  # Succès si au moins un article est stocké
            
        except Exception as e:
            self.logger.error(f"Error storing articles in Airtable: {str(e)}")
            return False
    
    def _convert_to_airtable_format(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convertit un article au format Airtable avec tous les champs nécessaires.
        
        Args:
            article: Article à convertir
            
        Returns:
            Article formaté pour Airtable
        """
        airtable_record = {}
        
        # Champs de base
        if article.get("title"):
            airtable_record["Title"] = str(article["title"])[:500]
        
        if article.get("url"):
            airtable_record["URL"] = str(article["url"])
        
        if article.get("source"):
            airtable_record["Source"] = str(article["source"])
        
        if article.get("content"):
            airtable_record["Content"] = str(article["content"])[:1000]
        
        if article.get("author"):
            airtable_record["Author"] = str(article["author"])
        
        if article.get("collector"):
            airtable_record["Collector"] = str(article["collector"])
        
        # Hash pour éviter les doublons
        if article.get("hash"):
            airtable_record["Hash"] = str(article["hash"])
        
        # Tags
        if article.get("tags"):
            airtable_record["Tags"] = ", ".join(article["tags"])
        
        # Dates avec format adapté pour Airtable
        if article.get("published_date"):
            try:
                formatted_date = self._format_date_for_airtable(article["published_date"])
                if formatted_date:
                    airtable_record["Published_Date"] = formatted_date
            except Exception as e:
                self.logger.warning(f"Failed to format published_date: {e}")
        
        if article.get("collected_date"):
            try:
                formatted_date = self._format_date_for_airtable(article["collected_date"])
                if formatted_date:
                    airtable_record["Collected_Date"] = formatted_date
            except Exception as e:
                self.logger.warning(f"Failed to format collected_date: {e}")
        
        # Métadonnées Reddit
        if article.get("collector") == "reddit":
            if article.get("reddit_score") is not None:
                airtable_record["Reddit_Score"] = int(article["reddit_score"])
            
            if article.get("reddit_comments") is not None:
                airtable_record["Reddit_Comments"] = int(article["reddit_comments"])
            
            if article.get("subreddit"):
                airtable_record["Subreddit"] = str(article["subreddit"])
        
        return airtable_record
    
    def _format_date_for_airtable(self, date_obj) -> str:
        """
        Formate une date pour Airtable (format compatible).
        
        Args:
            date_obj: Objet datetime ou string
            
        Returns:
            Date formatée pour Airtable (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS.000Z)
        """
        if not date_obj:
            return ""
        
        if isinstance(date_obj, str):
            try:
                from dateutil import parser
                parsed_date = parser.parse(date_obj)
                return parsed_date.strftime("%Y-%m-%d")
            except:
                return date_obj
        
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%Y-%m-%d")
        
        return ""
    
    def check_duplicate(self, article_hash: str) -> bool:
        """
        Vérifie si un article existe déjà dans Airtable.
        
        Args:
            article_hash: Hash de l'article
            
        Returns:
            True si l'article existe déjà
        """
        if not article_hash:
            return False
        
        # Utilise le cache si il est récent
        if self._is_cache_valid() and article_hash in self._hash_cache:
            return True
        
        try:
            # Recherche par hash dans Airtable
            formula = f"{{Hash}} = '{article_hash}'"
            records = self.airtable.search("Hash", article_hash)
            
            exists = len(records) > 0
            
            # Met à jour le cache
            if exists:
                self._hash_cache.add(article_hash)
            
            return exists
            
        except Exception as e:
            self.logger.error(f"Error checking duplicate: {str(e)}")
            return False
    
    def _is_cache_valid(self) -> bool:
        """
        Vérifie si le cache est encore valide.
        
        Returns:
            True si le cache est valide
        """
        if not self._last_cache_update:
            return False
        
        return datetime.now() - self._last_cache_update < self._cache_ttl
    
    def _refresh_hash_cache(self):
        """
        Actualise le cache des hash depuis Airtable.
        """
        try:
            # Récupère tous les hash récents
            formula = f"IS_AFTER({{Collected_Date}}, DATEADD(TODAY(), -7, 'days'))"
            records = self.airtable.get_all(formula=formula, fields=["Hash"])
            
            self._hash_cache = {record["fields"].get("Hash") for record in records 
                              if record["fields"].get("Hash")}
            self._last_cache_update = datetime.now()
            
            self.logger.info(f"Refreshed hash cache with {len(self._hash_cache)} entries")
            
        except Exception as e:
            self.logger.error(f"Error refreshing hash cache: {str(e)}")
    
    def get_recent_articles(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Récupère les articles récents d'Airtable.
        
        Args:
            days: Nombre de jours dans le passé
            
        Returns:
            Liste des articles récents
        """
        try:
            # Formule Airtable pour les articles récents
            formula = f"IS_AFTER({{Collected_Date}}, DATEADD(TODAY(), -{days}, 'days'))"
            
            records = self.airtable.get_all(
                formula=formula,
                sort=[("Collected_Date", "desc")]
            )
            
            articles = []
            for record in records:
                article = record["fields"]
                article["airtable_id"] = record["id"]
                articles.append(article)
            
            self.logger.info(f"Retrieved {len(articles)} recent articles")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error retrieving recent articles: {str(e)}")
            return []
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à Airtable.
        
        Returns:
            True si la connexion fonctionne
        """
        try:
            # Test simple en récupérant les métadonnées de la table
            records = self.airtable.get_all(max_records=1)
            self.logger.info("Airtable connection test successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Airtable connection test failed: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur les données stockées.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        try:
            # Total d'articles
            total_records = len(self.airtable.get_all(fields=["Hash"]))
            
            # Articles récents (7 derniers jours)
            recent_articles = self.get_recent_articles(7)
            recent_count = len(recent_articles)
            
            # Articles par source
            source_stats = {}
            for article in recent_articles:
                source = article.get("Source", "Unknown")
                source_stats[source] = source_stats.get(source, 0) + 1
            
            return {
                "total_articles": total_records,
                "recent_articles_7days": recent_count,
                "articles_by_source": source_stats,
                "cache_size": len(self._hash_cache),
                "last_cache_update": self._last_cache_update
            }
            
        except Exception as e:
            self.logger.error(f"Error getting stats: {str(e)}")
            return {}