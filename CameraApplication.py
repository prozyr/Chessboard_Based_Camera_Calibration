import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from CameraModel import CameraModel, calibrate_camera
import pprint

class CameraApplication:

    def __init__(self, chessboard_size, camera_number, height, width):
        np.set_printoptions(floatmode='fixed', precision=4)
        self.pp = pprint.PrettyPrinter(indent=4)

        #Variables
        self.chessboard_size = chessboard_size
        self.cameraModel = None
        self.height = height
        self.width = width
        self.cap = cv2.VideoCapture(camera_number)
        self.counter = 0  # Licznik
        #UI
        self.window = tk.Tk()
        self.window.wm_title("Camera calibration")
        self.window.config(background="#263A52")

        self.original_imageFrame = tk.Frame(self.window, width=self.width, height=self.height)
        self.original_imageFrame.grid(row=0, column=0, padx=2, pady=2)

        self.chessBoardDetection_imageFrame = tk.Frame(self.window, width=self.width, height=self.height)
        self.chessBoardDetection_imageFrame.grid(row=0, column=1, padx=2, pady=2)

        self.undistorted_imageFrame = tk.Frame(self.window, width=self.width, height=self.height)
        self.undistorted_imageFrame.grid(row=1, column=1, padx=2, pady=2)

        self.display1 = tk.Label(self.original_imageFrame)
        self.display1.grid(row=0, column=0, padx=2, pady=2)

        self.display2 = tk.Label(self.chessBoardDetection_imageFrame)
        self.display2.grid(row=0, column=1, padx=2, pady=2)

        self.display3 = tk.Label(self.undistorted_imageFrame)
        self.display3.grid(row=1, column=1, padx=2, pady=2)

        ##Bottom frame
        self.bottom_frame = tk.Frame(self.window, width=self.width, height=self.height / 2)
        self.bottom_frame.grid(row=1, column=0, padx=10, pady=5)

        ##Buttons frame
        self.buttons_frame = tk.Frame(self.bottom_frame, width=self.width, height=self.height / 2)
        self.buttons_frame.grid(row=0, column=0, padx=10, pady=5)

        self.counter_label = tk.Label(self.buttons_frame, text="Frame counter: 0")
        self.counter_label.grid(row=0, column=0, padx=10, pady=2)

        self.add_image_for_calibration_button = tk.Button(self.buttons_frame, text="Add image for calibration", command=self.add_image_for_calibration)
        self.add_image_for_calibration_button.grid(row=1, column=0, padx=10, pady=2)

        self.images_for_calibration_label = tk.Label(self.buttons_frame, text="Images for calibration: 0")
        self.images_for_calibration_label.grid(row=1, column=1, padx=10, pady=2)

        self.remove_all_images_for_calibration_button = tk.Button(self.buttons_frame, text="Remove all images for calibration", command=self.remove_all_images_for_calibration)
        self.remove_all_images_for_calibration_button.grid(row=1, column=2, padx=10, pady=2)

        self.camera_calibration_button = tk.Button(self.buttons_frame, text="Calibrate camera", command=self.calibrate_camera)
        self.camera_calibration_button.grid(row=2, column=1, padx=10, pady=2)

        ##Data frame
        self.data_frame = tk.Frame(self.bottom_frame, width=self.width, height=self.height / 2)
        self.data_frame.grid(row=1, column=0, padx=10, pady=5)

        self.label_intrinsic = tk.Label(self.data_frame, text="mtx - intrinsic")
        self.label_intrinsic.grid(row=3, column=0, padx=10, pady=2)
        self.text_intrinsic = tk.Text(self.data_frame, height=3, width=40, bg="light yellow")
        self.text_intrinsic.grid(row=4, column=0, padx=10, pady=2)

        self.label_newmtx = tk.Label(self.data_frame, text="new optimal mtx")
        self.label_newmtx.grid(row=5, column=0, padx=10, pady=2)
        self.text_newmtx = tk.Text(self.data_frame, height=3, width=40, bg="light yellow")
        self.text_newmtx.grid(row=6, column=0, padx=10, pady=2)

        self.label_dst = tk.Label(self.data_frame, text="dst - distortion coefficients")
        self.label_dst.grid(row=7, column=0, padx=10, pady=2)
        self.text_dst = tk.Text(self.data_frame, height=3, width=40, bg="light yellow")
        self.text_dst.grid(row=8, column=0, padx=10, pady=2)

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
        ret, corners = cv2.findChessboardCorners(gray, self.chessboard_size, None)
        if ret:
            cv2.drawChessboardCorners(frame2, self.chessboard_size, corners, ret)
            if self.cameraModel is not None:
                print("Live Error: {}".format(self.cameraModel.live_img_error(gray, corners)))

        cv2image = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display2.imgtk2 = imgtk
        self.display2.configure(image=imgtk)

        if self.cameraModel is not None:
            frame = self.cameraModel.undistort_img(frame)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display3.imgtk2 = imgtk
        self.display3.configure(image=imgtk)

        self.counter += 1
        self.counter_label.config(text="Frame counter: {}".format(self.counter))

        self.window.after(10, self.show_frame_wrapper)

    def calibrate_camera(self):
        cameraModel = calibrate_camera(self.images_for_calibration, self.chessboard_size)

        self.text_intrinsic.insert(tk.END, cameraModel.mtx)
        self.text_newmtx.insert(tk.END, str(cameraModel.newcameramtx))
        self.text_dst.insert(tk.END, cameraModel.dist)

        print(cameraModel.mean_error_for_images_used_for_calibration())

        self.images_for_calibration = []
        self.cameraModel = cameraModel

    def add_image_for_calibration(self):
        _, frame = self.cap.read()
        self.images_for_calibration.append(frame)
        self.images_for_calibration_label.config(text="Images for calibration: {}".format(
            len(self.images_for_calibration)))

    def remove_all_images_for_calibration(self):
        self.images_for_calibration = []
        self.images_for_calibration_label.config(text="Images for calibration: {}".format(
            len(self.images_for_calibration)))

    def run(self):
        self.window.mainloop()


