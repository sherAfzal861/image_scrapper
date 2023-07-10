import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def download_image(url, directory):
    if url.startswith('data:image'):
        print(f"Skipped: {url} (data URI)")
        return

    response = requests.get(url)
    if response.status_code == 200:
        file_name = os.path.join(directory, os.path.basename(urlparse(url).path))
        if not os.path.exists(file_name):
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {url}")
        else:
            print(f"Skipped: {url} (already downloaded)")

def scrape_images(url, directory):
    visited_urls = set()
    downloaded_images = set()

    def recursive_scrape(url):
        if url in visited_urls:
            return
        visited_urls.add(url)

        response = requests.get(url)
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        image_tags = soup.find_all('img')
        for img_tag in image_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = urljoin(url, img_url)
                if img_url not in downloaded_images:
                    download_image(img_url, directory)
                    downloaded_images.add(img_url)

        anchor_tags = soup.find_all('a')
        for anchor_tag in anchor_tags:
            anchor_url = anchor_tag.get('href')
            if anchor_url:
                anchor_url = urljoin(url, anchor_url)
                recursive_scrape(anchor_url)

    recursive_scrape(url)

# Example usage:
url = "https://umw.edu.pk"
directory = "images"
scrape_images(url, directory)
