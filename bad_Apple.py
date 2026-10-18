from helper import get_frames,get_pixels
import time
import os,copy
from multiprocessing import Process,Barrier
from concurrent.futures import Future,ThreadPoolExecutor,wait
import requests
WIDTH, HEIGHT =16,16
WORKERS = 4
FRAME_DURATION=0.2
from playsound3 import playsound

def sound(file):
    playsound(file)

def send_request(val,color,session):
    session.post(f"http://localhost:8080/api/color/HTTP%20Lever%20{val}/{color.lower()}")

import time

def draw(frames, start_x, start_y, end_x, end_y, barrier):
    total_frames = len(frames)
    start_time = time.perf_counter()
    session = requests.Session()
    empty=[["0"]*16 for _ in range(16)]
    for i in range(total_frames):
        barrier.wait()
        frame_start = time.perf_counter()
        prev=copy.deepcopy(empty)
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                val = y * WIDTH + x + 1
                color = frames[i][y][x]
                if color!=prev[y][x]:
                    prev[y][x]=color
                    send_request(val, color,session)
                    


        end_time=time.perf_counter()
        if end_time-frame_start<FRAME_DURATION:
            time.sleep(end_time-frame_start)
            print(end_time-frame_start)

if __name__ == '__main__':
    barrier = Barrier(WORKERS)
    frames=get_frames("vid.mp4","frames")

    time.sleep(5)
    rows_per_worker = HEIGHT // WORKERS
    procs = []
    pixels = get_pixels("frames", frames)
    s=True
    for i in range(WORKERS):
        start_y = i * rows_per_worker
        end_y = HEIGHT if i == WORKERS - 1 else start_y + rows_per_worker

        p = Process(
            target=draw,
            args=(pixels,  0, start_y, WIDTH, end_y, barrier)
        )
        procs.append(p)
        p.start()
        if s:
            audio='vid.mp4'
            p = Process(
                target=sound,
                args=(audio,)
            )
            procs.append(p)
            p.start()
            
            s=False

    for p in procs:
        p.join()
