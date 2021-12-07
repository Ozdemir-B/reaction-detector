from os import write
from deepface import DeepFace
import cv2
import argparse
import time
import json

def write_image(img,text,org):
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    org = org # start coordinates for the text
    # fontScale
    fontScale = 0.5
    # Blue color in BGR
    color = (255, 0, 0)
    # Line thickness of 2 px
    thickness = 1
    # Using cv2.putText() method
    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

def pipe(img):
    # pipe processes images given. 
    # it processes only one image per time.
    result=DeepFace.analyze(img_path = img ,actions = ['age', 'gender', 'race', 'emotion']) #actions = ['age', 'gender', 'race', 'emotion']
    #img = cv2.imread('C:/Users/PC/Desktop/developer/reaction-detector/2.jpg', 1) # 1 for colored, 0 for black and white
    x1 = result["region"]["x"]
    y1 = result["region"]["y"]
    x2=result["region"]["w"]+x1
    y2 = result["region"]["h"]+y1

    cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)  # draws rectangle around the detected object
    
    org = (x1, y1-10)
    
    write_image(img,result["dominant_emotion"],(x1, y1-10))
    write_image(img,result["dominant_race"],(x1,y1-30))
    write_image(img,result["gender"],(x1,y2+15))
    write_image(img,str(result["age"]),(x1,y2+35))
    #cv2.imshow("lalala", img)
    #k = cv2.waitKey(0) # 0==wait forever
    return result


def pipeline_webcam(profile,show = 0,run_file=""):
    cap = cv2.VideoCapture(0) # 0 for webcam, video directory for a video.
    results = []
    with open(profile,"w") as f:
        json.dump({'emotions':[]},f)
    while(cap.isOpened()):
       
        ret, frame = cap.read()
        if ret == True:
            with open(run_file,"r") as run:
                run = json.load(run)
            
            if run.get("run") == 1:
                #print("---------------- detection running --------------------")
                try:
                    result=pipe(frame)
                    print_result = {"age":result["age"],"gender":result["gender"],"race":result["dominant_race"],"emotion":result["dominant_emotion"]}
                    results.append(print_result)
                    print(print_result)
                    with open(profile,"r") as f:
                        prof = json.load(f)
                    prof["emotions"].append(print_result)
                    with open(profile,"w") as f:
                        json.dump(prof,f)
                except Exception as e:
                    print("face couldn't detected. Exception > ",str(e))
            else:
                pass#print("---------------- detection not running --------------------")
            if run.get("run") == 2:
                break
            if show:
                cv2.imshow('Frame', frame)
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                return results
                break
                
        else:
            return results
            break
    
    cap.release()
   
    # Closes all the frames
    cv2.destroyAllWindows()
    return results

def pipeline_webcam_2():
    cap = cv2.VideoCapture(0) # 0 for webcam, video directory for a video.
    while(cap.isOpened()):

        ret, frame = cap.read()
        if ret == True:
            try:
                result=pipe(frame)
                print_result = {"age":result["age"],"gender":result["gender"],"race":result["dominant_race"],"emotion":result["dominant_emotion"]}

                print(print_result)
            except Exception as e:
                print("face couldn't detected. Exception > ",str(e))
            if True:
                cv2.imshow('Frame', frame)
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
                
        else:
            break
    
    cap.release()
   
    # Closes all the frames
    cv2.destroyAllWindows()


def pipeline(video_path):
    cap = cv2.VideoCapture(video_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            result=pipe(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
                
        else:
            break
    
    cap.release()
   
    # Closes all the frames
    cv2.destroyAllWindows()

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
                
        else:
            break

def pipeline2(video_path = 0):
    print("---video_path->",video_path)
    cap = cv2.VideoCapture(video_path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            result = pipe(frame)
            #print(result["dominant_emotion"])
            #cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
                
        else:
            break
    
    cap.release()
   
    # Closes all the frames
    cv2.destroyAllWindows()
                
            
if __name__ == "__main__":

    """parser = argparse.ArgumentParser(description="video directory")
    parser.add_argument("-v","--video",type=str,required=True)
    video_dir = parser.parse_args().video
    print(video_dir)
    video_path = video_dir"""
    #video_path = "video_smile_1_144.mp4"   #"C:/Users/PC/Desktop/developer/reaction-detector/video_crying_360_1.mp4"
    pipeline_webcam_2()