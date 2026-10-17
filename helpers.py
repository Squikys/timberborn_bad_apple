from PIL import Image,ImageOps
import requests
import time
def rgb_to_hex(r, g, b):
        return f'{r:02X}{g:02X}{b:02X}' 
def draw(start_index,start_x,start_y,end_x,end_y,n):

    val=start_index
    for y in range(start_y,end_y):
        for x in range(start_x,end_x):
            pixel=n.getpixel(xy=(x,y))
            color=rgb_to_hex(pixel[0],pixel[1],pixel[2])
            # s=requests.post(f"http://localhost:8080/api/switch-on/HTTP%20Lever%20{val}")
            s=requests.post(f"http://localhost:8080/api/color/HTTP%20Lever%20{val}/{color.lower()}")
            val+=1

from multiprocessing import Process
import time
import os

def f(x):
    return x*x

WIDTH, HEIGHT = 96, 64
WORKERS = 32

def run(path):
    img = Image.open(path)

    n=ImageOps.pad(img, (96,64),color="white")
    n=ImageOps.mirror(n)
    colors = [f'{r:02X}{g:02X}{b:02X}' for r, g, b in n.getdata()]
    n.save('image_scaled_opt.jpg')


    time.sleep(5)
    start = time.perf_counter()
    rows_per_worker = HEIGHT // WORKERS
    procs = []

    for i in range(WORKERS):
        start_y = i * rows_per_worker
        end_y = start_y + rows_per_worker
        start_index = start_y * WIDTH
        p = Process(target=draw, args=(start_index, 0, start_y, WIDTH, end_y,n))
        procs.append(p)
        p.start()

    for p in procs:
        p.join()
    print(f"{len(colors)/(time.perf_counter()-start):.0f} req/s")

    
    
