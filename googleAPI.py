import requests
import os
from io import BytesIO
from PIL import Image
import random

# Set Google Custom Search API credentials
api_key = 'AIzaSyCJrrd6p6U_pvA4Ufc-1TtBqMmEqXh2kB4'
            # , 'AIzaSyDm6VHjAg_usnrsQW57xTL2Iltc5r1yXmM', 'AIzaSyDf2a2_-kvbK-5_pGahux-yJ-ZONzBFyz0']
import requests
import os
from io import BytesIO
from PIL import Image
import random

# Set Google Custom Search API credentials
# api_key = 'YOUR_GOOGLE_API_KEY'
cx = 'f142811ddf511472d'
service = 'tattoo_service'
query = 'getting a tattoo from shop'

# Set the number of images to fetch per API call
images_per_api_call = 10

# Create a loop to call the code 6 times
for _ in range(6):
    # Generate random values for some search parameters
    img_size = random.choice(['huge', 'icon', 'large', 'medium', 'small', 'xlarge', 'xxlarge'])
    img_type = random.choice(['clipart', 'face', 'lineart', 'stock', 'photo', 'animated'])
    img_color_type = random.choice(['color', 'gray', 'mono', 'trans'])
    img_dominant_color = random.choice(['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'teal', 'white', 'yellow'])

    # Construct the Google Custom Search API endpoint URL
    endpoint = 'https://www.googleapis.com/customsearch/v1'

    # Set the Google Custom Search parameters
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'rights': 'cc_publicdomain',
        'searchType': 'image',
        'num': images_per_api_call,
        'imgSize': img_size,
        'imgType': img_type,
        'imgColorType': img_color_type,
        'imgDominantColor': img_dominant_color,
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        directory = f"images/{service}/{query}"
        os.makedirs(directory, exist_ok=True)

        for item in data.get('items', []):
            image_url = item.get('link')
            if image_url:
                # Download and save image
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    with Image.open(BytesIO(image_response.content)) as img:
                        img.save(os.path.join(directory, f"{item['title']}.jpg"))
                        print(f"Image saved: {item['title']}")
                else:
                    print(f"Failed to download image: {image_response.status_code} - {image_response.text}")

    else:
        print(f"Error: {response.status_code} - {response.text}")
