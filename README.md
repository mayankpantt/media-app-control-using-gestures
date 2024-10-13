Gesture Control using Mediapipe and OpenCV
This project uses Mediapipe and OpenCV to recognize hand gestures and control media playback, volume, and screen brightness. It's a fun and interactive way to control your computer using hand gestures.

Requirements
Python 3.7 or later
OpenCV 4.10.0 or later
Mediapipe 0.10.14 or later
PyAutoGUI 0.9.54 or later
screen_brightness_control 0.23.0 or later


Installation
Clone the repository using git clone 
Install the required packages using pip install -r requirements.txt
Make sure you have a working webcam and a compatible operating system (Windows, macOS, or Linux)

Usage
Run the script using python major.py
Make sure your webcam is turned on and you're in a well-lit environment

Use the following hand gestures to control your computer:

Gesture Controls                                Gesture	Action
Right Hand Palm	                                Play/Pause
Both Hands Fist	                                Mute/Unmute
Right Hand Two Fingers Up                       Decrease Brightness
Left Hand Two Fingers Up 	                      Increase Brightness
Left hand Index Finger Right Side Point	        Skip Forward
Left hand Index Finger Left Side Point          Left	Rewind
Pinch Right Hand Thumb And Index Finger         Volume Up
Pinch Right Left Thumb And Index Finger         Volume Down


Features
Hand gesture recognition using Mediapipe
Media playback control using PyAutoGUI
Volume control using PyAutoGUI
Screen brightness control using screen_brightness_control
Support for multiple hand gestures


Troubleshooting
Make sure your webcam is turned on and you're in a well-lit environment
If you're experiencing issues with hand gesture recognition, try adjusting the lighting or using a different webcam
If you're experiencing issues with media playback or volume control, try restarting the script or checking your system settings

