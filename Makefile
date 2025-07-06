# SparkScraper Makefile
# Common development tasks

.PHONY: help install test lint clean run-cli run-web run-legacy setup sample

# Default target
help:
	@echo "SparkScraper - Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install     - Install dependencies"
	@echo "  setup       - Interactive API setup"
	@echo ""
	@echo "Running:"
	@echo "  run-cli     - Run CLI interface"
	@echo "  run-web     - Run web interface"
	@echo "  run-legacy  - Run original scraper"
	@echo ""
	@echo "Development:"
	@echo "  test        - Run test suite"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean generated files"
	@echo ""
	@echo "Utilities:"
	@echo "  sample      - Generate sample output"
	@echo "  config      - Show configuration"

# Installation
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

setup:
	@echo "Running interactive setup..."
	python cli.py setup

# Running the application
run-cli:
	@echo "Starting CLI interface..."
	python cli.py scrape

run-web:
	@echo "Starting web interface..."
	python web_interface.py

run-legacy:
	@echo "Running legacy scraper..."
	python sparkscraper.py

# Development tasks
test:
	@echo "Running tests..."
	python -m pytest test_sparkscraper.py -v

lint:
	@echo "Running linting..."
	flake8 *.py
	mypy *.py --ignore-missing-imports

format:
	@echo "Formatting code..."
	black *.py

clean:
	@echo "Cleaning generated files..."
	rm -f sparkscraper_ideas.md
	rm -f sparkscraper_ideas.json
	rm -f sparkscraper_ideas.csv
	rm -f sparkscraper.log
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache

# Utilities
sample:
	@echo "Generating sample output..."
	python cli.py sample

config:
	@echo "Showing configuration..."
	python cli.py config

# Development environment setup
dev-setup: install
	@echo "Setting up development environment..."
	pip install -r requirements.txt
	@echo "Development environment ready!"

# Quick start
quick-start: install setup
	@echo "Quick start complete!"
	@echo "Run 'make run-cli' to start scraping" 