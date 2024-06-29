import datetime
from datetime import datetime
import time
from time import sleep
import subprocess
import schedule
import psutil
import os
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010


PROCNAME = "python"

serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial)


def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(["name", "exe", "cmdline"]):
        if name == p.info['name'] or \
                p.info['exe'] and os.path.basename(p.info['exe']) == name or \
                p.info['cmdline'] and p.info['cmdline'][0] == name:
            ls.append(p)
    return ls

def matar():
    print("Entre en kill")
    #a = find_procs_by_name(PROCNAME)
    #print(a)
    for proc in psutil.process_iter():
        #print(proc.cmdline())
    # check whether the process name matches
        if ("python" and "/opt/Scripts/otro.py") in proc.cmdline():
            #proc.kill()
            print(proc.cmdline())
            p = psutil.Process(proc.pid)
            print(p.pid)
            #proc.kill()
            cmd = "sudo kill {}".format(p.pid)
            os.system(cmd)
            print(cmd)

def check():
    now = datetime.now()
    print(now.hour)
    match now.hour:
        case 0:
            print("Son las 00:00")
            matar()
        case 1:
            print("Son las 01:00")
            matar()
        case 2:
            print("Son las 02:00")
            matar()
            device.clear()
        case 3:
            print("Son las 03:00")
            matar()
        case 4:
            print("Son las 04:00")
            matar()
        case 5:
            print("Son las 05:00")
            matar()
        case 6:
            print("Son las 06:00")
            matar()
        case 7:
            print("Son las 07:00")
            matar()
        case 22:
            print("Son las 22:00")
            matar()
        case 23:
            print("Son las 23:00")
            matar()

        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            #return "Something's wrong with the internet"
            print("Es de dia debe estar la pantalla prendida")

# Schedule the task to run every 5 minutes
#schedule.every(5).minutes.do(check)

# Run the scheduled tasks indefinitely
while True:
   #schedule.run_pending()
   time.sleep(40)
   check()
