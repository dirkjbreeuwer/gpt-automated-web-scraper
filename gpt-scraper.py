from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.llms import OpenAI
import argparse
from website_analysis.dom_analysis import HtmlLoader, UrlHtmlLoader
from scraper_generation.scraper_generator import ScrapingCodeGenerator, CodeWriter 
from data_extraction.data_extractor import CodeExecutor 



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






# python3 gpt-scraper.py --source-type "file" --source "./results/denver.html" --requirements "Extract the average monthly temperature in denver"