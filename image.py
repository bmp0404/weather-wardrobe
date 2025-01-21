import os
import requests
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_KEY = os.getenv("UNSPLASH_KEY")  # Make sure it's in your .env

def fetch_outfit_images(query):
    
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Accept-Version": "v1",
        "Authorization": f"Client-ID {UNSPLASH_KEY}"
    }
    params = {
        "query": query,
        "orientation": "portrait",  # or "landscape", "squarish"
        "per_page": 3               # up to 3 images
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Debug 
    print("Unsplash status code:", response.status_code)
    print("Unsplash data:", data)

    # If no valid results, return empty list
    if "results" not in data or len(data["results"]) == 0:
        return []

    # list of up to 3 image URLs
    image_urls = []
    for result in data["results"]:
        image_url = result["urls"]["regular"]
        image_urls.append(image_url)

    return image_urls
