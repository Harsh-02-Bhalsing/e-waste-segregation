import streamlit as st
import cv2
import torch
import numpy as np
from PIL import Image
from ultralytics import YOLO

# Page configuration
st.set_page_config(page_title="Upload Image Detection", page_icon="🖼️", layout="wide")

st.title("Upload Image for E-Waste Detection")

# Load YOLO model (adjust path as needed)
model = YOLO("D:/PBL/project1/yolo11n.pt")

# Define E-Waste class labels (indices)
e_waste_classes = {
    62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 78
}

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    # Run detection
    results = model(img_np)
    annotated_image = img_np.copy()
    detected_items = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0].item()
            class_id = int(box.cls[0])
            label = model.names[class_id]

            # Draw bounding box and label
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(annotated_image, f"{label} ({confidence:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Add to detection list if e-waste
            if class_id in e_waste_classes:
                detected_items.append(f"E-Waste → {label} (Confidence: {confidence:.2f})")

    # Display results in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ Annotated Image")
        st.image(annotated_image, channels="RGB", use_container_width=True)


    with col2:
        st.subheader("📋 Detection Summary")
        if detected_items:
            for item in detected_items:
                st.write(item)
        else:
            st.write("No E-Waste Detected.")
