from datetime import datetime
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os

class InMemoryIndex:
    #In-memory index for storing word-to-url mappings

    def __init__(self):
        self.word_to_urls = {}

    def add_document(self, url, content):
        #Add a document to the in-memory index
        words = content.split()
        for word in words:
            if word not in self.word_to_urls:
                self.word_to_urls[word] = [url]
            else:
                self.word_to_urls[word].append(url)

    def get_index(self):
        #Retrieve the in-memory index
        return self.word_to_urls


class SearchEngineIndex:
    #Search engine index for managing Whoosh index and in-memory index

    def __init__(self, index_dir='indexdir', index_name='basic'):
        self.schema = Schema(url=ID(stored=True), content=TEXT(stored=True), title=TEXT(stored=True),
                             time=TEXT(stored=True))
        self.ix = self.create_or_open_index(index_dir, index_name)
        self.writer = self.ix.writer()
        self.in_memory_index = InMemoryIndex()

    def create_or_open_index(self, index_dir, index_name):
        #Create or open the Whoosh index
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
            return create_in(dirname=index_dir, schema=self.schema, indexname=index_name)
        elif not exists_in(dirname=index_dir, indexname=index_name):
            return create_in(dirname=index_dir, schema=self.schema, indexname=index_name)
        else:
            return open_dir(dirname=index_dir, indexname=index_name, schema=self.schema)

    def add_document(self, url, content, title):
        #Add a document to both the Whoosh index and in-memory index
        with self.writer as writer:
            writer.add_document(url=url, content=content, title=title, time=f'{datetime.now():%d-%m-%Y %H:%M:%S%z}')
            self.in_memory_index.add_document(url, content)

    def commit(self):
        #Commit changes to the Whoosh index
        self.writer.commit()

    def search(self, query_str):
        #Search the Whoosh index and return results
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(query_str)
            results = searcher.search(query)
            results_list = []

            for hit in results:
                results_list.append({"url": hit['url'], "text": hit.highlights("content", top=2),
                                     "title": hit['title'], "time": hit['time']})

            return results_list

    def get_in_memory_index(self):
        #Retrieve the in-memory index
        return self.in_memory_index.get_index()
