from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import logging

class BaseCollector(ABC):
    """
    Classes abstraites pour tous les collecteurs de données.
    Définit l'interface commune pour la collecte de contenu environnemental.
    """
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialise de collecteur de base.
        
        Args:
            name: Nom du collecteur
            config: COnfiguration spécifique au collecteur
        """
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"collector.{name}")
        self.is_enabled = self.config.get("enabled", True)
        
    @abstractmethod
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collecte les données depuis la source.
        
        Returns:
            Liste de dictionnaires contenant les données collectées
        """
        pass
    
    def _create_article_dict(self, title: str, url: str, source: str,
                           content: str = "", published_date: datetime = None,
                           author: str = "", tags: List[str] = None) -> Dict[str, Any]:
        """
        Crée un dictionnaire standardisé pour un article.
        
        Args:
            title: Titre de l'article
            url: URL de l'article
            source: Source de l'article
            content: Contenu/résumé de l'article
            published_date: Date de publication
            author: Auteur de l'article
            tags: Mots-clés/tags associés
            
        Returns:
            Dictionnaire standardisé
        """
        return {
            "title": self._clean_text(title),
            "url": url,
            "source": source,
            "content": self._clean_text(content),
            "published_date": published_date or datetime.now(),
            "collected_date": datetime.now(),
            "author": author,
            "tags": tags or [],
            "collector": self.name,
            "hash": self._generate_hash(title, url)
        }
    
    def _clean_text(self, text: str) -> str:
        """
        Nettoie le texte en supprimant les caractères indésirables.
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            Texte nettoyé
        """
        if not text:
            return ""
        
        # Supprime les caractères indésirables
        cleaned = " ".join(text.split())
        return cleaned.strip()
    
    def _generate_hash(self, title: str, url: str) -> str:
        """
        Génère un hash unique pour éviter les doublons.
        
        Args:
            title: Titre de l'article
            url: URL de l'article
            
        Returns:
            Hash unique
        """
        import hashlib
        content = f"{title}{url}".encode('utf-8')
        return hashlib.md5(content).hexdigest()
    
    def _is_relevant(self, text: str, keywords: List[str] = None) -> bool:
        """
        Vérifie si le contenu est pertinent selon les mots-clés.
        
        Args:
            text: Texte à analyser
            keywords: Liste de mots-clés environnementaux
            
        Returns:
            True si pertinent, False sinon
        """
        if not keywords:
            keywords = [
                "climate", "environment", "sustainability", "renewable", 
                "carbon", "green", "eco", "pollution", "conservation"
            ]
            
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retourne l'état du collecteur.
        
        Returns:
            Dictionnaire avec le statut du collecteur
        """
        return {
            "name": self.name,
            "enabled": self.is_enabled,
            "config": self.config
        }
        
    def __str__(self) -> str:
        return f"Collector({self.name})"
    
    def __repr__(self) -> str:
        return f"Collector(name='{self.name}', enabled={self.is_enabled})"
    