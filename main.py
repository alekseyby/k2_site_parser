import os
import requests
from bs4 import BeautifulSoup


home_url = '##############'
en_category_url = home_url + 'en/products/by-series'


def get_data(url_address):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/58.0.3029.110 Safari/537.3'}
    req = requests.get(url_address, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    products = soup.find_all('li', 'col-md-4 col-xs-6')

    products_urls = []
    for product in products:
        product_url = home_url + product.find('div', 'hover').find('a').get('href')
        products_urls.append(product_url)

    for product_url in products_urls:
        product_name = product_url.split('/')[-1]
        # create folder with product name
        os.makedirs(f'data/{product_name}', exist_ok=True)
        req = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        images = soup.find_all('div', 'col-md-8 product-images')
        description = soup.find('div', 'description')
        try:
            with open(f'data/{product_name}/description.txt', 'w', encoding="utf-8") as file:
                file.write(description.get_text())
        except AttributeError:
            print(f'"{product_name}" has not description')
        for image in images:
            image_urls = image.select('a[data-fancybox-group="gallery"]')
            for idx, image_url in enumerate(image_urls):
                image_url = image_url.get('href')
                try:
                    # download images and save it into the folder
                    img_data = requests.get(image_url).content
                    with open(f'data/{product_name}/image_{idx}.jpg', 'wb') as img:
                        img.write(img_data)
                except Exception as ex:
                    print(f'Error occurred: {ex} for "{product_name}"')


# FIXME

"need to fix hardcoded pagination"
for page in range(1, 70):
    get_data(en_category_url + f'?page={page}')
    print(f'Page {page} is parsed')


