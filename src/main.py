import os
import yaml
import logging
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

from collectors import RedditCollector, RSSCollector
from storage import AirtableStorage

class InfoWatchdog:
    """
    Agent principal de veille environnementale.
    Orchestre la collecte de données depuis multiple sources et leur stockage.
    """
    
    def __init__(self, config_path: str = "config/config.yml"):
        """
        Initialise l'agent de veille.
        
        Args:
            config_path: Chemin vers le fichier de configuration
        """
        # Charge les variables d'environnement
        load_dotenv()
        
        # Configure le logging
        self._setup_logging()
        
        # Charge la configuration
        self.config = self._load_config(config_path)
        
        # Initialise les composants
        self.collectors = []
        self.storage = None
        
        self._initialize_components()
        
        self.logger = logging.getLogger("infowatchdog")
        self.logger.info("InfoWatchdog initialized successfully")
    
    def _setup_logging(self):
        """Configure le système de logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('infowatchdog.log'),
                logging.StreamHandler()
            ]
        )
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Charge la configuration depuis un fichier YAML.
        
        Args:
            config_path: Chemin vers le fichier de configuration
            
        Returns:
            Configuration sous forme de dictionnaire
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            return config
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            return {}
        except yaml.YAMLError as e:
            logging.error(f"Error parsing configuration file: {e}")
            return {}
    
    def _initialize_components(self):
        """Initialise les collecteurs et le système de stockage."""
        # Initialise les collecteurs
        self._initialize_collectors()
        
        # Initialise le stockage
        self._initialize_storage()
    
    def _initialize_collectors(self):
        """Initialise tous les collecteurs configurés."""
        collectors_config = self.config.get("collectors", {})
        
        # Collecteur Reddit
        reddit_config = collectors_config.get("reddit", {})
        if reddit_config.get("enabled", True):
            try:
                reddit_config.update({
                    "client_id": os.getenv("REDDIT_CLIENT_ID"),
                    "client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
                    "user_agent": os.getenv("REDDIT_USER_AGENT", "InfoWatchdog/1.0")
                })
                reddit_collector = RedditCollector(reddit_config)
                self.collectors.append(reddit_collector)
                logging.info("Reddit collector initialized")
            except Exception as e:
                logging.error(f"Failed to initialize Reddit collector: {e}")
        
        # Collecteur RSS
        rss_config = collectors_config.get("rss", {})
        if rss_config.get("enabled", True):
            try:
                rss_collector = RSSCollector(rss_config)
                self.collectors.append(rss_collector)
                logging.info("RSS collector initialized")
            except Exception as e:
                logging.error(f"Failed to initialize RSS collector: {e}")
    
    def _initialize_storage(self):
        """Initialise le système de stockage."""
        storage_config = self.config.get("storage", {})
        storage_type = storage_config.get("type", "airtable")
        
        if storage_type == "airtable":
            try:
                airtable_config = {
                    "api_key": os.getenv("AIRTABLE_API_KEY"),
                    "base_id": os.getenv("AIRTABLE_BASE_ID"),
                    "table_name": os.getenv("AIRTABLE_TABLE_NAME", "Environmental_News"),
                    "enabled": storage_config.get("enabled", True)
                }
                self.storage = AirtableStorage(airtable_config)
                logging.info("Airtable storage initialized")
            except Exception as e:
                logging.error(f"Failed to initialize Airtable storage: {e}")
        else:
            logging.error(f"Unsupported storage type: {storage_type}")
    
    def collect_all(self) -> List[Dict[str, Any]]:
        """
        Lance la collecte depuis tous les collecteurs actifs.
        
        Returns:
            Liste de tous les articles collectés
        """
        all_articles = []
        
        self.logger.info("Starting data collection from all sources")
        
        for collector in self.collectors:
            if not collector.is_enabled:
                continue
                
            try:
                self.logger.info(f"Collecting from {collector.name}")
                articles = collector.collect()
                all_articles.extend(articles)
                self.logger.info(f"Collected {len(articles)} articles from {collector.name}")
                
            except Exception as e:
                self.logger.error(f"Error collecting from {collector.name}: {e}")
        
        self.logger.info(f"Total articles collected: {len(all_articles)}")
        return all_articles
    
    def store_articles(self, articles: List[Dict[str, Any]]) -> bool:
        """
        Stocke les articles collectés.
        
        Args:
            articles: Liste d'articles à stocker
            
        Returns:
            True si le stockage a réussi
        """
        if not self.storage:
            self.logger.error("No storage system initialized")
            return False
        
        if not articles:
            self.logger.info("No articles to store")
            return True
        
        try:
            self.logger.info(f"Storing {len(articles)} articles")
            success = self.storage.store(articles)
            
            if success:
                self.logger.info("Articles stored successfully")
            else:
                self.logger.error("Failed to store some articles")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error storing articles: {e}")
            return False
    
    def run_collection_cycle(self) -> Dict[str, Any]:
        """
        Exécute un cycle complet de collecte et stockage.
        
        Returns:
            Rapport du cycle d'exécution
        """
        start_time = datetime.now()
        self.logger.info("Starting collection cycle")
        
        # Collecte les données
        articles = self.collect_all()
        
        # Stocke les données
        storage_success = self.store_articles(articles)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Génère le rapport
        report = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration.total_seconds(),
            "articles_collected": len(articles),
            "storage_success": storage_success,
            "collectors_status": [collector.get_status() for collector in self.collectors],
            "storage_status": self.storage.get_status() if self.storage else None
        }
        
        self.logger.info(f"Collection cycle completed in {duration.total_seconds():.2f} seconds")
        return report
    
    def test_connections(self) -> Dict[str, bool]:
        """
        Teste toutes les connexions (collecteurs et stockage).
        
        Returns:
            Dictionnaire avec les résultats des tests
        """
        results = {}
        
        # Teste les collecteurs
        for collector in self.collectors:
            if hasattr(collector, 'test_connection'):
                results[f"collector_{collector.name}"] = collector.test_connection()
            else:
                results[f"collector_{collector.name}"] = True  # Pas de test spécifique
        
        # Teste le stockage
        if self.storage:
            results["storage"] = self.storage.test_connection()
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Récupère les statistiques du système.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        stats = {
            "collectors": {
                "total": len(self.collectors),
                "enabled": len([c for c in self.collectors if c.is_enabled]),
                "details": [c.get_status() for c in self.collectors]
            }
        }
        
        if self.storage:
            stats["storage"] = self.storage.get_stats() if hasattr(self.storage, 'get_stats') else self.storage.get_status()
        
        return stats
    
    def __str__(self) -> str:
        return f"InfoWatchdog(collectors={len(self.collectors)}, storage={self.storage.name if self.storage else 'None'})"