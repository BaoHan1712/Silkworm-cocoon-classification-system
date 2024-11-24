from ultralytics import YOLO

# Load your custom trained model
model = YOLO('model\ken_final.pt')

# Export to TensorRT .engine format
# model.export(format='onnx',imgsz = 320, half=True,simplify = True)
# model.predict(source="Screenshot 2024-10-10 155739.png", save = True, imgsz = 640)

# Export to TensorRT .engine format
model.export(format='engine',imgsz = 640, half=True,simplify = True, workspace = 6)
