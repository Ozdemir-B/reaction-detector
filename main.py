from multiprocessing import process
from lib.detector import pipeline_webcam,pipeline
from lib import detector as det
import time
import cv2
#from lib.UI.scene import start,play
import argparse
from lib.flask_dash import client
from lib.download import Download
import threading
import multiprocessing
from lib import detector
import json
from statistics import mode
import os
from keyboard import press_and_release as par

results = []

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            #result=pipe(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break     
        else:
            break
    
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

def start(video_path,profile):
    global results
    
    detector_process = multiprocessing.Process(target=pipeline_webcam,args=["profiles/"+profile+".json",1,"access.json"])
    with open(video_path.split(".")[0]+".json","rb") as read_json:
        punchline = json.load(read_json)
    print(punchline)
    timer_process = multiprocessing.Process(target = timer, args = [punchline.get("start"),punchline.get("end")])
    play_process = multiprocessing.Process(target=play_video,args=["media/komik_720p.mp4"])

    play_process.start()
    detector_process.start()
    timer_process.start()

    play_process.join()
    detector_process.join()
    timer_process.join()

    #print("res_value _> ",res_value.value )
    #detector.play_video(video_path="media/komik_720p.mp4")
    
    
def change_run_file(file="",mode=0):
    with open(file,"r") as f:
        js = json.load(f)
    if js.get("run"):
        js["run"] = 0
    else:
        js["run"] = 1
    if mode == 2:
        js["run"] = 2
        print("mode 2 mode 2 mode 2 mode 2 mode 2 ")
    with open(file,"w") as f:
        json.dump(js,f)
    print(js)

def timer(start,end): # to end or start the program.
    #global results
    start -= 4
    play = 0
    t1 = time.time()
    
    #detector_thread = threading.Thread(target=pipeline_webcam,args=[1,"access.json"])
    while True:
        print(time.time()-t1)
        time.sleep(1)
        #t2 = time.time()
        t2 = 0
        if time.time() - t1 >= start and play == 0: #start detection
            change_run_file("access.json")
            print("->->-> detection started")
            #detector_thread.start()
            #results.append("-*-*-*-*-")
            play = 1
        if time.time() - t1 >= start+11 and play == 1:
            change_run_file("access.json")
            print("-->->-> detection ended")
            #detector_thread.join()
            #print(results)
            play = 2
            #t2 = time.time()
            change_run_file("access.json",mode=2)
            break
        """if time.time() - t1 >= start+15 and play == 2:
            par("ctrl+c")
            break"""

if __name__ == "__main__":
    os.system("mkdir profiles")
    with open("access.json","w") as f:
        js = {"run":0}
        json.dump(js,f)
    """parser = argparse.ArgumentParser(description="video directory")
    parser.add_argument("-v","--video",type=str,required=True)
    parser.add_argument("-p","--profile",type=str,required=True)
    video_dir = parser.parse_args().video
    profile = parser.parse_args().profile"""
    video_dir = input("video location:")
    video_name = video_dir.split("/")[-1].split(".")[0] #if len(video_dir.split("/")) == 1 else video_dir.split('\')[-1].split(".")[0]
    profile = input("enter a profile name:")
    print(video_name)
    command_2 = f"mkdir profiles/{video_name}"
    print("video_name = "+command_2)
    #os.system(command_2)
    try:
        start(video_path=video_dir,profile=profile)
        
        print("Keyboard --- Interrupt")
        file = "access.json"
        with open(file,"r") as f:
            js = json.load(f)
        js["run"] = 0
        with open(file,"w") as f:
            json.dump(js,f)

        with open("profiles/"+profile+".json","r") as f:
            prof = json.load(f)
        if prof.get("emotions"):
            emotions = [e.get("emotion") for e in prof.get("emotions")]
            ages = [a.get("age") for a in prof.get("emotions")]
            races = [r.get("race") for r in prof.get("emotions")]
            genders = [g.get("gender") for g in prof.get("emotions")]

            mode_emotion = mode(emotions)
            mode_age = mode(ages)
            mode_race = mode(races)
            mode_gender = mode(genders)

            prof["mode"]={"age":mode_age,"gender":mode_gender, "race":mode_race, "emotion":mode_emotion}
            prof["video"] = video_name
            print(prof)
            with open("profiles/"+profile+".json","w") as f:
                
                json.dump(prof,f)
    except KeyboardInterrupt:
        print("Keyboard --- Interrupt")
        file = "access.json"
        with open(file,"r") as f:
            js = json.load(f)
        js["run"] = 0
        with open(file,"w") as f:
            json.dump(js,f)

        with open("profiles/"+profile+".json","r") as f:
            prof = json.load(f)
        if prof.get("emotions"):
            emotions = [e.get("emotion") for e in prof.get("emotions")]
            ages = [a.get("age") for a in prof.get("emotions")]
            races = [r.get("race") for r in prof.get("emotions")]
            genders = [g.get("gender") for g in prof.get("emotions")]

            mode_emotion = mode(emotions)
            mode_age = mode(ages)
            mode_race = mode(races)
            mode_gender = mode(genders)

            prof["mode"]={"age":mode_age,"gender":mode_gender, "race":mode_race, "emotion":mode_emotion}
            prof["video"] = video_name
            print(prof)
            with open("profiles/"+profile+".json","w") as f:
                
                json.dump(prof,f)

    
    