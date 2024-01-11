from crawler import WebCrawler
from flask import Flask, render_template, request

#define variables that can be changed
start_url='https://vm009.rz.uos.de/crawl/index.html'
index_dir='indexdir'
index_name='basic'
steps=15

# Initialize a web crawler with the specified parameters
crawler = WebCrawler(start_url, index_dir, index_name)

# Start crawling toy webpages with a maximum of n steps
crawler.start(steps)
