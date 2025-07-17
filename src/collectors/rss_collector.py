import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Any
from .base_collector import BaseCollector

class RSSCollector(BaseCollector):
    """
    Collecteur pour les flux RSS de sites environnementaux.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le collecteur RSS.
        
        Args:
            config: Configuration avec la liste des feeds RSS
        """
        super().__init__("rss", config)
        
        self.feeds = config.get("feeds", [])
        self.timeout = config.get("timeout", 30)
        self.user_agent = config.get("user_agent", "InfoWatchdog RSS Collector/1.0")
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collecte les articles depuis tous les flux RSS configurés.
        
        Returns:
            Liste d'articles formatés
        """
        articles = []
        
        if not self.is_enabled:
            self.logger.info("RSS collector is disabled")
            return articles
        
        try:
            for feed_config in self.feeds:
                feed_url = feed_config.get("url")
                feed_name = feed_config.get("name", feed_url)
                
                self.logger.info(f"Collecting from RSS feed: {feed_name}")
                feed_articles = self._collect_from_feed(feed_url, feed_name)
                articles.extend(feed_articles)
                
            self.logger.info(f"Collected {len(articles)} articles from RSS feeds")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error collecting from RSS feeds: {str(e)}")
            return articles
    
    def _collect_from_feed(self, feed_url: str, feed_name: str) -> List[Dict[str, Any]]:
        """
        Collecte les articles d'un flux RSS spécifique.
        
        Args:
            feed_url: URL du flux RSS
            feed_name: Nom du flux pour identification
            
        Returns:
            Liste d'articles du flux
        """
        articles = []
        
        try:
            # Configuration pour les requêtes
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'application/rss+xml, application/xml, text/xml'
            }
            
            # Récupère le flux RSS
            response = requests.get(feed_url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse le flux RSS
            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                self.logger.warning(f"RSS feed may have issues: {feed_name}")
            
            for entry in feed.entries:
                # Vérifie la pertinence du contenu
                full_text = f"{entry.get('title', '')} {entry.get('summary', '')}"
                if not self._is_relevant(full_text):
                    continue
                
                article = self._create_article_dict(
                    title=entry.get('title', 'No title'),
                    url=entry.get('link', ''),
                    source=feed_name,
                    content=self._extract_content(entry),
                    published_date=self._parse_date(entry),
                    author=self._extract_author(entry),
                    tags=self._extract_tags_from_entry(entry)
                )
                
                # Ajoute des métadonnées RSS spécifiques
                article.update({
                    "feed_url": feed_url,
                    "categories": entry.get('tags', []),
                    "guid": entry.get('id', entry.get('guid', ''))
                })
                
                articles.append(article)
                
        except requests.RequestException as e:
            self.logger.error(f"Network error fetching RSS feed {feed_name}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error parsing RSS feed {feed_name}: {str(e)}")
        
        return articles
    
    def _extract_content(self, entry) -> str:
        """
        Extrait le contenu d'une entrée RSS.
        
        Args:
            entry: Entrée RSS
            
        Returns:
            Contenu textuel
        """
        # Essaie différents champs pour le contenu
        content_fields = ['summary', 'description', 'content']
        
        for field in content_fields:
            if hasattr(entry, field):
                content = getattr(entry, field)
                if isinstance(content, list) and content:
                    content = content[0].get('value', '')
                if content:
                    # Supprime les balises HTML basiques
                    import re
                    content = re.sub(r'<[^>]+>', '', str(content))
                    return content[:1000]  # Limite à 1000 caractères
        
        return ""
    
    def _parse_date(self, entry) -> datetime:
        """
        Parse la date de publication d'une entrée RSS.
        
        Args:
            entry: Entrée RSS
            
        Returns:
            Date de publication ou date actuelle si non trouvée
        """
        date_fields = ['published_parsed', 'updated_parsed']
        
        for field in date_fields:
            if hasattr(entry, field):
                date_tuple = getattr(entry, field)
                if date_tuple:
                    try:
                        return datetime(*date_tuple[:6])
                    except (TypeError, ValueError):
                        continue
        
        # Essaie de parser les dates string
        date_string_fields = ['published', 'updated']
        for field in date_string_fields:
            if hasattr(entry, field):
                date_string = getattr(entry, field)
                if date_string:
                    try:
                        from dateutil import parser
                        return parser.parse(date_string)
                    except Exception:
                        continue
        
        return datetime.now()
    
    def _extract_author(self, entry) -> str:
        """
        Extrait l'auteur d'une entrée RSS.
        
        Args:
            entry: Entrée RSS
            
        Returns:
            Nom de l'auteur
        """
        author_fields = ['author', 'dc_creator']
        
        for field in author_fields:
            if hasattr(entry, field):
                author = getattr(entry, field)
                if author:
                    return str(author)
        
        return "Unknown"
    
    def _extract_tags_from_entry(self, entry) -> List[str]:
        """
        Extrait les tags/catégories d'une entrée RSS.
        
        Args:
            entry: Entrée RSS
            
        Returns:
            Liste de tags
        """
        tags = []
        
        # Récupère les catégories RSS
        if hasattr(entry, 'tags'):
            for tag in entry.tags:
                if hasattr(tag, 'term'):
                    tags.append(tag.term)
                elif isinstance(tag, str):
                    tags.append(tag)
        
        # Ajoute des tags basés sur le contenu
        environmental_keywords = [
            "climate", "renewable", "solar", "wind", "carbon", "emission",
            "sustainability", "green", "eco", "pollution", "conservation",
            "biodiversity", "recycling", "plastic", "ocean", "forest"
        ]
        
        title = entry.get('title', '').lower()
        for keyword in environmental_keywords:
            if keyword in title:
                tags.append(keyword)
        
        return list(set(tags))  # Supprime les doublons
    
    def test_feed(self, feed_url: str) -> bool:
        """
        Teste un flux RSS spécifique.
        
        Args:
            feed_url: URL du flux à tester
            
        Returns:
            True si le flux est accessible, False sinon
        """
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(feed_url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            if feed.entries:
                self.logger.info(f"RSS feed test successful: {feed_url}")
                return True
            else:
                self.logger.warning(f"RSS feed has no entries: {feed_url}")
                return False
                
        except Exception as e:
            self.logger.error(f"RSS feed test failed {feed_url}: {str(e)}")
            return False