from flask import Flask,Response
import os
import soundex
from threading import Thread
from helpers import run,reset
images=os.listdir("assets")
app=Flask(__name__)

@app.route('/image/<string:image>',methods=["GET"])
def draw(image):
    s = soundex.getInstance()
    for img in images:
        if s.soundex(img.replace(".jpg",""))==s.soundex(image):
            res=img
            path=f"assets/{img}"
            Thread(target=run,args=(path,), daemon=True).start()
            return Response(response=res,status=200)
    
    return Response(status=404)

@app.route('/reset',methods=["GET"])
def clear():
    Thread(target=reset, daemon=True).start()
    return Response(status=200)
    
if __name__ == '__main__':
    app.run()