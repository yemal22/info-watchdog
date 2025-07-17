"""
Module collectors pour InfoWatchdog.
Contient les collecteurs de données pour différentes sources.
"""

from .base_collector import BaseCollector
from .reddit_collector import RedditCollector
from .rss_collector import RSSCollector

__all__ = [
    'BaseCollector',
    'RedditCollector', 
    'RSSCollector'
]