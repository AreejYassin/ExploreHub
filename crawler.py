import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from index import SearchEngineIndex


class WebCrawler:

    def __init__(self, start_url, index_dir, index_name):
        # List of URLs to visit
        self.to_visit = [start_url]
        # List of URLs already visited
        self.visited = []
        # Server domain extracted from the start URL
        self.server_domain = urlparse(start_url).netloc
        # Initialize the Index class with the directory
        self.index = SearchEngineIndex(index_dir=index_dir, index_name=index_name)

    def start_crawling(self, max_steps=None):
        # Continue crawling until there are no more URLs to visit or max_steps is reached
        while len(self.to_visit) > 0 and (max_steps is None or max_steps > 0):
            # Get the next URL
            current_url = self.to_visit.pop()

            if current_url not in self.visited:
                self.visited.append(current_url)
                # Get the text content and title of the webpage
                try:
                    response = requests.get(current_url)
                    if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
                        soup = BeautifulSoup(response.text, "html.parser")
                        website_text = soup.text
                        website_title = soup.find('title').text
                        normalized_text = re.sub(r'[^\w\s]', '', website_text).lower()
                        # Add the current page to the index
                        self.index.add_document(url=current_url, content=normalized_text, title=website_title)

                        # Get all the links from the webpage
                        new_urls = self.extract_links(current_url, soup)

                        # Check whether the links have been visited already and add them to the to_visit list respectively
                        for url in new_urls:
                            if url not in self.visited and url not in self.to_visit:
                                self.to_visit.append(url)

                except Exception as e:
                    print(f"Error processing {current_url}: {e}")

            # Decrease the step counter for the search
            if max_steps is not None:
                max_steps -= 1

        # Commit changes to the index
        self.index.commit()

    def extract_links(self, target_url, soup):
        # Extract links from the webpage
        urls = []
        target_domain = urlparse(target_url).netloc
        for link in soup.find_all("a"):
            url = link.get("href", "")
            full_url = urljoin(target_url, url)
            url_domain = urlparse(full_url).netloc
            # Make sure that the URL is in the same domain
            if url_domain == target_domain and full_url not in self.visited:
                urls.append(full_url)

        return urls
