import os
import json
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.parse

nums = 50
service = 'waxing'
query = 'waxing service'

def get_elems_upto_max_count(els, max_count):
    elems = []
    elemsCount = 0
    for el in els:
        if elemsCount >=  max_count:
            break

        elems.append(el)
        elemsCount = elemsCount + 1
    return elems

def save_image(url, folder_path):
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(url, stream=True)
        response.raise_for_status()
        image_name = os.path.join(folder_path, url.split("/")[-1])
        with open(image_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"Image saved: {image_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")

def handler(event, context):
    if 'body' in event.keys():
        body = event['body']
    else:
        body = event

    page_num = 1
    query = body.get('query', 'beauty')
    max_count = body.get('max_count')

    images = []
    folder_path = os.path.join("bing", service, query)
    os.makedirs(folder_path, exist_ok=True)

    encoded_query = urllib.parse.quote(query, safe=':/?=&')
    base_query_url = "https://www.bing.com/images/search?"

    while len(images) < max_count:
        query_url = base_query_url + f"q={encoded_query}"
        if "img_size" in body:
            query_url = query_url + f"&qft=+filterui:imagesize-{body['img_size']}"
        query_url = query_url + f"&form=IRFLTR&first={page_num}"

        print(query_url)

        try:
            response = requests.get(query_url)
            response.raise_for_status()

            bs = BeautifulSoup(response.content, 'html.parser')

            els = bs.findAll(class_='iusc')
            elems = get_elems_upto_max_count(els, max_count - len(images))
            print(elems)

            for elem in elems:
                if elem.has_attr('m'):
                    image_url = json.loads(elem['m']).get('murl')
                    save_image(image_url, folder_path)
                    image = {
                        "url": image_url,
                        "type": "PHOTO",
                    }
                    images.append(image)

            page_num += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching images: {e}")
            break

    print(f"Returning {len(images)} from bing")
    print(len(images))
    return {
        "query": query,
        "images": images
    }

evt = {
    "query": query,
    "img_size": "large",
    "max_count": nums
}
handler(evt, None)
