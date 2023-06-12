import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from static_camera_calibration_function import CameraModel
from static_camera_calibration_function import static_camera_calibration_function

class CameraApp:
    def __init__(self):

        self.cameraModel = None

        self.window = tk.Tk()
        self.window.wm_title("Camera calibration")
        self.window.config(background="#263A52")

        self.original_imageFrame = tk.Frame(self.window, width=600, height=500)
        self.original_imageFrame.grid(row=0, column=0, padx=10, pady=2)

        self.chessBoardDetection_imageFrame = tk.Frame(self.window, width=600, height=500)
        self.chessBoardDetection_imageFrame.grid(row=0, column=1, padx=10, pady=2)

        self.undistorted_imageFrame = tk.Frame(self.window, width=600, height=500)
        self.undistorted_imageFrame.grid(row=1, column=1, padx=10, pady=2)

        self.cap = cv2.VideoCapture(1)
        self.counter = 0  # Licznik

        self.display1 = tk.Label(self.original_imageFrame)
        self.display1.grid(row=0, column=0, padx=10, pady=2)

        self.display2 = tk.Label(self.chessBoardDetection_imageFrame)
        self.display2.grid(row=0, column=1, padx=10, pady=2)

        self.display3 = tk.Label(self.undistorted_imageFrame)
        self.display3.grid(row=1, column=1, padx=10, pady=2)

        ##Bottom frame
        self.bottom_frame = tk.Frame(self.window, width=600, height=200)
        self.bottom_frame.grid(row=1, column=0, padx=10, pady=5)

        self.counter_label = tk.Label(self.bottom_frame, text="Frame counter: 0")
        self.counter_label.grid(row=0, column=0, padx=10, pady=2)

        self.add_image_for_calibration_button = tk.Button(self.bottom_frame, text="Add image for calibration", command=self.add_image_for_calibration)
        self.add_image_for_calibration_button.grid(row=1, column=0, padx=10, pady=2)

        self.images_for_calibration_label = tk.Label(self.bottom_frame, text="Images for calibration: 0")
        self.images_for_calibration_label.grid(row=1, column=1, padx=10, pady=2)

        self.start_button = tk.Button(self.bottom_frame, text="Start", command=self.start_button_click)
        self.start_button.grid(row=2, column=1, padx=10, pady=2)



        self.images_for_calibration = []
        self.show_frame_wrapper()

    def show_frame_wrapper(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display1.imgtk = imgtk
        self.display1.configure(image=imgtk)

        frame2 = frame.copy()
        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
        if ret:
            cv2.drawChessboardCorners(frame2, (9, 6), corners, ret)
        cv2image = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display2.imgtk2 = imgtk
        self.display2.configure(image=imgtk)

        if self.cameraModel is not None:
            print("mark1")
            frame = self.cameraModel.undistort_img(frame)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display3.imgtk2 = imgtk
        self.display3.configure(image=imgtk)

        self.counter += 1
        self.counter_label.config(text="Frame counter: {}".format(self.counter))

        self.window.after(10, self.show_frame_wrapper)

    def start_button_click(self):
        cameraModel = static_camera_calibration_function(self.images_for_calibration)
        print("Camera model" + str(cameraModel.newcameramtx))
        self.images_for_calibration = []
        self.cameraModel = cameraModel

    def add_image_for_calibration(self):
        _, frame = self.cap.read()
        self.images_for_calibration.append(frame)
        self.images_for_calibration_label.config(text="Images for calibration: {}".format(
            len(self.images_for_calibration)))

    def run(self):
        self.window.mainloop()

app = CameraApp()
app.run()
