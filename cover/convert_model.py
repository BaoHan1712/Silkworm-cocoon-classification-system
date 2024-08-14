from ultralytics import YOLO

# Load your custom trained model
model = YOLO('model/ken.pt')

# Export to TensorRT .engine format
model.export(format='onnx',imgsz = 640, half=True,simplify = True)