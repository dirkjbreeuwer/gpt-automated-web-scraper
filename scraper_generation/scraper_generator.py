from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate

class ScrapingCodeGenerator:
    MODEL_NAME = "text-davinci-003"
    SCRAPING_CODE = f"""
from bs4 import BeautifulSoup
from website_analysis.dom_analysis import HtmlLoader, UrlHtmlLoader

# Create HtmlLoader or UrlHtmlLoader based on the source type
def create_html_loader(source, source_type):
    if source_type == 'url':
        return UrlHtmlLoader(source)
    else:  # source_type == 'file'
        return HtmlLoader(source)

html_loader = create_html_loader("{{source}}", "{{source_type}}")
response = html_loader.load()

html_soup = BeautifulSoup(response, 'html.parser')
    """
    PROMPT_TEMPLATE = """
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
    


    def __init__(self, html_loader, source, source_type):
        self.html_loader = html_loader
        self.llm = self.initialize_llm()
        self.prompt_template = self.initialize_template()
        self.scraping_code = self.SCRAPING_CODE.format(source=source, source_type=source_type)

    def initialize_llm(self):
        load_dotenv()
        return OpenAI(model_name=self.MODEL_NAME, temperature=0)

    def initialize_template(self):
        return PromptTemplate(input_variables=["requirements","html"], template=self.PROMPT_TEMPLATE)


    def generate_scraping_code(self, user_requirements):
        """
        Returns the LLM response based on the prompt, requirements and html
        """
        html_code = self.html_loader.load()
        formatted_prompt = self.prompt_template.format(requirements=user_requirements, html=html_code)
        generated_code = self.llm(formatted_prompt)

        full_scraping_code = f"""
{self.scraping_code}
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