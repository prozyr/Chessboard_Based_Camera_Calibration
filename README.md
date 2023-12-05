## Welcome to chessboard camera calibration project

This project provides users with ability to use chessboard camera calibration method, which correct lens distortions that occur in the mechanical and digital parts of camera.
Based on several shots of the chessboard, distortion-correcting parameters are calculated.


There are two ways of camera calibration
- Static Camera Calibration
- Live camera calibration

## Table of Contents


- [Static camera calibration](#static-camera-calibration)
- [Live camera calibration](#live-camera-calibration)
- [License](#license)
- [Installation](#installation)
- 
<h3 style="align-items: center; text-align: center;">Image example of fishEye distortion</h3>
<div style="display: grid; grid-template-columns: repeat(2, auto); text-align: center; width: 90%; gap: 20px;">
  <div>
    <img src="./photos/Series1_1.jpg" width="100%"/>
    <p><strong>Image before</strong></p>
  </div>
  <div>
    <img src="./UndistortedResult.jpg" width="100%"/>
    <p><strong>Image after</strong></p>
  </div>
</div>

## Static camera calibration  
As an input to camera calibration program you provide a photo or a series of photos which are distored. As an output program provides an undistorted photo and a text file with new calculated camera parameters. <br>
**Run `static_images_calibration.py` for basic, static camera calibration.**   

## Live camera calibration
For this mode to run having working camera is required. Running the program provides you with GUI made with TKinter python library. 

![image](https://github.com/prozyr/CVAPR---projekt/assets/128191169/aebb98d9-99ce-4bcd-ab0a-e6a16a016f1c)
<p><strong>GUI</strong></p>

GUI consists of 4 panels. Original frame, frame with detected chessboard corners needed for camera calibration algorythm, output undistorted frame and control panel, that lets you add images based of which new camera parametres will be calculated, delete all of them  and button which calibrate camera based of caputred frames.  <br>
**Run `main.py` for live camera calibration.**  

## Installation
Running this project requires:
- Python
- Python Libraries (OpenCV,TKinter,Numpy)

Install packages with the package manager manually if not already downloaded.
    
    $ pip install numpy
    $ pip install tk
    $ pip install opencv-python

##License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)
- **[MIT license](http://opensource.org/licenses/mit-license.php)**
