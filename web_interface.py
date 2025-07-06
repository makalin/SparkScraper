"""
Web Interface for SparkScraper
Simple Flask-based web interface for running the scraper
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from sparkscraper_enhanced import EnhancedSparkScraper
from config import SparkScraperConfig

app = Flask(__name__)

# Global scraper instance
scraper = None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/config')
def get_config():
    """Get current configuration"""
    validation = SparkScraperConfig.validate_config()
    return jsonify({
        'validation': validation,
        'default_keywords': SparkScraperConfig.DEFAULT_KEYWORDS,
        'default_subreddits': SparkScraperConfig.DEFAULT_SUBREDDITS,
        'output_formats': SparkScraperConfig.OUTPUT_FORMATS
    })

@app.route('/api/scrape', methods=['POST'])
def scrape():
    """Run the scraper"""
    global scraper
    
    try:
        data = request.get_json()
        keywords = data.get('keywords', SparkScraperConfig.get_keywords())
        subreddits = data.get('subreddits', SparkScraperConfig.get_subreddits())
        output_formats = data.get('output_formats', ['markdown'])
        
        # Initialize scraper
        scraper = EnhancedSparkScraper()
        
        # Run scraping
        results = scraper.run(keywords, subreddits, output_formats)
        
        return jsonify({
            'success': True,
            'message': f'Successfully scraped {len(results)} ideas',
            'results_count': len(results),
            'output_files': [fmt for fmt in output_formats]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download/<format>')
def download_file(format):
    """Download generated files"""
    filename = f"sparkscraper_ideas.{format}"
    
    if not os.path.exists(filename):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filename, as_attachment=True)

@app.route('/api/sample')
def generate_sample():
    """Generate sample output"""
    global scraper
    
    try:
        from test_sparkscraper import TestSparkScraper
        
        # Create test instance
        test_instance = TestSparkScraper()
        test_instance.setUp()
        
        # Create scraper and process sample data
        scraper = EnhancedSparkScraper()
        all_ideas = (
            scraper.processor.process_ideas(test_instance.test_reddit_ideas, "reddit") +
            scraper.processor.process_ideas(test_instance.test_twitter_ideas, "twitter") +
            scraper.processor.process_ideas(test_instance.test_linkedin_ideas, "linkedin")
        )
        
        # Save in all formats
        scraper.save_output(all_ideas, ['markdown', 'json', 'csv'])
        
        return jsonify({
            'success': True,
            'message': 'Sample files generated successfully',
            'files': ['sparkscraper_ideas.md', 'sparkscraper_ideas.json', 'sparkscraper_ideas.csv']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create basic HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SparkScraper Web Interface</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        input[type="text"], textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        textarea {
            height: 100px;
            resize: vertical;
        }
        .checkbox-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }
        button:hover {
            background-color: #2980b9;
        }
        button:disabled {
            background-color: #bdc3c7;
            cursor: not-allowed;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            display: none;
        }
        .status.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .download-links {
            margin-top: 20px;
        }
        .download-links a {
            display: inline-block;
            margin-right: 10px;
            padding: 8px 16px;
            background-color: #27ae60;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .download-links a:hover {
            background-color: #229954;
        }
        .config-status {
            margin-bottom: 20px;
            padding: 15px;
            background-color: #e8f4fd;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 SparkScraper Web Interface</h1>
        
        <div class="config-status" id="configStatus">
            <strong>Configuration Status:</strong> Loading...
        </div>
        
        <form id="scrapeForm">
            <div class="form-group">
                <label for="keywords">Keywords (comma-separated):</label>
                <textarea id="keywords" name="keywords" placeholder="project ideas, startup ideas, side project"></textarea>
            </div>
            
            <div class="form-group">
                <label for="subreddits">Subreddits (comma-separated):</label>
                <textarea id="subreddits" name="subreddits" placeholder="sideprojects, startups, entrepreneur"></textarea>
            </div>
            
            <div class="form-group">
                <label>Output Formats:</label>
                <div class="checkbox-group">
                    <div class="checkbox-item">
                        <input type="checkbox" id="markdown" name="output_formats" value="markdown" checked>
                        <label for="markdown">Markdown</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="json" name="output_formats" value="json">
                        <label for="json">JSON</label>
                    </div>
                    <div class="checkbox-item">
                        <input type="checkbox" id="csv" name="output_formats" value="csv">
                        <label for="csv">CSV</label>
                    </div>
                </div>
            </div>
            
            <button type="submit" id="scrapeBtn">Start Scraping</button>
            <button type="button" id="sampleBtn">Generate Sample</button>
        </form>
        
        <div class="status" id="status"></div>
        <div class="download-links" id="downloadLinks"></div>
    </div>

    <script>
        // Load configuration on page load
        fetch('/api/config')
            .then(response => response.json())
            .then(data => {
                const configStatus = document.getElementById('configStatus');
                const validation = data.validation;
                
                let statusHtml = '<strong>Configuration Status:</strong><br>';
                for (const [service, configured] of Object.entries(validation)) {
                    const status = configured ? '✅ Configured' : '❌ Not Configured';
                    statusHtml += `${service.replace('_', ' ').toUpperCase()}: ${status}<br>`;
                }
                
                configStatus.innerHTML = statusHtml;
                
                // Set default values
                document.getElementById('keywords').value = data.default_keywords.join(', ');
                document.getElementById('subreddits').value = data.default_subreddits.join(', ');
            })
            .catch(error => {
                console.error('Error loading config:', error);
            });

        // Handle form submission
        document.getElementById('scrapeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const scrapeBtn = document.getElementById('scrapeBtn');
            const status = document.getElementById('status');
            const downloadLinks = document.getElementById('downloadLinks');
            
            // Get form data
            const keywords = document.getElementById('keywords').value.split(',').map(k => k.trim()).filter(k => k);
            const subreddits = document.getElementById('subreddits').value.split(',').map(s => s.trim()).filter(s => s);
            const outputFormats = Array.from(document.querySelectorAll('input[name="output_formats"]:checked')).map(cb => cb.value);
            
            // Disable button and show loading
            scrapeBtn.disabled = true;
            scrapeBtn.textContent = 'Scraping...';
            status.style.display = 'none';
            downloadLinks.innerHTML = '';
            
            // Send request
            fetch('/api/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    keywords: keywords,
                    subreddits: subreddits,
                    output_formats: outputFormats
                })
            })
            .then(response => response.json())
            .then(data => {
                status.style.display = 'block';
                
                if (data.success) {
                    status.className = 'status success';
                    status.textContent = data.message;
                    
                    // Show download links
                    let linksHtml = '<strong>Download Files:</strong><br>';
                    data.output_files.forEach(format => {
                        linksHtml += `<a href="/api/download/${format}" target="_blank">Download ${format.toUpperCase()}</a>`;
                    });
                    downloadLinks.innerHTML = linksHtml;
                } else {
                    status.className = 'status error';
                    status.textContent = 'Error: ' + data.error;
                }
            })
            .catch(error => {
                status.style.display = 'block';
                status.className = 'status error';
                status.textContent = 'Error: ' + error.message;
            })
            .finally(() => {
                scrapeBtn.disabled = false;
                scrapeBtn.textContent = 'Start Scraping';
            });
        });

        // Handle sample generation
        document.getElementById('sampleBtn').addEventListener('click', function() {
            const sampleBtn = this;
            const status = document.getElementById('status');
            const downloadLinks = document.getElementById('downloadLinks');
            
            sampleBtn.disabled = true;
            sampleBtn.textContent = 'Generating...';
            status.style.display = 'none';
            downloadLinks.innerHTML = '';
            
            fetch('/api/sample')
                .then(response => response.json())
                .then(data => {
                    status.style.display = 'block';
                    
                    if (data.success) {
                        status.className = 'status success';
                        status.textContent = data.message;
                        
                        // Show download links
                        let linksHtml = '<strong>Download Sample Files:</strong><br>';
                        data.files.forEach(filename => {
                            const format = filename.split('.').pop();
                            linksHtml += `<a href="/api/download/${format}" target="_blank">Download ${format.toUpperCase()}</a>`;
                        });
                        downloadLinks.innerHTML = linksHtml;
                    } else {
                        status.className = 'status error';
                        status.textContent = 'Error: ' + data.error;
                    }
                })
                .catch(error => {
                    status.style.display = 'block';
                    status.className = 'status error';
                    status.textContent = 'Error: ' + error.message;
                })
                .finally(() => {
                    sampleBtn.disabled = false;
                    sampleBtn.textContent = 'Generate Sample';
                });
        });
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w') as f:
        f.write(html_template)
    
    print("🌐 Starting SparkScraper Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 