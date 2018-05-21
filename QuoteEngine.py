# Quoter.py - A class that generates randomized wallpapers using quotes from goodreads.

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import os, random
import time

'''
A quote object has two properties retrieved from a bs4 object:

quote_text - String of text representing desired quote
quote_author - Name of author who corresponds to the quote
'''
class Quote:
    quote_text = ''
    quote_author = ''
    quote_soup = ''

    def __init__(self, res):
        quote_index = random.randint(1, 15)
        self.quote_soup = BeautifulSoup(res, 'html.parser')
        self.quote_text = self.generate_text(quote_index)
        self.quote_author = self.generate_author(quote_index)

    '''
    Grabs a random quote text from resource file using a random index
    '''
    def generate_text(self, quote_index):
        self.quote_text = self.quote_soup.select('div[class="quoteText"]')[quote_index].getText()
        return self.clean_quote(self.quote_text)

    '''
    Grabs the corresponding author to quote_text using the same randomized index
    '''
    def generate_author(self, quote_index):
        quote_author = self.quote_soup.select('a[class="authorOrTitle"]')[quote_index].getText()
        return quote_author

    '''
    Removes extraneous javascript present in the quote
    '''
    def clean_quote(self, quote_text):
        ind = quote_text.find('”')
        return quote_text[:ind + 1]

    def get_quote(self):
        return str(self.quote_text)

    def get_author(self):
        return str(self.quote_author)

class Quoter:
    save_directory = os.environ['USERPROFILE'] + '/Pictures/WallpaperQuotes'
    quote_obj = ''

    def __init__(self, res):
        self.quote_obj = Quote(res)

    '''
    Generate the finalized wallpaper
    '''
    def generate_wallpaper(self):
        im = Image.open('res/img/' + random.choice(os.listdir('res/img/')))
        fnt = ImageFont.truetype('res/fnt/MoonFlower.ttf', 30)

        # Separate drawing of text to fixed image size to retain consistency.
        quote_image = Image.new('RGBA', (im.width // 3, im.height // 2), (255, 255, 255, 0))
        draw_text = ImageDraw.Draw(quote_image)

        # quote_text separated to keep all text onscreen
        wrapped_quote = self.wrap_text(self.quote_obj.get_quote(), 70)
        line_index = 0
        first_line = True

        for line in wrapped_quote:
            if first_line:
                first_line = False
                draw_text.text((10, 10), line, font=fnt, fill='White')
            else:
                line_index += 1
                draw_text.text((20, 10 + (40 * line_index)), line, font=fnt, fill='White')

#        draw_text.text((430, (40 * (line_index + 1))), '-' + self.quote_author, font=fnt, fill='White')

        # Create wallpaper directory if not already available
        try:
            os.stat(self.save_directory)
        except:
            os.mkdir(self.save_directory)

        im.paste(quote_image, ((im.width - quote_image.width), 0), quote_image)
        im.save(self.save_directory + '/img-' + str(time.time()) + '.png')

    """
    Constrains the text to the bounds of the image
    """
    def wrap_text(self, text, char_limit):
        # char_limit - Max characters allowed per line
        # char_count = current character count for the line
        char_limit, char_count = char_limit, 0
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
