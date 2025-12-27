import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from .logging_config import logger


def extract_text_from_urls(urls: List[str]) -> Dict[str, str]:
    """
    Extract clean text content from a list of URLs
    
    Args:
        urls: List of URL strings
        
    Returns:
        Dictionary mapping URL to extracted content (Dict[str, str])
    """
    results = {}
    
    for url in urls:
        try:
            logger.info(f"Processing URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Try to find main content area in Docusaurus sites
            # Docusaurus typically has content in these selectors
            content_selectors = [
                'main div[class*="docItem"]',  # Docusaurus doc item content
                'article',  # General article content
                'main',  # Main content area
                'div[class*="container"]',  # Container with content
                'div[class*="content"]',  # Content class
                'div[class*="markdown"]',  # Markdown content
                'div[class*="theme"]',  # Docusaurus theme content
                'div[data-testid="doc-content"]',  # Docusaurus specific test id
                'div[class*="doc"]'  # Document-related classes
            ]
            
            content = None
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    break
            
            # If no content found with selectors, use body
            if not content:
                content = soup.body
            
            if content:
                # Get text and clean it up
                text = content.get_text(separator=' ')
                
                # Clean up the text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                results[url] = text
                logger.info(f"Successfully extracted {len(text)} characters from {url}")
            else:
                logger.warning(f"No content found for URL: {url}")
                results[url] = ""
                
        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            results[url] = ""
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")
            results[url] = ""
    
    return results