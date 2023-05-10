import os
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.indexes import VectorstoreIndexCreator


load_dotenv()


def list_html_files(folder_path):
    """
    List all HTML files in the specified folder.

    Args:
        folder_path (str): The path to the folder containing HTML files.

    Returns:
        list: A list of HTML file names.
    """
    html_files = []

    # List all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file has an .html or .htm extension
        if filename.lower().endswith((".html", ".htm")):
            html_files.append(filename)

    return html_files


if __name__ == "__main__":
    # Example usage
    folder_path = "./results"
    html_files = list_html_files(folder_path)

    # Location of the HTML files.
    loaders = [
        UnstructuredHTMLLoader(os.path.join(folder_path, fn)) for fn in html_files
    ]

    index = VectorstoreIndexCreator().from_loaders(loaders)
    print(index.query_with_sources("Is there any HTML in the documents?"))
