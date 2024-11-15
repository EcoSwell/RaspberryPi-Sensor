'''Display status/error messages on sensor LCD screen'''

import time
import st7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont

# create LCD class instance:
display = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
    )

display.begin() # initialize display

WIDTH = display.width # width of LCD display to calculate text position
HEIGHT = display.height # height of LCD display to calculate text position

# create empty black canvas to draw on LCD:
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0)) # create black image of same size as LCD 
draw = ImageDraw.Draw(img) # create empty black canvas


def display_text(text, font_size): # display text passed to function on sensor LCD screen
    # text settings:
    font = ImageFont.truetype(UserFont, font_size)
    text_colour = (255, 255, 255)
    back_colour = (0, 170, 170)
    size_x, size_y = draw.textsize(text, font) # size of text to be displayed on LCD screen
    # calculate text position:
    x = (WIDTH - size_x) / 2
    y = (HEIGHT / 2) - (size_y / 2)
    # draw background rectangle and write text:
    draw.rectangle((0, 0, 160, 80), back_colour)
    draw.text((x, y), text, font=font, fill=text_colour, align='center')
    display.display(img)
    return

def backlight_off():
    display.set_backlight(0) # turn off backlight
    return

def backlight_on():
    display.set_backlight(1) # turn on backlight
    return
