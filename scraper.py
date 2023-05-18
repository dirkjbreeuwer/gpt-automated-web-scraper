from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.llms import OpenAI
import requests
import subprocess
import argparse

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
    

class ScrapingCodeGenerator:
    static_code = """
from bs4 import BeautifulSoup

# Get the URL of the website
with open('./results/denver.html') as f:
    response = f.read()

html_soup = BeautifulSoup(response, 'html.parser')
        """
    def __init__(self, html_loader, llm, prompt_template):
        self.html_loader = html_loader
        self.llm = llm
        self.prompt_template = prompt_template

    def generate_scraping_code(self, user_requirements):
        """
        Returns the LLM response based on the prompt, requirements and html
        """
        html_code = self.html_loader.load()
        formatted_prompt = self.prompt_template.format(requirements=user_requirements, html=html_code)
        generated_code = self.llm(formatted_prompt)

        full_scraping_code = f"""
        {self.static_code}
        {generated_code}
        """
        return full_scraping_code

    
class CodeWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, scraping_code):
        """
        Writes the scraping code to a .py python file
        """
        with open(self.file_name, 'w') as file:
            file.write(scraping_code)


class CodeExecutor:
    def __init__(self, file_name):
        self.file_name = file_name

    def execute(self):
        """
        Execute the python file
        """
        subprocess.call(["python", self.file_name])


def main():
    parser = argparse.ArgumentParser(description='AI Web Scraper')
    parser.add_argument('--source', type=str, help='The URL or local path to HTML to scrape')
    parser.add_argument('--source-type', type=str, choices=['url', 'file'], help='Type of the source: url or file')
    parser.add_argument('--requirements', type=str, help='The user requirements for scraping')
    args = parser.parse_args()

    source = args.source
    source_type = args.source_type
    USER_REQUIREMENTS = args.requirements



    # Variables to define
    HTML_LOCATION = "./results/denver.html"
    MODEL_NAME = "text-davinci-003"
    TEMPLATE = """
        You are an expert website analyzer for a web scraping process. 
        Take the user requirements and convert it into clean python code to scrape the website.

        USER REQUIREMENTS:
        {requirements}

        HTML CODE YOU NEED TO SCRAPE:
        {html}

        FINISH THE PYTHON CODE TO SCRAPE THE WEBSITE:

from bs4 import BeautifulSoup

# Get the URL of the website
with open('./results/denver.html') as f:
    response = f.read()

html_soup = BeautifulSoup(response, 'html.parser')
        """

    # Load environment variables
    load_dotenv()

    # Create the LLM
    llm = OpenAI(model_name=MODEL_NAME, temperature=0)

    # Create prompt template
    prompt_template = PromptTemplate(input_variables=["requirements","html"], template=TEMPLATE)

    # create HtmlLoader or UrlHtmlLoader based on the source type
    if source_type == 'url':
        html_loader = UrlHtmlLoader(source)
    else:  # source_type == 'file'
        html_loader = HtmlLoader(source)

    # Instantiate ScrapingCodeGenerator with the html_loader
    code_generator = ScrapingCodeGenerator(html_loader, llm, prompt_template)

    # Generate scraping code
    scraping_code = code_generator.generate_scraping_code(USER_REQUIREMENTS)

    # Instantiate CodeWriter
    code_writer = CodeWriter('scraping_code.py')

    # Write the code to a file
    code_writer.write(scraping_code)

    # Instantiate CodeExecutor
    code_executor = CodeExecutor('scraping_code.py')

    # Execute the code
    code_executor.execute()

if __name__ == "__main__":
    main()






