# Quoter.py - A program that takes popular quotes from a quote archive website and inserts them into the user's wallpaper

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import requests, urllib3
import os, sys, random

# TODO: Normalize the posistioning of the quote in vertical space

quote_site = 'https://www.goodreads.com/quotes?page=' + str(random.randint(1, 50))


"""
Constrains the text to the bounds of the image
"""
def wrap_text(text):
    # char_limit - Max characters allowed per line
    # char_count = current character count for the line
    char_limit, char_count = 70, 0
    text = text.split()
    # Will contain final wrapped text
    text_wrapped = []

    line = ''

    for word in text:
        # Checks whether adding another word to the line will go over the char limit
        if (char_count + len(word)) < char_limit:
            char_count = char_count + len(word) + 1
            line += word + ' '

        # If the word would put line over the character limit
        else:
            text_wrapped.append(line)
            line = word + ' '
            char_count = len(word) + 1

    text_wrapped.append(line)

    return text_wrapped

"""
Removes extraneous javascript from the quote
"""
def clean_quote(quote_text):
    ind = quote_text.find('”')
    print(ind)

    return quote_text[:ind + 1]


def main():
    im = Image.open('res/img/' + str(random.randint(1, 6)) + '.png')
    fnt = ImageFont.truetype('res/fnt/MoonFlowerBold.ttf', 30)
    res = requests.get(quote_site)

    # Error Checking: Throws if the download of the resource fails
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    # Create a parsable bs4 object with the downloaded web page
    quote_soup = BeautifulSoup(res.text, 'html.parser')
    # Store all quotes from the page
    # div[class="quote"] > span[class="text"]
    quote_text = clean_quote(quote_soup.select('div[class="quoteText"]')[2].getText())

    # Grab the author of the stored quote
    # div[class="quote"]  small[class="author"]
    #quote_author = quote_soup.select('a[class="authorOrTitle"]')[1].getText()
    # Separate drawing of text to fixed image size to retain consistency.
    quote_image = Image.new('RGBA', (im.width // 3, im.height // 4), (255, 255, 255, 0))
    draw_text = ImageDraw.Draw(quote_image)

    # quote_text separated to keep all text onscreen
    wrapped_quote = wrap_text(quote_text)
    line_index = 0
    first_line = True

    for line in wrapped_quote:
        if first_line:
            first_line = False
            draw_text.text((10, 10), line, font=fnt, fill='White')
        else:
            line_index += 1
            draw_text.text((20, 10 + (40 * line_index)), line, font=fnt, fill='White')

    #draw_text.text((450, 10 + (40 * (line_index + 1))), '-' + quote_author, font=fnt, fill='White')

    try:
        os.stat('wallpaper/')
    except:
        os.mkdir('wallpaper/')

    im.paste(quote_image, ((im.width - quote_image.width), (im.height - quote_image.height)), quote_image)
    im.save('wallpaper/wallpaper.png')

if __name__ == '__main__':
    main()