from QuoteEngine import Quoter
import requests
import random

# Quotes are random and scraped from the goodreads top quotes page.
quote_site = 'https://www.goodreads.com/quotes?page=' + str(random.randint(1, 50))

def main():
    res = requests.get(quote_site)

    # Error Checking: Throws if the download of the resource fails
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % exc)

    wall = Quoter(res.text)
    wall.generate_wallpaper()

if __name__ == '__main__':
    main()
