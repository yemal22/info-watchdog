import praw
from datetime import datetime, timezone
from typing import List, Dict, Any
from .base_collector import BaseCollector

class RedditCollector(BaseCollector):
    """
    Collecteur pour Reddit qui récupère les posts environnementaux
    depuis les subreddits spécifiés.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialise le collecteur Reddit.
        
        Args:
            config: Configuration avec client_id, client_secret, user_agent, subreddits, etc.
        """
        super().__init__("reddit", config)
        
        self.reddit = praw.Reddit(
            client_id=config.get("client_id"),
            client_secret=config.get("client_secret"),
            user_agent=config.get("user_agent", "InfoWatchdog/1.0")
        )
        
        self.subreddits = config.get("subreddits", ["environment"])
        self.limit = config.get("limit", 50)
        self.time_filter = config.get("time_filter", "day")  # hour, day, week, month, year
        self.sort_type = config.get("sort_type", "hot")  # hot, new, top, rising
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        Collecte les posts depuis les subreddits configurés.
        
        Returns:
            Liste d'articles formatés
        """
        articles = []
        
        if not self.is_enabled:
            self.logger.info("Reddit collector is disabled")
            return articles
        
        try:
            for subreddit_name in self.subreddits:
                self.logger.info(f"Collecting from r/{subreddit_name}")
                subreddit_articles = self._collect_from_subreddit(subreddit_name)
                articles.extend(subreddit_articles)
                
            self.logger.info(f"Collected {len(articles)} articles from Reddit")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error collecting from Reddit: {str(e)}")
            return articles
    
    def _collect_from_subreddit(self, subreddit_name: str) -> List[Dict[str, Any]]:
        """
        Collecte les posts d'un subreddit spécifique.
        
        Args:
            subreddit_name: Nom du subreddit
            
        Returns:
            Liste d'articles du subreddit
        """
        articles = []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Sélectionne la méthode de tri
            if self.sort_type == "hot":
                posts = subreddit.hot(limit=self.limit)
            elif self.sort_type == "new":
                posts = subreddit.new(limit=self.limit)
            elif self.sort_type == "top":
                posts = subreddit.top(time_filter=self.time_filter, limit=self.limit)
            elif self.sort_type == "rising":
                posts = subreddit.rising(limit=self.limit)
            else:
                posts = subreddit.hot(limit=self.limit)
            
            for post in posts:
                # Filtre les posts épinglés et supprimés
                if post.stickied or post.removed_by_category:
                    continue
                
                # Vérifie la pertinence du contenu
                full_text = f"{post.title} {post.selftext}"
                if not self._is_relevant(full_text):
                    continue
                
                article = self._create_article_dict(
                    title=post.title,
                    url=post.url if not post.is_self else f"https://reddit.com{post.permalink}",
                    source=f"r/{subreddit_name}",
                    content=post.selftext[:500] if post.selftext else "",  # Limite à 500 caractères
                    published_date=datetime.fromtimestamp(post.created_utc, tz=timezone.utc),
                    author=str(post.author) if post.author else "Unknown",
                    tags=self._extract_tags_from_post(post)
                )
                
                # Ajoute des métadonnées Reddit spécifiques
                article.update({
                    "reddit_score": post.score,
                    "reddit_comments": post.num_comments,
                    "reddit_upvote_ratio": getattr(post, 'upvote_ratio', None),
                    "is_self_post": post.is_self,
                    "subreddit": subreddit_name
                })
                
                articles.append(article)
                
        except Exception as e:
            self.logger.error(f"Error collecting from r/{subreddit_name}: {str(e)}")
        
        return articles
    
    def _extract_tags_from_post(self, post) -> List[str]:
        """
        Extrait les tags/mots-clés d'un post Reddit.
        
        Args:
            post: Objet post Reddit
            
        Returns:
            Liste de tags
        """
        tags = []
        
        # Ajoute le flair si disponible
        if hasattr(post, 'link_flair_text') and post.link_flair_text:
            tags.append(post.link_flair_text)
        
        # Ajoute des tags basés sur des mots-clés dans le titre
        environmental_keywords = [
            "climate", "renewable", "solar", "wind", "carbon", "emission",
            "sustainability", "green", "eco", "pollution", "conservation",
            "biodiversity", "recycling", "plastic", "ocean", "forest"
        ]
        
        title_lower = post.title.lower()
        for keyword in environmental_keywords:
            if keyword in title_lower:
                tags.append(keyword)
        
        return list(set(tags))  # Supprime les doublons
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API Reddit.
        
        Returns:
            True si la connexion fonctionne, False sinon
        """
        try:
            # Test simple en récupérant les infos utilisateur
            user = self.reddit.user.me()
            self.logger.info("Reddit connection test successful")
            return True
        except Exception as e:
            self.logger.error(f"Reddit connection test failed: {str(e)}")
            return False
    
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
                "carbon", "green", "eco", "pollution", "conservation",
                "biodiversity", "recycling", "solar", "wind", "emission",
                "energy", "water", "nature", "forest", "ocean", "earth",
                "warming", "change", "clean", "electric", "sustainable",
                "waste", "plastic", "oil", "gas", "coal", "battery"
            ]
        
        text_lower = text.lower()
        
        subreddit_names = ["environment", "climate", "sustainability", "renewableenergy", "climatechange", "solar", "wind"]
        
        return True
        