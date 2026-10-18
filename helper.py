import ffmpeg
import os
import numpy as np
from PIL import Image,ImageOps

def get_frames(file:str,output:str):
    YOUR_FILE = file
    OUT_DIR = output
    FPS = 5

    os.makedirs(OUT_DIR, exist_ok=True)

    probe = ffmpeg.probe(YOUR_FILE)
    video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = video['width']

    (
        ffmpeg
        .input(YOUR_FILE)
        .filter('fps', fps=FPS)
        .filter('scale', width, -1)
        .output(f'{OUT_DIR}/frame_%05d.jpg', **{'q:v': 2})
        .run()
    )
    return os.listdir(output)
def rgb_map_to_hex(pixels):
    arr=[]

    for y in range(len(pixels)):
        temp=[]
        for x in range(len(pixels[y])):
            t=pixels[y][x]
            temp.append(f'{(t[0]):02X}{t[1]:02X}{t[2]:02X}')
        arr.append(temp)
    return  arr
def get_pixels(path,files):
    pixel_maps=[]
    for file in files:
        img = Image.open(os.path.join(path,file))

        n=ImageOps.fit(img, (16,16))

        n=ImageOps.mirror(n)
        arr=rgb_map_to_hex(np.array(n.convert("RGB")))
        pixel_maps.append(np.array(arr))
    return pixel_maps
