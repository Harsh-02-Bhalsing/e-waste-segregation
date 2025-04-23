from ultralytics import YOLO

# Load your trained YOLOv8 model
model = YOLO("D:/PBL/project/PBLproject/src/yolo11n.pt")

# Get all class labels
class_labels = model.names

# Print class labels
print("Class Labels:")
for class_id, class_name in class_labels.items():
    print(f"{class_id}: {class_name}")
