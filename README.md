# Wallpaper-Quotes
Scrapes github.com for quotes and and uses these quotes to insert into wallpapers.

## Usage
In order to use this program you will need to install three dependencies requests, BeautifulSoup4, and Pillow. In order to install these dependencies simply copy and paste the code below, line by line, into a terminal or command window.
```
pip install requests
pip install bs4
pip install pillow
```
After the dependencies are installed you may drop your wallpapers in the /res/img folder so that it may be automatically picked up by the program. After doing this run the program by typing the following command into a command window in the base directory of the program.
```
$ python Quoter.py
```
The newly generated image should be waiting in the /wallpaper directory. In order to get your wallpaper to automatically update set the slideshow folder in the personalization menu in windows to be the /wallpaper directory.
## Under Development
* Automatic running of the program at a specified time every day
* Name of author under the quote
* Name of book the exerpt is from
* Allow the user to request quotes from certain books or genere of books
* Allow the user to use custom fonts
* Normalize the vertical alignment of the quote
* Probably a lot more that I forgot about
