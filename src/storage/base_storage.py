from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

class BaseStorage(ABC):
    """
    Classe abstraite pour tous les systèmes de stockage.
    Définit l'interface commune pour stocker les données collectées.
    """
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialise le système de stockage.
        
        Args:
            name: Nom du système de stockage
            config: Configuration spécifique au stockage
        """
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"storage.{name}")
        self.is_enabled = self.config.get("enabled", True)
    
    @abstractmethod
    def store(self, articles: List[Dict[str, Any]]) -> bool:
        """
        Stocke une liste d'articles.
        
        Args:
            articles: Liste d'articles à stocker
            
        Returns:
            True si le stockage a réussi, False sinon
        """
        pass
    
    @abstractmethod
    def check_duplicate(self, article_hash: str) -> bool:
        """
        Vérifie si un article existe déjà (basé sur son hash).
        
        Args:
            article_hash: Hash unique de l'article
            
        Returns:
            True si l'article existe déjà, False sinon
        """
        pass
    
    @abstractmethod
    def get_recent_articles(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Récupère les articles récents.
        
        Args:
            days: Nombre de jours dans le passé
            
        Returns:
            Liste des articles récents
        """
        pass
    
    def filter_new_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filtre les articles pour ne garder que les nouveaux.
        
        Args:
            articles: Liste d'articles à filtrer
            
        Returns:
            Liste des articles non-dupliqués
        """
        if not articles:
            return []
        
        new_articles = []
        for article in articles:
            article_hash = article.get("hash")
            if article_hash and not self.check_duplicate(article_hash):
                new_articles.append(article)
        
        self.logger.info(f"Filtered {len(articles)} articles to {len(new_articles)} new articles")
        return new_articles
    
    def batch_store(self, articles: List[Dict[str, Any]], batch_size: int = 10) -> bool:
        """
        Stocke les articles par lots pour améliorer les performances.
        
        Args:
            articles: Liste d'articles à stocker
            batch_size: Taille des lots
            
        Returns:
            True si tous les lots ont été stockés avec succès
        """
        if not articles:
            return True
        
        success_count = 0
        total_batches = (len(articles) + batch_size - 1) // batch_size
        
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            if self.store(batch):
                success_count += 1
            else:
                self.logger.error(f"Failed to store batch {i//batch_size + 1}/{total_batches}")
        
        success_rate = success_count / total_batches
        self.logger.info(f"Stored {success_count}/{total_batches} batches successfully ({success_rate:.1%})")
        
        return success_rate == 1.0
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Teste la connexion au système de stockage.
        
        Returns:
            True si la connexion fonctionne, False sinon
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retourne le statut du système de stockage.
        
        Returns:
            Dictionnaire avec les informations de statut
        """
        return {
            "name": self.name,
            "enabled": self.is_enabled,
            "connection": self.test_connection(),
            "config": self.config
        }
    
    def __str__(self) -> str:
        return f"Storage({self.name})"
    
    def __repr__(self) -> str:
        return f"Storage(name='{self.name}', enabled={self.is_enabled})"