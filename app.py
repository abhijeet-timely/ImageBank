import requests
import os
from io import BytesIO
from PIL import Image

# Set Google Custom Search API credentials
api_key = 'AIzaSyCJrrd6p6U_pvA4Ufc-1TtBqMmEqXh2kB4'
cx = 'f142811ddf511472d'
service = 'haircut'
query = 'haircut at barber shop'


# Construct the Google Custom Search API endpoint URL
endpoint = 'https://www.googleapis.com/customsearch/v1'

# Set the Google Custom Search parameters
params = {
    'key': api_key,
    'cx': cx,
    'q': query,
    'rights':'cc_publicdomain',
    'searchType': 'image',
    'num': 10,
}

response = requests.get(endpoint, params=params)

if response.status_code == 200:
    data = response.json()
    directory = f"images/{service}/{query}"
    os.makedirs(directory, exist_ok=True)
    for item in data.get('items', []):
        image_url = item.get('link')
        if image_url:
            # Download image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Save image
                image_content = BytesIO(image_response.content)
                image = Image.open(image_content)
                image.save(os.path.join(directory, f"{item['title']}.png"))
                print(f"Image saved: {item['title']}")
            else:
                print(f"Failed to download image: {image_response.status_code} - {image_response.text}")



    
else:
    # Print an error message if the request to Google Custom Search API was not successful
    print(f"Error: {response.status_code} - {response.text}")