#!/usr/bin/python3

import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import jetson.inference
import jetson.utils
import cv2
import vlc
import RPi.GPIO as GPIO

image = "pill1.jpg"
img = Image.open(image)
img.verify()
img.show()

