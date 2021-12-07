from flask import Flask, request
import requests
import json
import cv2
import numpy as np
from .. import download

Download = download.Download

import argparse


app = Flask(__name__)


class Client:

    def __init__(self):
        pass

    def get_frame(self):

        url = f"localhost:4000/getMetaData"
        payload = ""
        payload = json.dumps(payload) # list of the workers thaw tmux will start
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response=requests.request("GET", url, headers=headers, data=payload,timeout = 0.1)
        except Exception as e:#requests.exceptions.ReadTimeout:
            print("exception in freshStart getworkers request -> ",str(e))

        frame_count = 0

        """while True:

            url = f"localhost:4000/getFrame"
            response=requests.request("GET", url, headers=headers, data=payload,timeout = 1)"""
    


            

            

    

    

    
    


if __name__ == "__main__":
    file = Download


