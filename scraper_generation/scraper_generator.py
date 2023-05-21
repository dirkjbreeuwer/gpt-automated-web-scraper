from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate

class ScrapingCodeGenerator:
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
    
    static_code = """
from bs4 import BeautifulSoup

# Get the URL of the website
with open('./results/denver.html') as f:
    response = f.read()

html_soup = BeautifulSoup(response, 'html.parser')
    """

    def __init__(self, html_loader):
        self.html_loader = html_loader
        self.llm = self.initialize_llm()
        self.prompt_template = self.initialize_template()

    def initialize_llm(self):
        load_dotenv()
        return OpenAI(model_name=self.MODEL_NAME, temperature=0)

    def initialize_template(self):
        return PromptTemplate(input_variables=["requirements","html"], template=self.TEMPLATE)


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