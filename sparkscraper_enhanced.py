"""
Enhanced SparkScraper with advanced features
Includes idea categorization, sentiment analysis, duplicate detection, and multiple output formats
"""

import praw
import tweepy
import requests
from bs4 import BeautifulSoup
import time
import json
import csv
import re
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from collections import Counter
import hashlib
from textblob import TextBlob
from config import SparkScraperConfig

# Set up logging
logging.basicConfig(
    level=getattr(logging, SparkScraperConfig.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(SparkScraperConfig.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IdeaProcessor:
    """Process and analyze scraped ideas"""
    
    def __init__(self):
        self.seen_ideas = set()
        self.idea_categories = SparkScraperConfig.IDEA_CATEGORIES
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\!\?\-]', '', text)
        # Normalize whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    def is_duplicate(self, idea: str) -> bool:
        """Check if idea is a duplicate using hash"""
        idea_hash = hashlib.md5(idea.lower().encode()).hexdigest()
        if idea_hash in self.seen_ideas:
            return True
        self.seen_ideas.add(idea_hash)
        return False
    
    def categorize_idea(self, idea: str) -> List[str]:
        """Categorize idea based on keywords"""
        idea_lower = idea.lower()
        categories = []
        
        for category, keywords in self.idea_categories.items():
            if any(keyword in idea_lower for keyword in keywords):
                categories.append(category)
        
        return categories if categories else ["general"]
    
    def analyze_sentiment(self, idea: str) -> float:
        """Analyze sentiment of idea using TextBlob"""
        try:
            blob = TextBlob(idea)
            return blob.sentiment.polarity
        except:
            return 0.0
    
    def filter_idea(self, idea: str) -> bool:
        """Filter ideas based on quality criteria"""
        # Check word count
        word_count = len(idea.split())
        if word_count < SparkScraperConfig.MIN_WORD_COUNT or word_count > SparkScraperConfig.MAX_WORD_COUNT:
            return False
        
        # Check for excluded words
        idea_lower = idea.lower()
        if any(excluded in idea_lower for excluded in SparkScraperConfig.EXCLUDED_WORDS):
            return False
        
        # Check for duplicates
        if self.is_duplicate(idea):
            return False
        
        return True
    
    def process_ideas(self, ideas: List[str], source: str) -> List[Dict[str, Any]]:
        """Process a list of ideas and return structured data"""
        processed_ideas = []
        
        for idea in ideas:
            cleaned_idea = self.clean_text(idea)
            
            if not self.filter_idea(cleaned_idea):
                continue
            
            processed_idea = {
                "text": cleaned_idea,
                "source": source,
                "categories": self.categorize_idea(cleaned_idea),
                "sentiment": self.analyze_sentiment(cleaned_idea),
                "word_count": len(cleaned_idea.split()),
                "timestamp": datetime.now().isoformat()
            }
            
            processed_ideas.append(processed_idea)
        
        return processed_ideas

class EnhancedSparkScraper:
    """Enhanced version of SparkScraper with advanced features"""
    
    def __init__(self):
        self.processor = IdeaProcessor()
        self.setup_apis()
    
    def setup_apis(self):
        """Setup API connections"""
        try:
            # Reddit setup
            self.reddit = praw.Reddit(
                client_id=SparkScraperConfig.REDDIT_CONFIG["client_id"],
                client_secret=SparkScraperConfig.REDDIT_CONFIG["client_secret"],
                user_agent=SparkScraperConfig.REDDIT_CONFIG["user_agent"]
            )
            logger.info("Reddit API configured successfully")
        except Exception as e:
            logger.warning(f"Reddit API setup failed: {e}")
            self.reddit = None
        
        try:
            # Twitter setup
            auth = tweepy.OAuth1UserHandler(
                consumer_key=SparkScraperConfig.TWITTER_CONFIG["consumer_key"],
                consumer_secret=SparkScraperConfig.TWITTER_CONFIG["consumer_secret"],
                access_token=SparkScraperConfig.TWITTER_CONFIG["access_token"],
                access_token_secret=SparkScraperConfig.TWITTER_CONFIG["access_token_secret"]
            )
            self.twitter_api = tweepy.API(auth)
            logger.info("Twitter API configured successfully")
        except Exception as e:
            logger.warning(f"Twitter API setup failed: {e}")
            self.twitter_api = None
    
    def scrape_reddit_enhanced(self, subreddits: List[str], keywords: List[str]) -> List[Dict[str, Any]]:
        """Enhanced Reddit scraping with multiple subreddits and keywords"""
        if not self.reddit:
            logger.warning("Reddit API not available")
            return []
        
        all_ideas = []
        
        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                logger.info(f"Scraping r/{subreddit_name}")
                
                for keyword in keywords:
                    try:
                        for submission in subreddit.search(keyword, limit=SparkScraperConfig.MAX_REDDIT_POSTS):
                            if "project" in submission.title.lower() or "idea" in submission.title.lower():
                                all_ideas.append(submission.title)
                        
                        time.sleep(SparkScraperConfig.RATE_LIMIT_DELAY)
                    except Exception as e:
                        logger.error(f"Error scraping keyword '{keyword}' from r/{subreddit_name}: {e}")
                        
            except Exception as e:
                logger.error(f"Error accessing subreddit r/{subreddit_name}: {e}")
        
        return self.processor.process_ideas(all_ideas, "reddit")
    
    def scrape_twitter_enhanced(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Enhanced Twitter scraping with multiple keywords"""
        if not self.twitter_api:
            logger.warning("Twitter API not available")
            return []
        
        all_ideas = []
        
        for keyword in keywords:
            try:
                logger.info(f"Scraping Twitter for '{keyword}'")
                tweets = self.twitter_api.search_tweets(
                    q=keyword, 
                    count=SparkScraperConfig.MAX_TWITTER_TWEETS, 
                    tweet_mode="extended"
                )
                
                for tweet in tweets:
                    text = tweet.full_text
                    if "project" in text.lower() or "idea" in text.lower():
                        all_ideas.append(text)
                
                time.sleep(SparkScraperConfig.RATE_LIMIT_DELAY)
            except Exception as e:
                logger.error(f"Error scraping Twitter for keyword '{keyword}': {e}")
        
        return self.processor.process_ideas(all_ideas, "twitter")
    
    def scrape_linkedin_enhanced(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Enhanced LinkedIn scraping (use with caution)"""
        all_ideas = []
        
        for keyword in keywords:
            try:
                logger.info(f"Scraping LinkedIn for '{keyword}'")
                url = f"https://www.linkedin.com/search/results/content/?keywords={keyword}"
                headers = {"User-Agent": SparkScraperConfig.USER_AGENT}
                
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Try multiple selectors for LinkedIn content
                selectors = [
                    "div.search-result__info",
                    "div.feed-shared-text",
                    "span.break-words"
                ]
                
                for selector in selectors:
                    posts = soup.find_all("div", class_=selector.split(".")[1])
                    for post in posts:
                        text = post.get_text().strip()
                        if "project" in text.lower() or "idea" in text.lower():
                            all_ideas.append(text)
                
                time.sleep(SparkScraperConfig.RATE_LIMIT_DELAY)
            except Exception as e:
                logger.error(f"Error scraping LinkedIn for keyword '{keyword}': {e}")
        
        return self.processor.process_ideas(all_ideas, "linkedin")
    
    def generate_markdown_enhanced(self, ideas: List[Dict[str, Any]]) -> str:
        """Generate enhanced markdown with categories and sentiment"""
        markdown = "# SparkScraper Project Ideas\n\n"
        markdown += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        markdown += f"Total ideas found: {len(ideas)}\n\n"
        
        # Group by source
        by_source = {}
        for idea in ideas:
            source = idea["source"]
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(idea)
        
        for source, source_ideas in by_source.items():
            markdown += f"## From {source.title()}\n\n"
            
            # Group by category
            by_category = {}
            for idea in source_ideas:
                for category in idea["categories"]:
                    if category not in by_category:
                        by_category[category] = []
                    by_category[category].append(idea)
            
            for category, category_ideas in by_category.items():
                markdown += f"### {category.replace('_', ' ').title()}\n\n"
                
                for i, idea in enumerate(category_ideas, 1):
                    sentiment_emoji = "😊" if idea["sentiment"] > 0 else "😐" if idea["sentiment"] == 0 else "😔"
                    markdown += f"{i}. {idea['text']} {sentiment_emoji}\n"
                
                markdown += "\n"
        
        return markdown
    
    def generate_json(self, ideas: List[Dict[str, Any]]) -> str:
        """Generate JSON output"""
        output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_ideas": len(ideas),
                "sources": list(set(idea["source"] for idea in ideas)),
                "categories": list(set(cat for idea in ideas for cat in idea["categories"]))
            },
            "ideas": ideas
        }
        return json.dumps(output, indent=2)
    
    def generate_csv(self, ideas: List[Dict[str, Any]]) -> str:
        """Generate CSV output"""
        if not ideas:
            return ""
        
        output = StringIO()
        fieldnames = ["text", "source", "categories", "sentiment", "word_count", "timestamp"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for idea in ideas:
            # Convert categories list to string
            idea_copy = idea.copy()
            idea_copy["categories"] = ", ".join(idea["categories"])
            writer.writerow(idea_copy)
        
        return output.getvalue()
    
    def save_output(self, ideas: List[Dict[str, Any]], formats: List[str] = None):
        """Save output in multiple formats"""
        if formats is None:
            formats = ["markdown"]
        
        for output_format in formats:
            if output_format == "markdown":
                content = self.generate_markdown_enhanced(ideas)
                filename = SparkScraperConfig.OUTPUT_FILENAME
            elif output_format == "json":
                content = self.generate_json(ideas)
                filename = "sparkscraper_ideas.json"
            elif output_format == "csv":
                content = self.generate_csv(ideas)
                filename = "sparkscraper_ideas.csv"
            else:
                logger.warning(f"Unknown output format: {output_format}")
                continue
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Output saved to {filename}")
            except Exception as e:
                logger.error(f"Error saving {filename}: {e}")
    
    def run(self, keywords: List[str] = None, subreddits: List[str] = None, 
            output_formats: List[str] = None):
        """Run the enhanced scraper"""
        if keywords is None:
            keywords = SparkScraperConfig.get_keywords()
        if subreddits is None:
            subreddits = SparkScraperConfig.get_subreddits()
        if output_formats is None:
            output_formats = ["markdown"]
        
        logger.info("Starting enhanced SparkScraper")
        logger.info(f"Keywords: {keywords}")
        logger.info(f"Subreddits: {subreddits}")
        
        all_ideas = []
        
        # Scrape from all sources
        reddit_ideas = self.scrape_reddit_enhanced(subreddits, keywords)
        twitter_ideas = self.scrape_twitter_enhanced(keywords)
        linkedin_ideas = self.scrape_linkedin_enhanced(keywords)
        
        all_ideas.extend(reddit_ideas)
        all_ideas.extend(twitter_ideas)
        all_ideas.extend(linkedin_ideas)
        
        logger.info(f"Total ideas collected: {len(all_ideas)}")
        
        # Save output
        self.save_output(all_ideas, output_formats)
        
        # Print summary
        print(f"\n🎉 SparkScraper completed!")
        print(f"📊 Total ideas found: {len(all_ideas)}")
        print(f"📁 Output saved in formats: {', '.join(output_formats)}")
        
        return all_ideas

if __name__ == "__main__":
    scraper = EnhancedSparkScraper()
    scraper.run() 