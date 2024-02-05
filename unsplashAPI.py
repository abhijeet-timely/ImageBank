import requests
import os

# Replace 'YOUR_ACCESS_KEY' with your Unsplash API access key
ACCESS_KEY = 'ZVfBRhKbb5PZdEbTGsDDSMzugIsew2GbmMx6OOMc11U'


q = 'bridal makeup srvices'
service = 'bridal_services'
nums = 100

def download_image(url, folder, filename):
    response = requests.get(url)
    if response.status_code == 200:
        # Create the folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Save the image
        with open(os.path.join(folder, filename), 'wb') as f:
            f.write(response.content)
        print(f"Image saved: {filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def search_and_download(query, folder, count):
    # API endpoint for searching photos
    endpoint = 'https://api.unsplash.com/photos/random'
    params = {
        'query': query,
        'count': count,
        'client_id': ACCESS_KEY
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        for index, photo in enumerate(data):
            image_url = photo['urls']['regular']
            filename = f"{query}_{index + 1}.jpg"
            download_image(image_url, folder, filename)
    else:
        print(f"Failed to retrieve images. Status code: {response.status_code}")

if __name__ == "__main__":
    search_query = q  # Replace with your desired search query
    save_folder = f'bing/{service}/{q}'  # Folder to save the downloaded images

    search_and_download(search_query, save_folder, nums)
