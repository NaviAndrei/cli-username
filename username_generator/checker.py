import requests
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
from .config import get_config_value

# Generic User-Agent to avoid simple bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# Common keywords that indicate a username might be available (Not Found)
NOT_FOUND_KEYWORDS = [
    "404", "not found", "doesn't exist", "couldn't find", 
    "page not found", "unavailable", "site not found",
    "nobody on reddit goes by that name", "user not found"
]

def check_individual_platform(platform: str, url_template: str, username: str, session: requests.Session) -> Tuple[str, str]:
    """Checks a single platform for username availability."""
    url = url_template.format(username=username)
    try:
        response = session.get(url, headers=HEADERS, timeout=5, allow_redirects=True)
        content_lower = response.text.lower()
        
        if response.status_code == 404:
            return platform, "AVAILABLE"
        elif any(keyword in content_lower for keyword in NOT_FOUND_KEYWORDS):
            return platform, "AVAILABLE"
        elif "login" in response.url.lower() or "accounts/login" in response.url.lower():
            return platform, "BLOCKED/WAF"
        elif response.status_code == 200:
            return platform, "TAKEN"
        elif response.status_code in [403, 429]:
            return platform, "BLOCKED/WAF"
        else:
            return platform, f"ERROR:{response.status_code}"
    except requests.RequestException:
        return platform, "TIMEOUT/FAIL"

def check_username_availability(username: str, platforms: Optional[List[str]] = None) -> Dict[str, str]:
    """Checks if a username is available across multiple platforms using multi-threading.
    
    Args:
        username: The username to check.
        platforms: List of platforms to check. If None, checks all configured targets.
        
    Returns:
        Dict[str, str]: A dictionary mapping platform name to status.
    """
    all_targets = get_config_value("check_targets", {})
    
    if platforms:
        targets = {k: v for k, v in all_targets.items() if k in platforms}
    else:
        targets = all_targets
        
    results = {}
    session = requests.Session()
    
    # Use ThreadPoolExecutor for parallel network requests
    with ThreadPoolExecutor(max_workers=min(len(targets), 10)) as executor:
        futures = [
            executor.submit(check_individual_platform, p, url, username, session)
            for p, url in targets.items()
        ]
        
        for future in futures:
            p, status = future.result()
            results[p] = status
            
    return results
