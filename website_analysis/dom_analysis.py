"""dom_analysis.py: A module for analyzing the Document Object Model (DOM) of a website.

This module is a part of the Website Structure Analysis component.
It is responsible for handling DOM parsing, element identification, and content extraction.
As the module evolves, it may include additional functionality related to DOM analysis.
"""

from bs4 import BeautifulSoup
import requests
import re


class HtmlLoader:
    def __init__(self, html_location):
        self.html_location = html_location

    def load(self):
        with open(self.html_location, 'r') as file:
            html_code = file.read()
        return html_code
    
class UrlHtmlLoader:
    def __init__(self, url):
        self.url = url

    def load(self):
        response = requests.get(self.url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        return response.text
    

class HTMLParser:
    def __init__(self, parser_type='html.parser'):
        self.parser_type = parser_type

    def parse(self, html):
        return BeautifulSoup(html, self.parser_type)


class HTMLSearcher:
    def search(self, parsed_html, target_string):
        # Case Insensitive Search
        elements_containing_string = parsed_html(text=re.compile(target_string, re.I))

        # If not found in text nodes, search within tags
        if not elements_containing_string:
            elements_containing_string = parsed_html(string=lambda text: target_string in text)

            # If still not found, search within tag attributes
            if not elements_containing_string:
                elements_containing_string = parsed_html(lambda tag: target_string in str(tag.attrs))

        if elements_containing_string:
            # Just take the first occurrence for this example
            return elements_containing_string[0]
        else:
            return None


class ParentExtractor:
    def extract(self, element, generations):
        parent = element
        for _ in range(generations):
            parent = parent.parent if parent.parent is not None else parent
        return parent

class HTMLPreparer:
    def prepare(self, element):
        # Convert the element back into a string of HTML
        element_html = str(element)

        # Strip out any leading/trailing white space
        prepared_html = element_html.strip()

        return prepared_html


class HTMLProcessingPipeline:
    def __init__(self, parser, searcher, extractor, preparer):
        self.parser = parser
        self.searcher = searcher
        self.extractor = extractor
        self.preparer = preparer

    def process(self, html, target_string, generations):
        parsed_html = self.parser.parse(html)
        target_element = self.searcher.search(parsed_html, target_string)
        parent_element = self.extractor.extract(target_element, generations)
        prepared_html = self.preparer.prepare(parent_element)
        return prepared_html
    

class HtmlManager:
    def __init__(self, source, source_type, target_string, max_length=4000):
        self.max_length = max_length
        self.target_string = target_string
        if source_type == 'url':
            self.loader = UrlHtmlLoader(source)
        else:  # source_type == 'file'
            self.loader = HtmlLoader(source)
        
    def process_html(self):
        html = self.loader.load()

        if len(html) >= self.max_length:
            # Create instances of each class
            parser = HTMLParser()
            searcher = HTMLSearcher()
            extractor = ParentExtractor()
            preparer = HTMLPreparer()

            # Create an instance of the pipeline using the instances of the classes
            pipeline = HTMLProcessingPipeline(parser, searcher, extractor, preparer)

            # Call the `process` method of the pipeline with the necessary parameters
            target_string = self.target_string
            generations = 3
            processed_html = pipeline.process(html, target_string, generations)
        else:
            processed_html = html
            

        return processed_html 


def main():
    # Choose a loader
    manager = HtmlManager('https://www.scrapethissite.com/pages/simple/', source_type='url')

    # Create instances of each class
    parser = HTMLParser()
    searcher = HTMLSearcher()
    extractor = ParentExtractor()
    preparer = HTMLPreparer()

    # Create an instance of the pipeline using the instances of the classes
    pipeline = HTMLProcessingPipeline(parser, searcher, extractor, preparer)

    # Call the `process` method of the pipeline with the necessary parameters
    html = manager.process_html() # the HTML you want to process
    target_string = "Andorra"
    generations = 2
    prepared_html = pipeline.process(html, target_string, generations)

    # Now you can use `prepared_html` as you see fit
    print(prepared_html)

if __name__ == "__main__":
    main()
