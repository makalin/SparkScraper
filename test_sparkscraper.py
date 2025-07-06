import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
import sys
from io import StringIO

# Import the functions we want to test
from sparkscraper import (
    scrape_reddit, 
    scrape_twitter, 
    scrape_linkedin, 
    generate_markdown
)

class TestSparkScraper(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_reddit_ideas = [
            "Build a weather app with real-time alerts",
            "Create a project management tool for freelancers",
            "Develop a recipe recommendation app"
        ]
        
        self.test_twitter_ideas = [
            "Idea: A platform to connect indie game devs with artists",
            "Project idea: AI-powered personal finance tracker",
            "Building a tool for remote team collaboration"
        ]
        
        self.test_linkedin_ideas = [
            "Develop a tool for remote team collaboration",
            "Project: Automated social media scheduler",
            "Idea: Blockchain-based supply chain tracker"
        ]

    def test_scrape_reddit_mock(self):
        """Test Reddit scraping with mock data."""
        with patch('sparkscraper.reddit') as mock_reddit:
            # Mock the subreddit and search results
            mock_subreddit = Mock()
            mock_submission1 = Mock()
            mock_submission1.title = "Build a weather app with real-time alerts"
            mock_submission2 = Mock()
            mock_submission2.title = "Random post about cats"
            mock_submission3 = Mock()
            mock_submission3.title = "Project idea: AI chatbot for customer service"
            
            mock_subreddit.search.return_value = [mock_submission1, mock_submission2, mock_submission3]
            mock_reddit.subreddit.return_value = mock_subreddit
            
            result = scrape_reddit("sideprojects", "project ideas", limit=3)
            
            # Should only return posts with "project" or "idea" in title
            expected = [
                "Build a weather app with real-time alerts",
                "Project idea: AI chatbot for customer service"
            ]
            self.assertEqual(result, expected)

    def test_scrape_twitter_mock(self):
        """Test Twitter scraping with mock data."""
        with patch('sparkscraper.twitter_api') as mock_api:
            # Mock tweet objects
            mock_tweet1 = Mock()
            mock_tweet1.full_text = "Idea: A platform to connect indie game devs with artists"
            mock_tweet2 = Mock()
            mock_tweet2.full_text = "Just had coffee"
            mock_tweet3 = Mock()
            mock_tweet3.full_text = "Project idea: AI-powered personal finance tracker"
            
            mock_api.search_tweets.return_value = [mock_tweet1, mock_tweet2, mock_tweet3]
            
            result = scrape_twitter("project ideas", count=3)
            
            expected = [
                "Idea: A platform to connect indie game devs with artists",
                "Project idea: AI-powered personal finance tracker"
            ]
            self.assertEqual(result, expected)

    def test_scrape_linkedin_mock(self):
        """Test LinkedIn scraping with mock data."""
        with patch('sparkscraper.requests.get') as mock_get:
            # Mock HTML response
            mock_response = Mock()
            mock_response.text = '''
            <html>
                <div class="search-result__info">Develop a tool for remote team collaboration</div>
                <div class="search-result__info">Random post about weather</div>
                <div class="search-result__info">Project: Automated social media scheduler</div>
            </html>
            '''
            mock_get.return_value = mock_response
            
            result = scrape_linkedin("project ideas")
            
            expected = [
                "Develop a tool for remote team collaboration",
                "Project: Automated social media scheduler"
            ]
            self.assertEqual(result, expected)

    def test_generate_markdown(self):
        """Test markdown generation with temporary file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as temp_file:
            temp_filename = temp_file.name
        
        try:
            generate_markdown(self.test_reddit_ideas, self.test_twitter_ideas, self.test_linkedin_ideas)
            
            # Read the generated file
            with open("sparkscraper_ideas.md", 'r') as f:
                content = f.read()
            
            # Check if all sections are present
            self.assertIn("# SparkScraper Project Ideas", content)
            self.assertIn("## From Reddit", content)
            self.assertIn("## From Twitter/X", content)
            self.assertIn("## From LinkedIn", content)
            
            # Check if ideas are included
            self.assertIn("Build a weather app with real-time alerts", content)
            self.assertIn("Idea: A platform to connect indie game devs with artists", content)
            self.assertIn("Develop a tool for remote team collaboration", content)
            
        finally:
            # Clean up
            if os.path.exists("sparkscraper_ideas.md"):
                os.remove("sparkscraper_ideas.md")

    def test_empty_results(self):
        """Test handling of empty results."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as temp_file:
            temp_filename = temp_file.name
        
        try:
            generate_markdown([], [], [])
            
            with open("sparkscraper_ideas.md", 'r') as f:
                content = f.read()
            
            # Should still generate the header
            self.assertIn("# SparkScraper Project Ideas", content)
            self.assertIn("## From Reddit", content)
            self.assertIn("## From Twitter/X", content)
            self.assertIn("## From LinkedIn", content)
            
        finally:
            if os.path.exists("sparkscraper_ideas.md"):
                os.remove("sparkscraper_ideas.md")

    def test_keyword_filtering(self):
        """Test that only relevant posts are filtered."""
        test_posts = [
            "Build a weather app with real-time alerts",
            "Random post about cats",
            "Project idea: AI chatbot",
            "Just sharing a photo",
            "Idea: New startup concept",
            "Today's weather is nice"
        ]
        
        # Simulate the filtering logic
        filtered = [post for post in test_posts 
                   if "project" in post.lower() or "idea" in post.lower()]
        
        expected = [
            "Build a weather app with real-time alerts",
            "Project idea: AI chatbot",
            "Idea: New startup concept"
        ]
        
        self.assertEqual(filtered, expected)

if __name__ == '__main__':
    unittest.main() 