import sys
import requests
import bs4
import time
import csv
from pathlib import Path
from urllib.parse import urljoin
import sys

web_page = input("Enter the link to the page you want to check for broken link : ")

# Retrieve content from webpage
try :
    page_result = requests.get(web_page, headers={'User-Agent': 'Mozilla/5.0'}, timeout = 10)
    page_result.raise_for_status()
except Exception as exc:
    print(f'An error occurred: {exc}')
    sys.exit(1)

# Retrieve search result links
soup = bs4.BeautifulSoup(page_result.content, 'html.parser')

# Searching for links to the search results
link_elems = soup.find_all('a')
# Variables Needed for The Check Results Summary
valid_links = 0
broken_links = 0
print(". . . Checking Links . . . \n")

total_links = len(link_elems)

# Dynamically get the Downloads directory path
downloads_path = Path.home() / "Downloads"
csv_file_path = downloads_path / "link_report.csv"

# Exporting CSV file of the links and their statuses
with open('csv_file_path', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Link', 'Status'])
    # Printing out all search results
    for link in link_elems:
        href = link.get('href')
        if href:
            # Checking each page link for any broken links
            try :
                if href.startswith('http'):
                    full_url = (f"{href}")
                    page_status = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout = 10)
                    print(f"Checking : {href} --> Status : {page_status}")
                    if 200 <= int(page_status.status_code) < 400 :
                        valid_links += 1
                    else :
                        broken_links += 1
                    writer.writerow([full_url, page_status])
             
                else:    
                    full_url  = urljoin(web_page, href)
                    page_status = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout = 10)
                    print(f"Checking : {full_url} --> Status : {page_status}")
                    if 200 <= int(page_status.status_code) < 400 :
                        valid_links += 1
                    else :
                        broken_links += 1
                writer.writerow([full_url, page_status])
            except requests.exceptions.RequestException as e:
               print(f"Error: {e}")
               broken_links += 1
               time.sleep(0.3)  # Gentle pause to avoid overloading servers
               writer.writerow([full_url, e])
      
print("\nExporting CSV File")
# Giving a Result Summary of the Broken Links Search
print(f"\n✅ CSV File Exported to: {csv_file_path}")
print(f"\nSummary:\nTotal links checked: {total_links}")
print(f"Valid links: {valid_links}")
print(f"Broken/Invalid links: {broken_links}")


        

