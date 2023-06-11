import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
window.wm_title("Camera calibration")
window.config(background="#FFFFFF")

imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

cap = cv2.VideoCapture(1)
counter = 0  # Licznik

def show_frame():
    global counter
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    display1.imgtk = imgtk
    display1.configure(image=imgtk)
    display2.imgtk = imgtk
    display2.configure(image=imgtk)

    counter += 1
    print("Licznik:", counter)

    window.after(10, show_frame)

def start_button_click():
    global counter
    counter = 0
    print("Licznik zresetowany!")

def show_frame_wrapper():
    show_frame()

display1 = tk.Label(imageFrame)
display1.grid(row=1, column=0, padx=10, pady=2)  # Display 1
display2 = tk.Label(imageFrame)
display2.grid(row=0, column=0)  # Display 2

start_button = tk.Button(window, text="Start", command=start_button_click)
start_button.grid(row=1, column=1, padx=10, pady=2)

sliderFrame = tk.Frame(window, width=600, height=100)
sliderFrame.grid(row=600, column=0, padx=10, pady=2)

window.after(10, show_frame_wrapper)  # Uruchamiając show_frame_wrapper()
window.mainloop()
