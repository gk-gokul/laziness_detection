qqqqqqqqqqimport cv2
import time
import pygame
import matplotlib.pyplot as plt

def play_alarm():
    pygame.mixer.music.load("alarm.wav")
    pygame.mixer.music.play(-1)

def calculate_distance(point1, point2):
    x1, y1, _ = point1
    x2, y2, _ = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def check_stillness(person_positions, distance_threshold, duration_threshold):
    if len(person_positions) < 2:
        return False

    initial_position = person_positions[0]
    current_position = person_positions[-1]
    distance = calculate_distance(initial_position, current_position)

    elapsed_time = current_position[2] - person_positions[-2][2]
    if distance < distance_threshold:
        if elapsed_time >= duration_threshold:
            return True
    else:
        return False


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Failed to open video capture.")
    exit()

ret, frame = cap.read()

if not ret:
    print("Failed to read frame.")
    exit()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (21, 21), 0)

motion_detected = False
person_positions = []
distance_threshold = 50  # Distance threshold to determine if a person is still
duration_threshold = 30  # Duration threshold in seconds for stillness detection (30 minutes)

timestamps = []
distances = []

pygame.mixer.init()

timer_start = time.time()
timer_duration = duration_threshold

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame.")
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Calculate the absolute difference between the current frame and the previous frame
    frame_diff = cv2.absdiff(gray, gray_frame)

    # Apply thresholding to obtain binary image
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # Perform morphological operations to remove noise
    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=2)

    # Find contours of the moving objects
    contours, _ = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        # Adjust the area threshold based on your scenario
        if cv2.contourArea(contour) < 500:
            continue

        # Get the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate the centroid of the bounding box
        centroid = (int(x + w / 2), int(y + h / 2))

        # Append the centroid and current timestamp to the person_positions list
        person_positions.append((centroid[0], centroid[1], time.time()))

        motion_detected = True

    # Check if motion is detected
    if motion_detected:
        # Reset the timer if motion is detected
        timer_start = time.time()
    else:
        # Check the elapsed time
        elapsed_time = time.time() - timer_start
        if elapsed_time >= timer_duration:
            print("Alarm: Person remained still for 30 seconds.")
            play_alarm()


  
    cv2.imshow('Motion Detection', frame)

    gray = gray_frame

    if len(person_positions) >= 2:
        distance = calculate_distance(person_positions[0], person_positions[-1])
        distances.append(distance)
        timestamps.append(time.time())

        plt.plot(timestamps, distances)
        plt.xlabel('Time')
        plt.ylabel('Distance')
        plt.title('Motion Detection Data')
        plt.pause(0.001)
        plt.clf()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pygame.mixer.music.stop()
pygame.mixer.quit()

cap.release()
cv2.destroyAllWindows()
