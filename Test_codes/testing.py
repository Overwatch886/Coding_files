import urllib.request as request
import re
from bs4 import BeautifulSoup

def scrape_amazon_product(url):
    try:
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')

        # Extract product categories
        product_categories = soup.find_all('a', href = re.compile("^catalogue/c+"))
        if product_categories:
            product_categories_list = [category.text.strip() for category in         product_categories]
        else:
            product_categories_list = "Not found"
            
         #Extract Product Name 
        product_name = soup.find_all('img', {'class': 'thumbnail'})
        if product_name:
           product_name_list = [product.text.strip() for product in product_name]
        else:
           product_name_list = "Not found"

        # Extract price
        prices = soup.find_all('p', {'class': 'price_color'})
        if prices:
            price_list = [price.text.strip() for price in prices]
        else:
            price_list = "Not found"

        # Extract description
        description = soup.find('div', {'class': 'product_price'})
        if description:
            description = description.text.strip()
        else:
            description = "Not found"

        # Extract image URL
        images = soup.find_all('img', None)
        if images:
            image_url = [image.get('src') for image in images]
        else:
            image_url = "Not found"

        print("Product Categories:", product_categories_list)
        print("Product Names:", product_name_list)
        print("Price:", price_list)
        print("Description:", description)
        print("Image URL:", image_url)

    except Exception as e:
        print(f"An error occurred: {e}")

url = input("Enter the Website URL: ")
scrape_amazon_product(url)