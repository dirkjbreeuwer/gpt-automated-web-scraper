"""utils.py: A utility script to analyze API calls using GPT-3."""

import openai
import json


def load_config():
    """
    Load the API key from the configuration file.

    :return: A dictionary containing the configuration data
    """
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
    return config_data


config = load_config()
openai_api_key = config["openai"]["api_key"]

# Set up the OpenAI API client
openai.api_key = openai_api_key


def analyze_api_calls(api_calls):
    """
    Analyze API calls using GPT-3 and return the analysis results.

    :param api_calls: A list of API calls to analyze
    :return: The API analysis results as a formatted string
    """
    # Prepare the API calls data for input to GPT-3
    api_calls_data = json.dumps(api_calls, indent=2)

    # Construct the GPT-3 prompt
    prompt = (
        f"We are trying to identify a website's internal API. \n\n"
        f"Here are all XML and JSON results we found when navigating this website:\n\n"
        f"{api_calls_data}\n\n"
        f"Can you please identify any APIs and return them in the following format:\n\n"
        f"| API | Payload | Response |\n"
    )

    # Call the GPT-3 API
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the API analysis results from the GPT-3 response
    api_analysis_results = response.choices[0].text.strip()

    return api_analysis_results
