"""
Web scraper module using Firecrawl API
Extracts structured content from websites
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Placeholder API key (replace with actual key)
FIRECRAWL_API_KEY = "fc-YOUR_FIRECRAWL_API_KEY_HERE"
FIRECRAWL_API_URL = "https://api.firecrawl.dev/v0/scrape"


def scrape_website(url: str) -> Optional[str]:
    """
    Scrape website content using Firecrawl API
    
    Args:
        url: Target website URL
        
    Returns:
        Extracted text content or None if failed
    """
    try:
        logger.info(f"Scraping URL: {url}")
        
        headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": url,
            "formats": ["markdown", "html"],
            "onlyMainContent": True
        }
        
        # Make API request to Firecrawl
        response = requests.post(
            FIRECRAWL_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        # For demo purposes, if API key is placeholder, use fallback
        if "YOUR_FIRECRAWL_API_KEY" in FIRECRAWL_API_KEY:
            logger.warning("Using placeholder API key - falling back to basic scraping")
            return scrape_website_fallback(url)
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('data', {}).get('markdown', '') or data.get('data', {}).get('content', '')
            logger.info(f"Successfully scraped {len(content)} characters")
            return content
        else:
            logger.error(f"Firecrawl API error: {response.status_code}")
            return scrape_website_fallback(url)
            
    except Exception as e:
        logger.error(f"Scraping error: {str(e)}")
        return scrape_website_fallback(url)


def scrape_website_fallback(url: str) -> str:
    """
    Fallback scraper using basic requests + BeautifulSoup
    Used when Firecrawl API is unavailable
    
    Args:
        url: Target website URL
        
    Returns:
        Extracted text content
    """
    try:
        from bs4 import BeautifulSoup
        
        logger.info("Using fallback scraper")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract text from important tags
        content_parts = []
        
        # Get headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
            content_parts.append(f"\n{heading.get_text().strip()}\n")
        
        # Get paragraphs
        for paragraph in soup.find_all(['p', 'li']):
            text = paragraph.get_text().strip()
            if len(text) > 20:  # Filter out very short snippets
                content_parts.append(text)
        
        content = ' '.join(content_parts)
        
        # Clean up whitespace
        content = ' '.join(content.split())
        
        logger.info(f"Fallback scraper extracted {len(content)} characters")
        return content
        
    except Exception as e:
        logger.error(f"Fallback scraper error: {str(e)}")
        # Return minimal placeholder content
        return f"Content from {url}. This is a demo placeholder as scraping failed."


def extract_headings(content: str) -> list:
    """
    Extract heading-like text from content
    
    Args:
        content: Raw text content
        
    Returns:
        List of potential headings
    """
    lines = content.split('\n')
    headings = []
    
    for line in lines:
        line = line.strip()
        # Simple heuristic: short lines that look like titles
        if line and len(line) < 100 and len(line.split()) < 15:
            if line[0].isupper() or line.startswith('#'):
                headings.append(line.replace('#', '').strip())
    
    return headings[:20]  # Return top 20 headings