#!/usr/bin/python3

import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import jetson.inference
import jetson.utils
import cv2
import vlc
import RPi.GPIO as GPIO

#==============================================================================================
# GPIO
#==============================================================================================
video_pin = 11
video_pin_current = True
audio_pin = 12
audio_pin_current = True
kid_pin   = 13
kid_pin_current = True


#==============================================================================================
# Pills
#==============================================================================================
NOPILL   = "None"
TYLENOL  = "tylenol"
ADVIL    = "advil"
DIARRHEA = "diarrhea"
ASPIRIN  = "aspirin"
MOTION   = "motion"

#==============================================================================================
# globals
#==============================================================================================
pillDetected_g = None
activeAudio_g  = None
activeCanva_g  = None
kidMode        = 0
titleMode      = 1

#==============================================================================================
# Image paths
#==============================================================================================
imgPath     = ""

title   = imgPath + "title.jpg"
noPillImg   = imgPath + "noPill.jpg"
tylenolImg  = imgPath + "pill1.jpg"
advilImg    = imgPath + "pill2.jpg"
diarrheaImg = imgPath + "pill3.jpg"
aspirinImg  = imgPath + "pill4.jpg"
motionImg   = imgPath + "pill5.jpg"

title_kid   = imgPath + "title_kid.jpg"
noPillImg_kid   = imgPath + "noPill_kid.jpg"
tylenolImg_kid  = imgPath + "pill1_kid.jpg"
advilImg_kid    = imgPath + "pill2_kid.jpg"
diarrheaImg_kid = imgPath + "pill3_kid.jpg"
aspirinImg_kid  = imgPath + "pill4_kid.jpg"
motionImg_kid   = imgPath + "pill5_kid.jpg"

#==============================================================================================
# Audio paths
#==============================================================================================
audioPath     = ""

titleAudio    = audioPath + "title.mp3"
noPillAudio   = audioPath + "noPill.mp3"
tylenolAudio  = audioPath + "pill1.mp3"
advilAudio    = audioPath + "pill2.mp3"
diarrheaAudio = audioPath + "pill3.mp3"
aspirinAudio  = audioPath + "pill4.mp3"
motionAudio   = audioPath + "pill5.mp3"

titleAudio_kid    = audioPath + "title_kid.mp3"
noPillAudio_kid   = audioPath + "noPill_kid.mp3"
tylenolAudio_kid  = audioPath + "pill1_kid.mp3"
advilAudio_kid    = audioPath + "pill2_kid.mp3"
diarrheaAudio_kid = audioPath + "pill3_kid.mp3"
aspirinAudio_kid  = audioPath + "pill4_kid.mp3"
motionAudio_kid   = audioPath + "pill5_kid.mp3"

#==============================================================================================
# Key bindings
#==============================================================================================
KILL_SCRIPT = "<Escape>"
KILL_CANVAS = "<s>"
KILL_AUDIO  = "<a>"
DETECT_PILL = "<k>"
PLAY_AUDIO  = "<l>"

#==============================================================================================
# UI Util Functions
#==============================================================================================
def close_root(event):
    root.destroy()

def endActiveCanva(event):

    global pillDetected_g
    global activeCanva_g

    if activeCanva_g is not None:
        activeCanva_g.forget()

    activeCanva_g = None

def openCanvas():

    global pillDetected_g
    global activeCanva_g

    endActiveCanva(None)

    if pillDetected_g in canvaDict[kidMode].keys():
        activeCanva_g = canvaDict[kidMode][pillDetected_g]
        activeCanva_g.pack(fill = BOTH, expand = True)

def endActiveAudio(event):

    global activeAudio_g

    if activeAudio_g is not None:
        activeAudio_g.stop()

def openAudio(event):

    global pillDetected_g
    global activeAudio_g

    endActiveAudio(None)

    if pillDetected_g in audioDict[kidMode].keys():
        activeAudio_g = audioDict[kidMode][pillDetected_g]
        activeAudio_g.play()

#==============================================================================================
# Pill detection functions
#==============================================================================================
def retrieveObject():

    global pillDetected_g

    img, width, height = camera.CaptureRGBA()
    detections         = net.Detect(img, width, height)

    bestScore = 0
    bestLab   = "None"

    for i in range(len(detections)):
        if detections[i].Confidence > bestScore:
            bestScore = detections[i].Confidence
            bestLab   = net.GetClassDesc(detections[i].ClassID)

    pillDetected_g = bestLab

def detectPill(event):

    global pillDetected_g

    retrieveObject()
    print(pillDetected_g)
    openCanvas()

#==============================================================================================
# root setup
#==============================================================================================
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg = 'white')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.bind(KILL_SCRIPT, close_root)
root.bind(KILL_CANVAS, endActiveCanva)
root.bind(KILL_AUDIO,  endActiveAudio)
root.bind(DETECT_PILL, detectPill)
root.bind(PLAY_AUDIO,  openAudio)

#==============================================================================================
# Building Canvas
#==============================================================================================
#----------------------------------------------------------------------------------------------
start = Canvas(root, width = w, height = h, highlightthickness = 0)
start.configure(bg = 'white')
start.place(x = int(w / 20), y = int(w / 20), anchor = 'ne')
imgstart        = Image.open(title)
imgstart_resize = imgstart.resize((int(w * 0.7), h), Image.ANTIALIAS)
imagestart      = ImageTk.PhotoImage(imgstart_resize)
start.create_image(int(w * 0.3), 0, anchor = NW, image = imagestart)


#----------------------------------------------------------------------------------------------
canvas0 = Canvas(root, width = w, height = h, highlightthickness = 0)
canvas0.configure(bg = 'white')
canvas0.place(x = int(w / 20), y = int(w / 20), anchor = 'ne')
img0        = Image.open(noPillImg)
img0_resize = img0.resize((int(w * 0.7), h), Image.ANTIALIAS)
image0      = ImageTk.PhotoImage(img0_resize)
canvas0.create_image(int(w * 0.3), 0, anchor = NW, image = image0)

#----------------------------------------------------------------------------------------------
canvas1 = Canvas(root, width = w, height = h, highlightthickness = 0)
canvas1.configure(bg = 'white')
canvas1.place(x = int(w / 20), y = int(w / 20), anchor = 'ne')
img1        = Image.open(tylenolImg)
img1_resize = img1.resize((int(w * 0.7), h), Image.ANTIALIAS)
image1      = ImageTk.PhotoImage(img1_resize)
canvas1.create_image(int(w * 0.3), 0, anchor = NW, image = image1)

#----------------------------------------------------------------------------------------------
canvas2 = Canvas(root, width = w, height = h, highlightthickness = 0)
canvas2.configure(bg = 'white')
canvas2.place(x = int(w / 20), y = int(w / 20), anchor = 'ne')
img2        = Image.open(advilImg)
img2_resize = img2.resize((int(w * 0.7), h), Image.ANTIALIAS)
image2      = ImageTk.PhotoImage(img2_resize)
canvas2.create_image(int(w * 0.3), 0, anchor = NW, image = image2)

#----------------------------------------------------------------------------------------------
canvas3 = Canvas(root, width = w, height = h, highlightthickness = 0)
canvas3.configure(bg = 'white')
canvas3.place(x = int(w / 20), y = int(w / 20), anchor = 'ne')
img3        = Image.open(diarrheaImg)
img3_resize = img3.resize((int(w * 0.7), h), Image.ANTIALIAS)
image3      = ImageTk.PhotoImage(img3_resize)
canvas3.create_image(int(w * 0.3), 0, anchor = NW, image = image3)

#----------------------------------------------------------------------------------------------
canvas4 = Canvas(root, width = w, height = h, highlightthickness = 0)
canvas4.configure(bg = 'white')
canvas4.place(x = int(w / 20), y = int(w / 20), anchor = 'ne')
img4        = Image.open(aspirinImg)
img4_resize = img4.resize((int(w * 0.7), h), Image.ANTIALIAS)
image4      = ImageTk.PhotoImage(img4_resize)
canvas4.create_image(int(w * 0.3), 0, anchor = NW, image = image4)

#----------------------------------------------------------------------------------------------
canvas5 = Canvas(root, width = w, height = h, highlightthickness = 0)
canvas5.configure(bg = 'white')
canvas5.place(x = int(w / 20), y = int(w / 20), anchor = 'ne')
img5        = Image.open(aspirinImg)
img5_resize = img5.resize((int(w * 0.7), h), Image.ANTIALIAS)
image5      = ImageTk.PhotoImage(img5_resize)
canvas5.create_image(int(w * 0.3), 0, anchor = NW, image = image5)

#----------------------------------------------------------------------------------------------
# canvas6  = buildCanva(noPillImg_kid)
# canvas7  = buildCanva(tylenolImg_kid)
# canvas8  = buildCanva(advilImg_kid)
# canvas9  = buildCanva(diarrheaImg_kid)
# canvas10 = buildCanva(aspirinImg_kid)
# canvas11 = buildCanva(motionImg_kid)
#----------------------------------------------------------------------------------------------

canvaDict = {0 :{NOPILL   : canvas0,
                 TYLENOL  : canvas1,
                 ADVIL    : canvas2,
                 DIARRHEA : canvas3,
                 ASPIRIN  : canvas4,
                 MOTION   : canvas5
                },
            # 1 : {NOPILL   : canvas6,
            #      TYLENOL  : canvas7,
            #      ADVIL    : canvas8,
            #      DIARRHEA : canvas9,
            #      ASPIRIN  : canvas10,
            #      MOTION   : canvas11
            #     }
            }

#==============================================================================================
# audio
#==============================================================================================
start_audio = vlc.MediaPlayer(titleAudio)
pill0_audio = vlc.MediaPlayer(noPillAudio)
pill1_audio = vlc.MediaPlayer(tylenolAudio)
pill2_audio = vlc.MediaPlayer(advilAudio)
pill3_audio = vlc.MediaPlayer(diarrheaAudio)
pill4_audio = vlc.MediaPlayer(aspirinAudio)
pill5_audio = vlc.MediaPlayer(motionAudio)

# pill6_audio  = vlc.MediaPlayer(noPillAudio_kid)
# pill7_audio  = vlc.MediaPlayer(tylenolAudio_kid)
# pill8_audio  = vlc.MediaPlayer(advilAudio_kid)
# pill9_audio  = vlc.MediaPlayer(diarrheaAudio_kid)
# pill10_audio = vlc.MediaPlayer(aspirinAudio_kid)
# pill11_audio = vlc.MediaPlayer(motionAudio_kid)

audioDict    = {0 : {NOPILL   : pill0_audio,
                     TYLENOL  : pill1_audio,
                     ADVIL    : pill2_audio,
                     DIARRHEA : pill3_audio,
                     ASPIRIN  : pill4_audio,
                     MOTION   : pill5_audio
                    },
                # 1 : {NOPILL   : pill6_audio,
                #      TYLENOL  : pill7_audio,
                #      ADVIL    : pill8_audio,
                #      DIARRHEA : pill9_audio,
                #      ASPIRIN  : pill10_audio,
                #      MOTION   : pill11_audio
                #     }
               }

#==============================================================================================
# camera setup
#==============================================================================================
cam = Label(root, width = 400, height = 400, highlightthickness = 0)
cam.configure(bg = 'white')
cam.place(x = 75, y = 75, anchor = 'nw')
camera  = jetson.utils.gstCamera(1280, 720, "csi://0")

#==============================================================================================
# GPIO setup
#==============================================================================================
GPIO.setmode(GPIO.BOARD)
GPIO.setup(video_pin, GPIO.IN)
GPIO.setup(audio_pin, GPIO.IN)
GPIO.setup(kid_pin,   GPIO.IN)

#==============================================================================================
# Model setup
#==============================================================================================
net = jetson.inference.detectNet(argv=["--model=ssd-mobilenet.onnx",
                                       "--labels=labels.txt",
                                       "--input-blob=input_0",
                                       "--output-cvg=scores",
                                       "--output-bbox=boxes"],
                                       threshold=0.5)

#==============================================================================================
# Frame display functions
#==============================================================================================
def title_screen():
    global titleMode

    if titleMode == 1:
        start.pack(fill = BOTH, expand = True)
        start_audio.play()

        if GPIO.input(video_pin) == False or GPIO.input(audio_pin) == False or GPIO.input(kid_pin) == False:
            start.forget()        
            start_audio.stop()
            titleMode = 0

def capture_frame():
    raw_img, width, height = camera.CaptureRGBA()
    rgb_img = jetson.utils.cudaAllocMapped(width=raw_img.width,height=raw_img.height,format='rgb8')

    jetson.utils.cudaConvertColor(raw_img, rgb_img)
    jetson.utils.cudaDeviceSynchronize()

    img_conv = jetson.utils.cudaToNumpy(rgb_img)

    img_cv1 = Image.fromarray(img_conv)
    img_cv2 = img_cv1.crop((280, 0, 1000, 720))
    img_cv3 = img_cv2.resize((400, 400), Image.ANTIALIAS)
    img_cv = img_cv3.rotate(270, fillcolor = 'white')
    
    return ImageTk.PhotoImage(image=img_cv)

def show_frames():
    title_screen()    

    img = capture_frame()
    cam.imgtk = img
    cam.configure(image=img)

    global video_pin_current
    global audio_pin_current
    global kid_pin_current

    video_pin_last    = video_pin_current
    video_pin_current = GPIO.input(video_pin)

    audio_pin_last    = audio_pin_current
    audio_pin_current = GPIO.input(audio_pin)

    kid_pin_last      = kid_pin_current
    kid_pin_current   = GPIO.input(kid_pin)

    if (video_pin_last == False) and (video_pin_current == True):
        detectPill(None)

    if (audio_pin_last == False) and (audio_pin_current == True):
        openAudio(None)

    if (kid_pin_last == False) and (kid_pin_current == True):
        kidMode = 1 - kidMode
        time.sleep(0.001)

    cam.after(1, show_frames)

#==============================================================================================
# Main
#==============================================================================================
def main():
    show_frames()
    root.mainloop()

if __name__ == "__main__":
    main()
