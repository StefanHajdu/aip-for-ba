import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from time import sleep

# Global variables
visited = set()
domain = "https://services8.arcgis.com/pRlN1m0su5BYaFAS/ArcGIS/rest/services"

# Function to download and save a webpage
def save_page(url, content):
    parsed_url = urlparse(url)
    path = parsed_url.path if parsed_url.path else "index.html"
    
    # Create directories if they don't exist
    if not path.endswith(".html"):
        path = os.path.join(path, "index.html")
    
    local_path = os.path.join("./data", parsed_url.netloc, path.strip("/"))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    # Save the HTML content
    with open(local_path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Saved: {url} -> {local_path}")

# Function to fetch and parse a URL
def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}, Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to crawl a webpage and find links
def crawl(url):
    global visited, domain
    if url in visited or domain not in url:
        return
    
    print(f"Crawling: {url}")
    visited.add(url)
    
    content = fetch_page(url)
    if content:
        save_page(url, content)
        if url.endswith(".pdf"):
            return
        # Parse the HTML content
        soup = BeautifulSoup(content, "html.parser")
        # Find all anchor tags
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # Resolve relative URLs
            full_url = urljoin(url, href)
            # Ensure that the URL belongs to the same domain
            if domain in full_url and full_url not in visited:
                sleep(1)  # Respect the website, avoid overloading the server
                crawl(full_url)

if __name__ == "__main__":
    # domain = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(start_url))
    crawl(domain)
