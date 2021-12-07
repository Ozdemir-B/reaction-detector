from flask import Flask, request
import requests
import cv2
import numpy as np
import json


app = Flask(__name__)



@app.route("/getMetaData",methods=["POST","GET"])
def get_data():
    data = request.json
    video_name = data["name"]
    
    return "OK"

@app.route("/getFrame",methods= ["POST","GET"])
def get_frame():
    data = requests.json
    cap = cv2.VideoCapture()
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            payload = json.dumps(frame)
            response=requests.request()
            #cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
                
        else:
            break
    
    cap.release()
    pass


if __name__ == "__main__":
    app.run(port=4000,debug = True)

    
