from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010
from time import sleep
from pathlib import Path
#from demo_opts import get_device
#from tkinter import font
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import sys
import subprocess
import time


# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial)

# Display Refresh
LOOPTIME = 1.0

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

font = ImageFont.truetype('PixelOperator.ttf', 16)#

cuenta = 0

logo = Image.open("/opt/Scripts/i.png").convert("RGBA")
logo2 = logo.resize((logo.width // 12, logo.height // 12))
#fff = Image.new(logo2.mode, logo2.size, (255,) *4 )
#img = Image.composite(fff)

while True:

   with canvas(device) as draw:
     #draw.rectangle(device.bounding_box, outline="white", fill="black")
     #draw.text((30, 40), "Hello World", fill="white")
     # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
     cmd = "hostname -I | cut -d\' \' -f1"
     IP = subprocess.check_output(cmd, shell = True )
     cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
     CPU = subprocess.check_output(cmd, shell = True )
     cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
     MemUsage = subprocess.check_output(cmd, shell = True )
     cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
     Disk = subprocess.check_output(cmd, shell = True )
     cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
     Temp = subprocess.check_output(cmd, shell = True )
     cmd = "mpstat | grep all | awk '{printf \"CPU: %.1f\", (($(NF-0))*-1)+100}'"
     CPU2 = subprocess.check_output(cmd, shell = True )
    


     # Pi Stats Display
     draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=font, fill=255)
     draw.text((0, 16), str(CPU2,'utf-8') , font=font, fill=255)
     draw.text((80, 16), str(Temp,'utf-8') , font=font, fill=255)
     draw.text((0, 32), str(MemUsage,'utf-8'), font=font, fill=255)
     draw.text((0, 48), str(Disk,'utf-8'), font=font, fill=255)

     # Display image
     #luma.oled.image(image)
     #oled.show()
     device.show()

     time.sleep(LOOPTIME)

     if cuenta >= 25:
      #device.cleanup()
      #draw.rectangle(device.bounding_box, outline="white", fill="black")
      #draw.rectangle((0, 0, device.width, device.height), outline=0, fill=0)
      #device.display(image)
      background = Image.new("RGBA", device.size, "black")
      posn = ((device.width - logo2.width) // 2, 0)
      #posn = (30,40)
      print(posn)
      #img = Image.composite(rot, fff, rot)
      background.paste(logo2, posn)
      device.display(background.convert(device.mode))
      time.sleep(5)
      #draw.text((30, 40), "Hello World", fill="white")
      cuenta = 0
     else:
      cuenta+=1
      print(cuenta)
time.sleep(LOOPTIME)
