# AI Virtual Mouse & Gesture Control System

## 1. Project Overview

I built this project using Python, OpenCV, MediaPipe, Haar Cascade, and PyAutoGUI.

The main purpose of this project was to understand how a webcam works with Python and how computer vision libraries can be used to interact with a computer using hand gestures.

Normally, we use a physical mouse and keyboard to control our computer. But in this project, I experimented with controlling certain computer operations using my hands in front of a webcam.

For example:
- Move my index finger → Move the computer cursor.
- Bring my thumb and index finger together → Perform a left click.
- Show a V gesture → Perform a right click.
- Show a thumbs-up → Increase system volume.
- Show a thumbs-down → Decrease system volume.
- Show an open palm → Pause cursor movement and gesture actions.

I also implemented face detection using OpenCV's Haar Cascade classifier.

**Important:** This project performs face detection, not facial recognition. It detects where a face is located in the webcam frame but does not identify the person.

The main objective was learning how different Python libraries communicate and work together to create a real-time computer vision application.

---

## 2. Technologies and Libraries Used

### 1. OpenCV (cv2)

OpenCV stands for Open Source Computer Vision Library.

I used OpenCV mainly for:
- Accessing the webcam.
- Reading video frames.
- Processing images.
- Converting BGR images into RGB.
- Flipping webcam frames.
- Drawing hand landmarks and connections.
- Drawing circles and rectangles.
- Displaying the webcam video.
- Detecting faces using Haar Cascade.

**In simple words:** OpenCV handles the webcam, image processing, video display, and face detection.

### 2. MediaPipe

MediaPipe is a framework developed by Google for building applications involving perception and computer vision.

I used MediaPipe Hands to detect and track hand landmarks.

It helps identify important points on the hand, such as:
- Thumb tip.
- Index finger tip.
- Middle finger tip.
- Ring finger tip.
- Pinky finger tip.
- Finger joints.

MediaPipe provides 21 landmarks for each detected hand.

I used these landmark positions to calculate whether a particular hand gesture was being performed.

**In simple words:** MediaPipe understands the position of my fingers and helps me identify hand gestures.

### 3. Haar Cascade (Face Detection)

Haar Cascade is an object detection method available in OpenCV.

I used the pre-trained `haarcascade_frontalface_default.xml` classifier to detect frontal faces.

It detects faces in webcam frames and returns their coordinates.

I used those coordinates to draw a green rectangle around detected faces.

**In simple words:** Haar Cascade detects where a face is present in the webcam video.

### 4. PyAutoGUI

PyAutoGUI is a Python library that allows us to control the computer using Python commands.

I used it to perform actual computer operations based on detected hand gestures.

Examples:
- `pyautogui.moveTo()` → Move the mouse cursor.
- `pyautogui.click()` → Perform a left click.
- `pyautogui.rightClick()` → Perform a right click.
- `pyautogui.press('volumeup')` → Increase volume.
- `pyautogui.press('volumedown')` → Decrease volume.
- `pyautogui.size()` → Get screen width and height.

**In simple words:** MediaPipe understands my gestures, but PyAutoGUI actually performs the computer actions.

### 5. NumPy

NumPy is a Python library used for numerical calculations and array operations.

Images and video frames are represented as numerical arrays.

I imported NumPy in this project, although I did not directly use `np` in the current implementation.

---

## 3. Importing Libraries

```python
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import pyautogui
```

What each import does:

- `cv2` → OpenCV functions.
- `mp` → MediaPipe functions.
- `python` and `vision` → MediaPipe Tasks API imports.
- `np` → NumPy functions.
- `pyautogui` → Computer and mouse control.

**Note:** I imported MediaPipe Tasks API modules, but my actual hand detection implementation uses the older `mp.solutions.hands` API. The Tasks imports are not required for the current code.

I also imported MediaPipe twice in my original code. Only one import is necessary.

---

## 4. Loading the Face Detection Model

```python
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
```

Here, I am loading a pre-trained Haar Cascade face detection model.

Let's understand the code:

**`cv2.CascadeClassifier()`**

This function loads a Haar Cascade classifier that can detect objects such as faces.

**`cv2.data.haarcascades`**

OpenCV provides a directory containing its Haar Cascade XML files.

Instead of manually writing the complete file path, I use OpenCV's built-in directory.

**`haarcascade_frontalface_default.xml`**

This is the actual XML file containing the pre-trained face detection classifier.

The model is used later to detect faces in webcam frames.

---

## 5. Accessing the Webcam

```python
cam = cv2.VideoCapture(0)
```

This is one of the most important parts of the project.

`cv2.VideoCapture()` is used to access a camera or video source.

The number `0` represents the default webcam.

Other camera devices may use `1`, `2`, etc.

**How does it work?**

When I execute this line, OpenCV attempts to connect to the webcam.

Once connected, I can continuously capture frames from the camera.

A webcam does not directly give us a complete video as one image. It continuously provides individual frames.

For example:

Frame 1 → Frame 2 → Frame 3 → Frame 4 → Frame 5

When these frames are displayed continuously, we see a live video.

### Initializing MediaPipe Hands

```python
my_hands = mp.solutions.hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

drawing_utils = mp.solutions.drawing_utils
```

Here, I initialize the MediaPipe Hands solution.

**`max_num_hands=2`**

MediaPipe can detect a maximum of two hands at a time.

**`min_detection_confidence=0.7`**

This sets the minimum confidence threshold for initial hand detection.

The value is 0.7, meaning 70%.

**`min_tracking_confidence=0.5`**

This sets the minimum confidence threshold for tracking an already detected hand.

**`drawing_utils`**

This module provides functions to draw hand landmarks and connections.

I use it later to visualize the hand skeleton on the webcam frame.

### Checking Webcam Availability

```python
if not cam.isOpened():
    raise IOError('Cant access webcam')
```

`cam.isOpened()` checks whether the webcam was successfully opened.

If the camera cannot be accessed, the program raises an error instead of continuing with an invalid camera connection.

---

## 6. Getting Screen Width and Height

```python
screen_width, screen_height = pyautogui.size()
```

This code gets the actual screen resolution of my computer.

For example, if my monitor resolution is 1920 × 1080:

- `screen_width = 1920`
- `screen_height = 1080`

Why do I need this?

Because webcam dimensions and computer screen dimensions are different.

For example:

Webcam frame = 640 × 480

Computer screen = 1920 × 1080

If my finger moves inside the webcam, I need to convert its coordinates into screen coordinates so that the actual mouse cursor follows my finger.

### Pinch and Cursor Variables

```python
is_pinch = False

smooth_cursor = 3

prev_x = 0
prev_y = 0
```

**`is_pinch`**

This variable stores whether a pinch gesture is currently active.

It helps prevent continuous clicking while the thumb and index finger remain together.

**`smooth_cursor = 3`**

This controls how smoothly the mouse cursor moves.

A larger value makes the cursor movement smoother but slower.

**`prev_x` and `prev_y`**

These variables store the previous cursor coordinates.

They are used to calculate smooth cursor movement instead of directly jumping to every new finger position.

---

## 7. The Main Webcam Loop

```python
while True:

    ret, frame = cam.read()

    if not ret:
        print('Cant read the video frames')
        break
```

This is the main loop of the project.

`while True` continuously executes the code until I manually stop the program or an error occurs.

### Understanding `cam.read()`

`cam.read()` captures a new frame from the webcam.

It returns two values:

**1. ret**

A Boolean value.

- `True` → Frame was successfully captured.
- `False` → Frame could not be captured.

**2. frame**

The actual image captured from the webcam.

So:

```python
ret, frame = cam.read()
```

means I am receiving both the success status and the actual webcam image.

If the frame cannot be captured, the loop stops.

---

## 8. Getting Frame Dimensions and Flipping the Webcam

```python
frame_height, frame_width, _ = frame.shape

frame = cv2.flip(frame, 1)
```

### `frame.shape`

It returns the dimensions of the image.

For example:

```python
(480, 640, 3)
```

This means:

- Height = 480 pixels.
- Width = 640 pixels.
- Channels = 3 (BGR colour channels).

The underscore `_` means I am ignoring the third value.

### `cv2.flip(frame, 1)`

This flips the webcam frame horizontally.

Why?

Because when I move my right hand to the right, I want the webcam display to behave like a mirror.

The value `1` means horizontal flipping.

---

## 9. Converting BGR to RGB

```python
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

output = my_hands.process(rgb)

hands = output.multi_hand_landmarks
```

This is where OpenCV and MediaPipe start working together.

### Why BGR to RGB?

OpenCV normally reads images in BGR format.

BGR means:

- Blue
- Green
- Red

MediaPipe's Hands solution expects an RGB image.

RGB means:

- Red
- Green
- Blue

Therefore, I convert the frame using:

```python
cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
```

### `my_hands.process(rgb)`

This sends the RGB image to MediaPipe.

MediaPipe processes the image and attempts to detect hands.

It identifies the hand landmarks and returns the detection results.

### `output.multi_hand_landmarks`

This extracts the detected hand landmarks.

If hands are detected, it contains their landmark information.

If no hands are detected, it returns `None`.

**Important:** This is the point where MediaPipe analyzes the webcam image and provides the information needed for gesture recognition.

---

## 10. Drawing Hand Landmarks

```python
if hands:

    for hand in hands:

        drawing_utils.draw_landmarks(
            frame,
            hand,
            mp.solutions.hands.HAND_CONNECTIONS
        )
```

First, I check whether MediaPipe detected any hands.

If hands are detected, I loop through them.

`draw_landmarks()` draws the hand skeleton on the webcam frame.

It displays:
- Small circles representing hand landmarks.
- Lines connecting different landmarks.

### Understanding Hand Connections

```python
mp.solutions.hands.HAND_CONNECTIONS
```

MediaPipe already knows which hand landmarks should be connected.

Instead of manually drawing every line, I use its predefined hand connections.

### Custom Landmark Drawing

I also used:

```python
landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
    color=(0, 255, 255),
    thickness=1,
    circle_radius=5
)
```

This controls the appearance of landmark points.

- `color` → Landmark colour.
- `thickness` → Line thickness.
- `circle_radius` → Size of landmark circles.

I also customized the connection lines:

```python
connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
    color=(255, 255, 255),
    thickness=1
)
```

This makes the hand skeleton easier to visualize.

---

## 11. Understanding MediaPipe Hand Landmarks

MediaPipe Hands provides 21 landmarks for every detected hand.

Each landmark contains three important values:

- `x` → Horizontal position.
- `y` → Vertical position.
- `z` → Relative depth information.

The x and y coordinates are normalized between approximately 0 and 1.

This means they are not actual pixel coordinates.

For example:

If the x coordinate is 0.5, it represents approximately the middle of the image horizontally.

### Important Landmark Indexes Used in My Project

| Landmark | Index |
|---|---:|
| Thumb tip | 4 |
| Thumb joint | 2 |
| Index finger tip | 8 |
| Index finger joint | 6 |
| Middle finger tip | 12 |
| Middle finger joint | 10 |
| Ring finger tip | 16 |
| Ring finger joint | 14 |
| Pinky tip | 20 |
| Pinky finger joint | 18 |

I extracted these landmarks:

```python
index_tip = hand.landmark[8]
thumb_tip = hand.landmark[4]

middle_tip = hand.landmark[12]
ring_tip = hand.landmark[16]
pinky_tip = hand.landmark[20]

index_joint = hand.landmark[6]
middle_joint = hand.landmark[10]
ring_joint = hand.landmark[14]
pinky_joint = hand.landmark[18]

thumb_join = hand.landmark[2]
```

Instead of checking the complete hand image manually, I use these landmark coordinates to understand finger positions.

For example:

If the index fingertip is above its joint, I can consider the index finger extended.

This is the basic idea behind my gesture detection logic.

---

## 12. Converting Finger Coordinates into Pixels

```python
x = int(index_tip.x * frame_width)
y = int(index_tip.y * frame_height)
```

MediaPipe returns normalized coordinates, but OpenCV drawing functions work with pixel coordinates.

Therefore, I multiply the normalized coordinates by the frame dimensions.

Example:

Suppose:

```python
index_tip.x = 0.5
index_tip.y = 0.4

frame_width = 640
frame_height = 480
```

Then:

```python
x = int(0.5 * 640)  # 320
y = int(0.4 * 480)  # 192
```

Now I have actual pixel coordinates.

### Drawing a Circle

```python
cv2.circle(
    frame,
    (x, y),
    15,
    (255, 0, 255),
    -1
)
```

This draws a filled circle around my index fingertip.

- `(x, y)` → Circle position.
- `15` → Radius.
- `(255, 0, 255)` → Colour in BGR format.
- `-1` → Filled circle.

I also print the fingertip coordinates to understand how the finger moves.

---

## 13. Converting Webcam Coordinates into Mouse Coordinates

```python
mouse_x = int(x * screen_width / frame_width)

mouse_y = int(y * screen_height / frame_height)
```

This is one of the most important parts of my virtual mouse.

The webcam and monitor have different resolutions.

For example:

Webcam:
- Width = 640
- Height = 480

Screen:
- Width = 1920
- Height = 1080

If my index finger reaches the middle of the webcam:

```python
x = 320
y = 240
```

The converted screen coordinates become:

```python
mouse_x = 960
mouse_y = 540
```

This represents the middle of my computer screen.

Therefore, my finger position inside the webcam is converted into the corresponding position on my computer screen.

---

## 14. Pinch Gesture – Left Click

```python
def pinch_click():

    global is_pinch

    distance = (
        (thumb_tip.x - index_tip.x)**2 +
        (thumb_tip.y - index_tip.y)**2
    )**0.5

    is_pinch_active = distance < 0.05

    if is_pinch_active and not is_pinch:
        pyautogui.click()
        print('clicked')

    is_pinch = is_pinch_active
```

The purpose of this function is to perform a left click when my thumb and index finger come close together.

### Understanding Distance Calculation

I calculate the distance between the thumb tip and index finger tip.

The formula is:

```python
distance = (
    (x2 - x1)**2 +
    (y2 - y1)**2
)**0.5
```

This is the Euclidean distance formula.

I use the normalized x and y coordinates provided by MediaPipe.

### Understanding the Threshold

```python
distance < 0.05
```

If the distance between my thumb and index finger is less than 0.05, I consider it a pinch gesture.

### Why `global is_pinch`?

I need to access and update the `is_pinch` variable outside the function.

### Why Check `not is_pinch`?

This is important.

Without this condition, the program could continuously click as long as my fingers remained together.

The condition:

```python
is_pinch_active and not is_pinch
```

means:

- Current frame → Pinch detected.
- Previous frame → Pinch was not active.
- Result → Perform one click.

This is called detecting a state transition.

---

## 15. Thumbs-Up and Thumbs-Down – Volume Control

```python
def thump():

    is_thump_up = thumb_tip.y < thumb_join.y

    is_thump_down = thumb_tip.y > thumb_join.y

    if is_thump_up:
        pyautogui.press('volumeup')

    if is_thump_down:
        pyautogui.press('volumedown')
```

I use the thumb tip and another thumb landmark to identify whether my thumb is pointing upward or downward.

### Why Compare Y Coordinates?

In image coordinates, the Y-axis starts from the top.

- Smaller Y value → Higher position.
- Larger Y value → Lower position.

Therefore:

```python
thumb_tip.y < thumb_join.y
```

means the thumb tip is above the thumb joint.

I interpret this as thumbs-up.

Similarly:

```python
thumb_tip.y > thumb_join.y
```

means the thumb tip is below the thumb joint.

I interpret this as thumbs-down.

### PyAutoGUI Volume Commands

```python
pyautogui.press('volumeup')
```

Sends a volume-up key command.

```python
pyautogui.press('volumedown')
```

Sends a volume-down key command.

**Important:** My current implementation can repeatedly send volume commands while the gesture remains active because the function runs continuously inside the webcam loop.

---

## 16. V Gesture – Right Click

```python
def right_click():

    two_fingers = (
        index_tip.y < index_joint.y and
        middle_tip.y < middle_joint.y and
        ring_tip.y > ring_joint.y and
        pinky_tip.y > pinky_joint.y
    )

    if two_fingers:
        pyautogui.rightClick()
```

The purpose of this function is to identify a V-shaped hand gesture.

I check four fingers:

**Index finger:**

```python
index_tip.y < index_joint.y
```

Index finger is extended upward.

**Middle finger:**

```python
middle_tip.y < middle_joint.y
```

Middle finger is extended upward.

**Ring finger:**

```python
ring_tip.y > ring_joint.y
```

Ring finger is considered folded.

**Pinky finger:**

```python
pinky_tip.y > pinky_joint.y
```

Pinky finger is considered folded.

If all four conditions are true, I consider it a V gesture and perform a right click.

```python
pyautogui.rightClick()
```

**Note:** These are simple landmark-based rules, not a sophisticated gesture recognition model. The result can vary depending on hand orientation and camera position.

---

## 17. Open Palm – Pause Cursor Movement

```python
is_open_palm = (
    index_tip.y < index_joint.y and
    middle_tip.y < middle_joint.y and
    ring_tip.y < ring_joint.y and
    pinky_tip.y < pinky_joint.y and
    thumb_tip.x < thumb_join.x
)
```

Here, I check whether the hand is open.

The first four conditions check whether the four fingers are extended.

The last condition checks the thumb's horizontal position.

If all conditions are true, I consider it an open palm.

### Pausing the System

```python
if is_open_palm:

    is_pinch = False

    cv2.putText(
        frame,
        'Paused',
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    print("PAUSED — cursor movement disabled")
```

When an open palm is detected:

- Cursor movement is disabled.
- The pinch state is reset.
- A PAUSED message appears on the webcam display.

`cv2.putText()` is used to write text on an image or video frame.

### Important

My current implementation pauses cursor movement and skips the other gesture functions while the open palm is detected.

It does not completely stop the webcam or face detection. The main loop continues running.

Also, the thumb condition depends on hand orientation and mirroring, so it may need adjustment for different hands.

---

## 18. Smooth Cursor Movement

```python
else:

    current_x = prev_x + (mouse_x - prev_x) / smooth_cursor

    current_y = prev_y + (mouse_y - prev_y) / smooth_cursor

    pyautogui.moveTo(
        int(current_x),
        int(current_y)
    )

    prev_x = current_x
    prev_y = current_y
```

This section controls the smoothness of the mouse cursor.

Without smoothing, the mouse cursor may jump around because hand landmarks can slightly change between frames.

I use the previous cursor position to calculate a new position.

### Understanding the Formula

```python
current_x = prev_x + (mouse_x - prev_x) / smooth_cursor
```

Let's assume:

```python
prev_x = 500
mouse_x = 800
smooth_cursor = 3
```

Then:

```python
current_x = 500 + (800 - 500) / 3
```

Result:

```python
current_x = 600
```

Instead of jumping directly from 500 to 800, the cursor moves towards 800 gradually.

The same logic applies to the Y coordinate.

### Updating Previous Coordinates

```python
prev_x = current_x
prev_y = current_y
```

After calculating the new position, I store it.

In the next webcam frame, these values become the previous coordinates.

This creates continuous smooth movement.

### Moving the Actual Mouse

```python
pyautogui.moveTo(int(current_x), int(current_y))
```

This moves the real computer mouse cursor to the calculated screen position.

---

## 19. Connecting All Gesture Functions

```python
pinch_click()

thump()

right_click()
```

These functions are called when an open palm is not detected.

This means the system continuously checks for:
- Pinch gesture.
- Thumbs-up.
- Thumbs-down.
- V gesture.

When a gesture is detected, PyAutoGUI performs the corresponding action.

This is how MediaPipe and PyAutoGUI work together.

MediaPipe detects hand positions, my Python conditions interpret the gestures, and PyAutoGUI executes the computer commands.

---

## 20. Face Detection Using Haar Cascade

```python
faces = face_cascade.detectMultiScale(
    frame,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)
```

This is where I use OpenCV's Haar Cascade model to detect faces.

### `detectMultiScale()`

This function searches for faces at different image scales.

It returns the coordinates of detected faces.

### Understanding Parameters

**`scaleFactor=1.1`**

Controls how much the image size is reduced between detection scales.

A smaller value means more scale checks, but it can increase processing time.

**`minNeighbors=5`**

Controls how many neighboring detections are required for a candidate region to be accepted.

A higher value generally makes detection stricter.

**`minSize=(30,30)`**

Defines the minimum face detection size in pixels.

### Drawing Face Rectangles

```python
for (x, y, w, h) in faces:

    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )
```

The face detector returns four values:

- `x` → Starting horizontal position.
- `y` → Starting vertical position.
- `w` → Width of the detected face.
- `h` → Height of the detected face.

`cv2.rectangle()` draws a green rectangle around each detected face.

This helps visualize where the face is located in the webcam frame.

**Technical note:** My current code passes the BGR colour frame directly into `detectMultiScale()`. Haar Cascade is normally used with grayscale images, so converting the frame using `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)` before detection would be a better approach.

---

## 21. Displaying the Webcam Video

```python
cv2.imshow('Displaying video frame', frame)
```

This displays the processed webcam frame in a separate window.

The frame contains:
- Live webcam video.
- Hand landmarks.
- Finger position indicator.
- Face detection rectangles.
- Pause message when applicable.

### Keyboard Input

```python
key = cv2.waitKey(10)

if key == 27:
    break
```

`cv2.waitKey(10)` waits for approximately 10 milliseconds and checks for keyboard input.

The number `27` represents the ESC key.

When I press ESC, the loop stops.

---

## 22. Releasing Webcam Resources

```python
cam.release()

cv2.destroyAllWindows()
```

These commands are important when closing the application.

**`cam.release()`**

Releases the webcam so other applications can use it.

**`cv2.destroyAllWindows()`**

Closes all OpenCV windows created by the program.

Without proper cleanup, the webcam or display windows might remain occupied after execution.

---

# 23. Complete Project Workflow

This is how the entire project works internally:

1. Import Python libraries.
2. Load the Haar Cascade face detection classifier.
3. Connect to the webcam.
4. Initialize MediaPipe Hands.
5. Get computer screen dimensions using PyAutoGUI.
6. Start the continuous webcam loop.
7. Capture a new webcam frame.
8. Flip the frame horizontally.
9. Convert BGR into RGB.
10. Send the frame to MediaPipe.
11. Detect hands and extract 21 landmarks.
12. Draw the hand skeleton.
13. Extract important fingertip and joint coordinates.
14. Convert normalized coordinates into webcam pixel coordinates.
15. Convert webcam coordinates into computer screen coordinates.
16. Check for pinch, thumbs-up, thumbs-down, V gesture, and open palm.
17. Use PyAutoGUI to execute the corresponding computer actions.
18. Detect faces using Haar Cascade.
19. Draw rectangles around detected faces.
20. Display the processed webcam frame.
21. Stop when ESC is pressed.
22. Release the webcam and close OpenCV windows.

# 24. How All Libraries Work Together

| Technology | Responsibility |
|---|---|
| OpenCV | Webcam access, frames, image processing and display |
| MediaPipe | Hand detection, tracking and landmark extraction |
| Haar Cascade | Face detection |
| Python logic | Interpreting landmark positions as gestures |
| PyAutoGUI | Performing mouse and system actions |
| NumPy | Numerical and array operations (not directly used in current code) |

**The most important concept I learned:**

OpenCV captures the webcam image.

MediaPipe analyzes the image and identifies hand landmarks.

My Python conditions use those landmarks to identify gestures.

PyAutoGUI executes the corresponding computer operations.

Haar Cascade independently detects faces in the same webcam frame.

# 25. Limitations and Improvements

This was an educational project, so the gesture recognition logic is based on simple coordinate comparisons.

Some improvements I can make in the future:

1. Improve gesture recognition using more landmark comparisons.
2. Add a cooldown for volume and right-click actions to prevent repeated commands.
3. Improve cursor smoothing and add a configurable sensitivity setting.
4. Support both left and right hands reliably.
5. Improve pinch detection using actual pixel distance or hand-relative distance.
6. Convert frames to grayscale before Haar Cascade face detection.
7. Process each detected hand separately instead of using only the last hand's landmarks for gesture logic.
8. Add more gestures for keyboard and computer control.
9. Improve error handling and webcam initialization.
10. Organize gesture functions outside the main webcam loop.

# 26. Final Learning Outcome

Through this project, I learned how to:

- Access a webcam using OpenCV.
- Capture and process live video frames.
- Understand BGR and RGB colour formats.
- Use MediaPipe for real-time hand detection.
- Understand the 21 hand landmarks.
- Extract fingertip and joint coordinates.
- Use coordinate comparisons to detect gestures.
- Calculate the distance between two points using the Euclidean distance formula.
- Convert webcam coordinates into screen coordinates.
- Implement cursor smoothing.
- Control the mouse using PyAutoGUI.
- Detect faces using Haar Cascade.
- Combine multiple computer vision libraries in one Python application.

**My main takeaway:**

I learned how computer vision can be connected to real-world computer interactions. Instead of just detecting objects or processing images, I used webcam input and hand landmarks to control my computer through gestures.

This project gave me a practical introduction to real-time computer vision and gesture-based human-computer interaction.