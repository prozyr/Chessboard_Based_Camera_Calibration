import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_title("Camera calibration")
        self.window.config(background="#FFFFFF")

        self.imageFrame = tk.Frame(self.window, width=600, height=500)
        self.imageFrame.grid(row=0, column=0, padx=10, pady=2)

        self.cap = cv2.VideoCapture(1)
        self.counter = 0  # Licznik

        self.display1 = tk.Label(self.imageFrame)
        self.display1.grid(row=1, column=0, padx=10, pady=2)  # Display 1
        self.display2 = tk.Label(self.imageFrame)
        self.display2.grid(row=1, column=1, padx=10, pady=2)  # Display 2

        self.counter_label = tk.Label(self.window, text="Licznik: 0")
        self.counter_label.grid(row=0, column=0, padx=10, pady=2)

        self.start_button = tk.Button(self.window, text="Start", command=self.start_button_click)
        self.start_button.grid(row=0, column=1, padx=10, pady=2)

        self.sliderFrame = tk.Frame(self.window, width=600, height=100)
        self.sliderFrame.grid(row=600, column=0, padx=10, pady=2)

        self.show_frame_wrapper()

    def show_frame_wrapper(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display1.imgtk = imgtk
        self.display1.configure(image=imgtk)
        self.display2.imgtk = imgtk
        self.display2.configure(image=imgtk)

        self.counter += 1
        self.counter_label.config(text="Licznik: {}".format(self.counter))

        self.window.after(10, self.show_frame_wrapper)

    def start_button_click(self):
        self.counter = 0
        print("Licznik zresetowany!")

    def run(self):
        self.window.mainloop()

app = CameraApp()
app.run()
