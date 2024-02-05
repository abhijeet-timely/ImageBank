import json
from bs4 import BeautifulSoup
import requests
import os
import urllib.parse
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError, URLError

def get_elems_upto_max_count(els, max_count):
    elems = []
    elemsCount = 0
    for el in els:
        if elemsCount >= max_count:
            break

        elems.append(el)
        elemsCount = elemsCount + 1
    return elems

def save_images(images, query):
    folder_path = os.path.join('bing', query)
    os.makedirs(f'temp/{folder_path}', exist_ok=True)

    for idx, image in enumerate(images):
        image_url = image["url"]
        image_type = image["type"]
        image_extension = image_url.split('.')[-1]

        filename = f"{idx + 1}.{image_type.lower()}.{image_extension}"
        filepath = os.path.join(folder_path, filename)

        try:
            print(f"Downloading {filename}...")
            
            # Use urlopen with a context to handle SSL errors
            with urlopen(image_url) as response:
                with open(filepath, 'wb') as output_file:
                    output_file.write(response.read())
                    
        except (HTTPError, URLError) as e:
            print(f"Error downloading {filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while downloading {filename}: {e}")

def handler(event, context):
    if 'body' in event.keys():
        body = event['body']
    else:
        body = event

    page_num = 1
    query = body.get('query', 'beauty')
    max_count = body.get('max_count')

    images = []

    encoded_query = urllib.parse.quote(query, safe=':/?=&')
    base_query_url = "https://www.bing.com/images/search?"

    query_url = base_query_url + f"q={encoded_query}"
    if "img_size" in body:
        query_url = query_url + f"&qft=+filterui:imagesize-{body['img_size']}"
    query_url = query_url + f"&form=IRFLTR&first={page_num}"

    print(query_url)

    try:
        response = requests.get(query_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return {"error": f"HTTP Error: {errh}"}
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        return {"error": f"Request Exception: {err}"}

    bs = BeautifulSoup(response.content, 'html.parser')

    els = bs.findAll(class_='iusc')
    elems = get_elems_upto_max_count(els, max_count)
    print(elems)

    images = []
    for elem in elems:
        if elem.has_attr('m'):
            image = {
                "url": f"{json.loads(elem['m']).get('murl')}",
                "type": "PHOTO",
            }
            images.append(image)

    print(f"Returning {len(images)} from bing")
    print(images)

    # Save images to folder
    save_images(images, query)

    return {
        "query": query,
        "images": images
    }

evt = {
    "query": "hydrafacial stock images",
    "img_size": "large",
    "max_count": 100  # Just for testing, set to the desired number
}
handler(evt, None)
