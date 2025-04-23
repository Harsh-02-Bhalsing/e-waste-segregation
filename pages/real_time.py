import streamlit as st
import cv2
import torch
import numpy as np
from ultralytics import YOLO
from PIL import Image

# Streamlit Page Configuration
st.set_page_config(page_title="Real-Time E-Waste Detection", page_icon="📷", layout="wide")

st.title("Real-Time E-Waste Detection")

# Load the trained YOLO model
model = YOLO("D:/PBL/project1/yolo11n.pt")  # Update path as needed

# Define E-Waste class labels (indices)
e_waste_classes = {
    62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 78
}

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Webcam Feed")
    stframe = st.empty()  # Placeholder for video feed

with col2:
    st.subheader("Detections")
    detection_box = st.empty()  # Placeholder for detection results

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.warning("Failed to grab frame")
        break

    # Convert frame from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform e-waste detection
    results = model(rgb_frame)
    detected_items = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0].item()
            class_id = int(box.cls[0])
            label = model.names[class_id]

            # Draw bounding box

            cv2.rectangle(rgb_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(rgb_frame, f"{label} ({confidence:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # If item is in E-Waste category
            if class_id in e_waste_classes:
                detected_items.append(f"E-Waste → {label} (Confidence: {confidence:.2f})")

    # Display the webcam feed with detections
    stframe.image(rgb_frame, channels="RGB")

    # Update detection results in right column
    detection_box.write("\n".join(detected_items) if detected_items else "No E-Waste Detections")

cap.release()
