from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.speedrun.com"
START_URL = "https://www.speedrun.com/games?page={page}&platform=&sort=mostruns"

games = []

for page in range(1, 6):  # Pages 1 to 5
    url = START_URL.format(page=page)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all game card links
    game_cards = soup.select("a[href^='/']")  # All links starting with '/'

    for card in game_cards:
        # Get the image tag inside the link
        img_tag = card.find('img')
        if img_tag:  # Only process if there's an image (likely a game card)
            title = img_tag.get('alt', '').strip()
            href = card.get('href', '')

            # Skip non-game links (optional filtering)
            if href and not any(href.startswith(x) for x in ('/user/', '/forum/', '/blog/')):
                full_url = BASE_URL + href
                games.append((title, full_url))

# Create a dedicated folder
output_folder = Path("speedrun_data")
output_folder.mkdir(exist_ok=True)

# Save to files (with absolute paths)
txt_path = output_folder / "games.txt"

# Save to text file
with open(txt_path, 'w', encoding='utf-8') as f:
    for title, url in games:
        f.write(f"{title} - {url}\n")
