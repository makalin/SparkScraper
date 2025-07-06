"""
Configuration file for SparkScraper
Centralizes all settings and API configurations
"""

import os
from typing import List, Dict, Any

class SparkScraperConfig:
    """Configuration class for SparkScraper"""
    
    # API Configuration
    REDDIT_CONFIG = {
        "client_id": os.getenv("REDDIT_CLIENT_ID", "YOUR_REDDIT_CLIENT_ID"),
        "client_secret": os.getenv("REDDIT_CLIENT_SECRET", "YOUR_REDDIT_CLIENT_SECRET"),
        "user_agent": os.getenv("REDDIT_USER_AGENT", "SparkScraper v2.0 by /u/YOUR_REDDIT_USERNAME")
    }
    
    TWITTER_CONFIG = {
        "consumer_key": os.getenv("TWITTER_CONSUMER_KEY", "YOUR_TWITTER_API_KEY"),
        "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET", "YOUR_TWITTER_API_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN"),
        "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "YOUR_ACCESS_TOKEN_SECRET")
    }
    
    # Scraping Configuration
    DEFAULT_KEYWORDS = [
        "project ideas",
        "startup ideas", 
        "side project",
        "app ideas",
        "business ideas",
        "coding project",
        "developer project"
    ]
    
    DEFAULT_SUBREDDITS = [
        "sideprojects",
        "startups",
        "entrepreneur",
        "webdev",
        "programming",
        "indiehackers",
        "SaaS"
    ]
    
    # Rate Limiting
    RATE_LIMIT_DELAY = 1.0  # seconds between requests
    MAX_REDDIT_POSTS = 100
    MAX_TWITTER_TWEETS = 100
    MAX_LINKEDIN_POSTS = 50
    
    # Output Configuration
    OUTPUT_FILENAME = "sparkscraper_ideas.md"
    OUTPUT_FORMATS = ["markdown", "json", "csv"]
    
    # Filtering Configuration
    MIN_WORD_COUNT = 5
    MAX_WORD_COUNT = 200
    EXCLUDED_WORDS = [
        "spam", "advertisement", "promotion", "buy now", "click here",
        "limited time", "offer", "discount", "sale"
    ]
    
    # Categories for organizing ideas
    IDEA_CATEGORIES = {
        "web_app": ["web", "app", "website", "platform", "dashboard"],
        "mobile_app": ["mobile", "ios", "android", "app store"],
        "ai_ml": ["ai", "machine learning", "artificial intelligence", "neural network"],
        "fintech": ["finance", "payment", "banking", "investment", "crypto"],
        "healthcare": ["health", "medical", "fitness", "wellness"],
        "education": ["learning", "education", "course", "tutorial"],
        "productivity": ["productivity", "automation", "workflow", "efficiency"],
        "social": ["social", "community", "network", "connection"],
        "ecommerce": ["shop", "store", "marketplace", "retail"],
        "gaming": ["game", "gaming", "entertainment", "play"]
    }
    
    # User Agent for web scraping
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FILE = "sparkscraper.log"
    
    @classmethod
    def get_keywords(cls) -> List[str]:
        """Get keywords from environment or use defaults"""
        env_keywords = os.getenv("SPARKSCRAPER_KEYWORDS")
        if env_keywords:
            return [kw.strip() for kw in env_keywords.split(",")]
        return cls.DEFAULT_KEYWORDS
    
    @classmethod
    def get_subreddits(cls) -> List[str]:
        """Get subreddits from environment or use defaults"""
        env_subreddits = os.getenv("SPARKSCRAPER_SUBREDDITS")
        if env_subreddits:
            return [sub.strip() for sub in env_subreddits.split(",")]
        return cls.DEFAULT_SUBREDDITS
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate that all required configuration is present"""
        validation = {
            "reddit_configured": bool(cls.REDDIT_CONFIG["client_id"] != "YOUR_REDDIT_CLIENT_ID"),
            "twitter_configured": bool(cls.TWITTER_CONFIG["consumer_key"] != "YOUR_TWITTER_API_KEY"),
            "output_writable": True  # Will be checked at runtime
        }
        return validation 