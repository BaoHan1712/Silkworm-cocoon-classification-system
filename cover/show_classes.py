from ultralytics import YOLO

# Load a model
model = YOLO("silk.onnx")  
print(model.names) 
    