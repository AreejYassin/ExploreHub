# ExploreHub Search Engine

## Overview

ExploreHub is a simple search engine built using Python and Flask. It allows users to search through webpages indexed by the system.

## Features

- **Web Crawling:** The ExploreHub search engine includes a web crawler that systematically browses webpages starting from a specified URL and extracts relevant information for indexing.

- **Indexing:** The crawled data is indexed using the Whoosh search engine library, creating a searchable database for efficient retrieval of information.

- **Flask Web Application:** The search engine is integrated into a Flask web application, providing users with an intuitive interface to input search queries and retrieve relevant results.

## Crawling Algorithm

The web crawling algorithm employed by ExploreHub follows these steps:

1. **Seed URL:** The crawling process starts from a specified seed URL, which serves as the initial point of exploration.

2. **Breadth-First Search (BFS):** The crawler utilizes a breadth-first search strategy to systematically traverse webpages. This ensures that pages at the same level of depth are visited before moving on to deeper levels.

3. **URL Frontier:** A queue-based approach is used to maintain a list of URLs to be visited, known as the URL frontier. The crawler dequeues URLs for processing and enqueues newly discovered URLs during the crawl.

4. **Content Extraction:** For each visited webpage, relevant information such as text content and titles are extracted. This content is then used for indexing.

5. **URL Filtering:** To avoid revisiting already processed URLs and to focus on unique content, a set of visited URLs is maintained.


## Usage
**Starting the Web Application:**
# Run the Flask web application
    flask --app app run


## Code Structure

- **`crawler.py`:** Defines the `WebCrawler` class responsible for crawling webpages and extracting content.

- **`index.py`:** Implements the indexing functionality using the Whoosh search engine.

- **`app.py`:** Contains the Flask application setup, routes, and error handling. Utilizes the indexed data for handling search queries.

- **`templates/`:** Directory containing HTML templates for the web application.

- **`static/`:** Directory containing static assets (CSS, Bootstrap, etc.) for styling the web application.

## Dependencies

- Python 3.x
- Flask
- Whoosh
- BeautifulSoup
- Bootstrap

