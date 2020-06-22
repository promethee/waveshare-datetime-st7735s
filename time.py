# -*- coding: utf-8 -*-
import os
import json
from datetime import date, datetime
#from datetime import datetime
from pytz import timezone
import pytz
import re
import LCD_1in44
import LCD_Config
from PIL import Image, ImageDraw, ImageFont, ImageColor

version = '1.0.0'

WIDTH = 128
HEIGHT = 128
color = "WHITE"
day_number = '00'
month_number = '00'
margin = 4
#vertical_offsets = [margin / 4, (HEIGHT / 2) + margin / 4]
vertical_offsets = [margin / 4, (HEIGHT / 3) + margin, HEIGHT - (HEIGHT / 3) + margin]
target_size = [WIDTH - margin, HEIGHT / 3 - (margin / 2)]
font_sizes = dict({
  "DAYS": dict({}),
  "MONTHS": dict({}),
  "TIME": 26
})
#font_size_for_day = 100
#font_size_for_date = 100

LCD = LCD_1in44.LCD()
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
LCD.LCD_Init(Lcd_ScanDir)

max_step = float(7 + 12)
current_step = float(0)

def show_loading(current):
  font = ImageFont.truetype("DejaVuSansMono.ttf", 48)
  image = Image.new("RGB", (LCD.width, LCD.height), "BLACK")
  draw = ImageDraw.Draw(image)
  percent = (current / max_step) * 100
  draw.text((0, 0), str(percent)[0:3] + '%', color, font)
  LCD.LCD_ShowImage(image,0,0)
  LCD_Config.Driver_Delay_ms(500)

image = Image.new("RGB", (LCD.width, LCD.height), "BLACK")

# Adjusting font size for days enumeration
for day_index in range(1, 8):
  tmp_date = datetime(2020, 11, day_index)
  tmp_day_text = tmp_date.strftime("%A")
  draw = ImageDraw.Draw(image)
  font_size = 0
  font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
  size = draw.textsize(tmp_day_text, font)
  while size[0] < WIDTH:
    font_size = font_size + 2
    font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    size = draw.textsize(tmp_day_text, font)
    #print(tmp_day_text, 'font size for too large, reducing to', font_size)
  font_sizes["DAYS"][tmp_day_text] = font_size
  current_step = current_step + 1
  show_loading(current_step)

# Adjusting font size for months enumeration
for index in range(1, 13):
  tmp_date = datetime(2020, index, 22)
  tmp_month_text = tmp_date.strftime("%B %d")
  tmp_month = tmp_date.strftime("%B")
  draw = ImageDraw.Draw(image)
  font_size = 0
  font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
  size_month = draw.textsize(tmp_month_text, font)
  while size_month[0] < WIDTH:
    font_size = font_size + 2
    font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    size_month = draw.textsize(tmp_month_text, font)
    #print(tmp_month_text, 'font size for too large, reducing to', font_size)
  font_sizes["MONTHS"][tmp_month] = font_size
  current_step = current_step + 1
  show_loading(current_step)

while(True):
    now = datetime.now(tz=timezone("Europe/Paris"))
    day_text = now.strftime("%A")
    date_text = now.strftime("%B %d")
    month_text = now.strftime("%B")
    time_text = now.strftime("%H:%M:%S")

    image = Image.new("RGB", (LCD.width, LCD.height), "BLACK")
    draw = ImageDraw.Draw(image)

    #displaying day text
    font = ImageFont.truetype("DejaVuSansMono.ttf", font_sizes["DAYS"][day_text])
    horizontal_offset = (HEIGHT / 2) - (size[0] / 2) - (margin / 2)
    draw.text((horizontal_offset, vertical_offsets[0]), day_text, color, font)

    #displaying month text
    font = ImageFont.truetype("DejaVuSansMono.ttf", font_sizes["MONTHS"][month_text])
    horizontal_offset = (HEIGHT / 2) - (size[0] / 2) - (margin / 2)
    draw.text((horizontal_offset, vertical_offsets[1]), date_text, color, font)

    font = ImageFont.truetype("DejaVuSansMono.ttf", font_sizes["TIME"])
    horizontal_offset = (HEIGHT / 2) - (size[0] / 2) - (margin / 2)
    draw.text((horizontal_offset, vertical_offsets[2]), time_text, color, font)

    LCD.LCD_ShowImage(image,0,0)
    LCD_Config.Driver_Delay_ms(500)
