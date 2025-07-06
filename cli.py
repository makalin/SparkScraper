"""
Command Line Interface for SparkScraper
Provides a user-friendly way to run the scraper with various options
"""

import click
import os
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv
from sparkscraper_enhanced import EnhancedSparkScraper
from config import SparkScraperConfig

# Load environment variables
load_dotenv()

console = Console()

@click.group()
@click.version_option(version="2.0.0", prog_name="SparkScraper")
def cli():
    """SparkScraper - Harvest project ideas from Reddit, Twitter, and LinkedIn"""
    pass

@cli.command()
@click.option('--keywords', '-k', help='Comma-separated keywords to search for')
@click.option('--subreddits', '-s', help='Comma-separated subreddits to search')
@click.option('--output', '-o', multiple=True, 
              type=click.Choice(['markdown', 'json', 'csv']), 
              default=['markdown'], 
              help='Output formats (can specify multiple)')
@click.option('--limit', '-l', default=100, help='Maximum number of posts per source')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def scrape(keywords, subreddits, output, limit, verbose):
    """Scrape project ideas from multiple sources"""
    
    # Display welcome message
    welcome_text = Text("🚀 SparkScraper v2.0", style="bold blue")
    console.print(Panel(welcome_text, title="Welcome"))
    
    # Parse keywords and subreddits
    if keywords:
        keywords_list = [k.strip() for k in keywords.split(',')]
    else:
        keywords_list = SparkScraperConfig.get_keywords()
    
    if subreddits:
        subreddits_list = [s.strip() for s in subreddits.split(',')]
    else:
        subreddits_list = SparkScraperConfig.get_subreddits()
    
    # Display configuration
    config_table = Table(title="Configuration")
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Value", style="green")
    
    config_table.add_row("Keywords", ", ".join(keywords_list[:3]) + ("..." if len(keywords_list) > 3 else ""))
    config_table.add_row("Subreddits", ", ".join(subreddits_list[:3]) + ("..." if len(subreddits_list) > 3 else ""))
    config_table.add_row("Output Formats", ", ".join(output))
    config_table.add_row("Post Limit", str(limit))
    
    console.print(config_table)
    
    # Validate configuration
    validation = SparkScraperConfig.validate_config()
    validation_table = Table(title="API Configuration Status")
    validation_table.add_column("Service", style="cyan")
    validation_table.add_column("Status", style="green")
    
    for service, configured in validation.items():
        status = "✅ Configured" if configured else "❌ Not Configured"
        validation_table.add_row(service.replace("_", " ").title(), status)
    
    console.print(validation_table)
    
    # Confirm before proceeding
    if not click.confirm("Do you want to proceed with scraping?"):
        console.print("Scraping cancelled.")
        return
    
    # Run scraper with progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Initializing scraper...", total=None)
        
        try:
            scraper = EnhancedSparkScraper()
            
            progress.update(task, description="Scraping Reddit...")
            reddit_ideas = scraper.scrape_reddit_enhanced(subreddits_list, keywords_list)
            
            progress.update(task, description="Scraping Twitter...")
            twitter_ideas = scraper.scrape_twitter_enhanced(keywords_list)
            
            progress.update(task, description="Scraping LinkedIn...")
            linkedin_ideas = scraper.scrape_linkedin_enhanced(keywords_list)
            
            progress.update(task, description="Processing and saving results...")
            
            all_ideas = reddit_ideas + twitter_ideas + linkedin_ideas
            scraper.save_output(all_ideas, output)
            
            progress.update(task, description="Complete!")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return
    
    # Display results summary
    results_table = Table(title="Scraping Results")
    results_table.add_column("Source", style="cyan")
    results_table.add_column("Ideas Found", style="green")
    
    results_table.add_row("Reddit", str(len(reddit_ideas)))
    results_table.add_row("Twitter", str(len(twitter_ideas)))
    results_table.add_row("LinkedIn", str(len(linkedin_ideas)))
    results_table.add_row("Total", str(len(all_ideas)))
    
    console.print(results_table)
    
    # Show output files
    output_files = []
    for fmt in output:
        if fmt == "markdown":
            output_files.append("sparkscraper_ideas.md")
        elif fmt == "json":
            output_files.append("sparkscraper_ideas.json")
        elif fmt == "csv":
            output_files.append("sparkscraper_ideas.csv")
    
    console.print(f"\n[green]Output saved to:[/green] {', '.join(output_files)}")

@cli.command()
def config():
    """Show current configuration"""
    console.print(Panel("🔧 SparkScraper Configuration", style="bold blue"))
    
    # API Configuration
    api_table = Table(title="API Configuration")
    api_table.add_column("Service", style="cyan")
    api_table.add_column("Status", style="green")
    
    validation = SparkScraperConfig.validate_config()
    for service, configured in validation.items():
        status = "✅ Configured" if configured else "❌ Not Configured"
        api_table.add_row(service.replace("_", " ").title(), status)
    
    console.print(api_table)
    
    # Default Settings
    settings_table = Table(title="Default Settings")
    settings_table.add_column("Setting", style="cyan")
    settings_table.add_column("Value", style="green")
    
    settings_table.add_row("Default Keywords", ", ".join(SparkScraperConfig.DEFAULT_KEYWORDS[:3]) + "...")
    settings_table.add_row("Default Subreddits", ", ".join(SparkScraperConfig.DEFAULT_SUBREDDITS[:3]) + "...")
    settings_table.add_row("Rate Limit Delay", f"{SparkScraperConfig.RATE_LIMIT_DELAY}s")
    settings_table.add_row("Max Reddit Posts", str(SparkScraperConfig.MAX_REDDIT_POSTS))
    settings_table.add_row("Max Twitter Tweets", str(SparkScraperConfig.MAX_TWITTER_TWEETS))
    
    console.print(settings_table)

@cli.command()
@click.option('--format', '-f', type=click.Choice(['markdown', 'json', 'csv']), 
              default='markdown', help='Output format for the sample')
def sample(format):
    """Generate a sample output file with mock data"""
    from test_sparkscraper import TestSparkScraper
    
    console.print("Generating sample output...")
    
    # Create test instance to get sample data
    test_instance = TestSparkScraper()
    test_instance.setUp()
    
    # Create mock scraper and save sample
    scraper = EnhancedSparkScraper()
    all_ideas = (
        scraper.processor.process_ideas(test_instance.test_reddit_ideas, "reddit") +
        scraper.processor.process_ideas(test_instance.test_twitter_ideas, "twitter") +
        scraper.processor.process_ideas(test_instance.test_linkedin_ideas, "linkedin")
    )
    
    scraper.save_output(all_ideas, [format])
    
    console.print(f"[green]Sample {format} file generated successfully![/green]")

@cli.command()
def test():
    """Run the test suite"""
    import pytest
    import sys
    
    console.print("Running test suite...")
    
    # Run tests
    exit_code = pytest.main(["-v", "test_sparkscraper.py"])
    
    if exit_code == 0:
        console.print("[green]All tests passed![/green]")
    else:
        console.print("[red]Some tests failed![/red]")
        sys.exit(exit_code)

@cli.command()
def setup():
    """Interactive setup for API keys"""
    console.print(Panel("🔑 SparkScraper Setup", style="bold blue"))
    
    console.print("This will help you set up your API keys for SparkScraper.\n")
    
    # Reddit setup
    console.print("[cyan]Reddit API Setup:[/cyan]")
    console.print("1. Go to https://www.reddit.com/prefs/apps")
    console.print("2. Click 'Create App' or 'Create Another App'")
    console.print("3. Fill in the details and get your credentials\n")
    
    reddit_client_id = click.prompt("Reddit Client ID", type=str)
    reddit_client_secret = click.prompt("Reddit Client Secret", type=str, hide_input=True)
    reddit_user_agent = click.prompt("Reddit User Agent", 
                                   default="SparkScraper v2.0 by /u/YOUR_USERNAME", type=str)
    
    # Twitter setup
    console.print("\n[cyan]Twitter API Setup:[/cyan]")
    console.print("1. Go to https://developer.twitter.com")
    console.print("2. Create a new app and get your credentials\n")
    
    twitter_consumer_key = click.prompt("Twitter Consumer Key", type=str)
    twitter_consumer_secret = click.prompt("Twitter Consumer Secret", type=str, hide_input=True)
    twitter_access_token = click.prompt("Twitter Access Token", type=str)
    twitter_access_token_secret = click.prompt("Twitter Access Token Secret", type=str, hide_input=True)
    
    # Create .env file
    env_content = f"""# SparkScraper Environment Variables
REDDIT_CLIENT_ID={reddit_client_id}
REDDIT_CLIENT_SECRET={reddit_client_secret}
REDDIT_USER_AGENT={reddit_user_agent}

TWITTER_CONSUMER_KEY={twitter_consumer_key}
TWITTER_CONSUMER_SECRET={twitter_consumer_secret}
TWITTER_ACCESS_TOKEN={twitter_access_token}
TWITTER_ACCESS_TOKEN_SECRET={twitter_access_token_secret}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    console.print("\n[green]✅ Setup complete![/green]")
    console.print("Your API keys have been saved to .env file.")
    console.print("You can now run: python cli.py scrape")

if __name__ == '__main__':
    cli() 