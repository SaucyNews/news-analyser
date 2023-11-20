"""
Simple script to fetch a random from the Guardian API and return it in a JSON format.
"""

import sys
import re
import requests
from datetime import datetime
from random import randint

from analyser.config import app_config

ENDPOINT = "https://content.guardianapis.com/search"


def get_random_article():
    """
    Fetches a random article from the Guardian API and returns it in a JSON format.
    """

    api_key = app_config.GUARDIAN_API_KEY

    if api_key is None:
        print(
            "No Guardian API key found; please create one and assign it to GUARDIAN_API_KEY in the .env file."
        )
        sys.exit(1)

    params = {
        "order-by": "newest",
        "from-date": datetime.now().strftime("%Y-%m-%d"),
        "page-size": 200,
        "show-tags": "all",
        "show-fields": "all",
        "show-elements": "all",
        "show-references": "all",
        "api-key": app_config.GUARDIAN_API_KEY,
    }

    response = requests.get(ENDPOINT, params=params)

    if response.status_code != 200:
        print("Error fetching article from Guardian API")
        sys.exit(1)

    data = response.json()
    articles = data["response"]["results"]

    return articles[randint(0, len(articles) - 1)]


def format_body(body):
    """
    Formats the body of the article to remove HTML tags and convert to lowercase.
    """
    body = body.lower()

    # Convert IMG tags to text
    body = re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>', r"\[IMG \1\]", body)

    # Remove remaining Tags
    body = re.sub(r"<[^>]*>", "", body)

    # Replace ampersand
    body = re.sub(r"&amp;", "and", body)

    # Extend contractions
    body = re.sub(r"'re", " are", body)
    body = re.sub(r"'s", " is", body)
    body = re.sub(r"'d", " would", body)
    body = re.sub(r"'ll", " will", body)
    body = re.sub(r"'t", " not", body)
    body = re.sub(r"'ve", " have", body)
    body = re.sub(r"'m", " am", body)

    # Remove remaining special characters
    body = re.sub(r"[^a-zA-Z0-9,.\(\)]+", " ", body)

    # Remove duplicate spaces
    body = re.sub(r"\s+", " ", body)
    return body


if __name__ == "__main__":
    print(app_config.GUARDIAN_API_KEY)
