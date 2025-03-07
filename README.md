# SparkScraper

**SparkScraper** is a Python-based tool that scrapes Reddit, Twitter (X), and LinkedIn to extract project ideas and compiles them into a neatly formatted Markdown file. Whether you're a developer, entrepreneur, or hobbyist looking for inspiration, SparkScraper harvests creative sparks from the web!

## Features
- **Multi-Platform Scraping**: Gathers project ideas from Reddit, X/Twitter, and LinkedIn.
- **Markdown Output**: Saves results in an organized `sparkscraper_ideas.md` file.
- **Customizable**: Adjust keywords and sources to fit your needs.
- **Simple & Lightweight**: Built with Python and minimal dependencies.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/makalin/sparkscraper.git
   cd sparkscraper
   ```

2. **Install Dependencies**:
   ```bash
   pip install praw tweepy requests beautifulsoup4
   ```

3. **Set Up API Keys**:
   - **Reddit**: Register an app at [Reddit Apps](https://www.reddit.com/prefs/apps) and update `client_id`, `client_secret`, and `user_agent`.
   - **Twitter/X**: Get API keys from [Twitter Developer Portal](https://developer.twitter.com) and fill in `consumer_key`, `consumer_secret`, `access_token`, and `access_token_secret`.
   - **LinkedIn**: Scraping-based (no API); use with caution.

4. **Update the Code**:
   Replace placeholders in `sparkscraper.py` with your credentials.

## Usage

Run the script with default settings:
```bash
python sparkscraper.py
```

- **Customize**: Edit `keyword` and `subreddit` variables in the script to target specific topics or communities.
- **Output**: Check `sparkscraper_ideas.md` for the results.

Example output:
```markdown
# SparkScraper Project Ideas

Generated by SparkScraper - Harvesting inspiration from the web!

## From Reddit
1. Build a weather app with real-time alerts

## From Twitter/X
1. Idea: A platform to connect indie game devs with artists

## From LinkedIn
1. Develop a tool for remote team collaboration
```

## Requirements
- Python 3.x
- Libraries: `praw`, `tweepy`, `requests`, `beautifulsoup4`

## Notes
- **LinkedIn Scraping**: Limited by lack of a public API. Use responsibly and respect Terms of Service.
- **Rate Limits**: APIs have restrictions; add delays (e.g., `time.sleep()`) if needed.
- **Legal**: Ensure compliance with each platform's policies.

## Contributing
Feel free to fork, submit issues, or send pull requests! Ideas for enhancements:
- NLP filtering for better idea detection.
- GUI for easier use.
- Database storage for large-scale scraping.

## License
MIT License - See [LICENSE](LICENSE) for details.
