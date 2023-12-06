# Motion Detection Alarm 

## Overview

 - Captures video from a connected webcam.
 - Converts each frame to grayscale and applies Gaussian blur
 - Calculates absolute difference between consecutive frames to detect motion
 - Applies thresholding and morphological operations to remove noise
 - Detects contours in diff image to identify motion
 - Tracks centroid of contours over time to calculate if person has moved
 - Triggers alarm if no motion detected for set duration threshold


## Usage
The main parameters to configure are:

 - **distance_threshold** - max distance in pixels between contour centroids to be considered no motion
 - **duration_threshold** - number of seconds with no detected motion to trigger alarm


## Installation

This project requires OpenCV and Python 3. The main dependencies are:

 - OpenCV
 -  NumPy 
 - Matplotlib 
 - PyGame
 
They can be installed via pip:
    *pip install opencv-python numpy matplotlib pygame*

## Customization

Some ways this can be adapted or built upon:

 - Integrate with a security camera feed instead of webcam
 -  Save images on motion detection for security monitoring  
 - Send email/SMS alerts instead of sound alarm
 - Detect different types of motion (person, vehicle, animal, etc) 
 - Track motion of multiple subjects

## License 

This project is open source under the MIT license. Feel free to use and adapt it for your needs.
