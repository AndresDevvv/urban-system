import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Read keywords from file
with open('Keywords.txt', 'r') as file:
    keywords = file.read().splitlines()

# Initialize list to store magnet/torrent links
magnet_links = []

# Search and scrape magnet/torrent links
for keyword in keywords:
    search_keyword = quote(keyword)
    search_url = f'https://thepiratebay.org/search.php?q={search_keyword}'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    listings = soup.find_all('a', href=True)
    for listing in listings:
        listing_name = listing.text.strip()
        listing_keywords = listing_name.split()

        # Check if all keywords are present in the listing name
        if all(keyword in listing_keywords for keyword in keywords):
            listing_url = listing['href']
            break

    if 'listing_url' in locals():
        magnet_url = f'https://thepiratebay.org{listing_url}'
        magnet_response = requests.get(magnet_url)
        magnet_soup = BeautifulSoup(magnet_response.text, 'html.parser')

        magnet_link = magnet_soup.find('a', href=True)
        if magnet_link:
            magnet_links.append(magnet_link['href'])
            print(f"Successfully retrieved magnet link: {magnet_link['href']}")
        else:
            print(f"No magnet link found for keyword: {keyword}")
    else:
        print(f"No listing found for keyword: {keyword}")

    # Clear the locally scoped variables for the next iteration
    locals().clear()

# Save magnet/torrent links to magnets.txt
with open('magnets.txt', 'w') as file:
    for magnet_link in magnet_links:
        file.write(f"{magnet_link}\n")

print("All magnet/torrent links saved to magnets.txt")
