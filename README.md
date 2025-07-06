# SparkScraper

**SparkScraper** is a Python-based tool that scrapes Reddit, Twitter (X), and LinkedIn to extract project ideas and compiles them into multiple formats. Whether you're a developer, entrepreneur, or hobbyist looking for inspiration, SparkScraper harvests creative sparks from the web!

## ✨ Features

### Core Features
- **Multi-Platform Scraping**: Gathers project ideas from Reddit, X/Twitter, and LinkedIn
- **Multiple Output Formats**: Markdown, JSON, and CSV output options
- **Idea Categorization**: Automatically categorizes ideas (web apps, mobile apps, AI/ML, fintech, etc.)
- **Sentiment Analysis**: Analyzes the sentiment of each idea
- **Duplicate Detection**: Removes duplicate ideas using intelligent hashing
- **Quality Filtering**: Filters out spam and low-quality content

### Advanced Features
- **CLI Interface**: User-friendly command-line interface with rich output
- **Web Interface**: Simple Flask-based web GUI
- **Configuration Management**: Centralized config with environment variable support
- **Rate Limiting**: Respects API rate limits with configurable delays
- **Logging**: Comprehensive logging for debugging and monitoring
- **Testing Suite**: Complete test coverage with mock data

### Output Enhancements
- **Structured Data**: Rich metadata including source, categories, sentiment, and timestamps
- **Multiple Formats**: Choose from Markdown, JSON, or CSV output
- **Organized Results**: Ideas grouped by source and category
- **Statistics**: Summary statistics and insights

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/makalin/sparkscraper.git
   cd sparkscraper
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys**:
   - **Reddit**: Register an app at [Reddit Apps](https://www.reddit.com/prefs/apps) and update `client_id`, `client_secret`, and `user_agent`.
   - **Twitter/X**: Get API keys from [Twitter Developer Portal](https://developer.twitter.com) and fill in `consumer_key`, `consumer_secret`, `access_token`, and `access_token_secret`.
   - **LinkedIn**: Scraping-based (no API); use with caution.

4. **Set Up API Keys** (Choose one method):

   **Method A: Interactive Setup**
   ```bash
   python cli.py setup
   ```

   **Method B: Manual Setup**
   Create a `.env` file in the project root:
   ```bash
   # Reddit API
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=SparkScraper v2.0 by /u/your_username

   # Twitter API
   TWITTER_CONSUMER_KEY=your_consumer_key
   TWITTER_CONSUMER_SECRET=your_consumer_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   ```

## Usage

### Command Line Interface (Recommended)

**Basic Usage:**
```bash
python cli.py scrape
```

**Advanced Usage:**
```bash
# Custom keywords and subreddits
python cli.py scrape --keywords "AI projects,startup ideas" --subreddits "sideprojects,entrepreneur"

# Multiple output formats
python cli.py scrape --output markdown json csv

# Custom post limit
python cli.py scrape --limit 50
```

**Other Commands:**
```bash
# Show configuration
python cli.py config

# Generate sample output
python cli.py sample --format json

# Run tests
python cli.py test

# Interactive setup
python cli.py setup
```

### Web Interface

Start the web interface:
```bash
python web_interface.py
```

Then open your browser to `http://localhost:5000`

### Legacy Usage

Run the original script:
```bash
python sparkscraper.py
```

Example output:
```markdown
# SparkScraper Project Ideas

Generated on: 2024-01-15 14:30:25
Total ideas found: 45

## From Reddit

### Web App
1. Build a weather app with real-time alerts 😊
2. Create a project management tool for freelancers 😊

### AI/ML
1. AI-powered personal finance tracker 😊

## From Twitter/X

### Social
1. Idea: A platform to connect indie game devs with artists 😊

### Productivity
1. Project idea: Automated social media scheduler 😊

## From LinkedIn

### Productivity
1. Develop a tool for remote team collaboration 😊
```

**JSON Output Example:**
```json
{
  "metadata": {
    "generated_at": "2024-01-15T14:30:25.123456",
    "total_ideas": 45,
    "sources": ["reddit", "twitter", "linkedin"],
    "categories": ["web_app", "ai_ml", "social", "productivity"]
  },
  "ideas": [
    {
      "text": "Build a weather app with real-time alerts",
      "source": "reddit",
      "categories": ["web_app"],
      "sentiment": 0.3,
      "word_count": 8,
      "timestamp": "2024-01-15T14:30:25.123456"
    }
  ]
}
```

## Requirements
- Python 3.8+
- See `requirements.txt` for complete dependency list

## Project Structure
```
SparkScraper/
├── sparkscraper.py              # Original scraper
├── sparkscraper_enhanced.py     # Enhanced version with advanced features
├── cli.py                       # Command-line interface
├── web_interface.py             # Web GUI
├── config.py                    # Configuration management
├── test_sparkscraper.py         # Test suite
├── requirements.txt             # Dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

## Notes
- **LinkedIn Scraping**: Limited by lack of a public API. Use responsibly and respect Terms of Service.
- **Rate Limits**: APIs have restrictions; add delays (e.g., `time.sleep()`) if needed.
- **Legal**: Ensure compliance with each platform's policies.

## Contributing
Feel free to fork, submit issues, or send pull requests! Ideas for enhancements:
- **NLP Enhancement**: Better idea detection using advanced NLP models
- **Database Integration**: SQLite/PostgreSQL storage for large-scale scraping
- **Scheduling**: Automated scraping with cron jobs
- **API Endpoints**: REST API for integration with other tools
- **Analytics Dashboard**: Web dashboard with charts and insights
- **Export Options**: PDF, Excel, or other format exports
- **Machine Learning**: ML-based idea ranking and recommendation
- **Social Features**: Share and collaborate on ideas
- **Mobile App**: React Native or Flutter mobile interface
- **Plugin System**: Extensible architecture for custom scrapers

## License
MIT License - See [LICENSE](LICENSE) for details.

Ignite Your Next Big Idea with SparkScraper!