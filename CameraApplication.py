import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from CameraModel import CameraModel, calibrate_camera
import pprint
import random
from tkinter import font

class CameraApplication:

    def __init__(self, chessboard_size, camera_number, height, width):
        np.set_printoptions(floatmode='fixed', precision=4)
        self.pp = pprint.PrettyPrinter(indent=4)

        # Variables
        self.chessboard_size = chessboard_size
        self.cameraModel = None
        self.height = height
        self.width = width
        self.cap = cv2.VideoCapture(camera_number)
        self.counter = 0  # Frame counter

        # UI setup
        self.window = tk.Tk()
        self.window.wm_title("Camera calibration")
        self.window.config(background="#263A52")

        # Frames for displaying images
        self.original_imageFrame = tk.Frame(self.window, width=self.width, height=self.height)
        self.original_imageFrame.grid(row=0, column=0, padx=2, pady=2)

        self.chessBoardDetection_imageFrame = tk.Frame(self.window, width=self.width, height=self.height)
        self.chessBoardDetection_imageFrame.grid(row=0, column=1, padx=2, pady=2)

        self.undistorted_imageFrame = tk.Frame(self.window, width=self.width, height=self.height)
        self.undistorted_imageFrame.grid(row=1, column=1, padx=2, pady=2)

        # Labels for displaying images
        self.display1 = tk.Label(self.original_imageFrame)
        self.display1.grid(row=0, column=0, padx=2, pady=2)

        self.display2 = tk.Label(self.chessBoardDetection_imageFrame)
        self.display2.grid(row=0, column=1, padx=2, pady=2)

        self.display3 = tk.Label(self.undistorted_imageFrame)
        self.display3.grid(row=1, column=1, padx=2, pady=2)

        # Bottom frame
        self.bottom_frame = tk.Frame(self.window, width=self.width, height=self.height / 2)
        self.bottom_frame.grid(row=1, column=0, padx=10, pady=5)

        # Buttons frame
        self.buttons_frame = tk.Frame(self.bottom_frame, width=self.width, height=self.height / 2)
        self.buttons_frame.grid(row=0, column=0, padx=10, pady=5)

        # Widgets for controlling the application
        self.counter_label = tk.Label(self.buttons_frame, text="Frame counter: 0")
        self.counter_label.grid(row=0, column=0, padx=10, pady=2)

        self.define_chessboard_size = tk.Button(self.buttons_frame, text="Define chessboard size", command=self.clicker)
        self.define_chessboard_size.grid(row=0, column=1, padx=10, pady=2)

        self.add_image_for_calibration_button = tk.Button(self.buttons_frame, text="Add image for calibration", command=self.add_image_for_calibration)
        self.add_image_for_calibration_button.grid(row=1, column=0, padx=10, pady=2)

        self.images_for_calibration_label = tk.Label(self.buttons_frame, text="Images for calibration: 0")
        self.images_for_calibration_label.grid(row=1, column=1, padx=10, pady=2)

        self.remove_all_images_for_calibration_button = tk.Button(self.buttons_frame, text="Remove all images for calibration", command=self.remove_all_images_for_calibration)
        self.remove_all_images_for_calibration_button.grid(row=1, column=2, padx=10, pady=2)

        self.camera_calibration_button = tk.Button(self.buttons_frame, text="Calibrate camera", command=self.calibrate_camera)
        self.camera_calibration_button.grid(row=2, column=1, padx=10, pady=2)

        # Data frame
        self.data_frame = tk.Frame(self.bottom_frame, width=self.width, height=self.height / 2)
        self.data_frame.grid(row=1, column=0, padx=10, pady=5)

        # Labels and Text widgets for displaying calibration results
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

        # Live error and mean error display
        self.label_live_error = tk.Label(self.bottom_frame, text="Live error")
        self.label_live_error.grid(row=9, column=0, padx=10, pady=2)
        self.text_live_error = tk.Label(self.bottom_frame, text="Calibrate camera previous")
        self.bold_font = font.Font(self.text_live_error, self.text_live_error.cget("font"))
        self.bold_font.configure(weight="bold", size=14)  # Adjust the size as needed
        self.text_live_error.configure(font=self.bold_font)
        self.text_live_error.grid(row=10, column=0, padx=10, pady=2)

        self.label_error = tk.Label(self.bottom_frame, text="Mean error of images used in calibration")
        self.label_error.grid(row=11, column=0, padx=10, pady=2)
        self.text_error = tk.Text(self.bottom_frame, height=1, width=40, bg="light yellow")
        self.text_error.grid(row=12, column=0, padx=10, pady=2)

        # List to store images for calibration
        self.images_for_calibration = []

        # Start the main loop
        self.show_frame_wrapper()

    def show_frame_wrapper(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)

        # Display the original camera feed
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display1.imgtk = imgtk
        self.display1.configure(image=imgtk)

        # Draw chessboard corners if detected
        frame2 = frame.copy()
        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, self.chessboard_size, None)
        if ret:
            cv2.drawChessboardCorners(frame2, self.chessboard_size, corners, ret)
            if self.cameraModel is not None:
                # Display live error on the UI
                if random.random() < 0.3:
                    self.text_live_error.config(text="{}".format(self.cameraModel.live_img_error(gray, corners)))

        # Display the camera feed with chessboard corners drawn
        cv2image = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display2.imgtk2 = imgtk
        self.display2.configure(image=imgtk)

        # Undistort the image using the calibrated camera model
        if self.cameraModel is not None:
            frame = self.cameraModel.undistort_img(frame)

        # Display the undistorted image
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display3.imgtk2 = imgtk
        self.display3.configure(image=imgtk)

        # Update frame counter
        self.counter += 1
        self.counter_label.config(text="Frame counter: {}".format(self.counter))

        # Call the show_frame_wrapper method after 10 milliseconds
        self.window.after(10, self.show_frame_wrapper)

    def calibrate_camera(self):
        # Calibrate the camera using the collected images
        cameraModel = calibrate_camera(self.images_for_calibration, self.chessboard_size)

        # Display the calibration results on the UI
        self.text_intrinsic.insert(tk.END, cameraModel.mtx)
        self.text_newmtx.insert(tk.END, str(cameraModel.newcameramtx))
        self.text_dst.insert(tk.END, cameraModel.dist)

        self.text_error.delete("1.0", tk.END)
        self.text_error.insert(tk.END, "{}".format(cameraModel.mean_error_for_images_used_for_calibration()))

        # Clear the list of images for calibration and store the calibrated camera model
        self.images_for_calibration = []
        self.cameraModel = cameraModel

    def add_image_for_calibration(self):
        # Capture a frame from the camera and add it to the list for calibration
        _, frame = self.cap.read()
        self.images_for_calibration.append(frame)
        self.images_for_calibration_label.config(text="Images for calibration: {}".format(
            len(self.images_for_calibration)))

    def remove_all_images_for_calibration(self):
        # Remove all images from the list for calibration
        self.images_for_calibration = []
        self.images_for_calibration_label.config(text="Images for calibration: {}".format(
            len(self.images_for_calibration)))

    def run(self):
        # Start the main Tkinter loop
        self.window.mainloop()

    def clicker(self):
        # Display a pop-up window for setting the chessboard size
        global pop
        pop = tk.Toplevel(self.window)
        pop.title("Set the size of chessboard")
        pop.geometry("400x300")
        pop.config(bg="gray")

        pop_label = tk.Label(pop, text="Size")
        pop_label.pack(pady=10)
        my_frame = tk.Frame(pop, bg="gray")
        my_frame.pack(pady=5)
        tk.Label(my_frame, text="Enter First Number", font=('Calibri 10')).pack()
        a = tk.Entry(my_frame, width=35)
        a.pack(pady=5)
        tk.Label(my_frame, text="Enter Second Number", font=('Calibri 10')).pack()
        b = tk.Entry(my_frame, width=35)
        b.pack(pady=5)
        OK = tk.Button(my_frame, text="OK", command=lambda: self.number(a, b), bg="white")
        OK.pack(pady=5)

    def number(self, a, b):
        # Set the chessboard size based on user input
        try:
            int(a.get())
            int(b.get())
            self.chessboard_size = (int(a.get()), int(b.get()))
            pop.destroy()
        except ValueError:
            tk.messagebox.showerror(title="ERROR", message="Error")
