import serial.tools.list_ports
from ultralytics import YOLO
import cv2 as cv

arduinoData = serial.Serial("COM3", 9600)


def send_coordinates_to_arduino(x1, y1, x2, y2):
    # Convert the coordinates to a string and send it to Arduino
    coordinates = f"{y1},{x1}\r"
    arduinoData.write(coordinates.encode())
    print(f"{x1}{y1}\n")


model = YOLO("E:\\MV_Project\\Group6_Object_Recog_Tracking\\best.pt")

cap = cv.VideoCapture(0)
# cap = cv.VideoCapture("http://10.91.70.28:4747/video")
cap.set(3, 1280)  # Set width
cap.set(4, 720)  # Set height

class_names = {0: "Basketball", 1: "Volleyball"}


# def preprocess_frame(frame):
# Convert to grayscale
# gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

# Apply bilateral filter to reduce noise and preserve edges
# blurred_frame = cv.bilateralFilter(gray_frame, 11, 17, 17)

# Convert back to color (3 channels) if needed for YOLO
# color_frame = cv.cvtColor(blurred_frame, cv.COLOR_GRAY2BGR)

# return color_frame


while cap.isOpened():
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # Run YOLO predictions on the frame
    # preprocessed_frame = preprocess_frame(frame)

    results = model(frame, classes=[0, 1], line_width=3)  # type: ignore

    # Visualize results on the frame
    for result in results:
        for box in result.boxes:
            # Extract bounding box details
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0]  # Confidence score
            cls = int(box.cls[0])  # Class index

            # Draw the bounding box
            color = (
                (0, 255, 0) if cls == 0 else (0, 0, 255)
            )  # Green for Basketball, Red for Volleyball
            cv.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Add the label
            label = f"{class_names[cls]} {conf:.2f}"  # type: ignore
            cv.putText(
                frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

            # Send "ball" to Arduino if the class is Volleyball
            if cls == 1:
                try:
                    send_coordinates_to_arduino(x1, y1, x2, y2)
                except Exception as e:
                    print(f"Failed to send data to Arduino: {e}")

    # Display the frame with bounding boxes
    cv.imshow("Real-Time Detection", frame)

    # Exit on pressing 'q'
    if cv.waitKey(1) & 0xFF == 27:
        break


# Release resources
cap.release()
cv.destroyAllWindows()
