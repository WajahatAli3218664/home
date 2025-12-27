from typing import List
from .config import Config


def get_all_urls() -> List[str]:
    """
    Retrieve the list of URLs to be processed
    
    Returns:
        List of URL strings from configuration
    """
    return Config.SOURCE_URLS