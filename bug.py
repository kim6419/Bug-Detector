import cv2
import requests

cap = cv2.VideoCapture(0)

width = 640
height = 480
cap.set(3, width)
cap.set(4, height)

_, prev_frame = cap.read()

# Size of the wider rectangular area (e.g. width x height)
rect_width, rect_height = 150, 200  # Increase width and height

while True:
    ret, frame = cap.read()

    frame = cv2.resize(frame, (width, height))

    diff = cv2.absdiff(prev_frame, frame)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

    # Calculate the coordinates of the top-left and bottom-right corners of the centered rectangle
    center_x, center_y = width // 2, height // 2
    rect_x1 = center_x - rect_width // 2
    rect_y1 = center_y - rect_height // 2
    rect_x2 = center_x + rect_width // 2
    rect_y2 = center_y + rect_height // 2

    # Draw the wider rectangle on the frame
    cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), 2)

    # Check if there is movement
    if cv2.countNonZero(threshold) > 500:
        # Logic to obtain the midpoint coordinates of the object (as an example, set x and y arbitrarily)
        object_x, object_y = 320, 240 # Relative coordinates from the center coordinates

        # Check if an object is outside the bounds of the wider rectangle
        x_min, y_min = int(width / 2 - rect_width / 2), int(height / 2 - rect_height / 2)
        x_max, y_max = int(width / 2 + rect_width / 2), int(height / 2 + rect_height / 2)

        if object_x < x_min or object_x > x_max or object_y < y_min or object_y > y_max:
            print("Object out of bounds! Capturing the image.")
            cv2.imwrite('captured_image.jpg', frame)

            # You can perform further actions here with the captured image

    cv2.imshow('Motion Detection', threshold)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    prev_frame = frame

cap.release()
cv2.destroyAllWindows()


